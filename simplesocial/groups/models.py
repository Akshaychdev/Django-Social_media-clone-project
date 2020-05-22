from django.urls import reverse
from django.db import models
# Helps to remove any character that are alpha-numeric, if there is a string with spaces if it is tobe used as of url,
# then it is lowercased and replace whitespaces with "-" or "_", creates slugs for url
from django.utils.text import slugify

############################## GROUPS MODELS.PY FILE ###############################
# Create your models for 'groups' application here.

# Able to put links or markdown-text, pip install misaka
# markdown allows one to easily write things in italic, bold, large font etc... using special codes, like # and <i>
import misaka

# returns the user model ie, currently active in this project
from django.contrib.auth import get_user_model
# User object, call things back from the current user section(model)
User = get_user_model()

from django import template
# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
# For having custom template tags in the future
register = template.Library()

#### Main model ###
class Group(models.Model):
    """
    Contains a group-name, slug, description to the group(both text and html representation with masaka), 
    members of a group(manytomany relationship with users)
    """
    # All groups unique username
    name = models.CharField(max_length=255, unique=True)
    # Slug is a part of a URL which identifies a particular page on a website in a form readable by users.
    # like /blog/ instead of /1/. Good SEO(Search Engine Optimisation) to create consistency in title, heading and URL.
    # For making it work django offers us a slugfield.
    # unique ie every url code need to be unique, also don't need group slugs and group names to overlap each other
    slug = models.SlugField(allow_unicode=True, unique=True)
    # Description to the group
    description = models.TextField(blank=True, default='')
    # HTML version of the description(if needed)
    description_html = models.TextField(editable=False, default='', blank=True)
    # Members of a group
    # (Many-To-Many Relationship - both sides can relate to multiple instances of the other side),
    # A user can be in many groups, a group consist of many users
    # "through" model relates the source model, Group(contains manytomany field) to the target model (User).
    members = models.ManyToManyField(User, through='GroupMember')
    # ########[ManyToManyField.through
    # Django will automatically generate a table to manage many-to-many relationships. However, if you want to manually 
    # specify the intermediary table, you can use the through option to specify the Django model that represents the 
    # intermediate table that you want to use. The most common use for this option is when you want to associate extra 
    # data with a many-to-many relationship. ] #####################
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        1) To make slug from the name
        2) To make description_html from group description and save that
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.slug = slugify(self.name)
        # misaka features a fast HTML renderer, allowing to put markdown
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        """
        In urls.py of groups
        :return: 
        """
        return reverse('groups:single', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ['name']
    
class GroupMember(models.Model):
    """
    The class links users to various groups, it gives the identity(list) or connection between users and groups
    """
    # The model 'GroupMember' is related to model 'Group' through this foreign key
    # A member must have membership in a group
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    # Every groupmember is a user(authenticated signed user inbuilt class), the user can be a member of different groups
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        """
        grab current users username(chtrs of the User(inbuilt) model, defined in accounts app)
        :return:
        """
        return self.user.username
        
    class Meta:
        """
            
        """
        unique_together = ('group', 'user')