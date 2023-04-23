from rest_framework import serializers

from social_media.models import Post, Comment, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("user", "content")


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


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
        )


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=True
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


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
            "comments",
        )
