# Importing all the libraries 
import fastjsonschema 
import json
import sys

#Import library for RabbitMQ queue connector to Python
import pika
# Import configuration file
from . import capture_config as config
from . import capture_dao as dao

# Add top-level libraries in epcis_common_utils
sys.path.append("..")

from . import capture_config
from epcis_common_utils import epcis_exceptions as exception
from epcis_common_utils import epcis_utilities_methods as utils

# Creating validation object 
with open("capture_repository/capture_artifacts/epcis-json-schema.json") as fp :
    schema = json.load(fp)
    validation = fastjsonschema.compile(schema)


# Method to validate EPCIS document for capture operation
def validate_epcis_document_schema(epcis_document):
    try :
        validation(epcis_document)
    except :
        raise exception.validation_exception()

# Method to check if number of events in EPCIS document is within specified limit 
def validate_events_number(epcis_document):

    # Get the EPCIS events limit from capture file
    limit = capture_config.gs1_epcis_capture_limit["value"]

    # Get the EPCIS events array from Document
    events = epcis_document["epcisBody"]["eventList"]

    # Check for EPCIS event limit 
    if len(events) > limit:
        raise exception.capture_limit_exceeded_exception()

def insert_records(document):
    # Producer for Rabbimq
    # send document in particular queue 

    # Producer connection object for RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = config.rabbitmq_hostname))

    # Creating Channel
    channel = connection.channel()
    # Converting JSON document into string to send into queue
    message = json.dumps(document)

    #Declare Queue
    channel.queue_declare(queue = config.rabbitmq_queuename, durable = True)
    channel.basic_publish(
        exchange='',
        routing_key=config.rabbitmq_queuename,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
    ))

    # Print debug message into CLI
    print("[X] Message sent to consumer")

    # Close the connection
    connection.close()
    

# Method to validate and insert all epcis events 
def insert_events(epcis_document):

    # Generate capture id
    capture_id = utils.generate_identifier()
    # Generate dateformat for createdAt field
    date_created = utils.create_date_format()

    # Default value for capture error behavior in config file 
    error_behavior = capture_config.gs1_capture_error_behaviour["value"]
    # Check if error behavior is present in the request body
    if "captureErrorBehavior" in epcis_document:
        error_behavior = epcis_document["captureErrorBehavior"]

    # Create capture job JSON for response to client and insertion in MongoDB
    capture_msg =     {
    "EPCISCaptureJob": {
    "captureErrorBehaviour": error_behavior,
    "createdAt": date_created,
    "running": "true",
    "success": "true",
    "captureID": capture_id,
    capture_config.gs1_cbv_version["key"]:capture_config.gs1_cbv_version["value"],
    capture_config.gs1_epcis_capture_limit["key"]:capture_config.gs1_epcis_capture_limit["value"],
    capture_config.gs1_epcis_capture_file_size_limit["key"]:capture_config.gs1_epcis_capture_file_size_limit["value"],
    }}
 
    response_status_code = 201

    try:
        # Check if EPCIS document is black document or not 
        utils.check_for_null_request_body(epcis_document)

        # Check if number of EPCIS events is less than limit specified in config file
        validate_events_number(epcis_document)

        # Check if EPCIS document is valid or not 
        validate_epcis_document_schema(epcis_document)

        #validateEPCISDocumentSize()

        # Insert captureID in the EPCIS document
        epcis_document["captureID"]=capture_id
        # Insert errorBehavior in the EPCIS document 
        epcis_document["errorBehavior"]=error_behavior
        # Send message to producer for publish into queue
        insert_records(epcis_document)

    except Exception as e: 
        # Generate error message and store in capture document
        error_msg =  utils.create_error_message(e)
        capture_msg["EPCISCaptureJob"]["errors"] = error_msg
        response_status_code = e.response_code

        # FinishedAt attribute only to be added for validation failures
        capture_msg["EPCISCaptureJob"]["finishedAt"] = utils.create_date_format()

        # Set running as false and success as false for validation failures
        capture_msg["EPCISCaptureJob"]["running"], capture_msg["EPCISCaptureJob"]["success"]="false", "false"
    
    #Insert the captureId in the Mongodb database
    dao.insert_single_into_mongo(capture_config.mongo_epcis_capturedata, capture_msg)

    # Remove object id from the response object
    capture_msg.pop("_id")
    return capture_msg, response_status_code


# Method to return capture job with captureid
def get_capture_job_by_id(capture_id):
    # Fetch result from dao methods 
    result = dao.find_in_mongo(config.mongo_epcis_capturedata, {"EPCISCaptureJob.captureID":capture_id})
    
    # Converting Mongodb find operation result into json convertable form 
    output = []
    for r in result:
        output.append(r)

    # Return capture record with captureId
    return output

# Method to return capture job with captureid
def get_all_capture_jobs():
    # Fetch result from dao methods 
    result = dao.find_in_mongo(config.mongo_epcis_capturedata, {}) 

    # Converting Mongodb find operation result into json convertable form 
    output = []
    for r in result:
        output.append(r)

    # Return capture record with captureId
    return output


# Method to return capture job stats
def return_capture_stats():
    # Fetch the results of capture stats 
    result = dao.count_capture_stats(config.mongo_epcis_capturedata)

    # Converting Mongodb find operation result into json convertable form 
    output = []
    for r in result:
        output.append(r)

    # Return capture record with captureId
    return output