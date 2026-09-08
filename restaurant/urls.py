from django.urls import path

from . import views


urlpatterns = [
    # Main page of the application.
    path("", views.index, name="index"),
]