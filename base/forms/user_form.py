from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from base.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        field_args = {
            "name" : {
                "error_messages" : {
                    "required" : "Please let us know what to call you!"
                }
            }
        }

    def clean(self) :
        return super().clean()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image_file', 'name', 'username', 'email', 'modo_apariencia']
 