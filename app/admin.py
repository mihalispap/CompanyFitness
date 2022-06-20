from django.contrib import admin
from app import models

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.CompanyTeam)
admin.site.register(models.FitnessStat)
admin.site.register(models.TeamMember)