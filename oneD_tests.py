import pathlib
from individual import *
from coupler import *

#from coupler import PascalSimulation
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# Load the netCDF data
inputdatapath = pathlib.Path('/home/michael/Projects/Migratory_crossroads/Models/PASCAL-v4.0/inputdata')

temperature_data_nc = nc.Dataset(inputdatapath / "temperature4di.nc", mode = "r")
food1concentration_data_nc = nc.Dataset(inputdatapath / "chl4di.nc", mode = "r")
nsv_data_nc = nc.Dataset(inputdatapath / "vo4di.nc", mode = "r")
esv_data_nc = nc.Dataset(inputdatapath / "uo4di.nc", mode = "r")
smld_data_nc = nc.Dataset(inputdatapath / "smld3di_v2.nc", mode = "r")
irradiance_data_nc = nc.Dataset(inputdatapath / "irradiance4di.nc")
pred1lightdep_data_nc = nc.Dataset(inputdatapath / "pred1lightdep4di.nc")
pred1dens_data_nc = nc.Dataset(inputdatapath / "pred1dens4di.nc")
cmm_data_nc = nc.Dataset(inputdatapath / "cmm3di.nc", mode = "r")

i = slice(9,11)
j = 10
t = slice(0,1460)

# Turn into struct like object
env_dict = dotdict({'temperature':temperature_data_nc.variables["temperature"][t, :, i, j].T,
'food1concentration':food1concentration_data_nc.variables["chl"][t, :, i, j].T,
'nsv':nsv_data_nc.variables["vo"][t, :, i, j].T,
'esv':esv_data_nc.variables["uo"][t, :, i, j].T,
'mld':smld_data_nc.variables["smld"][t, i, j].T,
'irradiance':irradiance_data_nc.variables["par"][t, :, i, j].T,
'pred1dens':pred1dens_data_nc.variables["p1risk"][t, :, i, j].T,
'pred1lightdep':pred1lightdep_data_nc.variables["parrs"][t, :, i, j].T
})

for k, v in env_dict.items():
	try:
		env_dict[k] = np.transpose(v,[2,0,1])
	except ValueError:
		env_dict[k] = np.transpose(v,[1,0])

tracker = dotdict({'environment':env_dict})
environment_ind = 0
cmm = cmm_data_nc.variables["cmmu"][:]
maxfood1concentration_idx = 10
mintemperature_idx = 1
maxtemperature_idx = 14

cmm_lower = cmm[:, maxfood1concentration_idx, maxtemperature_idx]
cmm_upper = cmm[:, maxfood1concentration_idx, mintemperature_idx]

diapausedepth = 903 # Has to be one of the values given in depthrange
global_settings = {'developmentalcoefficient':np.array([595.00, 388.00, 581.00]), 'pred2risk':0, 'bgmortalityrisk':0, 'maxirradiance':0.3, 'cmm_lower':cmm_lower, 'cmm_upper':cmm_upper, 'ageceiling':2180 , 'fecundityceiling':10, 'depthrange':np.array([1, 2, 3, 4, 6, 7, 8, 10, 12, 14, 16, 19, 22, 26, 30, 35, 41, 48, 56, 66, 78, 93, 110, 131, 156, 187, 223, 267, 319, 381, 454, 542, 644, 764, 903, 1063, 1246])}

"""
aa = SuperIndividual(global_settings, diapausedepth, env_dict, environment_ind)i


i = 0
while aa.lifestatus > 0:
   print(f'{aa.nvindividuals}, {aa.age}, {aa.zidx}, {aa.diapausestate}, {aa.developmentalstage}, {aa.structuralmass}, {aa.zpos}, {aa.diapausedepth}')
   aa.update_lifestage()
   i += 1
"""

nsup_individ = 100
nindivid_per_sup = 10000
timestep = dt.timedelta(seconds=21600)
start_date = dt.datetime(2010,1,1)
duration = 3
seeding_rate = 10

# expand the environment to cover the timeperiod
for k, v in env_dict.items():
	if k =='mld':
		env_dict[k] = np.tile(v,[duration,1])
	else:
		env_dict[k] = np.tile(v,[duration,1,1])
reader = env_dict

bb = Pascal1D(nsup_individ, nindivid_per_sup, global_settings, reader, timestep, start_date, duration, seeding_rate)
bb.run()
