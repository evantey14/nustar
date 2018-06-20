# NuSTAR Spectral Analysis
This is a framework for processing, grouping, binning, and analyzing NuSTAR data. It was originally made to automate Galactic Center data processing.

The main idea is to provide a clean and organized interface (via Python) for calling the host of command line tools (e.g. nuproducts, grppha, xspec) commonly used in performing spectral analysis on NuSTAR data. In particular, this allows automation of running an analysis over multiple data sets, organization of analyses that share similar structures, and recording of analyses conducted in the past -- lots of work which would have to otherwise be done manually. 

Note that this framework is _not_ meant as a substitute for the existing tools (i.e. it's dangerous to only understand the framework). Since the framework is just an interface, it's  _extremely_ important to understand the underlying tools being called. This also means the framework might not work in all cases. In these situations, you should default to using the original tools or you should carefully modify the framework to fit your needs.

## Native Spectral Analysis
The first step to using this framework is understanding the existing toolset. If you feel comfortable using `nuproducts`, `grppha`, and `xspec` to extract, bin, and analyze spectra feel free to continue. If you need a refresher, see [NATIVE_ANALYSIS.md](NATIVE_ANALYSIS.md)

## File Management
The root directory of this repository is divided into *packaged tools* and *experiments*. The tools are utilities used in experiments. Experiments are a set of Jupyter notebooks created to answer some question (e.g. Are the 2017 fluxes from the NE and SW regions consistent with the 2012 fluxes?). The purpose of this is to keep analyses organized and goal-oriented.

The tool files are arranged as follows:
* `nutools/__init__.py `: python file that maps python functions to command line commands (e.g. `bin_pha(infile, grpfile, outfile)` bins a spectrum using grppha and a grouping file)
* `nutools/*.pro`: GDL scripts used for creating spectra bin groups
* `nutools/spectra_analyzers/`: examples of xspec analyses. (No longer used in favor of sherpa python analysis.)

Experiment folders are arranged as follows:
* `experiments/EXP_NAME/*.ipynb`: The core analytical work, including extracting spectra, binning them, fitting models, etc.
* `experiments/EXP_NAME/config.py`: The experiment configuration. Defines locations of data, region, and product files.
* `experiments/EXP_NAME/regions/`: Default location for region files. 
* `experiments/EXP_NAME/products/`: Default location for nuproducts products (spectra, response, and background files).

## Getting Started

No prior software setup is required -- you should just clone/download the repository.

### Creating an experiment
When creating an experiment, you should first know what you're trying to accomplish with the experiment. Next, create a folder for it in the `experiments/` directory.

### Setting up an experiment
If relevant, create a `config.py` file with any configuration variables that are global to your experiment. This can include, for example, the path to the data you're analyzing.

### Conducting an experiment
The first step in conducting any experiment is to try the analysis with *native tools* to make sure it works and to make sure you understand what's going on.
 
Next, start the notebook server by calling `jupyter notebook` in the project's root directory. Follow the link provided to open the browser interface. From here, you can create notebooks to start conducting analyses. To kill the server, type `ctrl-c` then `y`. 

The interfacing between python and native tools can be found in [nutools/__init__.py](nutools/__init__.py). 

The main divergence from the native analysis is the use of [Sherpa](https://github.com/sherpa/sherpa) XSPEC. Sherpa provides XSPEC functions directly in Python, so there is no need to create our own interface between the two. You can find documentation [here](http://cxc.cfa.harvard.edu/sherpa/ahelp/index_context.html) and examples [here](https://github.com/sherpa/sherpa/wiki). Unfortunately, Sherpa is not a completely substitute for XSPEC, so use of XSPEC might sometimes still be required.  

Periodically, you should stop to clean up your notebooks -- organizing code/files and adding useful comments. When the experiment is eventually completed, it's recommended to create a mini results document/notebook to summarize the purpose, procedure, results, and conclusion of the experiment.

See [experiments/fluxconsistency](experiments/fluxconsistency/) for an example of an experiment.

## Working remotely
Since analyses are conducted in Jupyter notebooks, it's possible to do some analysis remotely. Follow [these instructions](http://jupyter-notebook.readthedocs.io/en/latest/public_server.html) to set up a public server.

Since you might be setting up the server over ssh, you can use [tmux](https://github.com/tmux/tmux/wiki) to keep the server running even if your ssh tunnel closes. You can do this by creating a session, then detaching it so it continues running in the background.

## Troubleshooting
It should be mentioned that you _will_ find oddities and strange errors as you use the framework (e.g. the nuproducts command has to be called differently than others because of how it handles terminals, shortened paths must sometimes be used because certain tools can't search deeper then a couple directories, etc). Typically these are because of limitations of the underlying tools. Don't be afraid to look into underlying causes of these problems (e.g. `group_pha()` isn't working? Does it work if you do it natively? Does it work if you shorten the file names? Does it only work if all the files are in the same directory? etc)

## Contributions
Let me know if there are features you'd like to see or if you've made features you think might be useful to others, and we can talk about how to add them to the codebase.

## Author

* Evan Tey

## Acknowledgments

* To Kerstin Perez and Shuo Zhang for informing the direction of the analysis.

