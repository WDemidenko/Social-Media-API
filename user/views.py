import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        email = self.request.query_params.get("email")
        queryset = self.queryset  # TODO fix n+1 problem

        if email:
            queryset = queryset.filter(email__icontains=email)

        return queryset.distinct()


def follow(request, user_id):
    """Add user_to_follow to current user's following"""
    user_to_follow = get_object_or_404(User, id=user_id)

    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    token = auth_header.split(" ")[1] if auth_header else ""

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id_from_token = decoded_token.get("user_id")

    user = get_object_or_404(User, id=user_id_from_token)

    user.following.add(user_to_follow)
    user.save()

    manage_url = reverse("user:manage")
    return HttpResponseRedirect(manage_url)


def unfollow(request, user_id):
    """Remove user_to_unfollow from current user's following"""
    user_to_follow = get_object_or_404(User, id=user_id)

    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    token = auth_header.split(" ")[1] if auth_header else ""

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user_id_from_token = decoded_token.get("user_id")

    user = get_object_or_404(User, id=user_id_from_token)

    user.following.remove(user_to_follow)
    user.save()

    manage_url = reverse("user:manage")
    return HttpResponseRedirect(manage_url)
