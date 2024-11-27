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
    subject = models.CharField(max_length=50, blank=True)
    message = models.TextField()

    class Meta:
        db_table = 'queries'

class bookSession(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    whatsapp_no = models.CharField(max_length=10)
    interview_date = models.CharField(max_length=50)
    interview_time = models.CharField(max_length=50)
    amount = models.IntegerField()
    image = models.ImageField(upload_to="../media")

    class Meta:
        db_table = 'bookings'