from django.urls import path

from . import views

app_name = "utils_test_app"
urlpatterns = [path("", views.index, name="index")]
