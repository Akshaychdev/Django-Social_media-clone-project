from django.urls import path
# Django 1.11 introduces a Loginview and a Logoutview, no need to add it extra in the views.py
# The name 'auth_views' given so as don't to mix-up with original views
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
]
