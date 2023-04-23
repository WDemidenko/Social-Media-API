from django.urls import path, include
from rest_framework import routers

from social_media.views import PostViewSet, CommentCreateView

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:pk>/comment/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
]

app_name = "social_media"
