import datetime
import os

import requests
from django import forms
from django.contrib import admin
from django.core.files.storage import FileSystemStorage

from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView

import urllib.parse

from CompanyFitness import settings

from app import models


class FitnessWizardUploadImage(forms.Form):
    screenshot = forms.FileField()


class FitnessStatForm(forms.ModelForm):
    tracked_on = forms.DateField()

    class Meta:
        model = models.FitnessStat
        fields = ['tracked_on', 'metric', 'value']


class FitnessWizard(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, settings.MEDIA_URL))
    form_list = [FitnessWizardUploadImage, FitnessStatForm]

    def done(self, form_list, **kwargs):
        fitness_stat = models.FitnessStat()
        if models.FitnessStat.objects.filter(
                team_member=models.TeamMember.objects.get(user=self.request.user),
                tracked_on=form_list[1].data['1-tracked_on'],
                metric=form_list[1].data['1-metric'],
        ).exists():
            fitness_stat = models.FitnessStat.objects.filter(
                team_member=models.TeamMember.objects.get(user=self.request.user),
                tracked_on=form_list[1].data['1-tracked_on'],
                metric=form_list[1].data['1-metric'],
            ).first()

        fitness_stat.team_member = models.TeamMember.objects.get(user=self.request.user)
        fitness_stat.file = form_list[0].files['0-screenshot']
        fitness_stat.value = form_list[1].data['1-value']
        fitness_stat.metric = form_list[1].data['1-metric']
        fitness_stat.tracked_on = form_list[1].data['1-tracked_on']

        fitness_stat.save()
        return redirect('/admin/')

    def get_context_data(self, form, **kwargs):

        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            file_path = os.path.join(settings.MEDIA_ROOT, settings.MEDIA_URL, self.request.FILES['0-screenshot'].name)
            endpoint = f'{"https://" if self.request.is_secure() else "http://"}{self.request.get_host()}'
            endpoint = f'{endpoint}/identify?image_path={urllib.parse.quote_plus(file_path)}'

            # TODO: handle multiple identified metrics
            data = requests.get(endpoint).json()
            form.fields['metric'].initial = data[0]['metric']
            form.fields['tracked_on'].initial = data[0]['tracked_on']
            form.fields['value'].initial = data[0]['value']
        return context


class FitnessForm(forms.ModelForm):
    class Meta:
        model = models.FitnessStat
        fields = '__all__'


class FitnessAdmin(admin.ModelAdmin):
    form = FitnessForm

    def get_queryset(self, request):
        team_member = models.TeamMember.objects.get(user=request.user)
        return models.FitnessStat.objects.filter(team_member=team_member).all()
