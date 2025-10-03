# analytics_app/models.py
from django.db import models
from django.contrib.auth.models import User
from tourism_app.models import TourismPlace, TourismCategory
from django.utils import timezone
from django.db.models import Count
import calendar

class AnalyticsData(models.Model):
    place = models.ForeignKey(TourismPlace, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['place', 'date']
        verbose_name = "Data Analitik"
        verbose_name_plural = "Data Analitik"

class PopularityTrend(models.Model):
    category = models.ForeignKey(TourismCategory, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_visits = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['category', 'month', 'year']
