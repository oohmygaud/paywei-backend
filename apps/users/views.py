from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum
from .serializers import (
    APIKeySerializer,
    UserSerializer,
    WhitelistAddressSerializer
)
from .models import CustomUser as User, APIKey, WhitelistAddress
from rest_framework import viewsets
from .permissions import IsOwner
from django.utils import timezone


# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    model = User
    permission_classes = (IsOwner,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    model = APIKey
    permission_classes = (IsOwner,)
    serializer_class = APIKeySerializer

    def get(self, request, format=None):
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not logged in'}, status=401)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return APIKey.objects.none()
        return APIKey.objects.filter(user=self.request.user)
    

class WhitelistAddressViewSet(viewsets.ModelViewSet):
    model = WhitelistAddress
    permission_classes = (IsOwner,)
    serializer_class = WhitelistAddressSerializer

    def get(self, request, format=None):
        if not self.request.user.is_authenticated:
            return Response({'error': 'You are not logged in'}, status=401)
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return WhitelistAddress.objects.none()
        return WhitelistAddress.objects.filter(user=self.request.user)