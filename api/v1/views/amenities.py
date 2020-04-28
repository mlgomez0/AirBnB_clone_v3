#!/usr/bin/python3
""" holds class State"""
from models.amenity import Amenity
from flask import jsonify, abort, request, Response, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False,
                 defaults={'amenity_id': 0})
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id):
    dic = storage.all(Amenity)
    ids = "Amenity." + str(amenity_id)
    if (amenity_id == 0):
        amenities_list = []
        for k, v in dic.items():
            amenities_list.append(v.to_dict())
        return jsonify(amenities_list)
    elif (ids not in dic.keys()):
        abort(404)
    else:
        return jsonify(dic[ids].to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    dic = storage.all(Amenity)
    ids = "Amenity." + str(amenity_id)
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.reload()
        storage.close()
        return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    try:
        json = request.get_json()
    except:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if ('name' not in json.keys()):
        return make_response(jsonify({'error': "Missing name"}), 400)
    obj = Amenity(**json)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    try:
        json = request.get_json()
    except:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if (json is None):
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    dic = storage.all(Amenity)
    ids = "Amenity." + str(amenity_id)
    if ("name" not in json.keys()):
        return make_response(jsonify({'error': "Missing name"}), 400)
    if (ids not in dic.keys()):
        abort(404)
    else:
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "updated_at"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
