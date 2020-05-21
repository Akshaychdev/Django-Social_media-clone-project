from django.contrib import admin
from . import models

# Register your models here.
# Setting up the Group model and the GroupMember model

# TabularInline class in admin, it allows one to utilise the admin interface in Django
# With the ability to edit models on the same page as the parent model(here Group is parent model)
# If one click the Group model in admin page, he can edit the GroupMember model too

class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

# No need to register GroupMember as it is inline to parent

admin.site.register(models.Group)