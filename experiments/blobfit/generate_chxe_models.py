# pure python verstion of single_gaussian_component_model.ipynb because this is faster
import sherpa.astro.ui as shp
import utils

shp.set_stat('cash')
shp.set_method('simplex')
shp.set_method_opt('verbose', 1)

utils.setup('numosaic_fin_combined_40-50keV.img')

utils.load_components('40-50 keV/bg 150-212.5.model')

# CHXE model
shp.set_full_model(psf(shp.gauss2d.chxe*emap) + bg*emap)

# inner radii chosen 
for r in [20, 24, 28, 32]:
    # from KP15, (ra, dec) = (266.4172 deg, -29.00716 deg)
    # systematic shifting error = 6" = 2.4 px
    # ellip = .52
    # theta = 57 deg (from positive north) 
    shp.set_par(chxe.xpos, 497.4, 497.4-4, 497.4+4)
    shp.set_par(chxe.ypos, 499.1, 499.1-4, 499.1+4)
    shp.set_par(chxe.fwhm, 30, 1, 200)
    shp.set_par(chxe.ellip, .5)
    shp.set_par(chxe.theta, -.9948)
    shp.set_par(chxe.ampl, 1e-5)
    shp.thaw(chxe.ellip, chxe.xpos, chxe.ypos)

    print(shp.get_model())

    shp.ignore2d('circle(500,500,1000)')
    shp.notice2d('circle(500,500,60)')
    shp.ignore2d('circle(500,500,' + str(r) + ')')
    shp.fit()
    
    print(shp.get_model())

    shp.set_conf_opt('numcores', 3)
    shp.set_conf_opt('maxiters', 50)
    shp.set_conf_opt('fast', True)
    shp.set_conf_opt('remin', 10000.0)
    shp.set_conf_opt('soft_limits', True)
    shp.freeze(chxe.xpos, chxe.ypos)

    #shp.conf(chxe.ellip, chxe.fwhm)
    
    utils.save_components('40-50 keV/chxe' + str(int(r*2.5)) + '.model', ['chxe'])
    shp.save('40-50 keV/fits/chxe150/chxe' + str(int(r*2.5)) + 'fit.sav')
