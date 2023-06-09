from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from social_media.models import Post
from social_media.serializers import PostListSerializer
from user.serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return (
            User.objects.filter(id=self.request.user.id)
            .prefetch_related("following")
            .first()
        )


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        email = self.request.query_params.get("email")
        queryset = self.queryset.prefetch_related("following")

        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "email",
                type={"type": "string"},
                description=(
                    "Filter by containing email text, " "example: ?email=abc"
                ),
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    """Add user_to_follow to current user's following"""
    user_to_follow = get_object_or_404(User, id=user_id)

    user = request.user

    user.following.add(user_to_follow)
    user.save()

    manage_url = reverse("user:manage")
    return HttpResponseRedirect(manage_url)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unfollow(request, user_id):
    """Remove user_to_unfollow from current user's following"""
    user_to_follow = get_object_or_404(User, id=user_id)

    user = request.user

    user.following.remove(user_to_follow)
    user.save()

    manage_url = reverse("user:manage")
    return HttpResponseRedirect(manage_url)


class FollowingListView(generics.ListAPIView):
    """Users that the current user is following"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.following.all().prefetch_related("following")


class FollowersListView(generics.ListAPIView):
    """Users that are following the current user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following=user)


class UserPostsView(generics.ListAPIView):
    """Retrieve all the posts of the user"""

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_posts = Post.objects.filter(user=user).prefetch_related(
            "hashtags", "liked_by"
        )

        return user_posts


class FollowingPostsView(generics.ListAPIView):
    """Posts of all users that the current user is following"""

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        following_users = current_user.following.all()
        following_posts = Post.objects.filter(
            user__in=following_users
        ).prefetch_related("hashtags", "liked_by")

        return following_posts


class LikedPostsView(generics.ListAPIView):
    """Retrieve all the posts that the user has liked"""

    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        liked_posts = user.liked_posts.all().prefetch_related(
            "hashtags", "liked_by"
        )

        return liked_posts
