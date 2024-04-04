from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .forms import NameForm

def index(request):
  return render(request, "polls/index.html")
    

def get_sheets(request):
  if request.method == 'POST':
    form = NameForm(request.POST)

    if form.is_valid():
      template = loader.get_template("polls/compare.html")
      context = form.cleaned_data

      return HttpResponse(template.render(context, request))


  return HttpResponse("Not valid")
# Create your views here.
