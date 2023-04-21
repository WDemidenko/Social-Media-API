import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Hashtag(models.Model):
    name = models.CharField(max_length=65, unique=True)

    def __str__(self) -> str:
        return self.name


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/posts/",
        f"{slugify(instance.title)}-{uuid.uuid4()}{extension}",
    )


class Post(models.Model):
    title = models.CharField(max_length=65, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="posts")
    image = models.ImageField(
        blank=True, null=True, upload_to=post_image_file_path
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()

    def __str__(self) -> str:
        return self.content
