from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Account, Client


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    # Form validations
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Incorrect email or password.")


class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=50, required=False)
    contact_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)
    date_hired = forms.DateField(required=False)
    email = forms.EmailField(max_length=150, help_text="Required. Add a valid email address.")

    class Meta:
        model = Account
        fields = ["email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already in use. Please use a different email."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
