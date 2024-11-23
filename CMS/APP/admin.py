from django.contrib import admin
from APP.models import Attendance

# Register your models here.

class attendance(admin.ModelAdmin):
    list_display = ('userid','name','status','datetime')

admin.site.register(Attendance,attendance)
