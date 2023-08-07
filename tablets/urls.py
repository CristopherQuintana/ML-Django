from django.urls import path
from . import views

urlpatterns = [
    path('', views.predictor_demanda, name='predictor_demanda'),
    path('notebooks/', views.notebooks_view, name='notebooks'),
    path('tablets/', views.tablets_view, name='tablets'),
    path('pcs/', views.pcs_view, name='pcs'),
    path('impresoras/', views.impresoras_view, name='impresoras'),
]