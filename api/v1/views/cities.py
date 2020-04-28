#!/usr/bin/python3
""" holds class City"""
from models.state import City, State
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    ids = "State." + state_id
    dic_obj = storage.all()
    city_dics = []
    if (ids in dic_obj.keys()):
        list_cities = dic_obj[ids].cities
        for city in list_cities:
            city_dics.append(city.to_dict())
        return jsonify(city_dics)
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    ids = "City." + city_id
    dic_obj = storage.all(City)
    if (ids in dic_obj.keys()):
        return jsonify(dic_obj[ids].to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    dic = storage.all(City)
    ids = "City." + city_id
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.reload()
        storage.close()
        return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    if ("State." + state_id not in storage.all(State).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if ('name' not in json.keys()):
            return make_response(jsonify({'error': "Missing name"}), 400)

        json['state_id'] = state_id
        obj = City(**json)
        storage.new(obj)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    if ("City." + city_id not in storage.all(City).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        dic = storage.all(City)
        ids = "City." + city_id
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "updated_at"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
