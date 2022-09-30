from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views     #dentro del mismo paquete importar vistas

app_name = "territorium"

urlpatterns = [
    path('', views.inicio, name="inicio"),
    
    path('aprendices/', views.aprendices, name="aprendices"),
    path('crear_aprendices/', views.aprendicesFormulario, name="crear_aprendiz"),
    path('guardar_aprendices/', views.aprendicesGuardar, name="guardar_aprendiz"),
    path('eliminar_aprendices/<int:id>',views.aprendicesEliminar, name="eliminar_aprendiz"),
    path('editarAprendices/<int:id>',views.editarAprendiz, name="editar_aprendiz"),
    path('actualizarAprendiz/',views.ActualizarAprendiz, name="actualizar_aprendiz"),
    path('BuscarAprendiz/',views.aprendicesBuscar, name="Buscar_aprendiz"),
    
    path('loginForm/',views.loginForm, name="loginForm"),
    path('login/',views.login, name="login"),
    path('loginC/',views.loginC, name="login_cerrar"),

    path('monitorias/', views.monitorias, name="monitorias"),
    path('crear_monitorias/', views.monitoriasFormulario, name="crear_monitoria"),
    path('guardar_monitorias/', views.monitoriasGuardar, name="guardar_monitoria"),
    path('eliminar_monitorias/<int:id>',views.monitoriasEliminar, name="eliminar_monitoria"),

    path('actividades/', views.actividades, name="actividades"),
    path('crear_actividades/', views.actividadesFormulario, name="crear_actividad"),
    path('guardar_actividades/', views.actividadesGuardar, name="guardar_actividad"),
    path('eliminar_actividades/<int:id>',views.actividadesEliminar, name="eliminar_actividad"),
    
    path('usuario/', views.usuario, name="usuario"),
    path('crear_usuario/', views.usuarioFormulario, name="crear_usuario"),
    path('guardar_usuario/', views.usuarioGuardar, name="guardar_usuario"),
    path('eliminar_usuario/<int:id>',views.usuarioEliminar, name="eliminar_usuario"),
    path('editarUsuario/<int:id>',views.editarUsuario, name="editar_usuario"),
    path('actualizarUsuario/',views.ActualizarUsuario, name="actualizar_usuario"),
    path('BuscarUsuario/',views.usuarioBuscar, name="Buscar_usuario"),

   
] 