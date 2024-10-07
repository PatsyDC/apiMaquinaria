from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ComentariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'user', 'texto']  # Incluye los campos que quieras mostrar

class EjemploSerializer(serializers.ModelSerializer):
    comentarios = ComentariosSerializer(many=True, read_only=True)  # Agrega esta línea para incluir los comentarios

    class Meta:
        model = PrimerEjemplo
        fields = ['id', 'descripcion', 'img', 'user', 'comentarios']  # Asegúrate de incluir 'comentarios'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields= '__all__'

class MaquinaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Maquina
        fields = '__all__' 

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'


