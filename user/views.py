from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
import json
from datetime import datetime, timedelta
import requests

# Create your views here.
class UserDetail(APIView):
    """
    Retrieve, update or delete a contient instance
    """
    def get_object(self, email):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return User.objects.get(pk=email)
        except User.DoesNotExist:
            raise Http404
  
    def get(self, request, format=None):
        contients = User.objects.all()
        serializer = UserSerializer(contients, many=True)
        return Response(serializer.data)
  
    def put(self, request, format=None):
        users = self.get_object(request.data['email'])
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            saving = User(**request.data)
            saving.save()
            return Response({'Status':'Updated Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, format=None):
        users = self.get_object(request.data['email'])
        serializer = UserSerializer(users,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            saving = User(**request.data)
            saving.save()
            return Response({'Status':'Updated Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            saving = User(**request.data)
            saving.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, format=None):
        users = self.get_object(request.data['email'])
        users.delete()
        return Response({'Status':'Deleted'}, status=status.HTTP_200_OK)
