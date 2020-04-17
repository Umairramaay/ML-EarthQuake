"""geoQuacks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
import django.contrib.auth.views
import geoQuackApp.views
from geoQuackApp.views import quake_dataset, quake_dataset_pred, quake_dataset_pred_risk
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', geoQuackApp.views.home, name='home'),
    url(r'^$', geoQuackApp.views.home, name='home'),
    url(r'^quake_dataset/', quake_dataset, name='quakedataset'),
    url(r'^quake_dataset_pred/', quake_dataset_pred, name='quakedatasetpred'),
    url(r'^quake_dataset_pred_risk/',
        quake_dataset_pred_risk, name="quakedatasetpredrisk"),


] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
