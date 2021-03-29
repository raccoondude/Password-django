from django.contrib import admin
from .models import User, Token
# Register your models here.
admin.site.register(Token)
admin.site.register(User)
