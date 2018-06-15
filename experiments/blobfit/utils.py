import os
import sherpa.astro.ui as shp

def setup(filename):
    # load combined mosaic, exposure map, and psf file
    shp.load_data(filename)

    shp.load_table_model('emap', 'nuexpo_fin_combined.img')
    shp.freeze(emap.ampl)

    # we're using an on axis psf provided in 
    # /packages/CALDB/data/nustar/fpm/bcf/psf/
    shp.load_psf('psf', 'nuA2dpsf20100101v003_onaxis.fits')
    shp.set_psf(psf)
    psf.center = (500.0, 500.0)
    psf.size = (200, 200) # from kerstin's code fit


'''
sherpa saves models as table values (not as components).
This function saves components of a model to a file 
by saving the important components and parameters.
example.model:
components: 2 
COMP1TYPE COMP1NAME NUMPARS
PAR1NAME PAR1MIN PAR1VAL PAR1MAX
PAR2NAME PAR2MIN PAR2VAL PAR2MAX
...
COMP2TYPE COMP2NAME NUMPARS
PAR1NAME PAR1MIN PAR1VAL PAR1MAX
PAR2NAME PAR2MIN PAR2VAL PAR2MAX
...
'''
def save_components(filename, compIDs=None):
    if os.path.isfile(filename): raise Exception("Model already exists.")
    with open(filename, 'w') as f:
        print('Saving ' + filename)
        print(shp.get_model())
        if compIDs is None: 
            compIDs = [c for c in shp.list_model_components() if c not in ['emap', 'psf']]
        f.write('components: ' + str(len(compIDs)) + '\n')
        for compID in compIDs:
            if compID not in ['psf', 'emap']:
                comp = shp.get_model_component(compID)
                f.write(comp.name.replace('.', ' ') + ' ' + str(len(comp.pars)) + '\n')
                for par in comp.pars:
                    f.write(par.name + ' ' +
                        str(par.min) + ' ' +
                        str(par.val) + ' ' +
                        str(par.max) + '\n')
        f.close()

def load_components(filename):
    with open(filename) as f:
        print('Loading ' + filename)
        numcomponents = f.readline().split(' ')[-1]
        for i in range(int(numcomponents)):
            comptype, compname, numpars = f.readline().split(' ')
            comp = shp.create_model_component(comptype, compname)
            for j in range(int(numpars)):
                parname, parmin, parval, parmax = f.readline().split(' ')
                for par in comp.pars:
                    if parname == par.name:
                        par.min, par.val, par.max = parmin, parval, parmax
            print(comp)
