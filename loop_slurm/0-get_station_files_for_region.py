# %% markdown
# Get station names within a region of interest and write them to a file
# NETWORK  CODE  LAT  LON  ELEV
# 
# %% codecell
import matplotlib.pyplot as plt
import obspy
from obspy.clients.fdsn import Client
from obspy import UTCDateTime
from obspy.core import AttribDict
from obspy.io.sac import SACTrace
import numpy as np
import matplotlib.pylab as plt
import os
import pandas as pd
# %matplotlib inline

# %% codecell
webservice = "IRIS"
networks = ""; #"YO" # YO ENAM; ZA NoMelt
tstart = "1999-01-01T00:00:00"
tend = "2100-01-01T00:00:00"
minlatitude = 41.8
maxlatitude = 47
minlongitude = -114.2
maxlongitude = -106
is_downsamp = 1 # downsample data?
sr_new = 1 # Hz New sample rate
trlen = 24*60*60 # s
# WARNING! List the full channel names. Do not use wildcards. Bad things will happen...
comps = ['BHZ'] #['BHZ','BH1','BH2','BDH'] #["HXZ", "HX1", "HX2"] #["LHZ", "LH1", "LH2"] #["HHZ", "HH1", "HH2"] #["HHZ", "HH1", "HH2", "BDH"]
homedir = "./OUT/" # "./"
is_removeresp = 1 # Remove response?
outunits = 'DISP' # DISP, VEL, ACC [For pressure channels, should use "VEL"]
is_overwrite = 0 # overwrite ? 

input_stalist = 0 # 0 if use all stations
if input_stalist: # List of stations
    stalist = 'path/to/local/station/file/stations.txt'
    text_file = open(stalist, "r")
    stations = text_file.read().split('\n')
    text_file.close()
    stations = ','.join(stations).replace(" ", "")
else: # Use all available stations
    stations = "*"

client = Client(webservice)
print(client)

# %% codecell
t1 = UTCDateTime(tstart)
t2 = UTCDateTime(tend)

# STATIONS
inventory = client.get_stations(network='*', station=stations,channel=','.join(comps), starttime=t1, endtime=t2, minlatitude=minlatitude, maxlatitude=maxlatitude, minlongitude=minlongitude, maxlongitude=maxlongitude)
print(inventory)
inventory.plot(projection="local",label=False)

file = open('stations_network.txt', 'w')
for inet in range(0,len(inventory)):
    for ista in range(0,len(inventory[inet])) :
        file.write("%5s %5s %12f %12f %12f\n" % (inventory[inet].code, inventory[inet].stations[ista]._code, 
                                            inventory[inet].stations[ista]._latitude, 
                                            inventory[inet].stations[ista]._longitude, 
                                            inventory[inet].stations[ista]._elevation))
file.close()

file = open('stations.txt', 'w')
for inet in range(0,len(inventory)):
    for ista in range(0,len(inventory[inet])) :
        file.write("%5s %12f %12f %12f\n" % (inventory[inet].stations[ista]._code, 
                                            inventory[inet].stations[ista]._latitude, 
                                            inventory[inet].stations[ista]._longitude, 
                                            inventory[inet].stations[ista]._elevation))
file.close()

