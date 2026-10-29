from django.urls import path

from . import views

app_name = 'impersonate'

urlpatterns = [
    path('<int:user_pk>/', views.ImpersonateConfirmView.as_view(), name='confirm'),
    path('start/', views.ImpersonateStartView.as_view(), name='start'),
    path('stop/', views.ImpersonateStopView.as_view(), name='stop'),
]
