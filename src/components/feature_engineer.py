import pandas as pd
import numpy as np


from src.logger.logger import logging
from src.exception.exception import CustomException
from src.utils.utils import save_object 

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
class FeatureEngineeringConfig:

    # defining the filename
    file_name:str='raw_with_engineered_features.csv'

    # definfing the path in aws s3 bucket for saving raw_with_engineered_features.csv    
    engineered_features_s3_path:str=f's3://{BUCKET_NAME}/{file_name}'

    # defining the path for saving the products.pkl file in the local
    products_list_path:str = os.path.join("artifacts","products.pkl")
    

class FeatureEngineering:

    def __init__(self):
        self.feature_engineering_config = FeatureEngineeringConfig()

    


    def initiate_feature_engineering(self,s3_path):
        logging.info("Feature Engineering Started")
        try:
            # reading the raw.csv from s3 bucket
            df = pd.read_csv(s3_path,storage_options={
                                                    'key': aws_access_key_id,
                                                    'secret': aws_secret_access_key
                                                    })
            logging.info("Successfully read raw.csv from aws s3 bucket")

            """ Adding Transaction ID"""
            # In our data we don't have the transaction_id, so let's create transaction_id ourself to identify the baskets  (group of products purchased in a single transaction)
            df['transaction_id'] = df['customer_id'].astype(str) + df['time_id'].astype(str)

            # selecting the columns of interest
            data = df[['transaction_id','customer_id','product_id','product_name','unit_sales','time_id']]

            # Counting the no of transaction each product has appeared in
            product_count = data.groupby('product_id')['transaction_id'].nunique()
            product_count = pd.DataFrame(product_count).rename(columns={'transaction_id':'count'})

            # sorting the dataframe in descending order
            product_count.sort_values('count',ascending=False,inplace=True)

            # saving the top 500 products into a list
            products = df['product_name'].value_counts().head(1000).index.tolist()
            save_object(products,self.feature_engineering_config.products_list_path)
            
            
            """ Since we have very large no of products, running Apriori algorithm takes longer time and expensiv. so let's limit ourself to only top N frequent products"""
            # setting the value of N to 100 that is we are considering only the top 100 frequent products (if N=0 means we are considering all products)
            N=0

            if N==0:
                # consider all products 
                top_N=product_count
                  
            else:
                  
                # filtering the top N 
                top_N = product_count.head(N)
            
            # getting top N products
            top_N_products =list(top_N.index)

            # filtering those only transaction which has anyone of this top N products
            mask = data['product_id'].isin(top_N_products)
            df_engineered = data[mask]
            
            # saving the data with engineered features
            df_engineered.to_csv(self.feature_engineering_config.engineered_features_s3_path,
                                 index=False,
                                 storage_options={ 'key': aws_access_key_id,
                                                   'secret': aws_secret_access_key
                                                 })
            
            logging.info("Succesfully saved the data with engineered features in aws s3 bucket")
            logging.info("Feature Engineering completed")


            return self.feature_engineering_config.engineered_features_s3_path

        except Exception as e:
            logging.info("Exception occured in the initiate_data_transformation")
            raise CustomException(e,sys)
    
        

if __name__=="__main__":
    obj=FeatureEngineering()
    obj.initiate_feature_engineering(f's3://{BUCKET_NAME}/raw.csv')