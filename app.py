# Importing Flask library 
from flask import Flask

# Importing Flask Cors library to enable Cors feature in application
from flask_cors import CORS

# Importing all the blueprints for capture endpoints
from capture_repository.capture_routes import capture_blueprints

# Importing all the blueprints for query endpoints
from query_repository.query_routes import query_blueprints


# Create the object of flask app
app = Flask(__name__)

# Add Cors to the Flask object
CORS(app)

# To pretty format the JSON response when rendered in browser
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Binding capture blueprints to URL endpoints 
app.register_blueprint(capture_blueprints, url_prefix='/capture')

# Binding query blueprints to URL endpoints 
app.register_blueprint(query_blueprints, url_prefix='/')


# Configuration for running flask application of EPCIS repository
if __name__ == "__main__":
    app.run(port=9000)