from django.contrib import admin
from django.urls import path
from App_Municipal.views import *

urlpatterns = [
    # Rutas generales
    path('admin/', admin.site.urls),
    path("", inicio, name="inicio"),
    path("logearse/", login, name="login"),
    path("logout/", logout_view, name="logout"),
    path('mensajePermiso/', mensajePermiso, name='mensajePermiso'),
    path('verificar_rol/', verificar_rol, name='redirect_url'),

    # Rutas del Administrador
    path('Panel_Administrador/', admin_dashboard, name='admin_dashboard'),
    path('Panel_Administrador/Perfil_Usuario/', perfil_usuario, name='Perfil_usuario_adm'),
    path('Panel_Administrador/Perfil_Usuario/Cambiar_Contraseña/', cambiar_contraseña_adm, name='cambiar_contraseña_adm'),

    # Rutas del Administrador: Gestión de Usuarios
    path('Panel_Administrador/usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('Panel_Administrador/usuarios/listar/', listar_usuarios, name='listar_usuario'),
    path('Panel_Administrador/usuarios/restablecer_contraseña/<int:user_id>/', restablecer_contraseña, name='restablecer_contraseña'),
    path('Panel_Administrador/usuarios/crear/', Ingresar_Usuario, name='ingresar_usuario'),
    path('Panel_Administrador/usuarios/eliminar/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('Panel_Administrador/usuarios/modificar/<int:user_id>/', modificar_usuario, name='modificar_usuario'),
    path('Panel_Administrador/usuarios/detalles/<int:user_id>/', detalle_usuario, name='detalles_usuario'),
    
    # Rutas del Administrador: Gestión de Solicitudes
    path('Panel_Administrador/solicitudes/', listar_solicitudes, name='listar_solicitudes'),
    path('Panel_Administrador/solicitudes/gestionar/', gestionar_solicitudes, name='gestionar_solicitudes'),
    path('Panel_Administrador/solicitudes/detalles/<int:id>/', detalles_solicitud, name='detalles_solicitud'),
    path('Panel_Administrador/solicitudes/cambiar_estado/<int:id>/', editar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('Panel_Administrador/solicitudes/eliminar/<int:id>/', eliminar_solicitud, name='eliminar_solicitud'),

    # Rutas del Vendedor
    path('Panel_Vendedor/', vendedor_dashboard, name='vendedor_dashboard'),
    path('Panel_Vendedor/Perfil_Usuario/', perfil_usuario, name='Perfil_usuario_vendedor'),
    path('Panel_Vendedor/Perfil_Usuario/Cambiar_Contraseña/', cambiar_contrasena_vendedor, name='cambiar_contraseña_vendedor'),
    path('Panel_Vendedor/solicitudes/buscar/', buscar_solicitudes, name='buscar_solicitud'),
    path('Panel_Vendedor/solicitudes/crear/', ingresar_solicitud, name='ingresar_solicitud'),
]
