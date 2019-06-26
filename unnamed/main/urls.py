from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('clear', views.clear, name='clear'),
    path('export', views.export, name='export'),
    path('export_filtered', views.export_filtered, name='export_filtered'),

]
