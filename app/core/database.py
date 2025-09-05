import motor.motor_asyncio
from beanie import init_beanie
from app.core.config import settings
from app.models.base import BaseDocument

async def init_db():
  mongo_uri = settings.MONGO_URI
  mongo_db_name = settings.MONGO_DB_NAME

  if not mongo_uri or not mongo_db_name:
    raise Exception("init_db: missing env variables")

  # database connection and  instance
  client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
  db = client[mongo_db_name]

  #import models here
  from app.models.user import User

  # register models
  await init_beanie(database=db, document_models=[User])

  # print after successful connection
  print("✅ mongodb was connected!")