# NuSTAR Spectral Analysis
This is a toolkit for processing, grouping, binning, and analyzing NuSTAR data. It was originally made to automate Galactic Center data processing.

The main idea is to provide a clean and organized interface (via Python) for calling the host of command line tools (e.g. nuproducts, grppha, xspec) commonly used in performing spectral analysis on NuSTAR data. In particular, this allows automatation of running an analysis over multiple data sets, organization of analyses that share similar structures, and recording of analyses conducted in the past -- lots of work which would have to otherwise be done manually. 

## Getting Started

No prior setup is required -- you should just clone/download the repository.

### File Management

The files are arranged as follows:

* `nutools/__init__.py `: python package that maps callable python functions to command line commands for a defined set of inputs
* `*.py`: files that generate inputs to be passed into the nutools package functions
* `*.pro`: GDL scripts used for grouping spectra
* `spectra_analyzers/`: `.xcm` files of preset xspec analyses (assuming loaded data) 

There shouldn't be any requirements on arrangement of data files, though I use:
* `data/`
    * `[observations]/`: folders that store Stage 2 cleaned data named by observation ID
    * `[experiments]/`: folders that store Stage 3 data products and additional files used in analysis named by experiment
    * `regions/`: region files used in extracting products

### Conducting an experiment

I call a cohesive data analysis that investigates a specific question an "experiment" (e.g. determining spectral model fits in a set of regions for each individual observations, analyzing spectra in a particular region from all observations).

The general outline for an experiment is as follows:
1. Generate raw spectra
    * Use `nuproducts.py` and/or `addspec.py` to create source spectra, background spectra, and response files from event files or existing spectra, respectively.
2. Define bins for spectra
    * Use `group_pha.py` to define bins (in a `.dat` file) via a GDL script.
        * Currently, this script creates bins such that bins have 20 counts over the background counts.
3. Bin spectra
    * Use `bin_pha.py` to call `grppha` with the `.dat` file and output the binned source spectra.
4. Perform `xspec` analysis: 
    * Use `xspec.py` to load data and conduct an xspec anaysis (e.g. `tbabsapec310.xcm` fits 3-10 keV data to a `tbabs*apec` model, saves an image of the spectra, and logs the flux and model parameter results)
    * Use `parse_xspec_log.py` to parse through the generated logs and print the outputs so they can easily be pasted into a spreadsheet.

Each `.py` file contains functions that generate lists of inputs. For a simplified example, if I wanted to run `nuproducts` on observations 1 and 2, for module A, in regions NE and SW, I would create a function `input_testexperiment()` that generates `[(1,A,NE), (1,A,SW), (2,A,NE), (2,A,SW)]` (note that in general, more parameters are needed than just these 3). Then `nutools.run` can run `nutools.nuproducts` on each of these input tuples. Next, I would do the same for `group_pha.py`, `bin_pha.py`, and depending on what analysis I'm conducting, `xspec.py`.

## Authors

* Evan Tey

## Acknowledgments

* To Kerstin Perez and Shuo Zhang for informing the direction of the analysis.
