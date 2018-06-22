import sherpa.astro.ui as shp

shp.restore('20-40 keV/fits/chxepwnblob.sav')


shp.set_conf_opt('numcores', 3)
shp.set_conf_opt('maxiters', 50)
shp.set_conf_opt('fast', True)
shp.set_conf_opt('remin', 10000.0)
shp.set_conf_opt('soft_limits', True)
shp.set_conf_opt('verbose', True)

shp.freeze(chxe)
shp.thaw(chxe.ampl)

print(shp.get_model())

shp.conf(blob.xpos, blob.ypos, blob.ellip, blob.fwhm, blob.theta, blob.ampl)
shp.save('20-40 keV/fits/chxepwnblobconf.sav')
