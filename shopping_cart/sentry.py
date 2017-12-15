# -*- coding: utf-8 -*-

from raven.contrib.flask import Sentry

sentry = Sentry()


def configure_sentry(app):
    sentry.init_app(app, dsn=app.config.get('SENTRY_DSN', ''))
