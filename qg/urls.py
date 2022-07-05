from django.urls import path
from . import views



urlpatterns = [
    path('', views.home_qg,name='home_qg'),
    path('references/', views.references,name='references'),
    path('FAQ/',views.FAQ,name='FAQ'),
    path('contact/',views.contact,name='contact'),
    path('users/',views.users,name='users'),
    path('start/',views.start,name='start'),
]