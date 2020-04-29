#!/usr/bin/python3
""" holds class User"""
from models.user import User
from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    dic_obj = storage.all(User)
    user_dics = []
    for k, v in dic_obj.items():
        user_dics.append(v.to_dict())
    return jsonify(user_dics)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    ids = "User." + user_id
    dic_obj = storage.all(User)
    if (ids in dic_obj.keys()):
        return jsonify(dic_obj[ids].to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    dic = storage.all(User)
    ids = "User." + user_id
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.reload()
        storage.close()
        return jsonify({})


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    try:
        json = request.get_json()
    except:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if ('email' not in json.keys()):
        return make_response(jsonify({'error': "Missing email"}), 400)
    if ('password' not in json.keys()):
        return make_response(jsonify({'error': "Missing password"}), 400)

    obj = User(**json)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    if ("User." + user_id not in storage.all(User).keys()):
        abort(404)
    else:
        try:
            json = request.get_json()
        except:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        if json is None:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        dic = storage.all(User)
        ids = "User." + user_id
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "upd\
                    ated_at" and k != "email"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
