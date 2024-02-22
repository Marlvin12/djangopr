# test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Data
from unittest.mock import patch
from io import BytesIO
import pandas as pd

class HelloViewTests(TestCase):
    def setUp(self):
        # Set up the test client and any other test variables
        self.client = Client()
        self.url = reverse('hello')  

    def test_hello_view_with_get_request(self):
        # Test handling of GET requests
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/index.html')

    def test_hello_view_with_post_request(self):
        # Prepare a mock CSV file for upload
        data = {'property_name': 'Test House', 'property_price': 200000, 'property_rent': 2000, 'emi': 500, 'tax': 100, 'other_exp': 50}
        df = pd.DataFrame([data])
        mock_csv_file = BytesIO()
        df.to_csv(mock_csv_file, index=False)
        mock_csv_file.seek(0)
        mock_csv_file.name = 'test_upload.csv'
        
        with patch('pandas.read_csv') as mock_read_csv:
            mock_read_csv.return_value = df
            

            Data.objects.create(name="Old Property", price=100000, rent=1000, emi=400, tax=80, exp=20, expenses_monthly=500, income_monthly=500)
            self.assertEqual(Data.objects.count(), 1) 
            
            response = self.client.post(self.url, {'file': mock_csv_file}, format='multipart')
            
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'myapp/index.html')
            
            self.assertEqual(Data.objects.count(), 1)
            new_data = Data.objects.first()
            self.assertNotEqual(new_data.name, "Old Property")  
            
