# File to contain all the MongoDB operations

# Importing library for Mongodb connection with Python
import pymongo

# Importing Configuration file
from . import capture_config as config

import sys
# Add top-level libraries in epcis_common_utils
sys.path.append("..")
from epcis_common_utils import epcis_utilities_methods as utils

# Establish connection with Mongodb database
mongodb_client = pymongo.MongoClient(config.mongo_url)
mongodb_database = mongodb_client[config.mongo_db]

# Function to insert array of epcisEvents into Mongodb collection
def insert_multiple_into_mongo(event_record, list_documents, master_id, error_behavior):

    # Create connection object to mongodb collection <event_record>
    mongodb_collection = mongodb_database[event_record]  # Meaningful names

    # List to store inserted epcis Event data ObjectID
    list_inserted_ids = []

    # Flag object to signal if all insert operation complete with success or not 
    flag = True 

    # Insert records one by one 
    for document in list_documents:
        # Updating/adding recordTime 
        document["recordTime"] = utils.create_date_format()

        # Check if eventID is present 
        if "eventID" not in document:
            # If not present add an event Id with generated Identifier
            document["eventID"] = utils.generate_identifier()  #generate_identifier

        # Add masterdata Id field
        document["masterDataId"] = master_id

        try:
            inserted_record = mongodb_collection.insert_one(document)
        except:
            flag = False

            # If error behavior is rollback and exception encountered 
            # Then return to consume application and try to undo all insertions
            if error_behavior == "rollback":
                return list_inserted_ids, flag

        # Append record of ObjectID into list of ids
        list_inserted_ids.append(inserted_record.inserted_id)

    return list_inserted_ids, flag

# Function to insert single document into Mongodb collection
def insert_single_into_mongo(event_record, document):

    # Create connection object to mongodb collection <event_record>
    mongodb_collection = mongodb_database[event_record]

    # Perform insert operation
    inserted_record = mongodb_collection.insert_one(document)

    # Return ObjectID of inserted document in MongoDB
    return inserted_record.inserted_id


# Function to return all the records  
def find_in_mongo(event_record, exp):

    # Create connection object to mongodb collection <event_record>
    mongodb_collection = mongodb_database[event_record]
    
    # Return all the records without _id field
    return mongodb_collection.find(exp,{"_id":0})

# Function to delete multiple records with list of object ids
def mongo_delete_multiple_from_mongo(event_record, list_of_ids):
    mongodb_collection = mongodb_database[event_record]

    # For each object id in list perform delete operation
    for id in list_of_ids:
        myquery = { "_id":id }
        # Delete one record
        mongodb_collection.remove(myquery)


# Function to delete single record with objectId 
def delete_from_mongo(event_record, record_id):
    mongodb_collection = mongodb_database[event_record]

    # Generate the query
    myquery = { "_id":record_id }
    # Delete one record
    mongodb_collection.remove(myquery)


# Function to update single record in Mongodb with capture_id of CaptureJob
def update_mongo_field(capture_record, id, document):
    mongodb_collection = mongodb_database[capture_record]    

    # Update the capture job document
    mongodb_collection.update_one({"EPCISCaptureJob.captureID":id}, {"$set":document})


# Function to return the capture jobs stats
def count_capture_stats(capture_record):
    mongodb_collection = mongodb_database[capture_record]

    # Return the count of capture jobs
    return mongodb_collection.aggregate([{"$group" : 
    {"_id":"$EPCISCaptureJob.success", "count":{"$sum":1}}}])