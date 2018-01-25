import itertools
from nutools import run, parse_xspec_log

years = ['2012', '2017']
observations = ['30001002001', '30001002003', '30001002004', '30302006004', '30302006006', '30302007002', '30302007004']
modules = ['A', 'B']
regions = ['NE', 'SW']

data_path = '/home/evan/spectra/data'

def input_individual(analysis, logtype, params):
    working_directory = data_path + '/' + 'individual'
    args = []
    for observation, module, region in list(itertools.product(observations, modules, regions)):
        logid = observation + module + region + analysis
        logfile = working_directory + '/' + \
                    'logs' + '/' + \
                    'nu' + observation + module + region + '_' + \
                    analysis + '_' + \
                    logtype + '.log'
        args.append((logid, logfile, params))
    return args

def input_combined(analysis, logtype, params):
    working_directory = data_path + '/' + 'combined'
    args = []
    for year, module, region in list(itertools.product(years, modules, regions)):
        logid = year + module + region + analysis
        logfile = working_directory + '/' + \
                    'logs' + '/' + \
                    year + '_' + module + '_' + region + '_' + \
                    analysis + '_' + \
                    logtype + '.log'
        args.append((logid, logfile, params))
    return args

# useful analysis & parameters:
# po phoindex (1)
# tbabsapec kT (1) nH (2)

run(input_individual('po1020', 'params', [1]), parse_xspec_log)
