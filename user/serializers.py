from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.db.models import Count, Avg, Sum


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'