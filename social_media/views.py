from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_media.models import Post, Comment
from social_media.serializers import (
    PostCreateSerializer,
    PostListSerializer,
    CommentSerializer,
    PostDetailSerializer,
    CommentListSerializer,
)


def ids_from_string(string_ids: str) -> list:
    return [int(str_id) for str_id in string_ids.split(",")]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        hashtags = self.request.query_params.get("hashtags")
        queryset = self.queryset

        if hashtags:
            hashtags_ids = ids_from_string(hashtags)
            queryset = queryset.filter(hashtags__id__in=hashtags_ids)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return self.serializer_class

    @action(detail=True, methods=["get"])
    def like(self, request, pk=None):
        """
        Add the current user to the 'liked_by' ManyToManyField for the post.
        """
        post = self.get_object()
        post.liked_by.add(request.user)
        return Response({"detail": "Post liked successfully."})

    @action(detail=True, methods=["get"])
    def unlike(self, request, pk=None):
        """
        Remove the current user from the 'liked_by' ManyToManyField for the post.
        """
        post = self.get_object()
        post.liked_by.remove(request.user)
        return Response({"detail": "Post unliked successfully."})


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, post_id=post_id)
