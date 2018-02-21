import itertools
from nutools import * 

observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
regions = ['NE', 'SW']
modules = ['A', 'B']

data_path = '/home/evan/spectra/data'

def input_individual():
    args = []
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        indir = data_path + '/' + \
                observation + '/'

        outdir = data_path + '/' + \
                 observation + '/' + \
                 'products' + module + region + '/'

        instrument = 'FPM' + module

        steminputs = 'nu' + observation

        stemout = 'nu' + observation + module + region

        srcregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'Source_' + region + '.reg'

        bkgregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'bg_' + observation + module + '.reg'
        
        evtfile = indir + steminputs + module + '01_cl.evt'
      
        args.append((indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile))
    return args

def input_clock():
    args = []
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = ['9', '10', '11', '12', '1', '2', '3', '4']
    for observation, region in list(itertools.product(observations, regions)):
        indir = data_path + '/' + \
                observation + '/'

        outdir = data_path + '/' + \
                 observation + '/' + \
                 'clock_products' + module + region + '/'

        instrument = 'FPM' + module

        steminputs = 'nu' + observation

        stemout = 'nu' + observation + module + region

        srcregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'Source_' + region + '.reg'

        bkgregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'bg_' + observation + module + '.reg'

        evtfile = indir + steminputs + module + '01_cl.evt'

        args.append((indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile))
    return args

def input_annulus():
    args = []
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = ['90', '110', '130']
    for observation, region in list(itertools.product(observations, regions)):
        indir = data_path + '/' + \
                observation + '/'

        outdir = data_path + '/' + \
                 observation + '/' + \
                 'annulus_products' + module + region + '/'

        instrument = 'FPM' + module

        steminputs = 'nu' + observation

        stemout = 'nu' + observation + module + region

        srcregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'annulus' + region + '.reg'

        bkgregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'bg_' + observation + module + '.reg'

        evtfile = indir + steminputs + module + '01_cl.evt'

        args.append((indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile))
    return args

def input_epanda():
    args = []
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = [size + direction
                    for size, direction
                    in list(itertools.product(['90', '110', '130'], ['N', 'E', 'S', 'W']))]
    for observation, region in list(itertools.product(observations, regions)):
        indir = data_path + '/' + \
                observation + '/'

        outdir = data_path + '/' + \
                 observation + '/' + \
                 'epanda_products' + module + region + '/'

        instrument = 'FPM' + module

        steminputs = 'nu' + observation

        stemout = 'nu' + observation + module + region

        srcregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'epanda' + region + '.reg'

        bkgregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'bg_' + observation + module + '.reg'

        evtfile = indir + steminputs + module + '01_cl.evt'

        args.append((indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile))
    return args

def input_extended():
    args = []
    observations = ['30001002001', '30001002003', '30001002004']
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        indir = data_path + '/' + \
                observation + '/'

        outdir = data_path + '/' + \
                 observation + '/' + \
                 'extended_products' + module + region + '/'

        instrument = 'FPM' + module

        steminputs = 'nu' + observation

        stemout = 'nu' + observation + module + region

        srcregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'extended_' + region + '.reg'

        bkgregionfile = data_path + '/' + \
                        'regions' + '/' + \
                        'bg_' + observation + module + '.reg'

        evtfile = indir + steminputs + module + '01_cl.evt'

        args.append((indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile))
    return args

#print(input_extended())
run(input_extended(), nuproducts)
