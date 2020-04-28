#!/usr/bin/python3
"""return json route status"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_rep():
    """return status in json format """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False, endpoint='count')
def print_count():
    classes_dic = {'City': 'cities',
                   'Amenity': 'amenities',
                   'Place': 'places',
                   'Review': 'reviews',
                   'State': 'states',
                   'User': 'users'}
    dic = storage.all()
    class_list = []
    final_dic = {}
    for k, v in classes_dic.items():
        if (storage.count(k) != 0):
            final_dic[v] = storage.count(k)
    return final_dic
