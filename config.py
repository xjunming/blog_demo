import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'IMSECRET_KEY' or os.environ.get('SECRET_KEY')
    RECAPTCHA_PUBLIC_KEY = 'IMRECAPTCHA_PUBLIC_KEY' or os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = 'IMRECAPTCHA_PRIVATE_KEY' or os.environ.get('RECAPTCHA_PUBLIC_KEY')