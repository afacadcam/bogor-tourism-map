# tourism_app/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.urls import reverse
from .models import TourismCategory, TourismPlace
import json

class TourismModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.category = TourismCategory.objects.create(
            name='Test Category',
            description='Test Description',
            icon='test-icon',
            color='#007bff'
        )
        
        self.place = TourismPlace.objects.create(
            name='Test Place',
            description='Test place description',
            category=self.category,
            location=Point(106.7997, -6.5972, srid=4326),
            address='Test Address',
            created_by=self.user
        )
    
    def test_tourism_place_creation(self):
        self.assertEqual(self.place.name, 'Test Place')
        self.assertEqual(self.place.category, self.category)
        self.assertEqual(self.place.latitude, -6.5972)
        self.assertEqual(self.place.longitude, 106.7997)
    
    def test_tourism_place_str(self):
        self.assertEqual(str(self.place), 'Test Place')

class APIEndpointsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.category = TourismCategory.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.place = TourismPlace.objects.create(
            name='Test Place',
            description='Test Description',
            category=self.category,
            location=Point(106.7997, -6.5972, srid=4326),
            address='Test Address',
            created_by=self.user
        )
    
    def test_tourism_places_api(self):
        response = self.client.get(reverse('tourism_places_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'FeatureCollection')
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['properties']['name'], 'Test Place')
    
    def test_find_nearby_places_api(self):
        response = self.client.get(
            reverse('find_nearby_places'),
            {'lat': -6.5972, 'lng': 106.7997, 'radius': 5}
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('places', data)
        self.assertEqual(len(data['places']), 1)

class FileImportTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_import_page_access(self):
        response = self.client.get(reverse('file_import'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Import Data Tempat Pariwisata')

# Run tests
# python manage.py test
