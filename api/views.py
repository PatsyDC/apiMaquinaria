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

#ejemplo

class EjemploListCreateView(generics.ListCreateAPIView):
    queryset = PrimerEjemplo.objects.all()
    serializer_class = EjemploSerializer

class EjemploRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrimerEjemplo.objects.all()
    serializer_class = EjemploSerializer

#comentarios 

class ComentariosListCreateView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

class ComentariosRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer

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