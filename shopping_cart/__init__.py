# -*- coding: utf-8 -*-

# Python Libs.
from flask import Flask
from flask_cors import CORS

# Apps
from .db import db
from .sentry import configure_sentry
from .api import configure_api
from .cache import cache


def create_app():
    app = Flask('api-shopping-cart')
    app.config.from_object('shopping_cart.config')

    # Add decorators in app
    @app.after_request
    def apply_caching(response):
        response.headers['X-Server'] = 'Created with love.'
        return response

    CORS(app, resources={r'/*': {'origins': '*'}})

    # Sentry Get Errors
    configure_sentry(app)

    # Configure MongoEngine
    db.init_app(app)

    # Configure API

    configure_api(app)

    # configure cache
    cache.init_app(app)

    return app


if __name__ == "__main__":
    create_app()
