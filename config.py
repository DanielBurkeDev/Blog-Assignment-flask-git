import os
from datetime import timedelta



# ======= App Config =========

SECRET_KEY = os.urandom(16)

# DB Config

# mysql
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://blogusr:FinnZee2016@localhost:3306/dbblog'

# sqlite
SQLALCHEMY_DATABASE_URI = 'sqlite:///dbblog'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Tokens
JWT_SECRET_KEY = os.urandom(16)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


# ======= END App Config =========