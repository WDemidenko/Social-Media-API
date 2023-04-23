from django.shortcuts import render
from rest_framework import viewsets, generics, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_media.models import Post, Comment, Hashtag
from social_media.serializers import (
    PostListSerializer,
    CommentSerializer,
    PostDetailSerializer,
    CommentListSerializer,
    HashtagSerializer,
    PostSerializer,
)
from user.permissions import IsStaffOrReadOnly


def ids_from_string(string_ids: str) -> list:
    return [int(str_id) for str_id in string_ids.split(",")]


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        hashtags = self.request.query_params.get("hashtags")
        queryset = self.queryset.prefetch_related("hashtags", "liked_by")

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You can only delete posts that you have created."
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You can only update posts that you have created."
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You can only partially update posts that you have created."
            )

        return super().partial_update(request, *args, **kwargs)


class CommentSetView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, post_id=post_id)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, post_id=post_id)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [IsStaffOrReadOnly]
