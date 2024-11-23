from django.db import models

# Create your models here.

class Attendance(models.Model):
    userid = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50)
    datetime = models.CharField(max_length=100,default=0)