# maps_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MapView.as_view(), name='map_view'),
    path('api/places/', views.tourism_places_api, name='tourism_places_api'),
    path('api/nearby/', views.find_nearby_places, name='find_nearby_places'),
]
