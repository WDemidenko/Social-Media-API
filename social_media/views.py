from django.shortcuts import render
from rest_framework import viewsets, generics

from social_media.models import Post
from social_media.serializers import PostCreateSerializer, PostListSerializer


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
            queryset = queryset.filter(
                hashtags__id__in=hashtags_ids
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        return self.serializer_class
