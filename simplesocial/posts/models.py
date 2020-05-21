from django.db import models

from django.urls import reverse
from django.conf import settings

import misaka

from groups.models import Group
# Create your models here.
######################################## POSTS MODELS.PY #############################################################

from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    """
    Attributes: user(foreignkey with toplvl User), created date, actual message, its html
    group(foreignkey relation with Group class in model of groups app)
    str representation
    save method
    url need to return
    Meta class
    """
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # To auto generate the date and time
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        """
        If someone writes html inside,
        misaka gets them supported
        :param args:
        :param kwargs:
        :return:
        """
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})
    
    class Meta:
        ordering = ['-created_at']
        # Every message is uniquely linked to user
        unique_together = ['user', 'message']