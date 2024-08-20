# PEP
Modelling the impact of `time to PEP', 'PEP duration' and PrEP-to-PEP transition on prophylactic efficacy 


## Table of Contents
-   [System requirements](#system-requirements)
      -   [Operating systems](#operating-systems)
      -   [Prerequisites](#prerequisites)
      -   [Dependencies](#dependencies)
-   [Usage](#Usage)
      -   [Data generation](#data-generation)
      -   [Plotting](#plotting)
      -   [PEP_Vectorized](#pep_vectorized)
- [About the data](#About-data)

## System requirements

### Operating systems
This workflow was tested on Ubuntu 20.04.5 LTS.

### Prerequisites
To run the analysis, some tools need to be installed. We recommend following the steps outlined below.

#### Install Conda/Miniconda

Conda will manage the dependencies of our program. Instructions can be found here: https://docs.conda.io/projects/conda/en/latest/user-guide/install.


#### Create the working environment

Create a new environment using the provided configuration file [`env.yml`](./env/env.yml). Go to the main folder of the repository and call:

```
conda env create -f env/env.yml
```

This step may take a few minutes. To activate the environment type:

```
conda activate pep
```

### Dependencies

This workflow uses the following dependencies:

```
  - numpy
  - scipy
  - pandas
  - torch
  - matplotlib
```
These dependencies will be installed automatically when creating the conda environment as described above.. 

## Usage
### Data generation
There are five Python scripts for generating the data used in each figure.
#### Figure 1:
To generate the data for Figure 1, run the following script:
```
./run_computation_fig1.py
```
Results will be saved as NumPy arrays with filenames in the format fig1{c/d}{drug}.npy.
#### Figure 2: 
To generate the data for Figure 2, run:
```
./run_computation_fig2.py
```
Data will be saved as csv file named 'fig2{b/c/d/e}.csv'.
#### Figure 3:
The data for Figure 3 is large, so specific scenarios must be defined using command-line arguments:
```
usage: run_computation_fig3.py [-h] [--gap GAP] [--drug3 DRUG3] [--duration DURATION] [--ifPrEP IFPREP]

optional arguments:
  -h, --help                show this help message and exit
  --exposure EXPOSURE       Time between last dose of PrEP and viral exposure (hr)
  --drug3 DRUG3             Third drug in addition to TDF and FTC, options are DTG and EFV
  --duration DURATION       Duration of PEP in days
  --ifPrEP IFPREP           Indicate if on-demand PrEP is used
  ```
  For example, to compute the scenario where exposure occurred 2 days after the last dose of PrEP, and TDF/FTC+DTG was used as PEP for 7 days (green line in Fig3B), run:
  ```
  ./run_computation_fig3.py --exposure 48 --drug3 dtg --duration 7
  ```
Please notice that the computation may be slow, depending on your system.

#### Figure 4 & 5:
The data for Figures 4 and 5 can be generated similarly. The following arguments apply to both figures:
```
usage: run_computation_fig4.py [-h] [--repeat REPEAT] [--drug3 DRUG3]

optional arguments:
  -h, --help       show this help message and exit
  --repeat REPEAT  Iteration number to repeat the computation
  --drug3 DRUG3    Third drug except for TDF and FTC, options are DTG and EFV
```
For example, to reproduce the result of Figure 4 for TDF/FTC+DTG, run:
```
./run_computation_fig4.py --drug3 dtg --repeat 100
```
Running this locally is not recommended due to the computation time required. For faster processing, consider running it on a high-performance computing (HPC) system with parallel jobs.


### Plotting
To generate the figures in the manuscript, use the plotting.py script. To run the script:
```
./plotting.py --figure i
```
Where i indicates the figure number (1-5) corresponding to the figure in the manuscript. After running the script, an SVG file named figi.svg will be saved.

### PEP_Vectorized
PEP_Vectorized is a package that computes prophylactic efficacy in a vectorized manner, allowing for the computation of PrEP and PEP efficacy trajectories for multiple regimens and individuals in a single run. For detailed usage instructions, please refer to the examples provided in 'PEP_Vectorized/example.ipynb'.

## About data
The 'data' folder contains pre-generated data that are necessary for plotting the figures in the paper.