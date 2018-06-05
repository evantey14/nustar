# Native Spectral Analysis
1. Extracting raw spectra
    * `nuproducts` generates spectra from raw event files (counts on the detector chips) for single observations. (Call `fhelp nuproducts` for more info.)
        * Input
            * Cleaned event file (`nu30001002001A01_cl.evt`): Output from `nupipeline` along with any other data cleaning.
            * a source region: Area of interested. Created in ds9.
            * a background region: Nearby area used as a reference point. Created in ds9.
            * plus a bit more information (e.g is it a point source?)
        * Relevant Output
            * source spectrum (`*_sr.pha`): Photon counts per channel in the source region.
            * response files (`*_sr.arf`, `*_sr.rmf`): Maps channels to energy bands.
            * background spectrum (`*_bk.pha`): Photon counts per channel in the background region.
    * `addspec`: TODO
2. Define bins
    * We use GDL procedures `groupingPHA_BACK.pro` and `groupingPHA_EXPO.pro` to create _grouping files_. These define energy bins by calcluating energy ranges that have at least $x$ source counts over the background starting from 0 keV (default $x$ = 20).
    1. Call `gdl` to enter the gdl shell.
    2. Load the procedure with `.comp groupingPHA_*.pro` (`BACK` is for individual spectra while `EXPO` is for combined spectra).
    3. Call `groupingpha2, 'SRCPHA', 'BGPHA', 'OUTFILE', x` with the actual filenames replaced.
    4. Exit the shell with `exit`.
3.  Bin spectra
    * Now that we've defined the bin groups, use `grppha` to generate binned spectra.
    1. Start the grppha shell with `grppha SRCPHA OUTFILE`.
    2.  Bin the spectra with `group GRPFILE` where `GRPFILE` is the output of the step 2.
    3. Exit the shell with `exit`.
4. Analyze the spectra:
    1. Enter xspec shell with `xspec`.
    2. Load data with `data BINNEDPHA` where `BINNEDPHA` is the output of step 3.
    3. Analyze! Here are a couple things you might want to do
        * Focus on data ranges with `ignore **-3.0 10.0-**` to focus on 3-10 keV.
        * Plot the data with `setplot energy` then `plot ldata`.
        * Fit a model
            * First set `abund wilm` and `xsect vern`.
            * Define the model with, for example, `model tbabs*apec`. See [this](https://heasarc.nasa.gov/xanadu/xspec/manual/node129.html) for more info on models.
            * Fit the model to the data with `fit`.
        * Calculate confidence intervals on parameters with, for example, `error 7` to find the 90% CI on the 7th model parameter.  
        * See the [XSPEC manual](https://heasarc.nasa.gov/xanadu/xspec/manual/XspecManual.html) for other tools.

