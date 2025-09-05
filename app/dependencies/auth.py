from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import verify_access_token
from app.models.user import User
from bson import ObjectId

# this object => help with extracting => bearer token => from request headers
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# token 
token = Depends(oauth2_scheme)

# pass token as default value
async def auth_user_guard(token: str = token) -> User:
  try: 
    # get payload out of token
    payload = verify_access_token(token=token)
    user_id = payload.get("sub") 

    # if user_id missing
    if (not user_id):
      raise HTTPException(status_code=401, detail="unauthorized: Invalid token")  

    # get user from db 
    user = await User.get(document_id=ObjectId(oid=user_id))

    # check if user not found in db
    if (not user):
      raise HTTPException(status_code=401, detail="unauthorized: no user")
    
    # return user => this value is passed to the route function
    return user
  except Exception as e:
    raise HTTPException(status_code=401, detail={"message": "except: Unauthorized", "error": e})