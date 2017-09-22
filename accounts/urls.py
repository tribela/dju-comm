from django.conf.urls import include, url
from registration.backends.hmac.views import RegistrationView

from .forms import RegistrationFormDjuComm

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view(
        form_class=RegistrationFormDjuComm),
        name='registration_register'
        ),
    url(r'^', include('registration.backends.hmac.urls')),
]
