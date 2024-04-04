from django.urls import path

from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("get_sheets", views.get_sheets, name="get_sheets"),
]
