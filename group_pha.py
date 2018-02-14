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

def input_combined():
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

def input_clock():
    args = []
    working_directory = data_path + '/' + 'clock'
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = ['9', '10', '11', '12', '1', '2', '3', '4']
    for observation, region in list(itertools.product(observations, regions)):
        stem = 'nu' + observation + module + region

        infile = working_directory + '/' + stem + '_sr.pha'
        bgfile = working_directory + '/' + stem + '_bk.pha'
        outfile = working_directory + '/' + stem + '_group.dat'
        minbincount = '20'
        is_individual = True

        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args

def input_ne():
    args = []
    working_directory = data_path + '/' + 'ne'
    for module in modules:
        infile = working_directory + '/' + module + '_NE.pha'
        bgfile = working_directory + '/' + module + '_NE.bak'
        outfile = working_directory + '/' + module + '_NE_group.dat'
        minbincount = '20'
        is_individual = False
        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args

def input_annulus():
    args = []
    working_directory = data_path + '/' + 'annulus'
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = ['90', '110', '130']
    for observation, region in list(itertools.product(observations, regions)):
        stem = 'nu' + observation + module + region

        infile = working_directory + '/' + stem + '_sr.pha'
        bgfile = working_directory + '/' + stem + '_bk.pha'
        outfile = working_directory + '/' + stem + '_group.dat'
        minbincount = '20'
        is_individual = True

        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args

def input_epanda():
    args = []
    working_directory = data_path + '/' + 'epanda'
    observations = ['30001002001', '30001002003', '30302007002', '30302007004']
    module = 'A'
    regions = [size + direction
                    for size, direction
                    in list(itertools.product(['90', '110', '130'], ['N', 'E', 'S', 'W']))]
    for observation, region in list(itertools.product(observations, regions)):
        stem = 'nu' + observation + module + region

        infile = working_directory + '/' + stem + '_sr.pha'
        bgfile = working_directory + '/' + stem + '_bk.pha'
        outfile = working_directory + '/' + stem + '_group.dat'
        minbincount = '20'
        is_individual = True

        args.append((infile, bgfile, outfile, minbincount, is_individual))
    return args


run(input_epanda(), group_pha)
