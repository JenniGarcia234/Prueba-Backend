from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from api_c.serializers import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, LoginSerializer, LogoutSerializer
from api_c.serializers import ProfileSerializer, StudentSerializer, ProfessorSerializer, ProfileSerializerP, ProfileSerializerS
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api_c.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.decorators import api_view
import jwt
from rest_framework.generics import ListAPIView, UpdateAPIView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api_c.renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect, HttpResponse
import os
from api_c.permissions import IsOwner, IsProfessor

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_c.permissions import IsProfessor
class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
          
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
#Get my profile student
class UserProfileStudent(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.pk)

#Get my profile professor
class UserProfileProfessor(ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.pk)

class UserProfileUpdateProfessor(UpdateAPIView):
    serializer_class = ProfileSerializerP
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_queryset(self, pk):
        try:
            profile = User.objects.get(pk=pk)
        except User.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return profile

    # Get my profile
    def get(self, request, pk):

        profile = self.get_queryset(pk)
        serializer = ProfileSerializerP(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update my profile
    def put(self, request, pk):
        profile = self.get_queryset(pk)

        if(request.user.username == profile.username): # Si el perfil corresponde a quien hace el request
            serializer = ProfileSerializerP(profile, data=request.data)
            if serializer.is_valid():
                serializer.save(is_professor=True, is_student=False)
                   
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileUpdateStudent(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_queryset(self, pk):
        try:
            profile = User.objects.get(pk=pk)
        except User.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return profile

    # Get my profile
    def get(self, request, pk):

        profile = self.get_queryset(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update my profile
    def put(self, request, pk):
        
        profile = self.get_queryset(pk)

        if(request.user.username == profile.username): # Si el perfil corresponde a quien hace el request
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save(is_professor=False, is_student=True)
                   
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)



class PasswordTokenCheckAPI(generics.GenericAPIView):


   def get(self, request, uidb64, token):

      try:
          id=smart_str(urlsafe_base64_decode(uidb64))
          user=User.objects.get(id=id)
          if not PasswordResetTokenGenerator().check_token(user, token):
              return Response({'error':'Token no valido, por favor, pide uno nuevo'},status=status.HTTP_401_UNAUTHORIZED )
          return Response({'sucess':'True, credenciales validas'},status=status.HTTP_200_OK)

      except DjangoUnicodeDecodeError as identifier:
             return Response({'error':'Token no valido, por favor, pide uno nuevo'},status=status.HTTP_401_UNAUTHORIZED )
      
    

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Se ha restablecido la contraseña'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):   
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


#Student list 
@permission_classes((IsProfessor, ))
@api_view(['GET'])
def students_list(self):
    items = User.objects.all().filter(is_student=True)
    serializer = StudentSerializer(items, many=True)
    return Response({'success': True, 'data': serializer.data})

@permission_classes((IsProfessor, ))
#Professors list 
@api_view(['GET'])
def professors_list(self):
    items = User.objects.all().filter(is_professor=True)
    serializer = ProfessorSerializer(items, many=True)
    return Response({'success': True, 'data': serializer.data})