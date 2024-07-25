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

### PEP_Vectorized
PEP_Vectorized is a package that can compute the prophylactic efficacy 
in a vectorized way, i.e. this package can compute the PrEP and PEP efficacy trajectory of multiple regimens for multiple individuals in a single run. For detailed usage of this package please check the examples in 'bottom_up/PEP_Vectorized/example.ipynb'. 

## About data
The folder 'data' contains pre-generated data that are necessary for plotting the figures in the paper.