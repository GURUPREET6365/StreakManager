from django.contrib import admin

# Register your models here.
from .models import Folder, File

# Register your models here.
admin.site.register(Folder)
admin.site.register(File)


