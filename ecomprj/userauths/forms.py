from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

INPUT_CLASSES='form-control' 
#form-control form-control-lg



class userRegisterForm(UserCreationForm):   # class extending usercreationform class
    username = forms.CharField(widget=forms.TextInput(attrs={'class':INPUT_CLASSES,'placeholder':"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Email",'class':INPUT_CLASSES,}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':INPUT_CLASSES,}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password",'class':INPUT_CLASSES,}))


    class Meta:                             # things we want to work with
        model = User  #model we are interacting with
        fields = ['username', 'email']
        # widgets={
        #     'username':forms.TextInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'email':forms.EmailInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'password1':forms.PasswordInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'password2':forms.PasswordInput(attrs={
        #         'pl'
        #         'class':INPUT_CLASSES
        #     }),
        # }
