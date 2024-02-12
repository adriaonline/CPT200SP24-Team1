from django.urls import path
from App import views

urlpatterns = [ 
    path("", views.home, name = "home")
]