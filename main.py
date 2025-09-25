import os
import sys
import warnings
import uuid
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv
from argon2 import PasswordHasher

import fastapi
from fastapi import FastAPI, Depends, Form, HTTPException, status, Request, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, Response, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


# warnings.filterwarnings("ignore")
os.system("cls")
load_dotenv()


app = FastAPI()


templates = Jinja2Templates(directory=["templates"])
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/me", StaticFiles(directory="me"), name="me")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ Home Page """
    return templates.TemplateResponse(
        "/resume/home.html", 
        {
            "request": request
        }
    )

@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    """ Resume Page """
    return templates.TemplateResponse(
        "/resume/resume.html", 
        {
            "request": request
        }
    )