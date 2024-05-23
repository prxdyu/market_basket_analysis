import pandas as pd
import numpy as np

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

from src.logger.logger import logging
from src.exception.exception import CustomException 

import os
import sys
from dataclasses import dataclass
from pathlib import Path


# defining the bucket name
BUCKET_NAME='marketbasketanalysisbucket'

# Retrieve repository secrets
import os
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class ModelTrainerConfig:
    rules_path=os.path.join("artifacts","association_rules.pkl")

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_training(self,s3_path):
        try:
            
            logging.info("Model training Started")
            # reading the data for modelling from S3 bucket
            data = pd.read_csv(s3_path,storage_options={
                                                    'key': aws_access_key_id,
                                                    'secret': aws_secret_access_key
                                                    })
            logging.info("Successfully read modelling data from s3 bucket")

            # setting-up the hyperparameters
            MIN_SUPPORT= 0.0001
            MIN_LIFT=50
            MIN_CONFIDENCE=0.01

            # generating the frequent_item sets using apriori
            frequent_itemsets = apriori(data,min_support=MIN_SUPPORT,use_colnames=True,low_memory=True)

            # mining association rules
            apriori_rules = association_rules(frequent_itemsets,metric='lift',min_threshold=1)

            # filtering recommendations where lift is greater than 50 and confidence is greater than 0.01
            apriori_rules_filtered = apriori_rules[(apriori_rules['lift']>=MIN_LIFT) & (apriori_rules['confidence']>=MIN_CONFIDENCE)]

            logging.info("Successfully mined association rules")

            # unfreezing the antecedents and consequents columns
            apriori_rules_filtered['antecedents']=apriori_rules_filtered['antecedents'].apply(lambda x:set(x))
            apriori_rules_filtered['consequents']=apriori_rules_filtered['consequents'].apply(lambda x:set(x))

            # exporting the rules for inference
            apriori_rules_filtered.to_pickle(self.model_trainer_config.rules_path)
            logging.info("Successfully saved association rules")
            logging.info("Model training Completed")



        except Exception as e:
            logging.info("Exception occured in the Model Training")
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=ModelTrainer()
    obj.initiate_model_training(f's3://{BUCKET_NAME}/modelling_data.csv')       