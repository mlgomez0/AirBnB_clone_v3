#!/usr/bin/python3
""" holds class Review"""
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    ids = "Place." + place_id
    dic_obj = storage.all()
    review_dics = []
    if (ids in dic_obj.keys()):
        list_reviews = dic_obj[ids].reviews
        for review in list_reviews:
            review_dics.append(review.to_dict())
        return jsonify(review_dics)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    ids = "Review." + review_id
    dic_obj = storage.all(Review)
    if (ids in dic_obj.keys()):
        return jsonify(dic_obj[ids].to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    dic = storage.all(Review)
    ids = "Review." + review_id
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.reload()
        storage.close()
        return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    if ("Place." + place_id not in storage.all(Place).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if ('user_id' not in json.keys()):
            return make_response(jsonify({'error': "Missing user_id"}), 400)
        if ("User." + json['user_id'] not in storage.all(User).keys()):
            abort(404)
        if ('text' not in json.keys()):
            return make_response(jsonify({'error': "Missing text"}), 400)

        json['place_id'] = place_id
        obj = Review(**json)
        storage.new(obj)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviews(review_id):
    if ("Review." + review_id not in storage.all(Review).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        dic = storage.all(Review)
        ids = "Review." + review_id
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "upd\
                    ated_at" and k != "place_id"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
