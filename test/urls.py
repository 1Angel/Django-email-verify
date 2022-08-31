from django.urls import path
from test.views import HomeView, RegisterView, activate
urlpatterns = [
    path('', HomeView, name='home'),
    path('register',RegisterView, name='register'),
    path('activate/<uidb64>/<token>',activate, name='activate')
]
