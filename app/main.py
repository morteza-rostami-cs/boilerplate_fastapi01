# env config
from app.core.config import settings
# database connection
from app.core.database import init_db
from fastapi import FastAPI
from contextlib import asynccontextmanager

# celery and redis worker
#from app.tasks.worker import *

# router validator
from fastapi import Body

#models
from app.models.user import User

# router
from app.routers.auth import router as auth_router
from app.routers.files import router as file_router
from app.routers.ws import router as ws_router
from app.routers.tasks import router as tasks_router

# run on fastapi app 
@asynccontextmanager
async def lifespan(app: FastAPI):
  #on start up

  # database connection
  await init_db()
  yield

  # on shutdown code => clean-up

# fast api app 
app = FastAPI(title="Fast api backend for bots", lifespan=lifespan)

# server static files from static folder
from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# index
@app.get("/")
async def index():
  return {"message": "main route"}

# register routes
app.include_router(router=auth_router)
app.include_router(router=file_router)
# websocket routes
app.include_router(ws_router)
app.include_router(tasks_router)

# health check
@app.get("/health")
async def health_check():
  return {
    "status": "OK", 
    # test env
    "ENV": settings.REDIS_PASS,
    "db": settings.REDIS_USERNAME  
  }

# test: create user
@app.post("/test")
async def create_user(email: str=Body(...), password: str = Body(...)):
  # create a user 
  #user = User(email=email, hashed_password=password)
  # save
  #await user.insert()
  #return user
  # from app.utils.security import hash_password, verify_password
  # # test password hashing
  # plain_password = "super1234"
  # hashed = hash_password(password=plain_password)
  # print("hashed password: ", hashed)

  # # verify
  # is_valid: bool = verify_password(plain_password=plain_password, hashed_password=hashed)
  # if (is_valid):
  #   print("password is valid")
  # else:
  #   print("invalid**")
  
  # return {"is_valid": is_valid}

  # test jwt token
  # from app.utils.security import generate_access_token, verify_access_token
  # start_payload = {"sub": "user_id_1"}

  # token = generate_access_token(
  #   data=start_payload,
  # )
  # print('jwt token: ', token)

  # # verify token
  # payload = verify_access_token(token=token)
  # print("payload: ", payload)

  # return {"token": token, "payload": payload}
  pass
