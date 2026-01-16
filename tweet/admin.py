from django.contrib import admin
from .models import Tweet, ContactMessage,Like
# Register your models here.

admin.site.register(Tweet)
admin.site.register(ContactMessage)
admin.site.register(Like)
