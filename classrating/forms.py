from django import forms
from .models import Class
from .tasks import import_excel


class ExcelImportForm(forms.ModelForm):

    excel_file = forms.FileField()

    class Meta:
        model = Class
        fields = ['year', 'semester', 'excel_file']

    def save(self):
        year = self.cleaned_data['year']
        semester = self.cleaned_data['semester']
        content = self.cleaned_data['excel_file'].read()
        import_excel.delay(year, semester, content)
