# pip install python-dotnet
from dotenv import load_dotenv
from os import environ

load_dotenv()

class AppConfig:
    is_development = environ.get("ENVIRONMENT") == "development" #either this returns true
    is_production = environ.get("ENVIRONMENT") == "production" #or this returns true
    mysql_host = environ.get("MYSQL_HOST")
    mysql_user = environ.get("MYSQL_USER")
    mysql_password = environ.get("MYSQL_PASSWORD")
    mysql_database = environ.get("MYSQL_DATABASE")
    session_secret_key = environ.get("SESSION_SECRET_KEY")
    password_salt = environ.get("PASSWORD_SALT")
