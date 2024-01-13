from django.urls import path
from . import views
from api.views import Projekat1

urlpatterns = [
   
    path('pytnik', Projekat1)
]
