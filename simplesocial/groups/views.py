from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
# The class based views
from django.views import generic

from groups.models import Group, GroupMember

########## Three Main Class Based VIews ##############
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    """
    Creating ones own Group
    """
    # The editable Fields, don,t need other fields like slug, members etc.
    fields = ('name', 'description')
    model = Group

class SingleGroup(generic.DetailView):
    """
    For looking at a single Group
    """
    model = Group

class ListGroups(generic.ListView):
    """
    List of groups
    """
    model = Group
