#!/usr/bin/python3
"""return json route status"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_rep():
    """return status in json format """
    return (jsonify({"status": "OK"}))
