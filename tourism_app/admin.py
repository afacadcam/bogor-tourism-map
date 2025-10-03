# tourism_app/admin.py

from django.contrib import admin
from .models import TourismPlace, TourismCategory

# Registrasi model TourismCategory agar muncul di admin
""" @admin.register(TourismCategory)
class TourismCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_color']  # Kolom yang ditampilkan di daftar
    list_editable = ['badge_color']  # Bisa edit langsung dari daftar
    search_fields = ['name']  # Bisa cari berdasarkan nama """


@admin.register(TourismCategory)
class TourismCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "badge_color", "colored_badge_preview"]
    list_editable = ["badge_color"]

    # Menampilkan preview badge berwarna di admin
    def colored_badge_preview(self, obj):
        from django.utils.html import format_html

        return format_html(
            '<span class="badge bg-{}">{}</span>', obj.badge_color, obj.name
        )

    colored_badge_preview.short_description = "Preview Badge"

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
                "css/custom.css",  # <-- ini file local static CSS
            )
        }


# Jika belum register TourismPlace, tambahkan juga
@admin.register(TourismPlace)
class TourismPlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "rating", "ticket_price"]
    list_filter = ["category"]
    search_fields = ["name", "address"]
