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
from FastHorizonAlg import FastHorizon

# from utils import read_mu_sid_groundtruth


def main():
    fast_horizon_algorithm = FastHorizon()
    fast_horizon_algorithm.evaluate(
        src_video_folder='/datasets/TMD/VideoFilesTMD',
        src_gt_folder='/datasets/TMD/GroundTruthFilesTMD/GT_Horizon/npy (For Python)',
        dst_video_folder='/datasets/TMD/results/fast_horizon/videos/',
        dst_quantitative_results_folder='/datasets/TMD/results/fast_horizon/',
        draw_and_save=True,
    )


if __name__ == '__main__':
    main()
