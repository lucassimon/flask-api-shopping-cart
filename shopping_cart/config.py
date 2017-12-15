# -*- coding: utf-8 -*-
from os import getenv
from os.path import join, dirname, isfile
from datetime import timedelta

# Python Libs.
from dotenv import read_dotenv


_ENV_FILE = join(dirname(__file__), '../.env')


if isfile(_ENV_FILE):
    read_dotenv(_ENV_FILE)

APP_PORT = int(getenv('APP_PORT'))
DEBUG = eval(getenv('DEBUG').title())
SENTRY_DSN = getenv('SENTRY_DSN')
SECRET_KEY = getenv('SECRET_KEY')
FRONTEND_URL = getenv('FRONTEND_URL')
MONGODB_HOST = getenv('MONGODB_URI')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(getenv('JWT_EXPIRING_TIME')))

MAX_CONTENT_LENGTH = 16 * 1024 * 1024
