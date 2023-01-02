# Importing all the libraries
from flask import Blueprint, request, jsonify
from . import query_interface

# Creating a blueprint for capture repository
query_blueprints = Blueprint('query_blueprints', __name__)


# Endpoint to return all the events in the repository based on or not on parameters
@query_blueprints.route('events', methods=['GET', 'POST'])
def returnEvents():

    if request.method == 'GET':
        result = query_interface.returnAllEvents()
        return jsonify(result), 200
    else:
        # result = query_interface.returnFilteredEvents()
        result = query_interface.returnFilteredEvents(request.args)
        return jsonify(result), 200


# Endpoint to return the event with eventID
@query_blueprints.route('events/<eventID>', methods=['GET'])
def returnEventById(eventID):
    result = query_interface.returnDataForEventId(eventID)
    return jsonify(result), 200

# Returns EPCIS events related to the given bizStep
@query_blueprints.route('bizSteps/<bizStep>', methods=['GET'])
def returnEventsByBizStep(bizStep):
    result = query_interface.returnAllbizStepEvents(bizStep)
    return jsonify(result), 200

# Returns EPCIS event(s) related to the given eventType only
@query_blueprints.route('eventTypes/<eventType>',methods=['GET'])
def returnEventsByType(eventType):
   result = query_interface.returnAllEventstype(eventType)
   return jsonify(result), 200


# Return EPCIS repository stats 
@query_blueprints.route("query-stats",methods=['GET'])
def event_repository_stats():
    event_records = query_interface.return_event_stats()
    return jsonify(event_records), 200

#Returns EPCIS event(s) related to the given disposition.
@query_blueprints.route('/dispositions/<disposition>',methods=['GET'])
def returnEvents(disposition):
    result =  query_interface.returnAllEventstype(disposition)
    return jsonify(result), 200