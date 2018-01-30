import os, re

def run(args, function):
    [function(*arg) for arg in args]

def nuproducts(indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile):
    # Executes nuproducts on a particular observation.
    if os.path.isfile(evtfile):
        os.system('nuproducts' + ' ' + \
                'indir=' + indir + ' ' + \
                'outdir=' + outdir + ' ' + \
                'instrument=' + instrument + ' ' + \
                'steminputs=' + steminputs + ' ' + \
                'stemout=' + stemout + ' ' + \
                'srcregionfile=' + srcregionfile + ' ' + \
                'bkgregionfile=' + bkgregionfile + ' ' + \
                'extended=yes')

def addspec(working_directory, observations, outfile):
    # create list of observations to add, then add with addspec
    os.chdir(working_directory) # addspec must be called in the directory of input spectra because it tries to extrapolate the names of the response and bg files 
    with open('addspec_tmp.dat', 'w') as f:
        [f.write(observation + '\n') 
            for observation in observations 
            if os.path.isfile(observation)]
    os.system('addspec' + ' ' + \
                'addspec_tmp.dat' + ' ' + \
                outfile + ' ' + \
                'qaddrmf=yes' + ' ' + \
                'qsubback=yes') # outfile must not already exist. ! prevents addspec from finding files and clobber doesn't work 
    os.remove('addspec_tmp.dat')

def group_pha(infile, bgfile, outfile, minbincount, is_individual):
    # Create a grouping file by running groupingPHA_(EXPO|BACK).pro 
    if(os.path.isfile(infile)):
        with open('remove_bg.sh', 'w') as f:
            gdlfile = 'groupingPHA_BACK.pro' if is_individual else 'groupingPHA_EXPO.pro' 
            f.write('.comp ' + gdlfile + '\n')
            wrap = lambda x: '\'' + x + '\'' # the GDL scripts expect files wrapped in ' 
            f.write('groupingpha2,' + wrap(infile) + ',' + wrap(bgfile) + ',' + wrap(outfile) + ',' + minbincount + '\n')
            f.write('exit\n')
            f.close()

        os.system('gdl remove_bg.sh') # Execute script since idk how else to execute it
        os.remove('remove_bg.sh')

def bin_pha(infile, grpfile, outfile):
    # Bin pha file using grppha and grouping file created by group_pha
    if(os.path.isfile(infile)):
        os.system('grppha' + ' ' + \
                        infile + ' ' + \
                        '!' + outfile + ' ' + \
                        '\'' + ' ' + 'group' + ' ' + grpfile + '\'' + ' ' + \
                        'exit')

def xspec(working_directory, data, analysis, stemout):
    # Perform xspec analysis on data using prewritten analysis
    os.chdir(working_directory) # xspec has trouble reading far away files

    inputdata = None 
    if(isinstance(data, str)):
        inputdata = data if os.path.isfile(data) else None
    elif(isinstance(data, list)):
        inputdata = ' '.join(spectrum for spectrum in data if os.path.isfile(spectrum))
 
    if(inputdata is not None):
        with open('xspec_tmp.xcm', 'w') as f:
            f.write('data ' + inputdata + '\n')
            
            with open(analysis) as af:
                for line in af:
                    if('STEM' in line):
                        line = line.replace('STEM', stemout) # insert stemout in placeholder file names for analysis logs/images
                    f.write(line)
                f.write('exit\n')
                f.close()

            os.system('xspec xspec_tmp.xcm')
            os.remove('xspec_tmp.xcm')

# capture any number in scientific notation
number = r'[+\-]?(?:\d*\.\d*)(?:[Ee][+\-]?\d+)?'

# capture xspec log number ranges which look like "min max (min-val,max-val)"
number_range = r'' + number + '\s*' + number + '\s*\(' + number + ',' + number + '\)'

def parse_red_chisq(log):
    red_chisq = re.findall(r'(?:Reduced chi-squared = \s*)' + number, log)[0]
    return red_chisq.split()[-1]

def parse_param(log, param):
    pound, param_index, param_min, param_max, param_err = re.findall(r'#\s*(?:' + str(param) + ')\s*' + number_range, log)[0].split()
    param_value = str(float(param_max) - float(param_err.split(',')[-1][:-1]))
    return ','.join([param_value, param_min, param_max])

def parse_xspec_log(logid, logfile, params):
    # parse generated xspec log for reduced chi squared and parameters
    line = logid
    if(os.path.isfile(logfile)):
        with open(logfile) as f:
            log = f.read()
            line += ',' + parse_red_chisq(log)
            for param in params:
                line += ',' + parse_param(log, param)
        print line 
