from django.contrib import admin
from django.shortcuts import redirect
from django_object_actions import DjangoObjectActions
from .models import Class, Professor, TimeTable
from .views import import_excel_file


class ClassAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['year', 'semester', 'title',
                    'division', 'classification', 'credit', 'professor']
    list_filter = ['year', 'semester', 'grade', 'credit']

    def import_excel(self, request, obj):
        return redirect(import_excel_file)

    import_excel.label = "Import Excel"
    import_excel.short_description = "Import class list from excel file"

    changelist_actions = ('import_excel', )


admin.site.register(Class, ClassAdmin)
admin.site.register(Professor)
admin.site.register(TimeTable)
