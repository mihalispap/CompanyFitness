"""CompanyFitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from CompanyFitness import settings
from app import forms
from app import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('identify', views.identify_fitness_metric),
                  path('fitness-upload/',
                       user_passes_test(lambda user: user.is_authenticated, '/admin/')(
                           forms.FitnessWizard.as_view([forms.FitnessWizardUploadImage, forms.FitnessStatForm]))
                       ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
