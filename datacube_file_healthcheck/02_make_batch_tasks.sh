#!/bin/bash
#
# 02_make_batch_tasks.sh file_list.txt
#
# run from the folder containing the file list
#

split -l 5000 $1 $1_parts_
x=$1_parts_*

for i in $x; do echo $i; j=`echo $i | rev | cut -d"/" -f1 | rev`; cp /g/data/v10/tmp/run_datacube_file_healthcheck_template.sh /g/data/v10/tmp/run_datacube_file_healthcheck_$j.sh; chmod +x /g/data/v10/tmp/run_datacube_file_healthcheck_$j.sh; echo $i; sed -i -e "s/input/$i/g" /g/data/v10/tmp/run_datacube_file_healthcheck_$j.sh; done
