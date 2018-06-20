# TODO: add print logging (particularly if files don't exist)
import os, re

def nuproducts(indir, outdir, instrument, steminputs, stemout, srcregionfile, bkgregionfile, evtfile):
    # returns nuproducts command on a particular observation
    # can't call command because of how nuproducts works
    if os.path.isfile(evtfile):
        print('Calling nuproducts for ' + evtfile)
        return 'nuproducts' + ' ' + \
                'indir=' + indir + ' ' + \
                'outdir=' + outdir + ' ' + \
                'instrument=' + instrument + ' ' + \
                'steminputs=' + steminputs + ' ' + \
                'stemout=' + stemout + ' ' + \
                'srcregionfile=' + srcregionfile + ' ' + \
                'bkgregionfile=' + bkgregionfile + ' ' + \
                'imagefile=NONE' + ' ' + \
                'lcfile=NONE' + ' ' + \
                'bkglcfile=NONE' + ' ' + \
                'correctlc=no' + ' ' + \
                'extended=yes'
    else:
        print(evtfile + ' does not exist')

def addspec(working_directory, product_directory, observations, outfile):
    # create list of spectra to add, then generate new source spectra, background spectra, and response file with addspec
    os.chdir(product_directory) # addspec must be called in the directory of input spectra because it tries to extrapolate the names of the response and bg files 

    print('Adding spectra: ' + outfile + ' ' + '|'.join(observations))

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

    os.chdir(working_directory) # change back to the original directory

def group_pha(infile, bgfile, outfile, minbincount, is_individual):
    # Create a grouping file by running groupingPHA_(EXPO|BACK).pro
    # Create a .sh file to run the GDL script on the input spectra (not aware of any better way to do this)
    if(os.path.isfile(infile)):
        print('grouping ' + infile)
        with open('remove_bg.sh', 'w') as f:
            gdlfile = os.path.dirname(__file__) + '/' + \
                ('groupingPHA_BACK.pro' if is_individual else 'groupingPHA_EXPO.pro')
            
            quotewrap = lambda x: '\'' + x + '\'' # the GDL scripts expect files wrapped in single quotes
            
            f.write('.comp ' + gdlfile + '\n')
            f.write('groupingpha2,' + quotewrap(infile) + ',' + \
                        quotewrap(bgfile) + ',' + \
                        quotewrap(outfile) + ',' + \
                        minbincount + '\n')
            f.write('exit\n')
            
            f.close()

        os.system('gdl remove_bg.sh')
        os.remove('remove_bg.sh')
    else:
        print(infile + ' does not exist')

def bin_pha(infile, grpfile, outfile):
    # Bin pha file using grppha and grouping file created by group_pha
    if(os.path.isfile(infile)):
        print('binning ' + infile)
        os.system('grppha' + ' ' + \
                        infile + ' ' + \
                        '!' + outfile + ' ' + \
                        '\'' + 'group' + ' ' + grpfile + '\'' + ' ' + \
                        'exit')
    else:
        print(infile + ' does not exist')

# The following functions are deprecated in favor of in sherpa xspec analysis
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
number = r'[+\-]?\d*\.?\d+(?:[Ee][+\-]?\d+)?'

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
