# returns the user model currently active
from django.contrib.auth import get_user_model
#A UserCreation Form is already built in to auth. package
from django.contrib.auth.forms import UserCreationForm

#No exact same name to the built in classes
class NewUserForm(UserCreationForm):
    """
    using modelform, with model
    get_user_model()[The inbuilt fun. to grab current active model.
    """
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        When a user comes ready to sign up, first the UserCreationForm is called, set up the metaClass(setting up
        these are the fields                                                                                                                                                                                                                                                                                                                                                                                                                                                                           want to use),
        set up the label as same as on html inside forms
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        # For the Own 'Display Names/custom names'(not a necessory)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = "Email Address"