# a collection of 2D fitting utilities

import os
import sherpa.astro.ui as shp

# load combined mosaic, exposure map, and psf file
def setup(filename):
    shp.load_data(filename)

    shp.load_table_model('emap', 'nuexpo_fin_combined.img')
    shp.freeze(emap.ampl)

    # we're using an on axis psf provided in 
    # /packages/CALDB/data/nustar/fpm/bcf/psf/
    shp.load_psf('psf', 'nuA2dpsf20100101v003_onaxis.fits')
    shp.set_psf(psf)
    psf.center = (500.0, 500.0)
    psf.size = (200, 200)

'''
sherpa saves models as tables of simulated values (not as components with parameters).
This makes it hard to keep track of the components we use to build full models especially
if they result from fitting (e.g. we don't want to have to refit the background model
every the system crashes). This function saves components of a model to a file by 
saving the important components and parameters.

Note this does not save the relationship between the components or the thaw/frozen state.

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
def save_components(filename, compIDstosave=None):
    if os.path.isfile(filename): raise Exception("Model already exists.")
    with open(filename, 'w') as f:
        print('Saving ' + filename)
        print(shp.get_model())
        if compIDstosave is None: 
            compIDstosave = [c for c in shp.list_model_components() if c not in ['emap', 'psf']]
        f.write('components: ' + str(len(compIDstosave)) + '\n')
        for compID in compIDstosave:
            if compID not in ['psf', 'emap']:
                comp = shp.get_model_component(compID)
                f.write(comp.name.replace('.', ' ') + ' ' + str(len(comp.pars)) + '\n')
                for par in comp.pars:
                    f.write(par.name + ' ' +
                        str(par.min) + ' ' +
                        str(par.val) + ' ' +
                        str(par.max) + '\n')
        f.close()

'''
loads components saved by the save_components function so they can be used as 
building blocks to form complex full models
'''
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
