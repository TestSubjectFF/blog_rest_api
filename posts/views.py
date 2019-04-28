from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given post.

    list:
    Return a list of all the existing posts.

    create:
    Create a new post instance(only superuser).

    update:
    Update existing post instance(only superuser).

    partial_update:
    Partially update existing post instance(only superuser).

    delete:
    Delete existing post instance(only superuser).
    """
    queryset = Post.objects.all().prefetch_related('comment_set')
    serializer_class = PostSerializer

    def get_permissions(self):
        """
        Any user can get collection of posts or a single post.
        Only superuser can modify or delete posts.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given comment.

    list:
    Return a list of all the existing comments(only superuser).

    create:
    Create a new comment instance.


    update:
    Update existing comment instance(only superuser).

    partial_update:
    Partially update existing comment instance(only superuser).

    delete:
    Delete existing comment instance(only superuser).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Any user can get a single comment.
        Only superuser can get collection of comment.
        Only superuser can modify or delete comment.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
