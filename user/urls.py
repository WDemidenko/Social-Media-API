from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import (
    CreateUserView,
    ManageUserView,
    UserViewSet,
    follow,
    unfollow, FollowersListView, FollowingListView, UserPostsView,
)

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("me/posts/", UserPostsView.as_view(), name="me-posts"),
    path(
        "follow/<int:user_id>/",
        follow,
        name="follow",
    ),
    path(
        "unfollow/<int:user_id>/",
        unfollow,
        name="unfollow",
    ),
    path("following/", FollowingListView.as_view(), name='following-list'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path("", include(router.urls)),
]

app_name = "user"
