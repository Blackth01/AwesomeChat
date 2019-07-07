import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'randompasswordhere'

    SQLALCHEMY_DATABASE_URI =  "mysql://username:password@localhost/databasename"
    SQLALCHEMY_POOL_RECYCLE = 4500

    SQLALCHEMY_TRACK_MODIFICATIONS = False

