# -*- coding: utf-8 -*-

from flask import jsonify, make_response


def handle_invalid_json(error):
    json_response = jsonify({
        'error': 'Invalid JSON: {}'.format(error.message),
        })

    return make_response(json_response, 400)
