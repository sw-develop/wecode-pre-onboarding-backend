from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from AppUser.models import AppUser
from AppUser.serializers import AddUserInfoSerializer


class AddUserInfoView(UpdateAPIView):
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)

    queryset = AppUser.objects.all()
    serializer_class = AddUserInfoSerializer
