from fastapi import APIRouter, HTTPException, status, Depends, Body
#hash_password, verify_password, create_access_token
from app.utils.security import hash_password, verify_password, generate_access_token, verify_access_token
from pydantic import BaseModel, EmailStr
from app.models.user import User
# for setup dependency on a route
from fastapi import Depends

# dependency => or middleware
from app.dependencies.auth import auth_user_guard

router = APIRouter(prefix='/auth', tags=["auth"])

# request schemas
#---------------

# signup => pydantic
class SignupRequest(BaseModel):
  email: EmailStr
  password: str

# login => pydantic
class LoginRequest(BaseModel):
  email: EmailStr
  password: str

# signup route
@router.post(path="/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest):
  # check existing user
  existing = await User.find_one(User.email == data.email)

  if (existing):
    raise HTTPException(status_code=400, details="Email already exists")
  
  user = User(
    email=data.email,
    hashed_password=hash_password(password=data.password)
  )

  # save new user
  await user.insert()

  return {"msg": "user created!", "user": user}

# login route
@router.post(path="/login")
async def login(data: LoginRequest):
  # check user with this email exists
  user = await User.find_one(User.email == data.email)
  
  if (not user):
    raise HTTPException(status_code=401, detail="Invalid email")

  # check user password
  is_password_valid = verify_password(plain_password=data.password, hashed_password=user.hashed_password)

  # check email and password
  if (not is_password_valid):
    raise HTTPException(status_code=401, detail="Invalid credentials")

  # payload
  payload = {"sub": str(user.id)}

  # generate access token
  token = generate_access_token(data=payload)

  return {
    "access_token": token,
    "token_type": "bearer"
  }

# test => profile
@router.get(path="/profile")
async def profile(auth_user: User = Depends(auth_user_guard)):
  return {
    "id": str(auth_user.id),
    "email": auth_user.email,
    "created_at": auth_user.created_at,
    "is_active": auth_user.is_active
  }