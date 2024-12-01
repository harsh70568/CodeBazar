
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeBazar.settings')
''' Initialize Django to access models and other Django functionality,
    Here, fastAPI doesn't know the models, where to get them and how to
    find them, so we intialise django. '''
import django
django.setup()

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from django.conf import settings
from frontend.models import Register, Contact, bookSession
from django.core.exceptions import ValidationError
from asgiref.sync import sync_to_async 
from fastapi.middleware.cors import CORSMiddleware
from django.contrib.auth.hashers import check_password, make_password
from pathlib import Path
import uuid

app = FastAPI()

''' Note - Here, Our backend server is running on PORT - 7000, Frontend server is running 
    on PORT 8000, so make sure we allow origin of frontend as req comes from frontend to backend. '''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://codebazar.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

UPLOAD_FOLDER = Path("payment_images")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True) 

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
    subject: str
    message: str

@app.get("/")
async def root():
    return {"msg": "base page"}

@app.post("/api/register")
async def register_user(details: RegisterForm):
    try:
        user = await sync_to_async(get_user_by_email)(details.email)
        if user:
            return {"msg": "User is already registered with us!", "name": "None"}
        else:
            new_entry = await sync_to_async(Register.objects.create)(
            name=details.name,
            email=details.email,
            password=make_password(details.password)
        )
            return {"msg" : "User is registered sucesfully", "name": details.name}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

@app.post("/api/login")
async def login_user(details: Login):
    try:
        user = await sync_to_async(get_user_by_email)(details.email)
        if not user:
            return {"msg" : "Email not exists"}
        if not check_password(details.password, user.password):
            return {"msg": "Invalid Credentials, Try again!"}
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
            subject=details.subject,
            message=details.message
        )
        return {"msg": "Your message has been sent successfully!"}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

@app.post("/api/book-session")
async def book_session(
    name: str = Form(...),
    email: str = Form(...),
    whatsapp_no: str = Form(...),
    interview_date: str = Form(...),
    interview_time: str = Form(...),
    amount: int = Form(...),
    image: UploadFile = File(...)
):
    try:
        if image:
            if not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Uploaded file is not an image")
            unique_filename = f"{uuid.uuid4().hex}_{image.filename}"
            image_path = UPLOAD_FOLDER / unique_filename
            with image_path.open("wb") as file:
                file.write(await image.read())

            image_url = str(image_path)
        else:
            image_url = None
        new_entry = await sync_to_async(bookSession.objects.create)(
            name= name,
            email= email,
            whatsapp_no= whatsapp_no,
            interview_date= interview_date,
            interview_time= interview_time,
            amount= amount,
            image= image_url
        )
        return {"msg": "Our Team will verify your payment and will send you an email soon!", "booking_id": new_entry.id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")