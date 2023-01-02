from epcis_common_utils import epcis_utilities_methods as utils
import json
import sys

# Configuration file for Mongodb dao methods
from . import query_dao as dao

# Configuration file for query interface
from . import query_config as config

# Add top-level libraries in epcis_common_utils
sys.path.append("..")

# Importing EPCIS utilities modules

# Parsing the mongodb-query-expression.json file
with open("query_repository/query_artifacts/mongodb-query-expressions.json") as fp:
    query_exp_file = json.load(fp)
    query_params = query_exp_file["params"]

# Create the epcis query document metadata


def formatOutputBody():
    d = dict()
    d["context"] = ["https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
                    {"example": "http://ns.example.com/epcis/"}]
    d["id"] = "https://id.example.org/document1"
    d["type"] = "EPCISQueryDocument"
    d["schemaVersion"] = "2.0"
    d["creationDate"] = utils.createDateFormat()
    return d

# Interface method to return all events from repository


def returnAllEvents():
    exp = {}
    ls = dao.findInMongo(config.mongo_epcis_eventsdata, exp)
    arr = []
    for elem in ls:
        arr.append(elem)

    formatted_output = formatOutputBody()
    formatted_output["epcisBody"] = {
        "queryResults": {"resultsBody": {"eventList": arr}}}
    return formatted_output

# Interface method to return event with event Id (eId) from repository


def returnDataForEventId(eId):
    exp = {"eventID": eId}
    ls = dao.findInMongo(config.mongo_epcis_eventsdata, exp)
    arr = []
    for elem in ls:
        arr.append(elem)

    formatted_output = formatOutputBody()
    formatted_output["epcisBody"] = {
        "queryResults": {"resultsBody": {"eventList": arr}}}
    return formatted_output

# Return EPCIS event related to bizStep from repository


def returnAllbizStepEvents(bizStep):
    exp = {"bizStep": bizStep}
    ls = dao.findInMongo(config.mongo_epcis_eventsdata, exp)
    arr = []
    for elem in ls:
        arr.append(elem)

    formatted_output = formatOutputBody()
    formatted_output["epcisBody"] = {
        "queryResults": {"resultsBody": {"eventList": arr}}}
    return formatted_output

# Returns EPCIS event(s) related to the given eventType only.


def returnAllEventstype(eventType):
    exp = {"type": eventType}
    ls = dao.findInMongo(config.mongo_epcis_eventsdata, exp)
    arr = []
    for elem in ls:
        arr.append(elem)

    formatted_output = formatOutputBody()
    formatted_output["epcisBody"] = {
        "queryResults": {"resultsBody": {"eventList": arr}}}
    return formatted_output

# Module to convert request params for EQ,GT,GE,LE,LT operators into MongoDb filter expression


def Eq_params(value):
    return value


def Gt_params(value):
    return {"$gt": value}


# Interface method to process the url params into Mongodb filter expressions
tags = ["EQ_", "GT_", "GE_", "LT_", "LE_", "MATCH_"]

# Interface method to create filter query expression for Mongodb find operations


def returnFilteredEvents(dictOfParams):
    # Dictionary to store all the formatted items (into Mongodb expression)
    MongoExp = dict()

    # Defining default variables
    key, value = 0, 0
    flag = 0

    # Iterate all the request parameters
    for k, v in dictOfParams.items():
        # Iterating tags
        for t in tags:
            if t in k:
                # Remove prefix tags from the key
                key = k[3:]

                # Convert for EQ events
                if t == "EQ_":
                    value = Eq_params(v)

                # Convert for GT eventts
                elif t == "GT_":
                    value = Gt_params(v)

                # Set flag
                flag = 1
                break

        # Check if flag is set or not
        if flag == 0:
            key, value = k, v

        # Convert the key to Search Key for Mongodb find operation
        param = query_params[key]
        searchKey = param["searchKey"]
        keyType = param["type"]

        if len(searchKey) > 1:
            pass
        else:
            key = searchKey[0]
            if keyType == "array":
                # Todo convert value to array format
                pass
            MongoExp[key] = value

    # Mongodb find expression and return data
    print(MongoExp)
    # return dao.findInMongo(config.mongo_epcis_eventsdata, MongoExp)
    return []



# Return the stats of records in repository database 
def return_event_stats():
    result = []
    list_records = dao.count_epcis_events(config.mongo_epcis_eventsdata)

    # Convert arrat representation of pycursor objects to array of json objects
    for record in list_records:
        result.append(record)

    return result