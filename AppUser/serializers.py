from rest_framework import serializers

from AppUser.models import AppUser


class AddUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['nickname', 'phone', 'birthdate']
