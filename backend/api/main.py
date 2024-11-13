
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeBazar.settings')
''' Initialize Django to access models and other Django functionality,
    Here, fastAPI doesn't know the models, where to get them and how to
    find them, so we intialise django. '''
import django
django.setup()

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from django.conf import settings
from django.db import IntegrityError
from frontend.models import Register 
from django.core.exceptions import ValidationError
from fastapi.responses import RedirectResponse
from asgiref.sync import sync_to_async 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

''' Note - Here, Our backend server is running on PORT - 7000, Frontend server is running 
    on PORT 8000, so make sure we allow origin of frontend as req comes from frontend to backend. '''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class RegisterForm(BaseModel):
    name: str
    email: str
    password: str


@app.get("/")
async def demo():
    return {"message": "hello harsh"}

@app.post("/api/register")
async def register_user(details: RegisterForm):
    try:
        new_entry = await sync_to_async(Register.objects.create)(
            name=details.name,
            email=details.email,
            password=details.password
        )
        return {"msg" : "user is registered sucesfully"}
        # return RedirectResponse(url='/index.html', status_code=302)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    