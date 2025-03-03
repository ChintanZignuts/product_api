from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

class ProductApiTestCase(APITestCase):
    # Create a product object before running each test
    def setUp(self):
        self.product1=Product.objects.create(name='Product 1', description='Product 1 description', price=100, stock=10)
        self.product2=Product.objects.create(name='Product 2', description='Product 2 description', price=200, stock=20)

        self.product_list_url=reverse('product-list-create')
        self.product_detail_url=lambda pk: reverse('product-detail', kwargs={'pk':pk})

    #list products
    def test_product_list(self):
        response=self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    #retrieve product
    def test_product_detail(self):
        response=self.client.get(self.product_detail_url(self.product1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Product 1')
    
    #create product
    def test_product_create(self):
        data={'name':'Product 3', 'description':'Product 3 description', 'price':300, 'stock':30}
        response=self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    #create product with invalid data
    def test_create_product_negative_price(self):
        data = {"name": "Invalid Product", "description": "Should fail", "price": -10.00}
        response = self.client.post(self.product_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)
        
    #update product
    def test_product_update(self):
        data={'name':'Product 1 updated', 'description':'Product 1 description updated', 'price':150, 'stock':15}
        response=self.client.put(self.product_detail_url(self.product1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Product 1 updated')

    #partial update product
    def test_partial_update_product(self):
        data = {"price": 2500.00}
        response = self.client.patch(self.product_detail_url(self.product1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.price, 2500.00)

    #delete product
    def test_delete_product(self):
        response = self.client.delete(self.product_detail_url(self.product1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())