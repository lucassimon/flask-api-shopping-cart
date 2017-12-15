# -*- coding: utf-8 -*-

# Python

# Flask
from flask import jsonify
# Apps
from .messages import _MSG102, _MSG206, _MSG300, _MSG301, _MSG906


def resp_notallowed_user(resource, msg=_MSG102):
    resp = jsonify({
        'status': 401,
        'resource': resource,
        'message': msg
    })

    resp.status_code = 401

    return resp


def resp_form_invalid(resource, errors):
    resp = jsonify({
        'resource': resource,
        'message': _MSG300,
        'errors': errors,
        'status': 400,
    })

    resp.status_code = 400

    return resp


def resp_does_not_exist(resource, description):
    resp = jsonify({
        'status': 404,
        'message': _MSG206.format(description),
        'resource': resource
    })

    resp.status_code = 404

    return resp


def resp_exception(resource, msg=_MSG906, description=''):
    resp = jsonify({
        'status': 500,
        'message': msg,
        'resource': resource,
        'description': '{}'.format(description)
    })

    resp.status_code = 500

    return resp


def resp_already_exists(resource, description=''):
    resp = jsonify({
        'resource': resource,
        'message': _MSG301.format(description),
        'status': 400
    })

    resp.status_code = 400

    return resp
