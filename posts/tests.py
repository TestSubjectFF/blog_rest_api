from django.contrib.auth import get_user_model
from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from .models import Post, Comment


class PostTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('posts.urls')),
    ]
    superuser_username = 'admin'
    superuser_password = 'password'

    regular_username = "user"
    regular_password = "password"

    number_of_posts = 10
    number_of_comments = 3

    def _create_post_api(self, data):
        url = reverse('post-list')
        return self.client.post(url, data=data, format='json')

    def setUp(self):
        # create superuser and regular user
        User = get_user_model()
        User.objects.create_superuser(self.superuser_username,
                                      'admin@example.com',
                                      self.superuser_password)
        User.objects.create_user(self.regular_username,
                                 'user@example.com',
                                 self.regular_password)
        # create_some_posts
        for i in range(self.number_of_posts):
            post = Post.objects.create(title=f'Post {i}',
                                text=f'Post {i} text')
            for j in range(self.number_of_comments):
                Comment.objects.create(post=post,
                                       username=f'Anonymous',
                                       text=f'Post {i} text')

    def test_create_post_by_unauthorised_user(self):
        """Unauthorised user can't create new post instance"""
        posts_count_before = Post.objects.all().count()

        data = {'title': 'First post.', 'text': 'Post content.'}
        response = self._create_post_api(data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.all().count(), posts_count_before)

    def test_create_post_by_regular_user(self):
        """Regular user can't create new post instance"""
        posts_count_before = Post.objects.all().count()

        data = {'title': 'First post.', 'text': 'Post content.'}
        self.client.login(username=self.regular_username,
                          password=self.regular_password)
        response = self._create_post_api(data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.all().count(), posts_count_before)

    def test_create_post_by_superuser(self):
        """Superuser can create new post instance."""
        data = {'title': 'First post.', 'text': 'Post content.'}
        self.client.login(username=self.superuser_username,
                          password=self.superuser_password)
        response = self._create_post_api(data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # post exists in DB
        self.assertEqual(Post.objects.filter(id=response.data['id']).count(), 1)

    def test_posts_list(self):
        """Anyone can get list of posts."""
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # number of posts returned by api is the same as in DB
        self.assertEqual(len(response.data), self.number_of_posts)
        # number of comments return by api is the same as in DB
        comments = response.data[0]['comment_set']
        self.assertEqual(len(comments), self.number_of_comments)

    def test_posts_read(self):
        """Anyone can get post instance."""
        post = Post.objects.all()[0]
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post.title)

    def test_nonexistent_post_read(self):
        """Return 404 when trying tot read post that doesn't exist"""
        post_id = 9999
        self.assertRaises(Post.DoesNotExist, Post.objects.get, pk=post_id)

        url = reverse('post-detail', kwargs={'pk': post_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_delete_unauthorised_user(self):
        """Unauthorised user can't delete post."""
        post = Post.objects.all()[0]
        url = reverse('post-detail', kwargs={'pk': post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.filter(pk=post.pk).count(), 1)

    def test_post_delete_regular_user(self):
        """Regular user can't delete post."""
        post = Post.objects.all()[0]
        url = reverse('post-detail', kwargs={'pk': post.pk})
        self.client.login(username=self.regular_username,
                          password=self.regular_password)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.filter(pk=post.pk).count(), 1)

    def test_post_delete_superuser(self):
        """Superuser can delete post."""
        post = Post.objects.all()[0]
        url = reverse('post-detail', kwargs={'pk': post.pk})
        self.client.login(username=self.superuser_username,
                          password=self.superuser_password)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Post.DoesNotExist, Post.objects.get, pk=post.pk)

    def test_nonexistent_post_delete(self):
        """Return 404 when trying to delete post that doesn't exist"""
        post_id = 9999
        self.assertRaises(Post.DoesNotExist, Post.objects.get, pk=post_id)

        url = reverse('post-detail', kwargs={'pk': post_id})
        self.client.login(username=self.superuser_username,
                          password=self.superuser_password)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)







