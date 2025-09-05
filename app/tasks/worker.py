# import dotenv variables for => worker process
# from dotenv import load_dotenv
# load_dotenv()

# just use pydantic settings for => importing config env variables 
from app.core.config import settings

from celery import Celery

# import tasks here for worker to know 
# import app.tasks.jobs

"""
redis://[:password]@host:port/db_number

# with username
redis://username:password@host:port/db_number

"""

import os

# get env variables
# host = os.getenv("REDIS_HOST")
# port = os.getenv("REDIS_PORT")
# username = os.getenv("REDIS_USERNAME")
# password = os.getenv("REDIS_PASS")
# db_name = os.getenv("REDIS_DB_NAME", 0)

host = settings.REDIS_HOST
port = settings.REDIS_PORT
username = settings.REDIS_USERNAME
password = settings.REDIS_PASS
db_name = settings.REDIS_DB_NAME

# --- Validate env variables ---
missing = []
for name, value in [
  ("REDIS_HOST", host), 
  ("REDIS_PORT", port),
  ("REDIS_USERNAME", username), 
  ("REDIS_PASS", password),
  ("REDIS_DB_NAME", db_name)]:

  if not value:
    missing.append(name)

if len(missing):
  raise EnvironmentError(f"Missing Redis env variables: {', '.join(missing)}")

# convert port/db_name to int
try:
  port = int(port)
  db_name = int(db_name)
except ValueError as e:
  raise ValueError(f"Invalid int for port or db_name: {e}")

# build redis URL
REDIS_URL = f"redis://{username}:{password}@{host}:{port}/{db_name}"

# initialize celery
celery_app = Celery(
  "worker",
  broker=REDIS_URL,
  backend=REDIS_URL,
  # register jobs
  include=["app.tasks.jobs"]
)

celery_app.conf.update(
  task_serializer="json",
  result_serializer="json",
  accept_content=["json"],
  timezone="UTC",
  enable_utc=True
)

# redis connection test

import redis

try:
  r = redis.Redis(
    host=host,
    port=int(port),
    username=username,
    password=password,
    decode_responses=True
  )
  if (r.ping()):
    print("✅ connected to redis!")
except redis.RedisError as e:
  print("❌ Redis connection failed:", e)

# """Basic connection example.
# """
# """
# import redis

# r = redis.Redis(
#     host='',
#     port=17846,
#     decode_responses=True,
#     username="default",
#     password="",
# )

# success = r.set('foo', 'bar')
# # True

# result = r.get('foo')
# print(result)
# # >>> bar
