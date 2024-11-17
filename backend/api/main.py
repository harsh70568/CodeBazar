
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
from frontend.models import Register, Contact
from django.core.exceptions import ValidationError
from fastapi.responses import RedirectResponse
from asgiref.sync import sync_to_async 
from fastapi.middleware.cors import CORSMiddleware
from django.contrib.auth.hashers import check_password, make_password

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

class Login(BaseModel):
    email: str
    password: str

class ContactUs(BaseModel):
    name: str
    email: str
    phone_no: str
    message: str

@app.post("/api/register")
async def register_user(details: RegisterForm):
    try:
        new_entry = await sync_to_async(Register.objects.create)(
            name=details.name,
            email=details.email,
            password=make_password(details.password)
        )
        return {"msg" : "user is registered sucesfully", "name": details.name}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

@app.post("/api/login")
async def login_user(details: Login):
    try:
        # Check if user exists with the provided email
        user = await sync_to_async(get_user_by_email)(details.email)
        if not user:
            return {"msg" : "Email not exists"}
        if not check_password(details.password, user.password):
            return {"msg": "Password do not match, Try again!"}
        return {"msg": "Succesfully Logged in", "username": user.name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def get_user_by_email(email: str):
    try:
        user = Register.objects.filter(email=email).first()
        return user
    except Register.DoesNotExist:
        return None

@app.post("/api/contact")
async def contact_us(details: ContactUs):
    try:
        new_entry = await sync_to_async(Contact.objects.create)(
            name=details.name,
            email=details.email,
            phone_no=details.phone_no,
            message=details.message
        )
        return {"msg": "Your message has been sent successfully!"}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")