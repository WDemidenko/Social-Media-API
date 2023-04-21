from django.shortcuts import render
from rest_framework import viewsets, generics

from social_media.models import Post
from social_media.serializers import PostCreateSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        return self.serializer_class
