from django.urls import path
from . import views


urlpatterns = [  
  path('test_call/',views.test_call), 
  path('food/',views.food), 
  path('photo/',views.ph),
  path('check/',views.CheckExist)
]