from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional

# base model
from app.models.base import BaseDocument

# inherits BaseDoc
class User(BaseDocument):
  email: EmailStr = Field(..., unique=True)
  hashed_password: str
  #created_at: datetime = Field(default_factory=datetime.utcnow)
  is_active: bool = True

  class Settings:
    name = "users" # mongodb collection name