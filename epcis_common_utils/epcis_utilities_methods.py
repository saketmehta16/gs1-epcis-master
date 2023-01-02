from . import epcis_exceptions as exp

# Method to generate UUID
import uuid
# Method to work with datetime in Python
import datetime


# USe thunder client
# Format error message for EPCIS capture exceptiom
def create_error_message(e):
    error_msg = dict()

    # Add fields to error message 
    error_msg["type"] = e.type
    error_msg["title"] = e.title 
    error_msg["detail"] = e.message 

    return {"error":error_msg}


# Method to check if request body for a POST request is null or not 
def check_for_null_request_body(document):
    
    # Check if request body is null
    if len(document.keys()) == 0:
        raise exp.no_such_resource_exception()
        
    # If request body is not null
    else:
        pass 

# Method to generate Unique identifier
def generate_identifier():
    #UUID using UUID 1 format 
    identifier = uuid.uuid1()
    
    return str(identifier)


# Method to generate datetimestamp in current form
def create_date_format():
    format = "%y-%m-%dT%H:%M:%S.%f"
    date = datetime.datetime.utcnow()
    return date.strftime(format)
