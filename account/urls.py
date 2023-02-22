from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'account'

urlpatterns = [
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('validate-username', csrf_exempt(views.validate_username), name='validate-username'),
    path('validate-email', csrf_exempt(views.validate_email), name='validate-email'),
    path('update-profile', views.update_profile, name='update-profile')
]
