# -*- coding: utf-8 -*-

# Third
from flask_restful import Resource, Api

# Apps


# Admin


# Non Admin
from shopping_cart.cart.resources import Cart, CartDetail, CartAddProduct
from .messages import _MSG900, _MSG901, _MSG902, _MSG903, _MSG904


_API_ERRORS = {
    'UserAlreadyExistsError': {
        'status': 409,
        'message': _MSG901
    },
    'ResourceDoesNotExist': {
        'status': 410,
        'message': _MSG902
    },
    'MethodNotAllowed': {
        'status': 405,
        'message': _MSG903
    },
    'NotFound': {
        'status': 404,
        'message': _MSG904
    },
    'BadRequest': {
        'status': 400,
        'message': _MSG900
    },
    'InternalServerError': {
        'status': 500,
        'message': _MSG900
    }
}


# API Restful
class Index(Resource):
    def get(self):
        return {'hello': 'world by shopping cart service'}


api = Api(errors=_API_ERRORS)


def configure_admin_api():

    pass


def configure_api(app):

    # register the resources
    api.add_resource(Index, '/')

    # Cart
    api.add_resource(Cart, '/carts')
    api.add_resource(CartDetail, '/carts/<string:cart_id>')
    api.add_resource(CartAddProduct, '/carts/<string:cart_id>/product/add')

    api.init_app(app)