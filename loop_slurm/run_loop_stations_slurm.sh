#!/bin/bash -

# station file
file="stations_network.txt"

# loop over all stations in file and submit slurm job
while IFS=$' ' read -ra line
do
  network=${line[0]}
  station=${line[1]}
  lat=${line[2]}
  lon=${line[3]}
  elev=${line[4]}
  
  echo "$network $station"

  sbatch slurm_fetch_noise.sh network station

done < "$file"


