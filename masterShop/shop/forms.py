from django import forms
from shop.models import User

class RegForm(forms.Form):
    first_name  = forms.CharField()
    last_name   = forms.CharField()
    email       = forms.EmailField()
    country     = forms.CharField()
    address     = forms.CharField(widget=forms.Textarea)
    password    = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'country',
                  'address',
                  'password']
