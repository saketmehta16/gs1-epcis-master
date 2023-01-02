# File to store configurations for EPCIS capture Repository

# Configuration for maximum individual epcis events to store in 1 EpcisDocument
gs1_epcis_capture_limit = {"key":"GS1-EPCIS-Capture-Limit", "value":10}

#versionCBV= 2.0.0
gs1_cbv_version = {"key": "GS1-CBV-Version" , "value": 2.0 }

# GS1-EPCIS-Capture-File-Size-Limit
gs1_epcis_capture_file_size_limit = {"key": "GS1-EPCIS-Capture-File-Size-Limit" , "value": 1024} 

#GS1-Capture-Error-Behaviour
gs1_capture_error_behaviour = {"key": "GS1-Capture-Error-Behaviour" , "value": "rollback"}


# Mongodb configuration 
mongo_url = "mongodb://localhost:27017/"
mongo_db = "epcisdb"
mongo_epcis_eventsdata = "eventdata"