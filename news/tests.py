"""
Unit tests for the news application REST API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Article, Publisher, Newsletter

User = get_user_model()


class ArticleAPITestCase(APITestCase):
    """Test cases for the Article API."""
    
    def setUp(self):
        """Set up test data."""
        # Create publishers
        self.publisher1 = Publisher.objects.create(
            name='Tech News',
            description='Technology news publisher'
        )
        self.publisher2 = Publisher.objects.create(
            name='Sports Daily',
            description='Sports news publisher'
        )
        
        # Create users
        self.reader = User.objects.create_user(
            username='reader1',
            email='reader@test.com',
            password='testpass123',
            role='reader'
        )
        
        self.journalist1 = User.objects.create_user(
            username='journalist1',
            email='journalist1@test.com',
            password='testpass123',
            role='journalist'
        )
        self.journalist1.affiliated_publishers.add(self.publisher1)
        
        self.journalist2 = User.objects.create_user(
            username='journalist2',
            email='journalist2@test.com',
            password='testpass123',
            role='journalist'
        )
        self.journalist2.affiliated_publishers.add(self.publisher2)
        
        self.editor = User.objects.create_user(
            username='editor1',
            email='editor@test.com',
            password='testpass123',
            role='editor'
        )
        
        # Create articles
        self.article1 = Article.objects.create(
            title='Tech Article 1',
            content='Content about technology',
            summary='Tech summary',
            author=self.journalist1,
            publisher=self.publisher1,
            is_approved=True
        )
        
        self.article2 = Article.objects.create(
            title='Sports Article 1',
            content='Content about sports',
            summary='Sports summary',
            author=self.journalist2,
            publisher=self.publisher2,
            is_approved=True
        )
        
        self.article3 = Article.objects.create(
            title='Independent Article',
            content='Independent content',
            summary='Independent summary',
            author=self.journalist1,
            publisher=None,
            is_approved=True
        )
        
        # Create unapproved article
        self.article4 = Article.objects.create(
            title='Pending Article',
            content='Pending content',
            author=self.journalist1,
            publisher=self.publisher1,
            is_approved=False
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_api_requires_authentication(self):
        """Test that API requires authentication."""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_reader_with_no_subscriptions_gets_empty_list(self):
        """Test that reader with no subscriptions gets empty article list."""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_reader_gets_articles_from_subscribed_publisher(self):
        """Test that reader gets articles from subscribed publishers."""
        # Subscribe reader to publisher1
        self.reader.subscribed_publishers.add(self.publisher1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Tech Article 1')
    
    def test_reader_gets_articles_from_subscribed_journalist(self):
        """Test that reader gets articles from subscribed journalists."""
        # Subscribe reader to journalist1
        self.reader.subscribed_journalists.add(self.journalist1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should get both publisher article and independent article from journalist1
        self.assertEqual(len(response.data['results']), 2)
        titles = [article['title'] for article in response.data['results']]
        self.assertIn('Tech Article 1', titles)
        self.assertIn('Independent Article', titles)
    
    def test_reader_gets_articles_from_multiple_subscriptions(self):
        """Test that reader gets articles from all subscriptions."""
        # Subscribe to both publishers and journalist2
        self.reader.subscribed_publishers.add(self.publisher1, self.publisher2)
        self.reader.subscribed_journalists.add(self.journalist2)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should get articles from both publishers (no duplicates)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_api_only_returns_approved_articles(self):
        """Test that API only returns approved articles."""
        # Subscribe to publisher1 which has both approved and pending articles
        self.reader.subscribed_publishers.add(self.publisher1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only get approved article
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['is_approved'], True)
    
    def test_filter_by_publisher(self):
        """Test filtering articles by specific publisher."""
        self.reader.subscribed_publishers.add(self.publisher1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(
            f'/api/articles/by_publisher/?publisher_id={self.publisher1.id}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publisher']['name'], 'Tech News')
    
    def test_filter_by_journalist(self):
        """Test filtering articles by specific journalist."""
        self.reader.subscribed_journalists.add(self.journalist1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(
            f'/api/articles/by_journalist/?journalist_id={self.journalist1.id}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_cannot_filter_by_unsubscribed_publisher(self):
        """Test that filtering by unsubscribed publisher returns error."""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(
            f'/api/articles/by_publisher/?publisher_id={self.publisher1.id}'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_subscriptions_endpoint(self):
        """Test the subscriptions info endpoint."""
        self.reader.subscribed_publishers.add(self.publisher1)
        self.reader.subscribed_journalists.add(self.journalist1)
        
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/articles/subscriptions/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['subscribed_publishers']), 1)
        self.assertEqual(len(response.data['subscribed_journalists']), 1)


class PublisherAPITestCase(APITestCase):
    """Test cases for the Publisher API."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='reader'
        )
        
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='Test description'
        )
        
        self.client = APIClient()
    
    def test_get_publishers_list(self):
        """Test retrieving list of publishers."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/publishers/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Publisher')


class JournalistAPITestCase(APITestCase):
    """Test cases for the Journalist API."""
    
    def setUp(self):
        """Set up test data."""
        self.reader = User.objects.create_user(
            username='reader',
            email='reader@test.com',
            password='testpass123',
            role='reader'
        )
        
        self.journalist = User.objects.create_user(
            username='journalist',
            email='journalist@test.com',
            password='testpass123',
            role='journalist',
            first_name='John',
            last_name='Doe'
        )
        
        self.client = APIClient()
    
    def test_get_journalists_list(self):
        """Test retrieving list of journalists."""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get('/api/journalists/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['username'], 'journalist')
