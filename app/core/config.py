# app/core/config.py
import os
# from pydantic import BaseConfig
from pydantic_settings import BaseSettings

# mongo 
# mongo_url = os.getenv("MONGO_URL")
# mongo_name = os.getenv("MONGO_DB_NAME")

# # env
ENV = os.getenv("ENV")

# # jwt
# jwt_secret = os.getenv("JWT_SECRET")
# jwt_algorithm = os.getenv("JWT_ALGORITHM")
# jwt_expire_minutes = os.getenv("JWT_EXPIRE_MINUTES")

class Settings(BaseSettings):
  PROJECT_NAME: str = "Bot API"
  VERSION: str = "1.0.0"
  DEBUG: bool = False
  ENV: str = "DEV"

  #mongo uri
  MONGO_URI: str 
  MONGO_DB_NAME: str 

  # JWT
  JWT_SECRET: str 
  JWT_ALGORITHM: str
  JWT_EXPIRE_MINUTES: int

  # redis 
  REDIS_PASS: str
  REDIS_HOST: str
  REDIS_PORT: int
  REDIS_USERNAME: str
  REDIS_DB_NAME: str

  # this is for celery => it eccept URL
  # REDIS_URL: str

  class Config:
    # loads values auto from .env file
    env_file = ".env"

settings = Settings()

# set debug based on ENV
settings.DEBUG = settings.ENV.upper() == "DEV"