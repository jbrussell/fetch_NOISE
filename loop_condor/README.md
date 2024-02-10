These scripts provide a way to download data for multiple stations at once using HTCondor https://htcondor.org/.
- 0: builds a file containing all stations in a region of interest.
- run_loop_stations_htcondor: loops over all N stations within stations_network.txt and submits N condor jobs that call 1-download_dayfiles_region_1sta_htcondor.py

IMPORTANT! Must modify the first line of 1-download_dayfiles_region_1sta_htcondor.py to point to your desired conda environment, otherwise condor cannot find your installed python packages. 