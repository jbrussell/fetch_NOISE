These scripts provide a way to download data for multiple stations at once using the slurm workload manager https://slurm.schedmd.com/documentation.html.
- 0: builds a file containing all stations in a region of interest.
- run_loop_stations_slurm: loops over all N stations within stations_network.txt and submits N slurm jobs by calling slurm_fetch_noise.sh, which calls 1-download_dayfiles_region_1sta.py

IMPORTANT! Must modify the line `conda activate obspy` to specify your conda environment within slurm_fetch_noise.sh.
