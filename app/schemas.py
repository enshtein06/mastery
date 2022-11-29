from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class VendorUserCreate(BaseModel):
  vendor_id: str

class VendorUserOut(BaseModel):
  id: int
  vendor_id: str
  created_at: datetime

  class Config:
    orm_mode = True

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class VendorUserUpdate(UserCreate):
  token: str
  pass

class UserOut(BaseModel):
  id: int
  email: str
  created_at: datetime

  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  accessToken: str
  refreshToken: str

class TokenData(BaseModel):
  id: Optional[str] = None

class ActivityBase(BaseModel):
  type: str
  title: str

class CreateActivity(ActivityBase):
  token: str
  pass

class Acitivity(ActivityBase):
  id: int
  created_at: datetime
  user_id: int
  total_time_in_minutes: int = 0
  # Keep it just as an example
  # user: UserOut

  class Config:
    orm_mode = True

class ExperienceBlockBase(BaseModel):
  time_in_seconds: int
  activity_id: int
  description: Optional[str] = None
  to_improve: Optional[str] = None
  rating: Optional[int] = None

class CreateExperienceBlock(ExperienceBlockBase):
  token: str
  pass

class ExperienceBlock(ExperienceBlockBase):
  id: int
  user_id: int
  created_at: datetime

  class Config:
    orm_mode = True
