from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime
from .models import Post, Comment, Like, User
import json

class TestUserViewSet(APITestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='user2@example.com',
            password='testpass123'
        )
        
        # Setup client and authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        # URLs
        self.users_url = reverse('user-list')
        
    def test_get_all_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # admin_user, user1, user2
    
    def test_get_user_detail(self):
        user_detail_url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.get(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')
    
    def test_create_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(self.users_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        
    def test_update_user(self):
        user_detail_url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {
            'username': 'updateduser',
            'password': 'testpass123'
        }
        response = self.client.put(user_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')
        
    def test_delete_user(self):
        user_detail_url = reverse('user-detail', kwargs={'pk': self.user2.id})
        response = self.client.delete(user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)


class TestPostViewSet(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        # Create test posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            content='This is test content 1',
            author=self.user
        )
        
        self.post2 = Post.objects.create(
            title='Test Post 2',
            content='This is test content 2',
            author=self.user
        )
        
        # Setup client and authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs
        self.posts_url = reverse('post-list')
        
    def test_get_all_posts(self):
        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_post_detail(self):
        post_detail_url = reverse('post-detail', kwargs={'pk': self.post1.id})
        response = self.client.get(post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post 1')
        
    def test_create_post(self):
        data = {
            'title': 'New Post',
            'content': 'This is a new post content',
            'author': self.user.id
        }
        response = self.client.post(self.posts_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        
    def test_update_post(self):
        post_detail_url = reverse('post-detail', kwargs={'pk': self.post1.id})
        data = {
            'title': 'Updated Post',
            'content': 'This is updated content',
            'author': self.user.id
        }
        response = self.client.put(post_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Post')
        
    def test_delete_post(self):
        post_detail_url = reverse('post-detail', kwargs={'pk': self.post2.id})
        response = self.client.delete(post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)
        
    def test_post_stats(self):
        stats_url = reverse('post-stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_posts'], 2)


class TestCommentViewSet(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is test content',
            author=self.user
        )
        
        # Create test comments
        self.comment1 = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment 1'
        )
        
        self.comment2 = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment 2'
        )
        
        # Setup client and authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # URLs
        self.comments_url = reverse('comment-list')
        
    def test_get_all_comments(self):
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_comment_detail(self):
        comment_detail_url = reverse('comment-detail', kwargs={'pk': self.comment1.id})
        response = self.client.get(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test comment 1')
        
    def test_create_comment(self):
        data = {
            'post': self.post.id,
            'author': self.user.id,
            'content': 'New comment'
        }
        response = self.client.post(self.comments_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        
    def test_update_comment(self):
        comment_detail_url = reverse('comment-detail', kwargs={'pk': self.comment1.id})
        data = {
            'post': self.post.id,
            'author': self.user.id,
            'content': 'Updated comment'
        }
        response = self.client.put(comment_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.content, 'Updated comment')
        
    def test_delete_comment(self):
        comment_detail_url = reverse('comment-detail', kwargs={'pk': self.comment2.id})
        response = self.client.delete(comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 1)
        
    def test_comments_by_post(self):
        by_post_url = reverse('comment-by-post', kwargs={'post_id': self.post.id})
        response = self.client.get(by_post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TestLikeViewSet(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            content='This is test content',
            author=self.user1
        )
        
        # Create test comment
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='Test comment'
        )
        
        # Create test likes
        self.post_like = Like.objects.create(
            user=self.user1,
            post=self.post,
            comment=None
        )
        
        self.comment_like = Like.objects.create(
            user=self.user2,
            post=None,
            comment=self.comment
        )
        
        # Setup client and authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        
        # URLs
        self.likes_url = reverse('like-list')
        
    def test_get_all_likes(self):
        response = self.client.get(self.likes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_like_detail(self):
        like_detail_url = reverse('like-detail', kwargs={'pk': self.post_like.id})
        response = self.client.get(like_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['post'], self.post.id)
        
    def test_create_like(self):
        data = {
            'user': self.user2.id,
            'post': self.post.id
        }
        response = self.client.post(self.likes_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 3)
        
    def test_delete_like(self):
        like_detail_url = reverse('like-detail', kwargs={'pk': self.post_like.id})
        response = self.client.delete(like_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 1)
        
    def test_likes_by_post(self):
        by_post_url = reverse('like-by-post', kwargs={'post_id': self.post.id})
        response = self.client.get(by_post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes_count'], 1)


class TestAuthEndpoints(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        # Setup client
        self.client = APIClient()
        
        # URLs
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        
    def test_register(self):
        data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect after successful registration
        self.assertEqual(User.objects.count(), 2)
        
    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect after successful login
        
    def test_logout(self):
        # First login
        self.client.login(username='testuser', password='testpassword')
        
        # Then logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect after successful logout

from django.test import TestCase

# Create your tests here.
