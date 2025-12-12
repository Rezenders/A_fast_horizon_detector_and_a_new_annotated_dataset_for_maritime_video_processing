# Copyright 2025 Gustavo Rezende Silva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import csv
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from math import fabs, cos, sin, sqrt, fmod
import json
import numpy as np


@dataclass
class GroundTruthEntry:
    filename: str
    x_midpoint: float
    y_midpoint: float
    angle: float


@dataclass
class ErrorSHL:
    pos_error: float = -1.0
    normalized_pos_error: float = -1.0
    angular_error: float = -1.0
    composite_error: float = field(init=False)

    def __post_init__(self):
        # Composite error combines angular and normalized positional components
        if self.normalized_pos_error < 0.0 or self.angular_error < 0.0:
            self.composite_error = -1.0
            return
        angular_term = 0.5 * self.angular_error / 180
        normalized_term = 0.5 * self.normalized_pos_error
        self.composite_error = 100 * sqrt(angular_term + normalized_term)


@dataclass
class ResultRow:
    filename: str = ''
    detected: bool = False
    time: float = -1.0
    error: ErrorSHL = field(default_factory=ErrorSHL)


def read_mu_sid_groundtruth(gt_file_path):
    """
    Reads ground truth horizon data from a specified file path.
    :param gt_file_path: absolute path to the ground truth file.
    :return: List of GroundTruthEntry objects read from the csv file.
    """
    entries = []
    with open(gt_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if len(row) < 8:
                print(f'Skipping row {idx}: expected at least 8 columns.')
                continue
            try:
                x_midpoint = float(row[5])
                y_midpoint = float(row[6])
                angle = float(row[7])
            except ValueError:
                # likely a header row
                continue
            filename = row[0].strip() + '.JPG'
            entries.append(GroundTruthEntry(
                filename=filename, x_midpoint=x_midpoint, y_midpoint=y_midpoint, angle=angle))
    return entries


def get_y_from_x_line(x: float, rho: float, theta: float) -> float:
    theta_rad = theta * (np.pi / 180.0)
    # theta_rad = np.pi/2 - theta_rad
    # if sin(theta_rad) == 0.0:
    # #     return x
    return (rho - x*cos(theta_rad)) / sin(theta_rad)


def evaluate_line(img_height: float, rho: float, theta: float, ground_truth: GroundTruthEntry) -> ErrorSHL:
    theta = 90.0 - theta  # convert reference frames
    pos_error = fabs(get_y_from_x_line(
        ground_truth.x_midpoint, rho, theta) - ground_truth.y_midpoint)
    delta_angle = fabs(theta - ground_truth.angle)
    if delta_angle > 180:
        delta_angle = fmod(fabs(theta - ground_truth.angle), 180.0)
    print(f'Height {img_height}')
    return ErrorSHL(
        pos_error=pos_error,
        normalized_pos_error=pos_error / img_height,
        angular_error=min(delta_angle, 180 - delta_angle),
    )


def compute_statistics(results: List[ResultRow]):
    sum_pos = 0.0
    sum_norm_pos = 0.0
    sum_angle = 0.0
    sum_composite_error = 0.0
    sum_time = 0.0
    for result in results:
        sum_pos += result.error.pos_error
        sum_norm_pos += result.error.normalized_pos_error
        sum_angle += result.error.angular_error
        sum_composite_error += result.error.composite_error
        sum_time += result.time

    n = len(results)
    if n == 0:
        return None
    mean_pos = sum_pos / n
    mean_norm_pos = sum_norm_pos / n
    mean_angle = sum_angle / n
    mean_composite_error = sum_composite_error / n
    mean_time = sum_time / n

    sq_sum_pos = 0.0
    sq_sum_norm_pos = 0.0
    sq_sum_angle = 0.0
    sq_sum_composite_error = 0.0
    sq_sum_time = 0.0

    for result in results:
        sq_sum_pos += (result.error.pos_error - mean_pos) ** 2
        sq_sum_norm_pos += (result.error.normalized_pos_error - mean_norm_pos) ** 2
        sq_sum_angle += (result.error.angular_error - mean_angle) ** 2
        sq_sum_composite_error += (result.error.composite_error - mean_composite_error) ** 2
        sq_sum_time += (result.time - mean_time) ** 2

    std_dev_pos = sqrt(sq_sum_pos / n)
    std_dev_norm_pos = sqrt(sq_sum_norm_pos / n)
    std_dev_angle = sqrt(sq_sum_angle / n)
    std_dev_composite_error = sqrt(sq_sum_composite_error / n)
    std_dev_time = sqrt(sq_sum_time / n)

    return {
        'mean': {
            'pos': mean_pos,
            'norm_pos': mean_norm_pos,
            'angle': mean_angle,
            'composite_error': mean_composite_error,
            'time': mean_time
        },
        'std_dev': {
            'pos': std_dev_pos,
            'norm_pos': std_dev_norm_pos,
            'angle': std_dev_angle,
            'composite_error': std_dev_composite_error,
            'time': std_dev_time
        }
    }


def save_results_to_csv(results: List[ResultRow], prefix: str = '', base_path: str = '.'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{base_path}/{prefix}_results_{timestamp}.csv'
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename', 'Detected', 'Time (s)', 'Positional Error (px)',
                         'Normalized Positional Error', 'Angular Error (deg)', 'Composite Error'])
        for result in results:
            writer.writerow([
                result.filename,
                result.detected,
                f'{result.time:.6f}',
                f'{result.error.pos_error:.2f}',
                f'{result.error.normalized_pos_error:.6f}',
                f'{result.error.angular_error:.2f}',
                f'{result.error.composite_error:.2f}'
            ])
    statistics = compute_statistics(results)
    statistics_filename = f'{base_path}/{prefix}_statistics_{timestamp}.json'
    with open(statistics_filename, 'w') as jsonfile:
        json.dump(statistics, jsonfile, indent=4)

    print(f'Results saved to {filename} and {statistics_filename}')