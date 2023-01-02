class validation_exception(Exception):
    def __init__(self):
        self.message = "Validation failed for EPCIS events"
        self.response_code = 400
        self.type = "epcisException:ValidationException"
        self.title = "Validation Exception"

class query_validation_exception(Exception):
    def __init__(self):
        self.message = "Query Validation failed for EPCIS events"
        self.response_code = 400
        self.type = "epcisException:QueryValidationException"
        self.title = "Query Validation Exception"

class query_parameter_exception(Exception):
    def __init__(self):
        self.message = "Query's Parameter failed for EPCIS events"
        self.response_code = 400
        self.type = "epcisException:QueryParameterException"
        self.title = "Query Parameter Exception"

class subscription_controls_exception(Exception):
    def __init__(self):
        self.message = "Subscription Controls failed for EPCIS events"
        self.response_code = 400
        self.type = "epcisException:SubscriptionControlsException"
        self.title = "Subscription Controls Exception"

class implementation_exception(Exception):
    def __init__(self):
        self.message = "Error occured during implementation of the EPCIS repository operation"
        self.response_code = [501,500]
        self.type = "epcisException:ImplementationException"
        self.title = "Implementation Exception"

class query_too_complex_exception(Exception):
    def __init__(self):
        self.message = "Query is too complex than EPCIS repository is will to execute"
        self.response_code = 413
        self.type = "epcisException:QueryTooComplexException"
        self.title = "Query Too Complex Exception"
       
class uri_too_long_exception(Exception):
    def __init__(self):
        self.message = "Length of query URI exceeds 2000 characters"
        self.response_code = 414
        self.type = "epcisException:URITooLongException"
        self.title = "URI Too Long Exception"
       
class unsupported_media_type_exception(Exception):
    def __init__(self):
        self.message = "EPCIS repository implementation does not support the media type"
        self.response_code = 415
        self.type = "epcisException:UnsupportedMediaTypeException"
        self.title = "Unsupported Media Type Exception"
    
class security_exception(Exception):
    def __init__(self):
        self.message = "The operation was not permitted due to an access control violation or other security concern"
        self.response_code = [403,401]
        self.type = "epcisexception:SecurityException"
        self.title = "Security Exception"

class no_such_resource_exception(Exception):
   def __init__(self):
        self.message = "The specified resource does not exists"
        self.response_code = 404
        self.type = "epcisexception:NoSuchResourceException"
        self.title = "No SuchResource Exception"

class not_acceptable_exception(Exception):
    def __init__(self):
        self.message = "NotAcceptableException failed for EPCIS events"
        self.response_code = 406
        self.type = "epcisexception:NotAcceptableException"
        self.title = "Not Acceptable Exception"

class query_too_large_exception(Exception):
    def __init__(self):
        self.message = "Error occured due to query is too large"
        self.response_code= 413
        self.type= "epcisException:QueryTooLargeException"
        self.title= "Query Too Large Exception"

class capture_limit_exceeded_exception(Exception):
    def __init__(self):
        self.message = "Error due to capture limit exceeded"
        self.response_code= 413
        self.type= "epcisException:CaptureLimitExceededException"
        self.title= "Capture Limit Exceeded Exception"

class resource_already_exists(Exception):
    def __init__(self):
        self.message = "Error occured due to resource already exists"
        self.response_code= 409
        self.type= "epcisException:ResourceAlreadyExistsException"
        self.title= "Resource Already Exists Exception"