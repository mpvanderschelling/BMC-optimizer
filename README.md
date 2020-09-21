# BMC-optimizer
Simple Bayesian Optimization python program to suggest new bulk moulding compound recipes for bio-based composites.
This program is designed in collaboration with NPSP B.V.

## Overview

This python scripts first builds a Gaussian process surrogate model given the data provided. Subsequently, several new recipes are proposed within the search space boundaries.
Contents of this readme:
* [Files](#files)
* [Getting started](#getting-started)
* [Database file](#database-file)
* [Configuration file](#configuration-file)
* [Available commands](#available-commands)
* [Available parameters](#available-parameters)

The files in this repository
* <b>bmc_requirements.txt</b>: Pip requirements file. No need to change this.<br>
* <b>config.txt</b>: Configuration file with model paramaters. Parameters are loaded up at the start of the program.<br>
* <b>help.txt</b>: File for which the contents are displayed if you are executing `help` within the python program.<br>
* <b>model.py</b>: The python model to execute.<br>

## Getting started
The following guidelines will help you get started with using the optimization model.
### Linux command line
<b>Step 1)</b> Clone the repository: `git clone https://github.com/mpvanderschelling/BMC-optimizer.git`<br>
<b>Step 2)</b> Make sure you are using Python 3.6+ <br>
<b>Step 3)</b> Install the required packages: `pip install -r requirements_bmc.txt` <br>
> Alternatively, you can install the required packages yourself: `scikit-optimize, pandas, datetime, xlrd.`

<b>Step 4)</b> Put a database excel file in the local folder <br>
<b>Step 5)</b> Run the `model.py` python script: `python model.py`

### Windows
Instructions for windows

## Database file

You have to provide your own database file. The database file consists of some necessary input paramaeter columns. Each row contains a new sample.

name | type fiber | type filler | fiber ratio | filler ratio | dry ratio | 
--- | --- | --- | --- | --- | --- |
FlaxOli50 | Flax | Olive stone | 0.0995 | 0.1542 | 0.6532 |
ReedPeach50 | Reed | Peach stone | 0.0732 | 0.1375 | 0.5592 |
... | ... | ... | ... | ... | ... |

Other columns are selected as output columns

density | impact | stiffness | flex. strength | E-modulus |
--- | --- | --- | --- | --- |
1.7187 | 2.1 | 9.7 | 28.8 | 4770 |
1.4654| 2.3 | 9.5 | 32.1 | 5647 |
... | ... | ... | ... | ... |

## Configuration file
The `config.txt` file contains the parameters you want to use in the model <br>
For each line, specify the parameter, followed by a space and end with the value of that parameter <br>
For more information on the optimization model parameters, consult the [scikit-optimize documentation](https://scikit-optimize.github.io/stable/modules/generated/skopt.Optimizer.html?highlight=optimizer#skopt.Optimizer).
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

You can alter the configuration file and save it locally to quickly load up custom parameters

## Available commands

The commands are divided into 4 categories: 
* `show` for showing parameters and data on the screen. 
* `set` for setting parameters to a certain value.
* `ask` for asking the surrogate model for proposed recipes.
* `print` for writing the config parameters to a file or exporting the suggested recipes.

**SHOW**<br>
`show` 			 show the config parameters<br>
`show config`		 show the config parameters<br>
`show data`	 show the entire database. If no data is important, it will ask to `set data`.<br>
`show <param>`		 show the requested parameter<br>

**SET**<br>
`set config`		 import the config parameters from the config file again<br>
> Warning: this neglects any changes of config parameters during the current session

`set now`			 set the variable now to the current time<br>
`set data`		 import a database (`*.xlsx`) and set to variable data<br>
`set materials`		specify the materials you want to investigate (fiber, natural filler)<br>
`set output`		 specify what you want to optimize for<br>
`set batch`		 specify the amount of BMC doughs you want to make<br>
`set <param> <value>`	 set the requested parameter to the requested value<br>

**ASK**<br>
`ask model`		 ask the optimization model for new recipes<br>

**PRINT**<br>
`print config`		 save the altered config parameters to the config.txt file<br>
`print model`		 print the suggested recipes to a `.csv` file<br>

**MISC**<br>
`help/?`			 show the available commands<br>
`exit`			 exit program<br>

## Available parameters

The following parameters can be used by `set` and `show`
> Setting `fiber_t` and `filler_t` is more convenient by calling `set materials`

name	|	type	|	description
---|---|---
`acq_func`	|string	|	Type of acquisition function used
`author`		|string|		Name that will be printed on the recipes
`batch`     | int |     Number of recipes to be generated
`config`		|list|		Copy of the imported config.txt file
`data`		|DataFrame|	Imported BMC database
`databasename`	|string|		Filename of the imported database
`dry_lb`		|float	|	Lower bound of the dry materials parameter
`dry_ub`		|float	|	Upper bound of the dry materials parameter
`fiber_lb`	|float	|	Lower bound of the fiber parameter
`fiber_ub`	|float	|	Upper bound of the fiber parameter
`fiber_t`		|string	|	Name of the fiber to investigate
`filler_lb`	|float	|	Lower bound of the natural filler parameter
`filler_ub`	|float	|	Upper bound of the natural filler parameter	
`filler_t`	|string	|	Name of the natural filler to investigate
`max_recipes`	|int	|	Maximum number of recipes to request
`now`		|datetime|	Current time at start of program
`strategy`	|str|		Parallel Bayesian Optimization strategy
`total_mass`	|float|		Total mass of each BMC dough
