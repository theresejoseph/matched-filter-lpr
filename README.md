# MatchedFiltedbasedLPR
<p align="center">
  <img src="https://github.com/user-attachments/assets/57f4cfb1-60b5-4a77-bb2f-01bafafff5bf" alt="image">
</p>
Place recognition is an important task within autonomous navigation, involving the re-identification of previously visited locations from an initial traverse. Unlike visual place recognition (VPR), LiDAR place recognition (LPR) is tolerant to changes in lighting, seasons, and textures, leading to high performance on benchmark datasets from structured urban environments. However, there is a growing need for methods that can operate in diverse environments with high performance and minimal training. In this paper, we propose a handcrafted matching strategy that performs roto-translation invariant place recognition and relative pose estimation for both urban and unstructured natural environments. Our approach constructs Birds Eye View (BEV) global descriptors and employs a two-stage search using matched filtering --- a signal processing technique for detecting known signals amidst noise. Extensive testing on the NCLT, Oxford Radar, and WildPlaces datasets consistently demonstrates state-of-the-art (SoTA) performance across place recognition and relative pose estimation metrics, with up to 15\% higher recall than previous SoTA.

## Installation

The search runs on an NVIDIA GPU through CuPy.

```bash
pip install numpy scipy pandas openpyxl matplotlib scikit-image opencv-python open3d imutils pykitti
pip install cupy-cuda12x   # match your CUDA version; cupyx.scipy.signal replaces the archived cuSignal
```

The Jackal rosbag loader also needs ROS 1 (`rosbag`, `sensor_msgs`, `tf`); the other datasets do not.

## Data

Download the datasets ([NCLT](http://robots.engin.umich.edu/nclt/), [Oxford Radar RobotCar](https://oxford-robotics-institute.github.io/radar-robotcar-dataset/), [Wild-Places](https://csiro-robotics.github.io/Wild-Places/)) and edit the paths under `details` in `scripts/config.json` for each run: the first entry is the scan folder, the second the pose file. Dataset parameters (cell size, descriptor size, rotation step, background weight) are in the same file.

## Usage

Run from the repository root:

```bash
python scripts/test.py       # place recognition and relative pose for the dataset chosen in main()
python scripts/evaluate.py   # recall and error plots from the saved results
```

`test.py` first saves the reference and query frame splits (`save_ref_query_split`), then writes one row per query to an Excel file under `results/`.

## Citation

```bibtex
@article{joseph2025matched,
  title   = {Matched Filtering based LiDAR Place Recognition for Urban and Natural Environments},
  author  = {Joseph, Therese and Fischer, Tobias and Milford, Michael},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2025}
}
```

