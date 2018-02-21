import itertools
from nutools import run, addspec

years = ['2012', '2017']
modules = ['A', 'B']
regions = ['NE', 'SW']
observations = {'2012': ['30001002001', '30001002003', '30001002004'],
                        '2017': ['30302006004', '30302006006', '30302007002', '30302007004']}

data_path = '/home/evan/spectra/data' 

def input_all():
    args = []
    working_directory = data_path + '/' + 'individual'
    for year, module, region in list(itertools.product(years, modules, regions)):
        input_obs = ['nu' + observation + module + region + '_sr.pha'
                        for observation in observations[year]]  
        outfile = data_path + '/' + 'combined' + '/' + \
                    year + '_' + module + '_' + region
        args.append((working_directory, input_obs, outfile))
    return args

def input_ne():
    args = []
    working_directory = data_path + '/' + 'ne'
    observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
    region = 'NE'
    for module in modules:
        input_obs = ['nu' + observation + module + region + '_sr.pha'
                        for observation in observations]
        outfile = working_directory + '/' + module + '_NE'
        args.append((working_directory, input_obs, outfile))
    return args

def input_annulus_2012_combined():
    args = []
    working_directory = data_path + '/' + 'annulus_2012_combined'
    year = '2012'
    module = 'A'
    regions = ['90', '110', '130']
    observations = ['30001002001', '30001002003']
    for region in regions:
        input_obs = ['nu' + observation + module + region + '_sr.pha'
                        for observation in observations]
        outfile = working_directory + '/' + year + module + region
        args.append((working_directory, input_obs, outfile))
    return args

#print(input_annulus())
run(input_annulus_2012_combined(), addspec)
