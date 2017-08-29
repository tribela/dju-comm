from django.contrib import admin
from django.conf.urls import url
from .models import Class, Professor, TimeTable
from .views import import_excel_file


class ClassAdmin(admin.ModelAdmin):
    list_display = ['year', 'semester', 'title',
                    'division', 'classification', 'credit', 'professor']
    list_filter = ['year', 'semester', 'grade', 'credit']

    # TODO: Add link to `import_excel_file` view on admin page.

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                '^import_excel/$',
                self.admin_site.admin_view(import_excel_file),
                name='Import excel'
            ),
        ]
        return custom_urls + urls


admin.site.register(Class, ClassAdmin)
admin.site.register(Professor)
admin.site.register(TimeTable)
