from django.urls import path
from . import views



urlpatterns = [
    path('', views.seleccionar_licencia, name='seleccionar_licencia'),
    path('resultado/', views.resultado, name='resultado'),
    path('ver-registros/', views.ver_registros, name='ver_registros'),  
    path('descargar_excel/', views.descargar_excel, name='descargar_excel'),  

]