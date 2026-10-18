# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import secrets

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Read the secret key from the environment. Without one, generate a random key per start
    # (sessions then reset on restart) instead of falling back to a value published in this repo.
    SECRET_KEY = os.getenv('SECRET_KEY') or secrets.token_hex(32)

    # Public Mapbox token for the map page (set MAPBOX_TOKEN in .env)
    MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN', '')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    
    
    SOCIAL_AUTH_GITHUB  = False

    GITHUB_ID      = os.getenv('GITHUB_ID')
    GITHUB_SECRET  = os.getenv('GITHUB_SECRET')

    # Enable/Disable Github Social Login    
    if GITHUB_ID and GITHUB_SECRET:
         SOCIAL_AUTH_GITHUB  = True

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # SQL Alcghely database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        os.getenv('DB_PASS'     , 'pass'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'appseed_db')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
