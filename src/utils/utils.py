import os
import sys
import pickle
import numpy as np
import pandas as pd
import boto3
from src.logger.logger import logging
from src.exception.exception import CustomException


# function to save an object from a pickle file    
def save_object(obj,file_path):
    try:
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

    except Exception as e:
        raise CustomException(e, sys)
    

# function to load an object from a pickle file    
def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception Occured in load_object function utils')
        raise CustomException(e,sys)
    
# function to download file form amazon s3 bucket
def download_file_from_s3(bucket_name, object_key, local_file_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_key, local_file_path)
    print(f'{object_key} has been downloaded from {bucket_name} to {local_file_path}')



# function to upload a file to amazon s3 bucket
def upload_file_to_s3(local_file_path, bucket_name, object_key):
    s3 = boto3.client('s3')
    s3.upload_file(local_file_path, bucket_name, object_key)
    print(f'{local_file_path} has been uploaded to {bucket_name} with key {object_key}')
