from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .forms import FileForm
from .untils.compare_sheets import compare_sheets

def index(request):
  return render(request, "polls/index.html")
    
def get_sheets(request):
  if request.method == 'POST':
    form = FileForm(request.POST, request.FILES)
    print(form.is_valid())

    if form.is_valid():
      if form.cleaned_data['columns']:
        columns = form.cleaned_data['columns']
      else:
        columns = []

      compare_sheets(request.FILES, columns)
      return HttpResponse("Ok")
    else:
      return HttpResponse("Not valid")
  else: 
    return HttpResponse("This route required a POST method!")


# return HttpResponse(template.render(context, request))
# Create your views here.
