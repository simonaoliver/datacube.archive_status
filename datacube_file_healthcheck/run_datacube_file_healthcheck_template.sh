#!/bin/bash
#PBS -P v10
#PBS -q normal
#PBS -l walltime=20:00:00,mem=8GB

module load agdc-py3-prod
module load udunits
cd /g/data/v10/tmp
python bad_netcdf_gdal_stats_compliance.py input 2> input.log

