from django import forms
from .models import Product
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'file']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data['password']