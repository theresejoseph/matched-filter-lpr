# MatchedFiltedbasedLPR
<p align="center">
  <img src="https://github.com/user-attachments/assets/57f4cfb1-60b5-4a77-bb2f-01bafafff5bf" alt="image">
</p>
Place recognition is an important task within autonomous navigation, involving the re-identification of previously visited locations from an initial traverse. Unlike visual place recognition (VPR), LiDAR place recognition (LPR) is tolerant to changes in lighting, seasons, and textures, leading to high performance on benchmark datasets from structured urban environments. However, there is a growing need for methods that can operate in diverse environments with high performance and minimal training. In this paper, we propose a handcrafted matching strategy that performs roto-translation invariant place recognition and relative pose estimation for both urban and unstructured natural environments. Our approach constructs Birds Eye View (BEV) global descriptors and employs a two-stage search using matched filtering --- a signal processing technique for detecting known signals amidst noise. Extensive testing on the NCLT, Oxford Radar, and WildPlaces datasets consistently demonstrates state-of-the-art (SoTA) performance across place recognition and relative pose estimation metrics, with up to 15\% higher recall than previous SoTA.

## Installation

```bash
pip install -r requirements.txt
pip install cupy-cuda12x   # optional, for the GPU: match your CUDA version
```

The search runs on an NVIDIA GPU through CuPy. Without CuPy, or with `MFLPR_DEVICE=cpu`, the same steps run in NumPy/SciPy on the CPU: the same algorithm, results equal up to floating-point rounding, but much slower, so use it to try the code or debug rather than for full runs. The Jackal rosbag loader also needs ROS 1 (`rosbag`, `sensor_msgs`, `tf`); the dataset-specific loaders (Open3D, OpenCV, pykitti) are only needed for their own dataset.

## Data

Download the datasets ([NCLT](http://robots.engin.umich.edu/nclt/), [Oxford Radar RobotCar](https://oxford-robotics-institute.github.io/radar-robotcar-dataset/), [Wild-Places](https://csiro-robotics.github.io/Wild-Places/)) and edit the paths under `details` in `scripts/config.json` for each run: the first entry is the scan folder, the second the pose file. Dataset parameters (cell size, descriptor size, rotation step, background weight) are in the same file.

## Usage

Run from the repository root:

```bash
python scripts/test.py --dataset NCLT --ref 10 --query 6        # one reference/query pair
python scripts/test.py --dataset WildPlaces_Venman --ref 1 --query 2 --no-excel
python scripts/evaluate.py                                       # recall and error plots from saved results
```

`--dataset` is a top-level key of `scripts/config.json`, and `--ref`/`--query` are run numbers under its `details`. For NCLT and Oxford Radar, `test.py` first saves the reference and query frame splits, then writes one row per query to an Excel file under `results/`. Run `python scripts/test.py --help` for all options.

## Tests

A few checks on synthetic point clouds (descriptor, downsampling, rotation, recovering a known translation) run in seconds with no dataset or GPU:

```bash
MFLPR_DEVICE=cpu python -m unittest discover -s tests -v
```

## Citation

```bibtex
@article{joseph2025matched,
  title   = {Matched Filtering based LiDAR Place Recognition for Urban and Natural Environments},
  author  = {Joseph, Therese and Fischer, Tobias and Milford, Michael},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2025}
}
```

