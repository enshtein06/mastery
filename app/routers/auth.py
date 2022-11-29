from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, utils, database, oauth2
from ..database import get_db

router = APIRouter(
  tags=["Authentiocation"]
)

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  user = db.query(models.User).filter(func.lower(models.User.email) == func.lower(user_credentials.username)).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

  if not utils.verify(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

  access_token = oauth2.create_access_token(data={"user_id": user.id})
  refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})

  return {"accessToken": access_token, "refreshToken": refresh_token}

@router.post("/refresh-token", response_model=schemas.Token)
async def refreshToken(db: Session = Depends(get_db), id = ""):
  current_user = oauth2.get_current_user(id, db)
  if not current_user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

  access_token = oauth2.create_access_token(data={"user_id": current_user.id})
  refresh_token = oauth2.create_refresh_token(data={"user_id": current_user.id})

  return {"accessToken": access_token, "refreshToken": refresh_token}

@router.post("/vendor-login", response_model=schemas.Token)
async def vendorLogin(user: schemas.VendorUserCreate, db: Session = Depends(get_db)):
  user_in_db = db.query(models.User).filter(models.User.vendor_id == user.vendor_id).first()

  if user_in_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
      detail=f"User with email = {user.vendor_id} already exist")

  newUser = models.User(**user.dict())

  db.add(newUser)
  db.commit()
  db.refresh(newUser)

  access_token = oauth2.create_access_token(data={"user_id": newUser.id})
  refresh_token = oauth2.create_refresh_token(data={"user_id": newUser.id})

  return {"accessToken": access_token, "refreshToken": refresh_token}
