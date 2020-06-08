''' Importing Area'''
import logging

'''Logic starts from here'''

# Method for maintaining Log files
def set_log(filename):
    logging.basicConfig(filename,level=logging.INFO)

# Method to write error on file
def log(e:Exception):
    logging.exception(str(e))


