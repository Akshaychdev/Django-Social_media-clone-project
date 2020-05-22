############ GROUP'S URLS.PY ################
from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    # List Group page, homepage of groups app
    path('', views.ListGroups.as_view(), name='all'),
    # The create-group view
    path('new/', views.CreateGroup.as_view(), name='create'),
    # Detail view, this time not with the primary key but with the more user readable slug
    # <slug> --> slugifies the actual group name
    path('posts/in/<slug>/', views.SingleGroup.as_view(), name='single'),
    # Views for joining and leaving group
    path('join/<slug>/', views.JoinGroup.as_view(), name='join'),
    path('leave/<slug>/', views.LeaveGroup.as_view(), name='leave'),
]