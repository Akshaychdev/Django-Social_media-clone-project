from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import  CreateView
from . import forms
# Create your views here.

class SignUp(CreateView):
    """
    View for form Signup from model User

    """
    # Class object attribute, dont need (), just setting the class
    form_class = forms.NewUserForm
    # Once successful signup, reverse them back to login page, reverse_lazy used cz
    # reverse_lazy won't execute until the value is needed.
    # It prevent 'Reverse Not Found' exceptions when working with URLs that may not be immediately known.
    # ie after form filled correctly and the submit button click up to end after parsing all the data
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'