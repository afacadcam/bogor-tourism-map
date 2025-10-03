# tourism_app/urls.py
from django.urls import path
from . import views
from .views import AddPlaceView

app_name = "tourism_app"  # WAJIB, agar namespace valid

urlpatterns = [
    path('import/', views.FileImportView.as_view(), name='file_import'),
    path('import-history/', views.ImportHistoryView.as_view(), name='import_history'),
    path('export-template/', views.export_sample_template, name='export_sample_template'),
    path('places/', views.PlaceListView.as_view(), name='place_list'),
    path('add-place/', AddPlaceView.as_view(), name='add_place'),
    path('places/<int:pk>/edit/', views.PlaceUpdateView.as_view(), name='place_edit'),
    path('places/<int:pk>/delete/', views.PlaceDeleteView.as_view(), name='place_delete'),
    path('places/export/csv/', views.export_places_csv, name='export_places_csv'),
    path('places/export/xls/', views.export_places_xls, name='export_places_xls'),
]
