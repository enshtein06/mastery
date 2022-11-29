from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from . import models
from .database import engine
from .routers import activities, auth, experience_block, user

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(activities.router)
app.include_router(auth.router)
app.include_router(experience_block.router)
app.include_router(user.router)

@app.get("/data-policy", response_class=HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse("data-policy.html", {"request": request})

@app.get("/temrs-of-use", response_class=HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse("temrs-of-use.html", {"request": request})
