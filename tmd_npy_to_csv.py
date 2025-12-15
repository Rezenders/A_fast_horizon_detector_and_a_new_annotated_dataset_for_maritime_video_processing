# Copyright 2025 CASNAV - Marinha do Brasil

from pathlib import Path
import numpy as np


def convert_folder_npy_to_csv(folder: Path) -> None:
    if not folder.is_dir():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    csv_dir = folder.parent / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)

    for npy_file in sorted(folder.glob("*.npy")):
        array = np.load(npy_file)
        csv_path = csv_dir / f"{npy_file.stem}.csv"
        np.savetxt(csv_path, array, delimiter=",")
        print(f"Saved {csv_path}")


def main() -> None:
    tmd_ground_truth_path = Path("/datasets/TMD/GroundTruthFilesTMD/GT_Horizon/npy (For Python)")
    convert_folder_npy_to_csv(tmd_ground_truth_path)


if __name__ == "__main__":
    main()
