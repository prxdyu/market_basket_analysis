# importing the libraries
import pandas as pd
import numpy as np
import s3fs

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from src.logger.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import download_file_from_s3,upload_file_to_s3

# defining the bucket name
BUCKET_NAME='marketbasketanalysisbucket'

# Retrieve repository secrets
import os
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


@dataclass
class DataIngestionConfig:
    # defining the filename
    file_name:str='raw.csv'
    # definfing the path in aws s3 bucket for saving raw.csv    
    raw_s3_path:str=f's3://{BUCKET_NAME}/{file_name}'
    


class DataIngestion:

    def __init__(self):
        # creating the object of the DataIngestionConfig class
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")
        try:
            
            # reading the food_mart_data from the aws s3 bucket
            data=pd.read_csv(f's3://{BUCKET_NAME}/food_mart_dataset.csv',index_col=0)

            logging.info("Successfully read food_mart_data.csv from AWS S3 bucket")
           
            # saving the raw data to the AWS S3 bucket
            data.to_csv(self.ingestion_config.raw_s3_path,index=False,storage_options={
                                                                                'key': aws_access_key_id,
                                                                                'secret': aws_secret_access_key
                                                                                })

            logging.info("Saved the raw.csv in the aws s3 bucket")
            logging.info("Data Ingestion Completed")

            return self.ingestion_config.raw_s3_path
            
        except Exception as e:
            logging.info("Exception occured in the data_ingestion")
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()