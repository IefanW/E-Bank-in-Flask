import os

WTF_CSRF_ENABLED = True # CSRF prevention should be enabled
SECRET_KEY = 'IefanWey' # key used to create cryptographically secure tokens


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
