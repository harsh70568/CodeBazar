from django.contrib import admin
from .models import Register, Login, Contact, bookSession

# Register your models here.
admin.site.register(Register)
admin.site.register(Login)
admin.site.register(Contact)
admin.site.register(bookSession)
