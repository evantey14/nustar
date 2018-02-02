import itertools
from nutools import run, bin_pha

years = ['2012', '2017']
observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
modules = ['A', 'B']
regions = ['NE', 'SW']

data_path = '/home/evan/spectra/data'

def input_individual():
    args = []
    working_directory = data_path + '/' + 'individual'
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        stem = 'nu' + observation + module + region

        infile = working_directory + '/' + stem + '_sr.pha'
        grpfile = working_directory + '/' + stem + '_group.dat'
        outfile = working_directory + '/' + stem + '_sr_bin.pha'

        args.append((infile, grpfile, outfile))

    return args

def input_combined():
    args = []
    working_directory = data_path + '/' + 'combined'
    for year, module, region, in list(itertools.product(years, modules, regions)):
        stem = year + '_' + module + '_' + region
        
        infile = working_directory + '/' + stem + '.pha'
        grpfile = working_directory + '/' + stem + '_group.dat'
        outfile = working_directory + '/' + stem + '_bin.pha'
    
        args.append((infile, grpfile, outfile))

    return args

def input_clock():
    args = []
    working_directory = data_path + '/' + 'clock'
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = ['9', '10', '11', '12', '1', '2', '3', '4']
    for observation, region in list(itertools.product(observations, regions)):
        stem = 'nu' + observation + module + region

        infile = working_directory + '/' + stem + '_sr.pha'
        grpfile = working_directory + '/' + stem + '_group.dat'
        outfile = working_directory + '/' + stem + '_sr_bin.pha'

        args.append((infile, grpfile, outfile))
    return args

run(input_clock(), bin_pha)
