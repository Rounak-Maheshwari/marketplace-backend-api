from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegisterView(GenericAPIView, CreateModelMixin):
    queryset = User
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ChangePasswordView(GenericAPIView, UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"detail": "Password updated successfully!"}, status=status.HTTP_200_OK)



