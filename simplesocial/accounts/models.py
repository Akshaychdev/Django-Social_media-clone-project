from django.db import models
from django.contrib import auth

# Create your models here.

#Using django's built in models, all the heavylifting done by django
class User(auth.models.User, auth.models.PermissionsMixin):
    """
    The primary attributes of the default user are:
    username, password, email, first_name, last_name,
    used this django user objects to create models & forms, so django take care of the
    signing info of users
    """

    def __str__(self):
        """
        To get String representation of a user
        do this
        :return: "@username"
        """
        return "@{}".format(self.username)
