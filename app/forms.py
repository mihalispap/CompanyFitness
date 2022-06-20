import datetime
import os

from django import forms
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

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
    file_storage = FileSystemStorage(location=os.path.join(settings.STATIC_URL, 'screenshots'))
    form_list = [FitnessWizardUploadImage, FitnessStatForm]

    def done(self, form_list, **kwargs):
        # TODO: add check for inexistent on the specific date
        fitness_stat = models.FitnessStat(
            team_member=models.TeamMember.objects.get(user=self.request.user),
            file=form_list[0].files['0-screenshot'],
            value=form_list[1].data['1-value'],
            metric=form_list[1].data['1-metric'],
            tracked_on=form_list[1].data['1-tracked_on'],
        )
        fitness_stat.save()
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            form.fields['metric'].initial = 'steps'
            form.fields['tracked_on'].initial = datetime.datetime.now()
            form.fields['value'].initial = 0
        return context
