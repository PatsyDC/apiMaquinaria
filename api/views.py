import os
from django.core.files import File
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.utils import timezone
from datetime import timedelta
from rest_framework import status #
from django.contrib.auth import authenticate #
from rest_framework_simplejwt.tokens import RefreshToken #
from .models import *
from .serializers import *

#token de usuarios
class CustomTokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            try:
                user_token = UserToken.objects.get(user=user)
                if user_token.is_valid():
                    return Response({
                        'access': user_token.token,
                        'message': 'Token existente válido'
                    })
                else:
                    user_token.delete()
            except UserToken.DoesNotExist:
                pass
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            UserToken.objects.create(
                user=user,
                token=access_token,
                expires_at=timezone.now() + timedelta(minutes=60)  # Ajusta según tus necesidades
            )
            
            return Response({
                'access': access_token,
                'message': 'Nuevo token creado'
            })
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Crear el usuario
            user = serializer.save()

            # Ruta de las imágenes predeterminadas
            profile_image_path = os.path.join(settings.MEDIA_ROOT, 'api/images/icon-userd.png')
            cover_image_path = os.path.join(settings.MEDIA_ROOT, 'api/images/fondo_portada.avif')

            # Verificar si las imágenes existen en el sistema de archivos
            if os.path.exists(profile_image_path) and os.path.exists(cover_image_path):
                # Abrir las imágenes como archivos
                with open(profile_image_path, 'rb') as profile_file, open(cover_image_path, 'rb') as cover_file:
                    # Crear el perfil del usuario con las imágenes predeterminadas
                    user_profile = UserProfile.objects.create(
                        user=user,
                        profile_image=File(profile_file, name='icon-userd.png'),
                        cover_image=File(cover_file, name='fondo_portada.avif')
                    )

                return Response({
                    "user": serializer.data,
                    "profile_created": True,
                    "message": "Usuario creado exitosamente con perfil y fotos por defecto."
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "error": "Las imágenes predeterminadas no se encuentran en la ruta especificada."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Permite actualizaciones parciales
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        # Si se proporciona una contraseña nueva, se configura correctamente
        if 'password' in serializer.validated_data:
            instance.set_password(serializer.validated_data['password'])
            instance.save()

############### CATEGORIAS ##############
class CategoriasListCreateView(generics.ListCreateAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

class CategoriasRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

############ MAQUINAS ###############
class MaquinaListCreateView(generics.ListCreateAPIView):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

class MaquinaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maquina.objects.all()
    serializer_class = MaquinaSerializer

####### PUBLICACIONES #################

class PublicacionListCreateView(generics.ListCreateAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class PublicacionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

    # Permitimos actualizaciones parciales (sin requerir todos los campos)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Esto permite actualizaciones parciales
        return super().update(request, *args, **kwargs)

#comentarios 

class ComentariosListCreateView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

class ComentariosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

# Vista para listar y crear el perfil de usuario
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # Aquí no necesitamos 'user_id' en la URL
        return UserProfile.objects.all()  # Devuelve todos los perfiles

# Vista para recuperar, actualizar y eliminar el perfil de usuario
class UserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        return UserProfile.objects.get(user__id=user_id)

