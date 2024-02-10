#!/bin/bash -
#SBATCH -o noise.out
#SBATCH -e noise.out
#SBATCH --ntasks-per-node 1
#SBATCH -J fetch_noise
#SBATCH --nodes 1
##SBATCH -p orca-1
#SBATCH -t 24:00:00
##SBATCH -D .

conda activate obspy

python 1-download_dayfiles_region_1sta.py --network $1 --station $2

