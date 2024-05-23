import os
import sys
import pickle
import numpy as np
import pandas as pd
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
    
