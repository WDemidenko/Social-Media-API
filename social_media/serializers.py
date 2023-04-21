from rest_framework import serializers

from social_media.models import Post, Comment, Hashtag


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "hashtags",
            "image",
            "liked_by",
        )


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        many=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "user",
            "hashtags",
            "image",
            "liked_by",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content")
