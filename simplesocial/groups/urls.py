############ GROUP'S URLS.PY ################
from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.ListGroups.as_view(), name='all'),
]