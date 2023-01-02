# File to contain all the MongoDB operations

# Importing library for Mongodb connection with Python
import pymongo

# Importing Configuration file
from . import query_config as config

# Importing system library to work with project folders
import sys
# Add top-level libraries in epcis_common_utils
sys.path.append("..")

# Establish connection with Mongodb database
myclient = pymongo.MongoClient(config.mongo_url)
mydb = myclient[config.mongo_db]

# Function to return all the records  
def findInMongo(eventRecord,exp):

    # Create connection object to mongodb collection <eventRecord>
    mycol = mydb[eventRecord]
    
    # Return all the records without _id field
    return mycol.find(exp,{"_id":0,"masterDataId":0})


# Function to return the count of epcis events captured in database
def count_epcis_events(event_record):

    # Create connection object to mongodb collection <eventRecord>
    mongo_collection = mydb[event_record]

    # Return the count of events
    return mongo_collection.aggregate([{"$group" : 
    {"_id":"$type", "count":{"$sum":1}}}])
