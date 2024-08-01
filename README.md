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
- [About data](#About-data)

## System requirements

### Operating systems
This workflow was tested on Ubuntu 20.04.5 LTS.

### Prerequisites
Some tools have to be installed to run the analysis. We recommend following the steps outlined below.

#### Install Conda/Miniconda

Conda will manage the dependencies of our program. Instructions can be found here: https://docs.conda.io/projects/conda/en/latest/user-guide/install.


#### Create the working environment

Create a new environment from the given environment config in [`env.yml`](./env/env.yml), where the pipeline will be executed.
Go to the main folder of the repository and call:

```
conda env create -f env/env.yml
```

This step may take a few minutes.

To activate the environment type:

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
```
They can be installed automatically by creating the conda environment above. 

## Usage
### Data generation

### Plotting
To plot the figures in the manuscript, the scipt plotting.py can be used. To run the script:
```
./plotting.py --figure i
```
with i indicates the figure number that is required, e.g. 1 refers to Figure 1 in the manuscript. Therefore this number is limited in 1-5, corresponding to Figure 1-5 in the paper. After running the script an svg file named 'figi.svg' will be saved.   

### PEP_Vectorized
PEP_Vectorized is a package that can compute the prophylactic efficacy 
in a vectorized way, i.e. this package can compute the PrEP and PEP efficacy trajectory of multiple regimens for multiple individuals in a single run. For detailed usage of this package please check the examples in 'PEP_Vectorized/example.ipynb'. 

## About data
The folder 'data' contains pre-generated data that are necessary for plotting the figures in the paper.