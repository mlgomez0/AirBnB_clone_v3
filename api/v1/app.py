#!/usr/bin/python3
""" return the status of your API """

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_all(self):
    """call the close method from storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """customized response to 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    if os.getenv('HBNB_API_HOST'):
        host_env = os.getenv('HBNB_API_HOST')
    else:
        host_env = "0.0.0.0"
    if os.getenv('HBNB_API_PORT'):
        port_env = os.getenv('HBNB_API_PORT')
    else:
        port_env = 5000
    app.run(host=host_env, port=port_env, threaded=True)
