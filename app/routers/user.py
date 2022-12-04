from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
  user_in_db = db.query(models.User).filter(models.User.email == user.email).first()

  if user_in_db:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
      detail=f"User with email = {user.email} already exist")

  # hash password
  hashed_password = utils.hash(user.password)
  user.password = hashed_password

  newUser = models.User(**user.dict())

  db.add(newUser)
  db.commit()
  db.refresh(newUser)

  return newUser

#@router.get("/{id}", response_model=schemas.UserOut)
#def getUser(id: int, db: Session = Depends(get_db)):
#  user = db.query(models.User).filter(models.User.id == id).first()

#  if not user: 
#    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#      detail=f"User with id = {id} doesn't exist")

#  return user

@router.put("/", response_model=schemas.Token)
async def updateVendorCreatedUser(
  user: schemas.VendorUserUpdate, 
  db: Session = Depends(get_db)
):
  current_user = oauth2.get_current_user(user.token, db)
  del user.token
  # hash password
  hashed_password = utils.hash(user.password)
  user.password = hashed_password
  user_query = db.query(models.User).filter(models.User.id == current_user.id)
  updated_user = user_query.first()

  if updated_user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={current_user.id} doesn't exist")

  user_query.update(user.dict(), synchronize_session=False)
  db.commit()

  access_token = oauth2.create_access_token(data={"user_id": updated_user.id})
  refresh_token = oauth2.create_refresh_token(data={"user_id": updated_user.id})

  return {
    "accessToken": access_token, 
    "refreshToken": refresh_token
  }

