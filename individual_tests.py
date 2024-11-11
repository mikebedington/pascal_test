from individual import *

cmm_nc = nc.Dataset('/home/michael/Projects/Migratory_crossroads/Models/PASCAL-v4.0/inputdata/cmm3di.nc')
cmm = cmm_nc['cmmu'][:]
"""
food1concentration_nc = food1concentration_data_nc.variables["chl"][:, :, 0:10, 0:10]
food1concentration = np.array(food1concentration_nc, dtype = np.float32)

#this estimates the ceiling maximum food1concentration across the upper pelagial (where development of super individuals usually takes place): depth cutoff point is 200 m (depthgrade index = 25) as an integer
maxfood1concentration = int(np.ceil(np.nanmax(food1concentration[:,0:25,:,:])))

maxfood1cocnetrat

#defines the developmental stage grading (n = 13), category#1 food concentration grading (n = 23) and temperature grading (n = 23) for slicing environmental-specific criticalmolting masses (<stage>, <f1con>, <temp>)
developmentalstagegrade = np.arange(start = 0, stop = 13, step = 1)
food1concentrationgrade = np.arange(start = 1, stop = 24, step = 1)
temperaturegrade = np.arange(start = -2, stop = 21, step = 1)

#index position of the minimum temperature (with respect to the temperaturegrade numpy array) as a minimum absolute error function (mae)
mintemperature_idx = np.argmin(abs(temperaturegrade - mintemperature))
#index position of the maximum temperature (with respect to the temperaturegrade numpy array) as a minimum absolute error function (mae)
maxtemperature_idx = np.argmin(abs(temperaturegrade - maxtemperature))
#index position of maximum category#1 food concentration (with respect to the food1concentrationgrade numpy array) as a minimum absolute error function (mae)

"""
maxfood1concentration_idx = 10
mintemperature_idx = 1
maxtemperature_idx = 14

#extracting the stage-specific critical molting masses bounds for the given model environment (slicing: <devstage, food1con, temp>)
#nb:higher body masses are prevalent at lower temperatures, due to the temperature-size rule
cmm_lower = cmm[:, maxfood1concentration_idx, maxtemperature_idx]
cmm_upper = cmm[:, maxfood1concentration_idx, mintemperature_idx]

diapausedepth = 903 # Has to be one of the values given in depthrange
global_settings = {'developmentalcoefficient':np.array([595.00, 388.00, 581.00]), 'pred2risk':0, 'bgmortalityrisk':0, 'maxirradiance':0.3, 'cmm_lower':cmm_lower, 'cmm_upper':cmm_upper, 'ageceiling':2180 , 'fecundityceiling':1000}
aa = superindividual(global_settings, diapausedepth)

dep_lay = 37

temperature = np.ones(dep_lay)*10
pdens = np.ones(dep_lay)*1
plight = np.ones(dep_lay)*0.2
irr = np.ones(dep_lay)*0.1
food = np.ones(dep_lay)*3

aa.mld = 30
aa.temperature = temperature
aa.pred1dens = pdens
#this estimates the normalized and range-scaled (0.1-0.9) ambient shortwave irradiance for the calculation of light dependence of the visual predation risk
aa.pred1lightdep = plight
aa.irradiance = irr
aa.zidx = 5
aa.food1concentration = food

i = 0
while aa.lifestatus > 0:
   print(f'{aa.nvindividuals}, {aa.age}, {aa.zidx}, {aa.diapausestate}, {aa.developmentalstage}, {aa.structuralmass}, {aa.zpos}, {aa.diapausedepth}')
   aa.update_lifestage()
   i += 1
