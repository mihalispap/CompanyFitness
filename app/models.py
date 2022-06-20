from django.contrib.auth.models import User
from django.db import models

fitness_metrics = [
    ('steps', 'steps'),
    ('calories', 'calories'),
    ('distance', 'distance'),
]


class Company(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        db_table = 'cf_company'

    def __str__(self):
        return f'{self.name}(id: {self.id})'


class CompanyTeam(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cf_company_team'

    def __str__(self):
        return f'{self.name} of {self.company}'


class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(CompanyTeam, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'cf_team_member'

    def __str__(self):
        return f'{self.user.email} of {self.team}'


class FitnessStat(models.Model):
    tracked_on = models.DateField(null=False, blank=False)
    metric = models.CharField(max_length=256, null=False, blank=False, choices=fitness_metrics)
    value = models.IntegerField(null=False, blank=False)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    file = models.FileField(null=True, blank=True)

    class Meta:
        db_table = 'cf_fitness_stat'
        unique_together = ('tracked_on', 'metric', 'team_member',)

    def __str__(self):
        return f'{self.metric} on {self.tracked_on} of {self.team_member}'

# @admin.action(description='Mark selected stories as published')
# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')
#
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ['title', 'status']
#     ordering = ['title']
#     actions = [make_published]
