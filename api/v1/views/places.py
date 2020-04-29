#!/usr/bin/python3
""" holds class City"""
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    ids = "City." + city_id
    dic_obj = storage.all()
    places_dics = []
    if (ids in dic_obj.keys()):
        list_places = dic_obj[ids].places
        for place in list_places:
            places_dics.append(place.to_dict())
        return jsonify(places_dics)
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    ids = "Place." + place_id
    dic_obj = storage.all(Place)
    if (ids in dic_obj.keys()):
        return jsonify(dic_obj[ids].to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    dic = storage.all(Place)
    ids = "Place." + place_id
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.reload()
        storage.close()
        return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    if ("City." + city_id not in storage.all(City).keys()):
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
        if ('user_id' not in json.keys()):
            return make_response(jsonify({'error': "Missing user_id"}), 400)
        if ("User." + json['user_id'] not in storage.all(User).keys()):
            abort(404)
        json['city_id'] = city_id
        obj = Place(**json)
        storage.new(obj)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    if ("Place." + place_id not in storage.all(Place).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        dic = storage.all(Place)
        ids = "Place." + place_id
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "updated_at"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
