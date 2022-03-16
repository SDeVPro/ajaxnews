
from django.urls import path
from news import views 

urlpatterns = [
    path('',views.index,name='index'),
]