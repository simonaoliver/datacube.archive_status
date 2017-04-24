#!/bin/bash
#
# 02_make_batch_tasks.sh filepath/filepattern
#
for i in `ls -1 $1*`; do cp /g/data/v10/tmp/run_datacube_file_healthcheck_template.sh /g/data/v10/tmp/run_datacube_file_healthcheck_$i.sh; chmod +x /g/data/v10/tmp/run_datacube_file_healthcheck_$i.sh; sed -i -e "s/input/$i/g" /g/data/v10/tmp/run_datacube_file_healthcheck_$i.sh; done
