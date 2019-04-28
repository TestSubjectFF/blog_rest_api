from rest_framework import serializers
from . import models


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'post', 'username', 'text', 'created')
        model = models.Comment


class PostSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'title', 'text', 'created', 'comment_set')
        model = models.Post
