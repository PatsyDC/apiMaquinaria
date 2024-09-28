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

class CategoriasSerializer(serializers.Serializer):
    class Meta:
        model = Categorias
        filter = '__all__'

class MaquinaSerializer(serializers.Serializer):
    class Meta:
        model = Maquina
        filter = '__all__'

class PublicacionSerializer(serializers.Serializer):
    class Meta:
        model = Publicacion
        filter = '__all__'


