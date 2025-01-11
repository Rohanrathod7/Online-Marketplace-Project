from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

INPUT_CLASSES='form-control pt-3 pb-3 ps-4 mb-2' 
INPUT_STYLE = 'color: black'
#form-control form-control-lg



class userRegisterForm(UserCreationForm):   # class extending usercreationform class
    username = forms.CharField(widget=forms.TextInput(attrs={'class':INPUT_CLASSES,'placeholder':"Username", 'style':INPUT_STYLE}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Email",'class':INPUT_CLASSES, 'style':INPUT_STYLE}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Password",'class':INPUT_CLASSES, 'style':INPUT_STYLE}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password",'class':INPUT_CLASSES, 'style':INPUT_STYLE}))


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

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':INPUT_CLASSES,'placeholder':"Full Name", 'style':INPUT_STYLE}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class':INPUT_CLASSES,'placeholder':"Bio"}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class':INPUT_CLASSES,'placeholder':"Phone", 'style':INPUT_STYLE}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':INPUT_CLASSES,'placeholder':"Image", 'style':INPUT_STYLE}))
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone', 'image', ]
        # widgets={
        #     'full_name':forms.TextInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'bio':forms.Textarea(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'phone':forms.NumberInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'image':forms.FileInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        #     'verified':forms.CheckboxInput(attrs={
        #         'class':INPUT_CLASSES
        #     }),
        # }