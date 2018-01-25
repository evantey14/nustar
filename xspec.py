import itertools
from nutools import run, xspec

years = ['2012', '2017']
observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
modules = ['A', 'B']
regions = ['NE', 'SW']

data_path = '/home/evan/spectra/data'
analysis_path = '/home/evan/spectra/scripts/spectra_analyzers'

def input_individual(analysis_file):
    args = []
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        working_directory = data_path + '/' + 'individual'
        data = 'nu' + observation + module + region + '_sr_bin.pha'
        analysis = analysis_path + '/' + analysis_file
        stemout = 'nu' + observation + module + region
        args.append((working_directory, data, analysis, stemout))
    return args

def input_combined(analysis_file):
    args = []
    for year, module, region in list(itertools.product(years, modules, regions)):
        working_directory = data_path + '/' + 'combined'
        data = year + '_' + module + '_' + region + '_bin.pha'
        analysis = analysis_path + '/' + analysis_file
        stemout = year + '_' + module + '_' + region
        args.append((working_directory, data, analysis, stemout))
    return args

run(input_combined('po2040.xcm'), xspec) 
