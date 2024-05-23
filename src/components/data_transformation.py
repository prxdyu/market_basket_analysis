import pandas as pd
import numpy as np


from src.logger.logger import logging
from src.exception.exception import CustomException 

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import sys
sys.path.insert(0, 'src')

# defining the bucket name
BUCKET_NAME='marketbasketanalysisbucket'

# Retrieve repository secrets
import os
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class DataTransformationConfig:
    # defining the filename
    file_name:str='modelling_data.csv'
    # definfing the path in aws s3 bucket for saving raw_with_engineered_features.csv    
    modelling_s3_path:str=f's3://{BUCKET_NAME}/{file_name}'

    

class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    

    def initiate_data_transformation(self,s3_path):
        logging.info("Data Transformation Started")
        try:
            # reading the raw_with_engineered_features.csv
            df=pd.read_csv(s3_path,storage_options={
                                                    'key': aws_access_key_id,
                                                    'secret': aws_secret_access_key
                                                    })

            logging.info("Successfully read raw_with_engineered_features.csv data from s3 ")

            # creating the dataset for apriori algorithm
            apriori_df = df.groupby(['transaction_id','product_name'])['unit_sales'].sum().unstack().reset_index().fillna(0).set_index('transaction_id')

            # doing one hot encoding

            def ohe(x):
                if x<=0:
                    return 0
                else:
                    return 1

            # applying One Hot encoding
            apriori_df = apriori_df.applymap(ohe)
            logging.info("Succesfully tranasformed data for Apriori modelling")

            apriori_df.to_csv(self.data_transformation_config.modelling_s3_path,
                              index=False,
                              storage_options={
                                                'key': aws_access_key_id,
                                                'secret': aws_secret_access_key
                                              })
            logging.info("Saved the data for Apriori modelling in the S3 bucket")
            logging.info("Data transformation completed")
            


            return self.data_transformation_config.modelling_s3_path

        except Exception as e:
            logging.info("Exception occured in the initiate_data_transformation")
            raise CustomException(e,sys)
    
        

if __name__=="__main__":
    obj=DataTransformation()
    obj.initiate_data_transformation(f's3://{BUCKET_NAME}/raw_with_engineered_features.csv')