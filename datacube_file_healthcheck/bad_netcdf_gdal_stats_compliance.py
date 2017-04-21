from netCDF4 import Dataset
import datacube
dc = datacube.Datacube(app='dc-example')

from compliance_checker.runner import ComplianceChecker, CheckSuite

# Load all available checker classes
check_suite = CheckSuite()
check_suite.load_all_available_checkers()

def compliance_check(netcdf):# Run cf and adcc checks with normal strictness, verbose text format to stdout
    return_value, error = ComplianceChecker.run_checker(
                                netcdf,
                                ['cf'], 0, 'lenient', '-', 'text')
    return(return_value, error)

import os
import logging
import click
import gdal
import glob

import uuid
from pathlib import Path
from typing import List
from datacube.utils import is_supported_document_type, read_documents

from gdalconst import *
LOG_FILENAME = '/g/data/v10/tmp/BAD_DATA.log'
# prevent aux.xml write
os.environ["GDAL_PAM_ENABLED"] = "NO"

def get_path_dataset_ids(path: Path) -> List[uuid.UUID]:
    """
    Get all dataset ids embedded by the given path.
    (Either a standalone metadata file or embedded in a given NetCDF)
    """
    ids = [uuid.UUID(metadata_doc['id']) for _, metadata_doc in read_documents(path)]
    return ids


def get_uri(filepath):
    uri='file://'+filepath
    return(uri)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
def run_checker(file):
     
    uri_path = get_uri(file)

    logging.info("Processing %s", uri_path)

    try:
        
        storage_unit = gdal.Open( file, GA_ReadOnly )
        subdatasets = storage_unit.GetSubDatasets()
        if (storage_unit.GetDriver().ShortName == 'netCDF'):
            compliance_result, compliance_error = compliance_check(file)

            if compliance_result == False:
                logging.error("Compliance failure for %s", file)

            else:
                logging.info("Compliance pass for %s", file)
    except ValueError:
        logging.error("Can't open NetCDF %s", file)

    for subdataset in subdatasets:

        if 'dataset' not in subdataset[0]:
            band = gdal.Open( subdataset[0], GA_ReadOnly )
            try:
                band.GetRasterBand(1).GetStatistics(0,1)
                logging.info("Band is OK %s", subdataset[0])
            except ValueError:
                logging.error("Statistics fail on %s", subdataset[0])



@click.command(help="Look for bad data in NetCDF - only checks if NetCDF can open file - not internal data integrity")
@click.argument('netcdf_list',
                type=click.Path(exists=True, readable=True),
                nargs=-1)

def main(netcdf_list):
    with open(netcdf_list[0]) as f:
        file_list = f.read().splitlines()  
    for n in file_list:
        if ('.nc' not in n): 
            duplicates = glob.glob(n+'*.nc') #assumes variable extension post $n pattern
        else:
            duplicates = glob.glob(n)
        for d in duplicates:
            uri_filepath='file://'+d

            try:


                nc_fid = Dataset(d, 'r')
                logging.info("NetCDF libary read OK %s", d)

                run_checker(d)

                uri_generator = dc.index.datasets.get_datasets_for_location(uri=uri_filepath)

                for i in uri_generator:
                    uuid = get_path_dataset_ids(d)
                    if (str(uuid[0]) == i.id) and i.is_archived:

                        logging.error("Dataset is Archived but NOT deleted TRASH %s", i)

            except OSError:
                logging.error("Bad data - check if indexed and recommend action %s", d)

                #Are the files in datacube and are they archived

                uri_generator = dc.index.datasets.get_datasets_for_location(uri=uri_filepath)

                for i in uri_generator:
                    if i.is_archived:

                        logging.error("Dataset is BAD and Archived but NOT deleted TRASH %s", i)

                    else:
                        logging.error("Dataset is BAD and NOT in DataCube - TRASH %s", i)




if __name__ == "__main__":
    main()
