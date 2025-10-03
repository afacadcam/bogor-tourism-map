# analytics_app/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Sum, Q
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from tourism_app.models import TourismPlace, TourismCategory, VisitorLog
from .models import AnalyticsData
import calendar
import pandas as pd
import io

class DashboardView:
    def analytics_dashboard(self, request):
        """Main analytics dashboard"""
        context = {
            'total_places': TourismPlace.objects.filter(is_active=True).count(),
            'total_categories': TourismCategory.objects.count(),
            'total_visits_today': VisitorLog.objects.filter(
                visit_date__date=timezone.now().date()
            ).count(),
            'total_visits_month': VisitorLog.objects.filter(
                visit_date__month=timezone.now().month,
                visit_date__year=timezone.now().year
            ).count(),
        }
        return render(request, 'analytics/dashboard.html', context)

def places_by_category_api(request):
    """API untuk chart distribusi tempat per kategori"""
    data = TourismCategory.objects.annotate(
        place_count=Count('tourismplace', filter=models.Q(tourismplace__is_active=True))
    ).values('name', 'place_count', 'color')
    
    chart_data = {
        'labels': [item['name'] for item in data],
        'datasets': [{
            'label': 'Jumlah Tempat',
            'data': [item['place_count'] for item in data],
            'backgroundColor': [item['color'] for item in data],
            'borderColor': [item['color'] for item in data],
            'borderWidth': 1
        }]
    }
    
    return JsonResponse(chart_data)

def monthly_visits_api(request):
    """API untuk chart kunjungan bulanan"""
    # Get data for last 12 months
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    
    monthly_data = VisitorLog.objects.filter(
        visit_date__gte=start_date,
        visit_date__lte=end_date
    ).extra(
        select={'month': 'EXTRACT(month FROM visit_date)', 
               'year': 'EXTRACT(year FROM visit_date)'}
    ).values('month', 'year').annotate(
        total_visits=Count('id')
    ).order_by('year', 'month')
    
    # Prepare labels and data
    labels = []
    visits_data = []
    
    for item in monthly_data:
        month_name = calendar.month_abbr[int(item['month'])]
        year = int(item['year'])
        labels.append(f"{month_name} {year}")
        visits_data.append(item['total_visits'])
    
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Kunjungan',
            'data': visits_data,
            'borderColor': '#007bff',
            'backgroundColor': 'rgba(0, 123, 255, 0.1)',
            'fill': True,
            'tension': 0.4
        }]
    }
    
    return JsonResponse(chart_data)

def top_places_api(request):
    """API untuk chart tempat paling populer"""
    top_places = TourismPlace.objects.filter(is_active=True).annotate(
        visit_count=Count('visitorlog')
    ).order_by('-visit_count')[:10]
    
    chart_data = {
        'labels': [place.name for place in top_places],
        'datasets': [{
            'label': 'Jumlah Kunjungan',
            'data': [place.visit_count for place in top_places],
            'backgroundColor': [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
            ],
            'borderWidth': 1
        }]
    }
    
    return JsonResponse(chart_data)

def rating_distribution_api(request):
    """API untuk chart distribusi rating"""
    rating_ranges = [
        (0, 1, '0-1'),
        (1, 2, '1-2'), 
        (2, 3, '2-3'),
        (3, 4, '3-4'),
        (4, 5, '4-5')
    ]
    
    rating_data = []
    labels = []
    
    for min_rating, max_rating, label in rating_ranges:
        count = TourismPlace.objects.filter(
            rating__gte=min_rating,
            rating__lt=max_rating,
            is_active=True
        ).count()
        rating_data.append(count)
        labels.append(f"{label} ⭐")
    
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Jumlah Tempat',
            'data': rating_data,
            'backgroundColor': [
                '#ff4757', '#ff7675', '#fdcb6e', '#6c5ce7', '#00b894'
            ],
            'borderWidth': 1
        }]
    }
    
    return JsonResponse(chart_data)

def visitor_analytics_api(request):
    """API untuk analytics pengunjung per hari"""
    # Last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    daily_visitors = VisitorLog.objects.filter(
        visit_date__date__gte=start_date,
        visit_date__date__lte=end_date
    ).extra(
        select={'date': 'DATE(visit_date)'}
    ).values('date').annotate(
        total_visits=Count('id'),
        unique_visitors=Count('visitor_ip', distinct=True)
    ).order_by('date')
    
    labels = []
    visits_data = []
    unique_data = []
    
    for item in daily_visitors:
        labels.append(item['date'].strftime('%d %b'))
        visits_data.append(item['total_visits'])
        unique_data.append(item['unique_visitors'])
    
    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Total Kunjungan',
                'data': visits_data,
                'borderColor': '#007bff',
                'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                'fill': False
            },
            {
                'label': 'Pengunjung Unik',
                'data': unique_data,
                'borderColor': '#28a745',
                'backgroundColor': 'rgba(40, 167, 69, 0.1)',
                'fill': False
            }
        ]
    }
    
    return JsonResponse(chart_data)

# Function-based views for URLs
def analytics_dashboard(request):
    return DashboardView().analytics_dashboard(request)


# Tambahkan fungsi ini di analytics_app/views.py
def export_analytics_excel(request):
    """Export analytics data to Excel file"""
    
    # Buat workbook Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    
    # Sheet 1: Places by Category
    places_by_category = TourismCategory.objects.annotate(
        place_count=Count('tourismplace', filter=Q(tourismplace__is_active=True))
    ).values('name', 'place_count')
    
    df_categories = pd.DataFrame(list(places_by_category))
    if not df_categories.empty:
        df_categories.to_excel(writer, sheet_name='Places by Category', index=False)
    
    # Sheet 2: Top Places
    top_places = TourismPlace.objects.filter(is_active=True).annotate(
        visit_count=Count('visitorlog')
    ).order_by('-visit_count')[:10].values('name', 'visit_count', 'rating', 'category__name')
    
    df_top_places = pd.DataFrame(list(top_places))
    if not df_top_places.empty:
        df_top_places.columns = ['Name', 'Visit Count', 'Rating', 'Category']
        df_top_places.to_excel(writer, sheet_name='Top Places', index=False)
    
    # Sheet 3: Monthly Visits
    from datetime import datetime, timedelta
    end_date = timezone.now()
    start_date = end_date - timedelta(days=365)
    
    monthly_visits = VisitorLog.objects.filter(
        visit_date__gte=start_date,
        visit_date__lte=end_date
    ).extra(
        select={'month': 'EXTRACT(month FROM visit_date)', 
               'year': 'EXTRACT(year FROM visit_date)'}
    ).values('month', 'year').annotate(
        total_visits=Count('id')
    ).order_by('year', 'month')
    
    df_monthly = pd.DataFrame(list(monthly_visits))
    if not df_monthly.empty:
        df_monthly.to_excel(writer, sheet_name='Monthly Visits', index=False)
    
    # Save workbook
    writer.close()
    output.seek(0)
    
    # Create response
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="analytics_data.xlsx"'
    
    return response