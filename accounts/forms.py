from django import forms
from django.contrib.auth import get_user_model
from registration.forms import RegistrationForm, validators

from .models import SchoolEmailDomain

User = get_user_model()


class RegistrationFormDjuComm(RegistrationForm):

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(validators.DUPLICATE_EMAIL)

        email_domain = self.cleaned_data['email'].split('@')[1]
        if not SchoolEmailDomain.objects.filter(domain=email_domain).exists():
            raise forms.ValidationError('School email is required')

        return self.cleaned_data['email']
