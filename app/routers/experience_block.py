from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
  prefix="/experience_block",
  tags=["Experience Block"]
)

@router.get("/", response_model=List[schemas.ExperienceBlock])
def getExperienceBlocks(
  db: Session = Depends(get_db),
  activity_id: int = 0,
  id = ""
):
  current_user = oauth2.get_current_user(id, db)
  experience_blocks = db.query(models.ExperienceBlock).filter(
    models.ExperienceBlock.user_id == current_user.id, 
    models.ExperienceBlock.activity_id == activity_id
  ).order_by(models.ExperienceBlock.created_at.desc()).all()
  return experience_blocks

@router.get("/{id}", response_model=schemas.ExperienceBlock)
async def getExperienceBlock(id: int, db: Session = Depends(get_db)):
  experience_block = db.query(models.ExperienceBlock).filter(models.ExperienceBlock.id == id).first()
  if not experience_block:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} was not found")
  return experience_block

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ExperienceBlock)
async def createExperienceBlock(
  experience_block: schemas.CreateExperienceBlock,
  db: Session = Depends(get_db),
):
  current_user = oauth2.get_current_user(experience_block.token, db)
  del experience_block.token
  new_experience_block = models.ExperienceBlock(user_id = current_user.id,  **experience_block.dict())

  db.add(new_experience_block)
  db.commit()
  db.refresh(new_experience_block)

  return new_experience_block

@router.put("/{id}", response_model=schemas.ExperienceBlock)
async def updateExperienceBlock(
  id: int,
  experience_block: schemas.CreateExperienceBlock,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(oauth2.get_current_user)
):
  experience_block_query = db.query(models.ExperienceBlock).filter(models.ExperienceBlock.id == id)
  updated_experience_block = experience_block_query.first()

  if updated_experience_block == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")
  
  if updated_experience_block.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  experience_block_query.update(experience_block.dict(), synchronize_session=False)
  db.commit()

  return experience_block_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteExperienceBlock(
  id: int,
  db: Session = Depends(get_db),
  current_user: models.User = Depends(oauth2.get_current_user)
):
  experience_block_query = db.query(models.ExperienceBlock).filter(models.ExperienceBlock.id == id)
  experience_block = experience_block_query.first()

  if experience_block == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} doesn't exist")

  if experience_block.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

  experience_block_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)
