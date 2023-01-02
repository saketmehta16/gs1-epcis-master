# Importing all the libraries
from flask import Blueprint, request, jsonify
from . import capture_interface

# Creating a blueprint for capture repository
capture_blueprints = Blueprint('capture_blueprints', __name__)


#Capture route for fetching all Capture job status or inserting epcis events
@capture_blueprints.route('/', methods=['GET','POST'])
def capture_status_or_insert():
    
    # Return status of all capture jobs
    if request.method == 'GET':
        # Call the interface method to return all the captureJobs 
        capture_records = capture_interface.get_all_capture_jobs()

        # Return all the status jobs
        return jsonify(capture_records), 200 

    # Interface for inserting records into repository
    else:
        # Accepting the json request body
        epcis_document = request.json

        # Calling insertEvent method to perform validation checks and then insert individual
        # EPCIS events
        response, status_code = capture_interface.insert_events(epcis_document)
        return response, status_code


#Capture route for fetching Capture job status with captureId
@capture_blueprints.route('/<capture_id>',methods=['GET'])
def capture_status_by_id(capture_id):
    
    # Call the interface method to return captureJob with captureId 
    capture_record = capture_interface.get_capture_job_by_id(capture_id)
    # Return all the status jobs
    return jsonify(capture_record), 200


@capture_blueprints.route('/capture-stats',methods=['GET'])
def capture_repository_stats():

    # Call the interface method to return capture job stats 
    capture_records = capture_interface.return_capture_stats()
    # Return all the capture jobs stats
    return jsonify(capture_records), 200