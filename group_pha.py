import itertools
from nutools import run, group_pha

years = ['2012', '2017']
observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
modules = ['A', 'B']
regions = ['NE', 'SW']

data_path = '/home/evan/spectra/data'

def input_observations():
    args = []
    working_directory = data_path + '/' + 'individual'
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        stem = 'nu' + observation + module + region
        
        infile = working_directory + '/' + stem + '_sr.pha'
        bgfile = working_directory + '/' + stem + '_bk.pha'
        outfile = working_directory + '/' + stem + '_group.dat'
        minbincount = '20'
        is_individual = True
        
        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args

def input_year_module_region():
    args = []
    working_directory = data_path + '/' + 'combined'
    for year, module, region in list(itertools.product(years, modules, regions)):
        stem = year + '_' + module + '_' + region
        
        infile = working_directory + '/' + stem + '.pha' 
        bgfile = working_directory + '/' + stem + '.bak' 
        outfile= working_directory + '/' + stem + '_group.dat'
        minbincount = '20' 
        is_individual = False   
     
        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args 

run(input_year_module_region(), group_pha)
