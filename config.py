DEBUG = True
SECRET_KEY = 'FEQ341TGVFZ'
DB_HOST = '127.0.0.1'
DB_USERNAME = 'weblog'
DB_PASSWORD = '123456'
DB_DATABASE = 'weblog'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_DATABASE)
