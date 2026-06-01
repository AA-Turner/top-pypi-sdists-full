from django.urls import include, path

from allianceauth.authentication import views

urlpatterns = [
    path('activate/complete/', views.activation_complete, name='registration_activation_complete'),
    path('activate/', views.ActivationView.as_view(), name='registration_activate'),
    path('register/', views.RegistrationView.as_view(), name='registration_register'),
    path('register/complete/', views.registration_complete, name='registration_complete'),
    path('register/closed/', views.registration_closed, name='registration_disallowed'),
    path('', include('django.contrib.auth.urls')),
]
