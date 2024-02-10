#!/bin/bash -

# station file
file="stations_network.txt"

mkdir ./condor_submit_files
mkdir ./condor_out_files

# loop over all stations in station file and submit condor job
while IFS=$' ' read -ra line
do
  network=${line[0]}
  station=${line[1]}
  lat=${line[2]}
  lon=${line[3]}
  elev=${line[4]}
  
  echo "$network $station"
 
  submit_file="./condor_submit_files/submit_${network}.${station}.txt"

  cat > $submit_file << EOL
Universe   = vanilla
Executable = 1-download_dayfiles_region_1sta_htcondor.py
Arguments  = $network $station
Log        = ./condor_out_files/${network}.${station}.log
Output     = ./condor_out_files/${network}.${station}.out
Error      = ./condor_out_files/${network}.${station}.error
Queue
EOL

  condor_submit $submit_file

done < "$file"


