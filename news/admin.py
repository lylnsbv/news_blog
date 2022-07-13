from django.contrib import admin
from .models import Articles, Category, Profile, Comment

admin.site.register(Articles)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
