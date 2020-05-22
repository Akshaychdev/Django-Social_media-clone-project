from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
# The class based views
from django.views import generic

from groups.models import Group, GroupMember

from django.shortcuts import get_object_or_404

# messeges from built-in messages app
from django.contrib import messages


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

############# The JoinGroup and LeaveGroup views ####################

#***************** To get an understanding of what python's super() function in django get methods ****************
#  visit: https://stackoverflow.com/questions/50192463/explain-return-super-getrequest-args-kwargs/50192672
#******************************************************************************************************************

# 'RedirectView':- CBV which Redirects to a given URL.
class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    """
    view for Joining the group, requires login,
    do the backend tojoin a user to the group,
    then redirects to
    """
    def get_redirect_url(self, *args, **kwargs):
        """
        Constructs the target URL for redirection.
        :param args: positional arguments captured from URL Pattern
        :param kwargs: keyword arguments captured from url pattern
        :return:to the detailed page of that group using slug
        """
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        """
        To give a user an Error or warning message,
        if they are already in the group
        """
        # Try to get the Group or return a 404 error
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            # Creating a GroupMember object, user= current user, group=current 'group'(variable above)
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            # shows an instant warning message
            messages.warning(self.request, 'Warning, already a member!')
        else:
            messages.success(self.request, 'You are now a Member!')
            
        # calling a method on the super object acts like calling that method on the class.
        return super().get(request, *args, **kwargs)
    
class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    """
    When you leave a group, you get redirected to
    same group
    """

    def get_redirect_url(self, *args, **kwargs):
        """
        The same thing as of JoinGroup
        :param args: positional arguments captured from URL Pattern
        :param kwargs: keyword arguments captured from url pattern
        :return:to the detailed page of that group using slug
        """
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        """
        To set you cannot leave a group, if you not in it 
        """
        # Try to get an object, membership
        try:
            # Try to get the existing membership in the group wanted to leave
            # By filtering entries in the GroupMember model(contains user-group relation data)
            membership = GroupMember.objects.filter(
                # user already in the group
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        # DoesNotExist call on a GroupMember object(that group member relation b/w the user and group not exists)
        except GroupMember.DoesNotExist:
            # one clicked the leave button in a group, he is not a member of
            messages.warning(self.request, 'Sorry you are not in this Group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')
            
        return super().get(request, *args, **kwargs)