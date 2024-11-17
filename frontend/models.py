from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'register_details'

class Login(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'login_details'

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_no = models.CharField(max_length=10)
    message = models.TextField()

    class Meta:
        db_table = 'queries'