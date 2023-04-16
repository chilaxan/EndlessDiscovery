from pymongo import MongoClient
from dotenv import dotenv_values

client = None
config = dotenv_values('.env')

def get_client(refresh=False):
    global client
    if client is not None and not refresh:
        return client
    client = MongoClient(config['ATLAS_URI'])
    return client

def get_database():
    return client[config['DB_NAME']]
