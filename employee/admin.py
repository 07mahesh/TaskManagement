from django.contrib import admin
from .models import Task,Department,UserProfile


admin.site.register(Task)
admin.site.register(Department)
admin.site.register(UserProfile)
