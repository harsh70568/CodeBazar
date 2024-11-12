
import random
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

app = FastAPI()

@app.get("/")
def demo():
    return {"message": "hello harsh"}

    