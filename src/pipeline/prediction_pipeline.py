import os
import sys
import pandas as pd

from src.exception.exception import CustomException
from src.logger.logger import logging



class PredictionPipeline:

    def __init__(self):
        pass

    def recommend(self,item):
         """
         item : dicationary of items 
         returns a list of dictionaries where each dictionary is a recommendation having one or more products
         """
         try:
            # initializing an empty list to store recommendations
            recommendations=[]
    
            # loading the association rules pickle file
            rules_path = os.path.join("artifacts","association_rules.pkl")
            rules = pd.read_pickle(rules_path)

            # computing the no of rules
            n=rules.shape[0]    
            
            # iterating through each rules and getting the recommendations
            for i in range(n):
                if item==rules.iloc[i,0]:
                    # getting the recommendation (a recommendation may consists one or more products)
                    recommendation= rules.iloc[i,1]
                    # iterating through the each recommendation
                    for j in recommendation:
                        recommendations.append(j)

            return set(recommendations)



         except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)
        

