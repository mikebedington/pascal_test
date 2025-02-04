import pathlib
from coupler import *
import numpy as np
from datetime import datetime, timedelta
from opendrift.readers.reader_constant import Reader as ConstantReader


nsup_individ = 100
nindivid_per_sup = 10000
timestep = dt.timedelta(seconds=21600)
start_date = dt.datetime(2010,1,1)
end_date = dt.datetime(2011,1,1)
duration = 3
seeding_rate = 10

# No horizontal movement, here only investigating vertical mixing and swimming
reader = ConstantReader(
        {'x_sea_water_velocity': 0.1, 'y_sea_water_velocity': 0.05, 'x_wind': 0, 'y_wind': 0,
         'temperature': 10, 'sea_water_salinity': 35,
         'land_binary_mask': 0, 'ocean_vertical_diffusivity': .02, 'food1concentration':10, 'irradiance':10, 
		 'pred1dens':10, 'pred1lightdep':10, 'mld':100, 'z':1500})

inputdatapath = pathlib.Path('/home/michael/Projects/Migratory_crossroads/Models/PASCAL-v4.0/inputdata')
cmm_data_nc = nc.Dataset(inputdatapath / "cmm3di.nc", mode = "r")

cmm = cmm_data_nc.variables["cmmu"][:]
maxfood1concentration_idx = 10
mintemperature_idx = 1
maxtemperature_idx = 14

cmm_lower = cmm[:, maxfood1concentration_idx, maxtemperature_idx]
cmm_upper = cmm[:, maxfood1concentration_idx, mintemperature_idx]

diapausedepth = 903 # Has to be one of the values given in depthrange
global_settings = {'developmentalcoefficient':np.array([595.00, 388.00, 581.00]), 'pred2risk':0, 'bgmortalityrisk':0, 'maxirradiance':0.3, 'cmm_lower':cmm_lower, 'cmm_upper':cmm_upper, 'ageceiling':2180 , 'fecundityceiling':10, 'depthrange':np.array([1, 2, 3, 4, 6, 7, 8, 10, 12, 14, 16, 19, 22, 26, 30, 35, 41, 48, 56, 66, 78, 93, 110, 131, 156, 187, 223, 267, 319, 381, 454, 542, 644, 764, 903, 1063, 1246])}

outputgrid = {'lon':[2.5, 3, 3.5, 4], 'lat':[60, 60.5, 61, 61.5]}

debug = ['lifestatus', 'nvindividuals', 'developmentalstage', 'thermalhistory', 'structuralmass', 'maxstructuralmass', 'reservemass', 'age', 'sex', 'timeofdiapauseentry', 'timeofdiapauseexit', 'structuralmassatdiapauseentry', 'reservemassatdiapauseentry', 'inseminationstate', 'reproductiveallocation', 'malegenome', 'totalfecundity', 'potentialfecundity', 'zpos', 'zidx'] 

bb = PascalAdvection(nsup_individ, nindivid_per_sup, global_settings, reader, timestep, start_date, duration, seeding_rate, outputgrid = outputgrid, debug=debug)
bb.run()




"""
Just testing opendrift component
o = PascalDrift(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(r)
o.set_config('general:use_auto_landmask', False)
# Adjusting some configuration
o.set_config('drift:vertical_mixing', False)
o.set_config('vertical_mixing:diffusivitymodel', 'windspeed_Sundby1983') # windspeed parameterization for eddy diffusivity
# Vertical mixing requires fast time step
o.set_config('vertical_mixing:timestep', 60.) # seconds

o.seed_elements(lon=3, lat=60.5, z=-10, number=nsup_individ, radius=30000, time=datetime.now()) # We kick off for all 

# Running model
o.run(duration=timedelta(hours=120), time_step=3600)

# Print and plot results.
# At the end the wind vanishes, and eggs come to surface
o.animation(fast=True, color='z')
o.plot_property('z', mean=True)

nsup = nsup_individ

tracker = PascalDrift()
tracker.add_reader(reader)
tracker.set_config('vertical_mixing:diffusivitymodel', 'windspeed_Sundby1983')
tracker.seed_elements(lon=3, lat=60.5, z=-10, number=nsup, radius=30000, time=start_date) # Need to change start times to fit sequential seeding in original pascal
tracker.run_prep(time_step=timestep.seconds,
                steps=None,
                time_step_output=None,
                duration=None,
                end_time=end_date,
                stop_on_error=True)

"""
