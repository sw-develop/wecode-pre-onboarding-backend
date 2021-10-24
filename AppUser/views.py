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


class SignOutView(DestroyAPIView):
    # 인증 & 허가 - JWTAuthentication, IsAuthenticated (기본 설정)

    queryset = User.object.all()

    def destroy(self, request, *args, **kwargs):
        instance = User.objects.get(pk=request.user.id)
        self.perform_destroy(instance)
        content = {'탈퇴 완료'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
