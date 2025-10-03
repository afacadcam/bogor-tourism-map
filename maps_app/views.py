# maps_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from tourism_app.models import TourismPlace, TourismCategory, VisitorLog
import json


class MapView(TemplateView):
    template_name = "maps/map_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = TourismCategory.objects.all()
        return context


def tourism_places_api(request):
    """API endpoint untuk data tempat pariwisata dalam format GeoJSON"""
    category_id = request.GET.get("category")

    places = TourismPlace.objects.filter(is_active=True)
    if category_id:
        places = places.filter(category_id=category_id)

    features = []
    for place in places:
        # Log visitor untuk analytics
        VisitorLog.objects.create(
            place=place,
            visitor_ip=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            session_key=request.session.session_key or "",
        )

        feature = {
            "type": "Feature",
            "properties": {
                "id": place.id,
                "name": place.name,
                "description": place.description,
                "category": place.category.name,
                "category_color": place.category.color,
                "category_icon": place.category.icon,
                "address": place.address,
                "phone": place.phone,
                "website": place.website,
                "email": place.email,
                "opening_hours": place.opening_hours,
                "ticket_price": str(place.ticket_price),
                "rating": place.rating,
                "image_url": place.image.url if place.image else None,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude],
            },
        }
        features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}

    return JsonResponse(geojson)


def find_nearby_places(request):
    """API untuk mencari tempat terdekat berdasarkan koordinat"""
    try:
        lat = float(request.GET.get("lat"))
        lng = float(request.GET.get("lng"))
        radius = float(request.GET.get("radius", 5))  # radius dalam km

        user_location = Point(lng, lat, srid=4326)

        # Import yang diperlukan di atas file
        from django.contrib.gis.db.models.functions import Distance as DistanceFunc

        nearby_places = (
            TourismPlace.objects.filter(
                location__distance_lte=(user_location, Distance(km=radius)),
                is_active=True,
            )
            .annotate(distance=DistanceFunc("location", user_location))
            .order_by("distance")
        )

        results = []
        for place in nearby_places:({
                    "id": place.id,
                    "name": place.name,
                    "distance_km": round(place.distance.km, 2),
                    "category": place.category.name,
                    "latitude": place.latitude,
                    "longitude": place.longitude,
                    "rating": place.rating,
                })

        return JsonResponse({"places": results})

    except (ValueError, TypeError) as e:
        return JsonResponse({"error": "Invalid parameters"}, status=400)


def get_client_ip(request):
    """Utility function untuk mendapatkan IP client"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
