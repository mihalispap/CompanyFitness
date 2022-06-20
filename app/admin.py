from django.contrib import admin
from app import models
from app import forms

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.CompanyTeam)
admin.site.register(models.TeamMember)
admin.site.register(models.FitnessStat)
