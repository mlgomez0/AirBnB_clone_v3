#!/usr/bin/python3
""" holds class State"""
from models.state import State
from flask import jsonify, abort, request, Response, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False,
                 defaults={'state_id': 0})
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    dic = storage.all(State)
    ids = "State." + str(state_id)
    if (state_id == 0):
        state_list = []
        for k, v in dic.items():
            state_list.append(v.to_dict())
        return jsonify(state_list)
    elif (ids not in dic.keys()):
        abort(404)
    else:
        return jsonify(dic[ids].to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_states(state_id):
    dic = storage.all(State)
    ids = "State." + str(state_id)
    if (ids not in dic.keys()):
        abort(404)
    else:
        storage.delete(dic[ids])
        storage.save()
        return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    try:
        json = request.get_json()
    except:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if ('name' not in json.keys()):
        return make_response(jsonify({'error': "Missing name"}), 400)
    obj = State(**json)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    try:
        json = request.get_json()
    except:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    dic = storage.all(State)
    ids = "State." + str(state_id)
    if (ids not in dic.keys()):
        abort(404)
    else:
        for k, v in json.items():
            if (k != 'id' and k != 'created_at' and k != "updated_at"):
                setattr(dic[ids], k, v)
        storage.save()
        return make_response(jsonify(dic[ids].to_dict()), 200)
