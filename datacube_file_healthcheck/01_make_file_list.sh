#!/bin/bash

for i in `ls -d /g/data/rs0/datacube/002/*`; do d=`date +%Y%m%d`; j=`echo ${i##*/}`; find $i -name "*.nc" > /g/data/v10/tmp/"$j"_"$d".txt; cat /g/data/v10/tmp/"$j"_"$d".txt | cut -d "_" -f 1-10 | cut -d "." -f 1 | sort | uniq -d > /g/data/v10/tmp/"$j"_"$d"_duplicated.txt; echo /g/data/v10/tmp/"$j"_"$d"_duplicated.txt; cat /g/data/v10/tmp/"$j"_"$d"_duplicated.txt | wc -l; done

for i in `ls -d /g/data/fk4/datacube/002/*`; do d=`date +%Y%m%d`; j=`echo ${i##*/}`; find $i -name "*.nc" > /g/data/v10/tmp/"$j"_"$d".txt; cat /g/data/v10/tmp/"$j"_"$d".txt | cut -d "_" -f 1-10 | cut -d "." -f 1 | sort | uniq -d > /g/data/v10/tmp/"$j"_"$d"_duplicated.txt; echo /g/data/v10/tmp/"$j"_"$d"_duplicated.txt; cat /g/data/v10/tmp/"$j"_"$d"_duplicated.txt | wc -l; done

