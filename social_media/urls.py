from django.urls import path, include
from rest_framework import routers

from social_media.views import PostViewSet, CommentSetView, HashtagViewSet, CommentCreateView

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("comments", CommentSetView)

urlpatterns = [
    path("", include(router.urls)),
    path("posts/<int:pk>/comment/create/", CommentCreateView.as_view(), name="comment_create"),
]

app_name = "social_media"
