# tourism_app/forms.py
from django import forms
from .models import DataImport, TourismPlace, TourismCategory

class FileImportForm(forms.ModelForm):
    class Meta:
        model = DataImport
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.csv,.xlsx,.xls',
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data['file']
        
        # Validasi ukuran file (max 10MB)
        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Ukuran file terlalu besar. Maksimal 10MB.")
        
        # Validasi ekstensi file
        allowed_extensions = ['.csv', '.xlsx', '.xls']
        file_extension = file.name.lower()[-4:] if len(file.name) > 4 else ''
        
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Format file tidak didukung. Gunakan CSV atau Excel.")
        
        return file

class TourismPlaceForm(forms.ModelForm):
    latitude = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '-6.5971'})
    )
    longitude = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': '106.8067'})
    )

    # TAMBAHKAN: Override widget untuk ticket_price agar bisa format initial
    ticket_price = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'inputmode': 'numeric',
            'autocomplete': 'off',
            'placeholder': '50000'
        })
    )

    phone = forms.RegexField(
        regex=r'^[0-9]+$',  # Hanya angka dari awal hingga akhir
        max_length=15,
        required=False,
        label='Nomor Telepon',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '081234567890'}),
        error_messages={'invalid': 'Masukkan hanya angka (tanpa spasi atau tanda lain).'}
    )

    class Meta:
        model = TourismPlace
        """ fields = [
            'name', 'description', 'category', 'address', 
            'phone', 'website', 'email', 'opening_hours', 
            'ticket_price', 'image'
        ] """
        fields = ['name', 'description', 'category', 'latitude', 'longitude', 'address', 'phone', 'website', 'email', 'image', 'rating', 'opening_hours', 'ticket_price']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'opening_hours': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Jika ada instance (mode edit), extract lat/lng dari location Point
        if self.instance and self.instance.pk and self.instance.location:
            # Point.y = latitude, Point.x = longitude
            self.fields['latitude'].initial = self.instance.location.y
            self.fields['longitude'].initial = self.instance.location.x

        if self.instance and self.instance.pk and self.instance.ticket_price:
            # Format ke ribuan dengan titik (misal: 50000 -> 50.000)
            price_value = int(self.instance.ticket_price)
            formatted_price = f"{price_value:,}".replace(',', '.')
            self.fields['ticket_price'].initial = formatted_price

    def clean_ticket_price(self):
        """Bersihkan format Rupiah sebelum validasi"""
        value = self.cleaned_data.get('ticket_price')
        if value:
            # Jika masih string dengan format, bersihkan
            if isinstance(value, str):
                clean_value = value.replace('.', '').replace(',', '')
                return clean_value
        return value
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set location dari latitude dan longitude
        from django.contrib.gis.geos import Point
        lat = self.cleaned_data['latitude']
        lng = self.cleaned_data['longitude']

        if lat is not None and lng is not None:
            instance.location = Point(lng, lat, srid=4326)
        
        if commit:
            instance.save()
        return instance
