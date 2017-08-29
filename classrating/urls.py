from django.conf.urls import url
from .views import import_excel_file

urlpatterns = [
    url(r'^import_excel/$', import_excel_file),
]
