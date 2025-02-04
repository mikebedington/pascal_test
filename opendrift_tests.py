import sys
sys.path.append('/home/michael/Projects/Migratory_crossroads/Models/pascal_modular/opendrift_pascal')

import numpy as np
from datetime import datetime, timedelta
from opendrift.readers.reader_constant import Reader as ConstantReader
from opendrift.models.oceandrift import OceanDrift

from pascal_drift import *

# No horizontal movement, here only investigating vertical mixing and swimming
reader = ConstantReader(
        {'x_sea_water_velocity': 0.1, 'y_sea_water_velocity': 0.05, 'x_wind': 0, 'y_wind': 0,
         'temperature': 10, 'sea_water_salinity': 35,
         'land_binary_mask': 0, 'ocean_vertical_diffusivity': .02, 'food1concentration':10, 'irradiance':10,
         'pred1dens':10, 'pred1lightdep':10, 'mld':100, 'z':1500})


o = PascalDrift(loglevel=20)  # Set loglevel to 0 for debug information
o.add_reader(reader)
o.set_config('general:use_auto_landmask', False)

# Adjusting some configuration
#o.set_config('drift:vertical_mixing', True)
o.set_config('vertical_mixing:diffusivitymodel', 'windspeed_Sundby1983') # windspeed parameterization for eddy diffusivity
# Vertical mixing requires fast time step
o.set_config('vertical_mixing:timestep', 60.) # seconds

o.seed_elements(lon=3, lat=60.5, z=-10, number=1000, radius=30000, time=dt.datetime(2010,1,1))

# Running model
o.run(duration=timedelta(days=365), time_step=3600*6)

# Print and plot results.
# At the end the wind vanishes, and eggs come to surface
o.animation(fast=True, color='z')
o.plot_property('z', mean=True)



nautilos_data = '/home/michael/Projects/Nautilos/OpenDrift/opendrift_bioplast_othercode/test_cases/get_data'




