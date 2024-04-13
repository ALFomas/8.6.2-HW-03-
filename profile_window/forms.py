from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    """Class extensions to the functionality of the base class"""

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
