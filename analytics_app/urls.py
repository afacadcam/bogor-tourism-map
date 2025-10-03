# analytics_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('api/category-distribution/', views.places_by_category_api, name='places_by_category_api'),
    path('api/monthly-visits/', views.monthly_visits_api, name='monthly_visits_api'),
    path('api/top-places/', views.top_places_api, name='top_places_api'),
    path('api/rating-distribution/', views.rating_distribution_api, name='rating_distribution_api'),
    path('api/visitor-analytics/', views.visitor_analytics_api, name='visitor_analytics_api'),
    path('export-excel/', views.export_analytics_excel, name='export_analytics_excel'),
]
