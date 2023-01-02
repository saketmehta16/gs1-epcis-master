import pika
import json 
import capture_repository.capture_config as config
import capture_repository.capture_dao as dao
import sys

# Add top-level libraries in epcis_common_utils
sys.path.append("..")
from epcis_common_utils import epcis_utilities_methods as utils
from epcis_common_utils import epcis_exceptions as exception

print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq_hostname))
channel = connection.channel()
channel.queue_declare(queue=config.rabbitmq_queuename, durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)

    # Load message into JSON format from message queue 
    epcis_document = json.loads(body.decode())

    # Extract Event List data 
    eventData = epcis_document["epcisBody"]["eventList"]
    epcis_document.pop("epcisBody")

    # Extract Capture Id
    captureId = epcis_document["captureID"]
    epcis_document.pop("captureID")

    # Extract Error Behavior 
    errorBehavior = epcis_document["errorBehavior"]
    epcis_document.pop("errorBehavior")
    
    # Extract Master Data 
    masterData = epcis_document

    # capture master data
    masterId = dao.insertSingleIntoMongo(config.mongo_epcis_masterdata,masterData)

    # capture event data
    listOfEventIds,flag = dao.insertMultipleIntoMongo(config.mongo_epcis_eventsdata,eventData,masterId,errorBehavior)

    # Chech if flag is False
    if flag == False:
        # For rollback we need to delete all inserted records if error is encountered during insertion of events
        if errorBehavior == "rollback":
            # Delete events by their objectIds
            dao.mongoDeleteMultipleFromMongo(config.mongo_epcis_eventsdata,listOfEventIds)
            # Delete masterdata by their objectId
            dao.deleteFromMongo(config.mongo_epcis_eventsdata,masterId)

        # Update the capture document after execution is done and exception encountered
        dao.updateMongoField(config.mongo_epcis_capturedata,captureId,{"EPCISCaptureJob.success":"false","EPCISCaptureJob.running":"false",
        "EPCISCaptureJob.finishedAt":utils.createDateFormat(),
        "EPCISCaptureJob.errors":utils.createErrorMessage(exception.ImplementationException())})

    else:
        # Update the capture document after execution is done successfully
        dao.updateMongoField(config.mongo_epcis_capturedata,captureId,{"EPCISCaptureJob.success":"true","EPCISCaptureJob.running":"false",
        "EPCISCaptureJob.finishedAt":utils.createDateFormat()})


    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=config.rabbitmq_queuename, on_message_callback=callback)
channel.start_consuming()