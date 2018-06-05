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

def input_individualASW(analysis_file):
    args = []
    module = 'A'
    region = 'SW'
    working_directory = data_path + '/' + 'individual'
    data = ['nu' + observation + module + region + '_sr_bin.pha'
            for observation in observations]
    analysis = analysis_path + '/' + analysis_file
    stemout = module + region
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

def generate_simulation():
    working_directory = data_path + '/' + 'simulations'
    import os
    os.chdir(working_directory) # xspec has trouble reading far away files
    
    models = ['po', 'bremss']
    params = ['min', 'best', 'max']

    nhvalue = 16.4
    paramvalues = {'po':{'min':1.2 , 'best':1.6 , 'max':1.9 }, 
                    'bremss':{'min':36 , 'best':66 , 'max':200 }}
    fluxvalues = {'po': 1.6e-4, 'bremss': 1.9e-4}

    for model, param in list(itertools.product(models, params)):
        stem = model + param 
         
        with open('xspec_tmp.xcm', 'w') as f:
            f.write('data A_NE.pha\n')
            f.write('model tbabs*' + model + ' & {'+str(nhvalue)+'} & {'+str(paramvalues[model][param])+'} & {'+str(fluxvalues[model])+'}\n')
            f.write('fakeit & {} & {} & {'+stem+'.fak} & {1e6, 1, 1e6}\n')
            f.write('exit\n')
            f.close()
            os.system('xspec xspec_tmp.xcm')
            os.remove('xspec_tmp.xcm')
    
def analyze_simulation(analysis_file):
    args = []
    working_directory = data_path + '/' + 'simulations'
    models = ['po', 'bremss']
    params = ['min', 'best', 'max']
    for model, param in list(itertools.product(models, params)):
        stem = model + param 
        data = stem + '_bin.fak'
        analysis = analysis_path + '/' + analysis_file
        stemout = stem
        args.append((working_directory, data, analysis, stemout))
    return args
  
#generate_simulation()
run(analyze_simulation('simanal10.xcm'), xspec) 
