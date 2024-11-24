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
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "Usuario creado exitosamente"
            }, status=status.HTTP_201_CREATED)
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

#comentarios 

class ComentariosListCreateView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

class ComentariosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

#### foto perfil - portada ##############

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
