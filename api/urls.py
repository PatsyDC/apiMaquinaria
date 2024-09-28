from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('ejemplo/', EjemploListCreateView.as_view(), name='ejjemplo-view'),
    path('ejemplo/<int:pk>/',EjemploRetrieveUpdateDestroyView.as_view(), name='ejjemplo'),
    path('comentario/', ComentariosListCreateView.as_view(), name='comentarios'),
    path('comentario/<int:pk>', ComentariosRetrieveUpdateDestroyView.as_view(), name='comentarios'),
    path('categorias/', CategoriasListCreateView.as_view(), name='categorias'),
    path('maquinas/', MaquinaListCreateView.as_view(), name='maquina'),
    path('maquinas/<int:pk>', MaquinaRetrieveUpdateDestroyView.as_view(), name='maquinaid'),
    path('publicaciones/', PublicacionListCreateView.as_view(), name='publicaciones'),
    path('publicaciones/<int:pk>', PublicacionRetrieveUpdateDestroyView.as_view(), name='publicacionesid'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)