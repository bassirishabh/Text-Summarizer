from django import forms
from .models import getFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class getFileModel(forms.ModelForm):
    class Meta:
        model=getFile
        fields=['file','length']


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model=User
        fields=('username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2')

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data



    def save(self, commit=True):
        user=super(RegistrationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'autocomplete': 'off'}))

    class Meta:
        fields = ('username', 'password')

class urlform(forms.Form):
    urlname = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL'}))
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sentence Count'}))

class demoform(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'text-input','placeholder': 'Enter Text','style':'width:100%', 'autocomplete': 'off'}))
    count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sentence Count'}))
