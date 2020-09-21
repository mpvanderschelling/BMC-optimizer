# BMC-optimizer
Simple Bayesian Optimization python program to suggest new bulk moulding compound recipes for bio-based composites.
This program is designed in collaboration with NPSP B.V.

## Contents
<b>bmc_requirements.txt</b>: Pip requirements file. No need to change this.<br>
<b>config.txt</b>: Configuration file with model paramaters. Parameters are loaded up at the start of the program.<br>
<b>help.txt</b>: File for which the contents are displayed if you are executing `help` within the python program.<br>
<b>model.py</b>: The python model to execute.<br>

## Getting started
The following guidelines will help you get started with using the optimization model.
### Linux command line
<b>Step 1)</b> Clone the repository: `git clone https://github.com/mpvanderschelling/BMC-optimizer.git`<br>
<b>Step 2)</b> Make sure you are using Python 3.6+ <br>
<b>Step 3)</b> Install the required packages: `pip install -r requirements_bmc.txt` <br>
<b>Step 4)</b> Put a database excel file in the local folder <br>
<b>Step 5)</b> Run the `model.py` python script: `python model.py`

### Windows
Instructions for windows

## Database file

The database file consists of some necessary input paramaeter columns <br>
Each row contains a new sample.
name | type fiber | type filler | fiber ratio | filler ratio | dry ratio | 
--- | --- | --- | --- | --- | --- |
FlaxOli50 | Flax | Olive stone | 0.0995 | 0.1542 | 0.6532 |

Other columns are selected as output columns

density | impact | stiffness | flex. strength | E-modulus |
--- | --- | --- | --- | --- | --- |
1.7187 | 2.1 | 9.7 | 28.8 | 4770 |

## Configuration file
The `config.txt` file contains the parameters you want to use in the model <br>
For each line, specify the parameter, followed by a space and end with the value of that parameter
For more information on the optimization model parameters, consult the [cikit-optimize documentation](https://scikit-optimize.github.io/stable/modules/generated/skopt.Optimizer.html?highlight=optimizer#skopt.Optimizer).
```
# search space boundaries
fiber_lb 0.05
fiber_ub 0.25
filler_lb 0.0
filler_ub 1.0
dry_lb 0.4
dry_ub 0.75

# Optimization model parameters
acq_func EI
strategy cl_min

# Recipe parameters
max_recipes 6
total_mass 2800.0

author Martin van der Schelling
```



