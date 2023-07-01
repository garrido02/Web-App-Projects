from django.contrib import admin
from .models import User, Message, Pack, Team

# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Pack)
admin.site.register(Team)
