from django.urls import path 
from . import views

urlpatterns = [
   path('testjson/',views.test),
   path('all-guests/',views.FBV_list),
]
