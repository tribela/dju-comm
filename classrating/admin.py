from django.contrib import admin

from .models import Class, Professor, TimeTable


admin.site.register(Class)
admin.site.register(Professor)
admin.site.register(TimeTable)
