from django.contrib import admin

# Register your models here.
from .models import Job, Candidate

admin.site.register(Job)
admin.site.register(Candidate)
