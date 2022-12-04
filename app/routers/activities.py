from typing import List
from fastapi import Response, Request, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
  prefix="/activities",
  tags=["Activities"]
)

@router.get("/", response_model=List[schemas.Acitivity])
def getActivities(
  db: Session = Depends(get_db),
  id = ""
):
  current_user = oauth2.get_current_user(id, db)
  activities = db.query(models.Activity).filter(models.Activity.user_id == current_user.id).all()
  experiences = db.query(models.ExperienceBlock).filter(models.ExperienceBlock.user_id == current_user.id).all()

  newActivities = []

  for activity in activities:
    total_time_in_seconds = 0
    for experience in experiences:
      if experience.activity_id == activity.id:
        total_time_in_seconds = total_time_in_seconds + experience.time_in_seconds

    activity.total_time_in_minutes = round(total_time_in_seconds / 60)
    newActivities.append(activity)

  return newActivities

# @router.get("/{id}", response_model=schemas.Acitivity)
# async def getActivity(id: int, db: Session = Depends(get_db)):
#   activity = db.query(models.Activity).filter(models.Activity.id == id).first()
#   if not activity:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} was not found")
#   return activity

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Acitivity)
async def createActivity(activity: schemas.CreateActivity, db: Session = Depends(get_db)):
  user = oauth2.get_current_user(activity.token, db)  
  del activity.token

  newActivity = models.Activity(user_id = user.id, **activity.dict())

  db.add(newActivity)
  db.commit()
  db.refresh(newActivity)

  return newActivity

@router.put("/{id}", response_model=schemas.Acitivity)
async def updatePost(
  id: int,
  activity: schemas.CreateActivity,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(oauth2.get_current_user)
):
  activity_query = db.query(models.Activity).filter(models.Activity.id == id)
  updated_activity = activity_query.first()

  if updated_activity == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")
  
  if updated_activity.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  activity_query.update(activity.dict(), synchronize_session=False)
  db.commit()

  return activity_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePost(
  id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(oauth2.get_current_user)
):
  activity_query = db.query(models.Activity).filter(models.Activity.id == id)
  activity = activity_query.first()

  if activity == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")

  if activity.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  activity_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)
