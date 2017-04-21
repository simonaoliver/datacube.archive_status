#!/bin/sh
for i in `ls /g/data/v10/tmp/run_datacube_file_healthcheck*part*.sh`; do qsub $i; done
