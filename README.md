
# Generalized Potential Heuristics for Classical Planning

This repository contains source code and benchmarks for the IJCAI 2019 paper 

    Guillem Francès, Augusto B. Corrêa, Cedric Geissmann and Florian Pommerening.
    "Generalized Potential Heuristics for Classical Planning."
    Twenty-Eighth International Joint Conference on Artificial Intelligence (IJCAI). 2019. 

The information and data contained in this repository should be enough to reproduce the experimental
results in the paper. However, to stay updated with further developments in the codebase and explore other 
experiments not reported in the paper, we recommend checking the official code repository of the project:
https://github.com/aibasel/basilisk


## Software Requirements

The code is developed in Python and requires both **Python 3.6+** and a working installation of IBM CPLEX,
which can be obtained free of charge for academic purposes, along with its Python API. The installation instructions 
and experiment results have been tested on an Ubuntu 16.04 machine with Python 3.5.2 and CPLEX 12.8. 


## Installation

**Ubuntu Packages.**
The following Ubuntu packages are necessary:
```bash
sudo apt install python3-dev python3-pip 
```

**Virtual Environment.**
For the installation of the Python code and dependencies, we _strongly recommend_ to install everything on a 
Python3 [virtual environment](https://docs.python.org/3/tutorial/venv.html). The following would be a possible
way of setting up a virtual environment dedicated to this project:
```bash
python3 -m venv frances-et-al-ijcai2019
source frances-et-al-ijcai2019/bin/activate
pip install --upgrade pip  # Upgrade Pip (optional, recommended)
``` 


The instructions that follow assume that both the `python` and `pip` commands refer to such a Python3 environment. 
It is important that you execute the instructions in the order given below.


**CPLEX Python API.** 
First install the CPLEX Python API: go to the directory `/path/to/cplex/python` in your CPLEX installation, and run
```bash
 python3 setup.py install
 ```

**Tarski.**
Our project uses a slightly modified version of the 
[Tarski Planning Problem Definition Module](https://github.com/aig-upf/tarski/). For the sake of 
ease of use and reproducibility, we have included the codebase here. 
Go to folder `tarski` and run:
```bash
cd ~/frances-et-al-ijcai2019/tarski
 pip install .
 ```

**Basilisk.**
Last, install this project's code itself. We recommend installing in development mode (-e).
Go to the root folder of this distribution and run:
```bash
cd ~/frances-et-al-ijcai2019
pip install -e .
```

This should install all the required dependencies and leave the experiments ready to be executed.


## Reproducing Experimental Results

Each individual experiment relies on a separate Python script that can be found in the `experiments` folder
(see e.g. `experiments/gripper.py` for an example). 
The experiments shown in the paper should be reproducible by issuing the following commmands:

```bash
./experiments/gripper.py gripper_std_inc --all
./experiments/miconic.py miconic_1_incremental --all
./experiments/spanner.py spanner_1_incremental --all
./experiments/visitall.py problem03full_incremental --all
```
