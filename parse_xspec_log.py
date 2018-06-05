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

def parse_simulation():
    from nutools import parse_red_chisq, number
    import re
    working_directory = data_path + '/' + 'simulations/logs'
    models = ['po', 'bremss']
    params = ['min', 'best', 'max']
    analyses = ['tbabspofit', 'tbabsbremssfit', 'tbabspofit10', 'tbabsbremssfit10', 'pofit20', 'bremssfit20']

    for model, param, analysis in list(itertools.product(models, params, analyses)):
        stem = model + param + '_' + analysis
        logfile = working_directory + '/' + stem + '.log' 
        line = stem
        with open(logfile) as f:
            log = f.read()
            line += ',' + parse_red_chisq(log)
            matches = re.findall(number + '\s*\+\/\-', log) 
            for i in range(len(matches)):
                line += ',' + matches[i].split()[0] 
       
        print(line)

parse_simulation()

# useful analysis & parameters:
# po phoindex (1)
# tbabsapec kT (1) nH (2)

#run(input_individual('po1020', 'params', [1]), parse_xspec_log)
