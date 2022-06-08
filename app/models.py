from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        db_table = 'cf_company'


class CompanyTeam(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cf_company_team'


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(CompanyTeam, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'cf_team_member'


class FitnessStat(models.Model):
    tracked_on = models.DateField(null=False, blank=False)
    metric = models.CharField(max_length=256, null=False, blank=False)
    value = models.IntegerField(null=False, blank=False)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cf_fitness_stat'
