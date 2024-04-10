from django import forms
from django.contrib.postgres.forms import SimpleArrayField

class FileForm(forms.Form):
    file_1 = forms.FileField()
    file_2 = forms.FileField()
    columns = SimpleArrayField(forms.CharField(max_length=100, required=False), required=False)