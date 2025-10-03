# tourism_app/models.py
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.utils import timezone

import uuid

class TourismCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    icon = models.CharField(max_length=50, default='map-pin', verbose_name="Icon")
    color = models.CharField(max_length=7, default='#007bff', verbose_name="Warna")
    
    class Meta:
        verbose_name = "Kategori Pariwisata"
        verbose_name_plural = "Kategori Pariwisata"

    # Tambahkan field untuk warna badge
    BADGE_COLOR_CHOICES = [
        ('primary', 'Biru'),
        ('secondary', 'Abu-abu'),
        ('success', 'Hijau'),
        ('danger', 'Merah'),
        ('warning', 'Kuning'),
        ('info', 'Cyan'),
        ('light', 'Putih'),
        ('dark', 'Hitam'),
        ('purple', 'Ungu'),
        ('orange', 'Oyen'),
        ('pink', 'Pink'),
        ('nature', 'Nature'),
    ]
    badge_color = models.CharField(
        max_length=20, 
        choices=BADGE_COLOR_CHOICES, 
        default='secondary'
    )
    
    def __str__(self):
        return self.name

class TourismPlace(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nama Tempat")
    description = models.TextField(verbose_name="Deskripsi")
    category = models.ForeignKey(TourismCategory, on_delete=models.CASCADE, verbose_name="Kategori")
    location = models.PointField(verbose_name="Lokasi Geografis")  # PostGIS Point field
    address = models.TextField(verbose_name="Alamat")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telepon")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    opening_hours = models.TextField(blank=True, verbose_name="Jam Operasional")
    ticket_price = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=0, default=0, verbose_name="Harga Tiket")
    rating = models.FloatField(default=0, verbose_name="Rating")
    image = models.ImageField(upload_to='places/', blank=True, null=True, verbose_name="Gambar")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Tempat Pariwisata"
        verbose_name_plural = "Tempat Pariwisata"
    
    def __str__(self):
        return self.name
    
    @property
    def latitude(self):
        return self.location.y if self.location else None
    
    @property
    def longitude(self):
        return self.location.x if self.location else None

class VisitorLog(models.Model):
    place = models.ForeignKey(TourismPlace, on_delete=models.CASCADE)
    visitor_ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True)
    
    class Meta:
        verbose_name = "Log Pengunjung"
        verbose_name_plural = "Log Pengunjung"

class DataImport(models.Model):
    IMPORT_TYPE_CHOICES = [
        ('csv', 'CSV File'),
        ('xlsx', 'Excel File (XLSX)'),
        ('xls', 'Excel File (XLS)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='imports/', verbose_name="File Import")
    file_type = models.CharField(max_length=10, choices=IMPORT_TYPE_CHOICES, verbose_name="Tipe File")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    total_rows = models.IntegerField(default=0, verbose_name="Total Baris")
    processed_rows = models.IntegerField(default=0, verbose_name="Baris Berhasil")
    error_rows = models.IntegerField(default=0, verbose_name="Baris Error")
    error_log = models.TextField(blank=True, verbose_name="Log Error")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Import Data"
        verbose_name_plural = "Import Data"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Import {self.file.name} - {self.status}"