import base64
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
        content = base64.b64encode(
            self.cleaned_data['excel_file'].read()
        ).decode('ascii')
        import_excel(year, semester, content)
