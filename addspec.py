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

run(input_all(), addspec)
