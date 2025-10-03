# bogor_tourism_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # tambahkan ini
    path("", include("maps_app.urls")),
    path("tourism/", include("tourism_app.urls", namespace="tourism_app")),  # Tambahkan namespace
    path("analytics/", include("analytics_app.urls")),
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )

# Custom admin site headers
admin.site.site_header = "Admin Pariwisata Bogor"
admin.site.site_title = "Bogor Tourism Admin"
admin.site.index_title = "Dashboard Administrasi"
