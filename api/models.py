from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()

class PrimerEjemplo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    descripcion = models.CharField(max_length=2500)
    img = models.ImageField(upload_to='api/images/')

    def __str__(self):
        return f'{self.user.username}'

class Categorias(models.Model):
    categoria = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name_plural = ('Categorias')

    def __str__(self):
        return f'{self.categoria}'

class Maquina(models.Model):
    modelo = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='api/images/')
    prefix = models.CharField(max_length=150)
    pdf_file = models.FileField(upload_to='api/pdfs/', null=True, blank=True)

    class Meta:
        verbose_name_plural = ('Máquinas')

    def __str__(self):
        return f'{self.modelo}'

class Publicacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_publicaciones')
    descripcion = models.TextField()
    img = models.ImageField(upload_to='api/images/')

    class Meta:
        verbose_name_plural = ('Publicaciones')

    def __str__(self):
        return f'{self.user}'

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comentarios')
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios', null=True, blank=True)
    texto = models.TextField()

    def __str__(self):
        return f'{self.user.username}'


