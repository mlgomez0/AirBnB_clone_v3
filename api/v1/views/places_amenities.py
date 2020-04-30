#!/usr/bin/python3
""" holds class Places-Amenity"""
from models.review import Review
from models.user import User
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
import os


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_ameni(place_id):
    """get amenities list"""
    ids = "Place." + place_id
    dic_obj = storage.all()
    amenities_dics = []
    if (ids in dic_obj.keys()):
        list_amenities = dic_obj[ids].amenities
        for amenity in list_amenities:
            amenities_dics.append(amenity.to_dict())
        return jsonify(amenities_dics)
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_ameny(place_id, amenity_id):
    """delete amenity"""
    dic_amenity = storage.all(Amenity)
    dic_place = storage.all(Place)
    id_ame = "Amenity." + amenity_id
    id_pla = "Place." + place_id
    if (id_ame not in dic_amenity.keys() or id_pla not in dic_place.keys()):
        abort(404)
    obj_amenity = storage.get(Amenity, amenity_id)
    obj_place = storage.get(Place, place_id)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if obj_amenity not in obj_place.amenities:
            abort(404)
        else:
            obj_place.amenities.remove(obj_amenity)
    else:
        if amenity_id not in obj_place.amenity_ids:
            abort(404)
        else:
            obj_place.amenity_ids.delete(amenity_id)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_revi(place_id, amenity_id):
    """POST amenity list"""
    dic_amenity = storage.all(Amenity)
    dic_place = storage.all(Place)
    id_ame = "Amenity." + amenity_id
    id_pla = "Place." + place_id
    if (id_ame not in dic_amenity.keys() or id_pla not in dic_place.keys()):
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    obj_place = storage.get(Place, place_id)
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity_obj in obj_place.amenities:
            return jsonify(amenity_obj.to_dict())
        else:
            obj_place.amenities.append(amenity_obj)
            storage.save()
            return jsonify(obj_amenity.to_dict(), 201)
    else:
        if amenity_id in obj_place.amenity_ids:
            obj_place.amenity_ids.append(amenity_id)
            storage.save()
            return jsonify(obj_amenity.to_dict(), 201)
