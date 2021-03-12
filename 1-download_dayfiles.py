# %% markdown
# # Download data for ambient noise
# ### Download day-long files for use with ambient noise codes.
# 
# ## Processing steps:
# 1) Remove instrument response
# 2) Merge data: find data gaps and fill with zeros
# 3) Trim data to be length of day to nearest second, zero padding if necessary
# 4) Anti-alias filter and downsample
# 5) Save as SAC file
# 
# ## File structure
# Instrument $\rightarrow$ Day $\rightarrow$ Z, H1, H2
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
%matplotlib inline

# %% codecell
webservice = "IRIS"
network = "YO" # YO ENAM; ZA NoMelt
tstart = "2014-04-13T00:00:00"
tend = "2015-03-29T00:00:00"
is_downsamp = 1 # downsample data?
sr_new = 1 # Hz New sample rate
trlen = 24*60*60 # s
comps = ['BHZ'] #["HXZ", "HX1", "HX2"] #["LHZ", "LH1", "LH2"] #["HHZ", "HH1", "HH2"] #["HHZ", "HH1", "HH2", "BDH"]
homedir = "path/to/output/data/directory/" # "./"
is_removeresp = 1 # Remove response?
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

datadir = homedir + network + '/'
if not os.path.exists(datadir):
    os.makedirs(datadir)
# %% codecell
t1 = UTCDateTime(tstart)
t2 = UTCDateTime(tend)

# STATIONS
inventory = client.get_stations(network=network, station=stations,channel=comps[0], starttime=t1, endtime=t2)
print(inventory)
inventory.plot(projection="local",label=False)

file = open('stations.txt', 'w')
for ista in range(0,len(inventory[0])) :
    file.write("%5s %12f %12f %12f\n" % (inventory[0].stations[ista]._code, 
                                        inventory[0].stations[ista]._latitude, 
                                        inventory[0].stations[ista]._longitude, 
                                        inventory[0].stations[ista]._elevation))
file.close()

# %% codecell
# DOWNLOAD DATA

# Build vector of start times
dayvec = pd.date_range(start=tstart, end=tend, freq=str(trlen)+'S')

# Loop through stations
for ista in range(0,len(inventory[0])) :
    station = inventory[0].stations[ista].code
    print('======== Working on STA : ' + station + "========")
    stadir = datadir + station + '/'
    if not os.path.exists(stadir):
        os.makedirs(stadir)
    
    # Loop through days
    for iday, DAY in enumerate(dayvec) :
        daystr = DAY.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        print('Working on ' + station + ' : ' + daystr)
    
            tdbeg = UTCDateTime(DAY.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            tdend = UTCDateTime((DAY+pd.Timedelta(seconds=trlen)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            
            for ch in comps :
                checkfile = stadir + '/' + station+'.'+tdbeg.datetime.strftime('%Y.%j.%H.%M.%S.')+ch+'.sac'
                if is_overwrite==0 and os.path.exists(checkfile):
                    print('Already processed '+checkfile)
                    continue
                    
                # Download data and process
                try:
                    st = client.get_waveforms(network=network, station=station, location="*", channel=ch, starttime=tdbeg, endtime=tdend, attach_response=True)
                except Exception:
                        print('Missing data for day: '+daystr)
                        continue
                sr = st[0].stats.sampling_rate
                if is_removeresp:
                    try:
                        st.remove_response(output="DISP", zero_mean=True, taper=True, taper_fraction=0.05, pre_filt=[0.001, 0.005, sr/3, sr/2], water_level=60)
                    except Exception:
                        print('Failed to remove response: '+daystr)
                        continue
                st.merge(method=1, fill_value=0) # fill all datagaps with 0
                st.trim(starttime=tdbeg, endtime=tdend, pad=True, nearest_sample=False, fill_value=0) # make sure correct length
                st.detrend(type='demean')
                st.detrend(type='linear')
                st.taper(type="cosine",max_percentage=0.05)
                if is_downsamp and sr!=sr_new:
                    st.filter('lowpass', freq=0.4*sr_new, zerophase=True) # anti-alias filter
                    st.filter('highpass', freq=1/60/60, zerophase=True) # Remove daily oscillations
                    st.decimate(factor=int(sr/sr_new), no_filter=True) # downsample
                    st.detrend(type='demean')
                    st.detrend(type='linear')
                    st.taper(type="cosine",max_percentage=0.05)
                
                # convert to SAC and fill out station/event header info
                for tr in st:
                    sac = SACTrace.from_obspy_trace(tr)
                    sac.stel = inventory[0].stations[ista].elevation
                    sac.stla = inventory[0].stations[ista].latitude
                    sac.stlo = inventory[0].stations[ista].longitude
                    kcmpnm = sac.kcmpnm
                    yr = str(st[0].stats.starttime.year)
                    jday = '%03i'%(st[0].stats.starttime.julday)
                    hr = '%02i'%(st[0].stats.starttime.hour)
                    mn = '%02i'%(st[0].stats.starttime.minute)
                    sec = '%02i'%(st[0].stats.starttime.second)
                    sac_out = stadir + '/' + station+'.'+yr+'.'+jday+'.'+hr+'.'+mn+'.'+sec+'.'+kcmpnm+'.sac'
                    sac.write(sac_out)
        
        

    
    

# %% codecell
