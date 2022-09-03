from django.contrib import admin

# Register your models here.
from videolist.models import Classification, Video, Comment

admin.site.register(Classification)
admin.site.register(Video)
admin.site.register(Comment)
