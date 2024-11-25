from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields= '__all__'

class MaquinaSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Maquina
        fields = '__all__' 

class ComentariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'  # Incluye los campos que quieras mostrar

class PublicacionSerializer(serializers.ModelSerializer):
    comentarios = ComentariosSerializer(many=True, read_only=True)

    class Meta:
        model = Publicacion
        fields = ['id', 'descripcion', 'img', 'user', 'comentarios']

    def update(self, instance, validated_data):
        # Actualizar la descripción si se pasa
        descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.descripcion = descripcion

        # Solo actualizar la imagen si se pasa una nueva
        img = validated_data.get('img', None)
        if img is not None:  # Si la imagen no es None, la actualizamos
            instance.img = img

        # Guardar la instancia después de actualizar
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Para confirmar la contraseña

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__' 
