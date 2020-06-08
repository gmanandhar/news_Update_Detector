
''' Importing Area'''
import os
import ssl

from datetime import datetime
from . import logger

''' Business Logic Area'''
# Method of HTTPS and SSL protocal error handling for MAC Only

def http_issue():
    if(not os.environ.get('PYTHONHTTPSVERIFY','') and getattr(ssl,'_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


# Methods of File Handling
# Method to writing filter code in file

def write_website(filename,data=''):
    try:
        with open(filename,'wb') as obj:
            obj.write(data)
    except Exception as e:
        print(e)
        logger.log(e)
        return False
    else:
        return data

# Method to return Filter data from the website

def read_website(filename):
    try:
        with open(filename) as obj:
            data= obj.read()
    except Exception as e:
        print(e)
        logger.log(e)
        return False
    else:
        return data


# Methods for caching

# Method to return last scraping time in miniutes of website
def get_last_scrap(filename):
    if not os.path.exists(filename):
        return -1 # Website not found
    # if website
    prv_time= os.path.getmtime(filename)
    current_time= datetime.timestamp(datetime.now)
    interval = current_time - prv_time
    minutes= int(round(interval / 60))
    return minutes

# Methods that check file time and confirm to re download or not
def check_cache(filename, cachetime):
    scrap_time = get_last_scrap(filename)

    #Checking caching duration
    if scrap_time < 0  or scrap_time >cachetime:
        return True
    else:
        return False