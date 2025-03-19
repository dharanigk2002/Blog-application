from importlib.metadata import requires

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Category, Post

class ContactForm(forms.Form):
    name = forms.CharField(label='name', max_length=100, required=True)
    email = forms.EmailField(label='email', required=True)
    message = forms.CharField(label='message', required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=50, required=True)
    email = forms.EmailField(label='email', required=True)
    password = forms.CharField(label='password', max_length=50, required=True)
    password_confirm = forms.CharField(label='password_confirm', max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password!=password_confirm:
            # raise forms.ValidationError("Passwords doesn't match")
            self.add_error('password_confirm', "Passwords do not match!")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, required=True)
    password = forms.CharField(label='password', max_length=50, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="email", max_length=50, required=True)

    def clean(self):
        cleaned_data=super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Invalid email id")
        return cleaned_data

class ResetPasswordForm(forms.Form):
    new_password=forms.CharField(label='new_password', max_length=50, required=True)
    confirm_password=forms.CharField(label='confirm_password', max_length=50, required=True)

    def clean(self):
        cleaned_data=super().clean()
        new_password=cleaned_data.get('new_password')
        confirm_password=cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password!=confirm_password:
            raise forms.ValidationError("Passwords doesn't match")
        return cleaned_data

class PostForm(forms.ModelForm):
    title = forms.CharField(label='title', max_length=50, required=True)
    content = forms.CharField(label='content', required=True)
    category = forms.ModelChoiceField(label='category', required=True, queryset=Category.objects.all())
    img_url = forms.ImageField(label='img_url', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):
        cleaned_data=super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and len(title)<5:
            raise forms.ValidationError("Title must be atleast 5 characters long")
        if content and len(content)<10:
            raise forms.ValidationError("Content must be atleast 10 characters long")
        return cleaned_data