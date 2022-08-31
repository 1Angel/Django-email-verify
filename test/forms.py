from django.contrib.auth.forms import UserCreationForm
from test.models import Account


class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = [
            "username", "email", "password1", "password2"
        ]