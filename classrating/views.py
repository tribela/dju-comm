from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ExcelImportForm


@staff_member_required
def import_excel_file(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid() or True:
            form.save()
            # TODO: Change this to admin page.
            return redirect('/')
        else:
            context = {
                'form': form
            }
    else:
        context = {
            'form': ExcelImportForm()
        }
    return render(request, "form.html", context)
