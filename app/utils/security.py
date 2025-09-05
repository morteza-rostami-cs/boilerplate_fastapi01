from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
# .env stuff 
from app.core.config import settings

# define a hashing scheme
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# hash password
def hash_password(password: str) -> str:
  """Hash a plaintext password"""
  return pwd_context.hash(password)

# decode and verify the hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(
    secret=plain_password,
    hash=hashed_password,
  )

# -------------------
# jwt stuff
# -------------------

# generate access token
def generate_access_token(data: dict, expires_delta: Optional[timedelta] =None) -> str:
  """generate a jwt token"""

  # .env values 
  jwt_expire_min = settings.JWT_EXPIRE_MINUTES
  jwt_secret = settings.JWT_SECRET
  jwt_algorithm = settings.JWT_ALGORITHM

  if (not jwt_expire_min or not jwt_secret or not jwt_algorithm):
    raise Exception("generate_access_token: missing env values")

  # copy dict
  payload = data.copy()

  # expiration date
  expire = datetime.utcnow() + (expires_delta or timedelta(minutes=jwt_expire_min))

  # set expires date
  payload.update({"exp": expire})

  # generate jwt with 
  encoded_jwt = jwt.encode(
    claims=payload, 
    key= jwt_secret,
    algorithm= jwt_algorithm,
  )

  return encoded_jwt

# verify access token
def verify_access_token(token: str) -> dict:
  """decode jwt token"""
  try:
    jwt_secret = settings.JWT_SECRET
    jwt_algorithm = settings.JWT_ALGORITHM

    if (not jwt_secret or not jwt_algorithm): 
      raise Exception("verify_access_token: missing jwt_secret & jwt_algorithm")

    # payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    payload = jwt.decode(
      token=token,
      key=jwt_secret,
      algorithms=[jwt_algorithm]
    )
    return payload

  except JWTError as e:
    raise ValueError("Invalid token") from e