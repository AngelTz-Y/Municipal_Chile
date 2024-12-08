from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .models import Solicitud

# Vista principal
def inicio(request):
    return render(request, 'inicio.html')


# Vista: admin_dashboard
@login_required
def admin_dashboard(request):
    if request.user.groups.filter(name='Administrador').exists():
        return render(request, 'InterfazAdmin/Panel_admin.html')
    else:
        return redirect('mensajePermiso')


# Vista: vendedor_dashboard
@login_required
def vendedor_dashboard(request):
    if request.user.groups.filter(name='Vendedor').exists():
        return render(request, 'InterfazVendedor/Panel_Vendedor.html')
    else:
        return redirect('mensajePermiso')


# Vista: verificar_rol
@login_required
def verificar_rol(request):
    if request.user.groups.filter(name='Administrador').exists():
        return redirect('admin_dashboard')
    elif request.user.groups.filter(name='Vendedor').exists():
        return redirect('vendedor_dashboard')
    else:
        return redirect('mensajePermiso')


# Vista: mensajePermiso
def mensajePermiso(request):
    return render(request, 'mensajePermiso.html')


# Vista: login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "El correo electrónico no está registrado.")
            return render(request, 'login.html')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            elif user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard')
            elif user.groups.filter(name='Vendedor').exists():
                return redirect('vendedor_dashboard')
            else:
                return redirect('mensajePermiso')
        else:
            messages.error(request, "Credenciales incorrectas.")
            return redirect('login')

    return render(request, 'login.html')


# Vista: logout_view
def logout_view(request):
    logout(request)
    return redirect('inicio')


# Vista: buscar_solicitudes
@login_required
def buscar_solicitudes(request):
    if request.user.groups.filter(name='Vendedor').exists():
        solicitudes = None
        if request.method == 'GET' and 'rut' in request.GET:
            rut = request.GET['rut']
            solicitudes = Solicitud.objects.filter(rut=rut)
        return render(request, 'InterfazVendedor/buscar_solicitud.html', {'solicitudes': solicitudes})
    else:
        return redirect('mensajePermiso')


# Vista: ingresar_solicitud
def ingresar_solicitud(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            rut = request.POST.get('rut')
            nombre = request.POST.get('nombre')
            apellidos = request.POST.get('apellidos')
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            comuna = request.POST.get('comuna')

            if Solicitud.objects.filter(rut=rut, estado='pendiente').exists():
                messages.error(request, "Ya existe una solicitud pendiente para este RUT.")
                return render(request, 'ingresar_solicitud.html')

            try:
                Solicitud.objects.create(
                    rut=rut,
                    nombre=nombre,
                    apellidos=apellidos,
                    direccion=direccion,
                    telefono=telefono,
                    comuna=comuna,
                    estado='pendiente'
                )
                messages.success(request, "Solicitud enviada con éxito.")
                return redirect('inicio')
            except Exception as e:
                messages.error(request, f'Error al procesar la solicitud: {e}')
                return render(request, 'ingresar_solicitud.html')

        return render(request, 'ingresar_solicitud.html')
    else:
        return redirect('mensajePermiso')


# Vista: gestionar_usuarios
@login_required
def gestionar_usuarios(request):
    if request.user.groups.filter(name='Administrador').exists():
        return render(request, 'InterfazAdmin/Gestion_usuario.html')
    else:
        return redirect('mensajePermiso')


# Vista: listar_usuarios
@login_required
def listar_usuarios(request):
    if request.user.groups.filter(name='Administrador').exists():
        usuarios = User.objects.all()
        return render(request, 'InterfazAdmin/listar_usuario.html', {'usuarios': usuarios})
    else:
        return redirect('mensajePermiso')


# Vista: Ingresar_Usuario
@login_required
def Ingresar_Usuario(request):
    if request.user.groups.filter(name='Administrador').exists():
        if request.method == 'POST':
            email = request.POST.get('email')
            firstname = request.POST.get('nombre')
            lastname = request.POST.get('apellido')
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('confirm_password')
            selected_role = request.POST.get('rol')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
                return redirect('ingresar_usuario')

            if pass1 != pass2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('ingresar_usuario')

            try:
                if selected_role == 'Administrador':
                    user = User.objects.create_superuser(username=email, email=email, password=pass1)
                    admin_group = Group.objects.get(name='Administrador')
                    user.groups.add(admin_group)
                elif selected_role == 'Vendedor':
                    user = User.objects.create_user(username=email, email=email, password=pass1)
                    vendedor_group = Group.objects.get(name='Vendedor')
                    user.groups.add(vendedor_group)

                user.first_name = firstname
                user.last_name = lastname
                user.save()
                messages.success(request, 'Usuario registrado exitosamente.')
                return redirect('listar_usuario')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al registrar el usuario: {e}')
                return redirect('ingresar_usuario')

        return render(request, 'InterfazAdmin/ingresar_usuario.html')
    else:
        return redirect('mensajePermiso')


# Vista: modificar_usuario
@login_required
def modificar_usuario(request, user_id):
    if request.user.groups.filter(name='Administrador').exists():
        usuario = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            role = request.POST.get('role')

            try:
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.email = email
                usuario.username = email
                usuario.groups.clear()
                group = Group.objects.get(name=role)
                usuario.groups.add(group)
                usuario.save()

                messages.success(request, 'Usuario modificado exitosamente.')
                return redirect('listar_usuario')
            except Exception as e:
                messages.error(request, f'Error al modificar usuario: {e}')
        grupos = Group.objects.all()
        return render(request, 'InterfazAdmin/modificar_usuario.html', {'usuario': usuario, 'grupos': grupos})
    else:
        return redirect('mensajePermiso')


# Vista: eliminar_usuario
@login_required
def eliminar_usuario(request, user_id):
    if request.user.groups.filter(name='Administrador').exists():
        usuario = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            try:
                usuario.delete()
                messages.success(request, 'Usuario eliminado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al eliminar usuario: {e}')
        return redirect('listar_usuario')
    else:
        return redirect('mensajePermiso')


# Vista: detalle_usuario
@login_required
def detalle_usuario(request, user_id):
    if request.user.groups.filter(name='Administrador').exists():
        usuario = get_object_or_404(User, id=user_id)
        return render(request, 'InterfazAdmin/detalles_usuario.html', {'usuario': usuario})
    else:
        return redirect('mensajePermiso')


# Vista: perfil_usuario
@login_required
def perfil_usuario(request):
    usuario = request.user
    if usuario.groups.filter(name='Administrador').exists():
        return render(request, 'InterfazAdmin/perfil_admin.html', {'usuario': usuario})
    elif usuario.groups.filter(name='Vendedor').exists():
        return render(request, 'InterfazVendedor/perfil_vendedor.html', {'usuario': usuario})
    else:
        return redirect('mensajePermiso')



# Vista: cambiar_contrasena para Administrador
@login_required
def cambiar_contraseña_adm(request):
    if request.user.groups.filter(name='Administrador').exists():
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = request.user

            if not user.check_password(old_password):
                messages.error(request, 'La contraseña actual es incorrecta.')
                return render(request, 'cambiar_contraseña.html')

            if new_password != confirm_password:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
                return render(request, 'cambiar_contraseña.html')

            user.set_password(new_password)
            user.save()
            logout(request)
            messages.success(request, 'Contraseña actualizada exitosamente. Por favor inicia sesión nuevamente.')
            return redirect('login')

        return render(request, 'cambiar_contraseña.html')
    else:
        return redirect('mensajePermiso')


# Vista: cambiar_contrasena para Vendedor
@login_required
def cambiar_contrasena_vendedor(request):
    if request.user.groups.filter(name='Vendedor').exists():
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = request.user

            if not user.check_password(old_password):
                messages.error(request, 'La contraseña actual es incorrecta.')
                return render(request, 'cambiar_contraseña.html')

            if new_password != confirm_password:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
                return render(request, 'cambiar_contraseña.html')

            user.set_password(new_password)
            user.save()
            logout(request)
            messages.success(request, 'Contraseña actualizada exitosamente. Por favor inicia sesión nuevamente.')
            return redirect('login')

        return render(request, 'cambiar_contraseña.html')
    else:
        return redirect('mensajePermiso')


@login_required
@permission_required('App_Municipal.change_password', raise_exception=True)
def restablecer_contraseña(request, user_id):
    """
    Permite a los Administradores restablecer la contraseña de otros usuarios.
    """
    if request.user.groups.filter(name='Administrador').exists():
        usuario = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            nueva_contrasena = request.POST.get('new_password')
            confirmar_contrasena = request.POST.get('confirm_password')

            if nueva_contrasena != confirmar_contrasena:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'InterfazAdmin/restablecer_contraseña.html', {'usuario': usuario})

            try:
                usuario.set_password(nueva_contrasena)
                usuario.save()
                messages.success(request, f'Contraseña de {usuario.username} actualizada exitosamente.')
                return redirect('listar_usuario')
            except Exception as e:
                messages.error(request, f'Error al restablecer la contraseña: {e}')

        return render(request, 'InterfazAdmin/restablecer_contraseña.html', {'usuario': usuario})

    else:
        # Redirigir si no tiene permiso
        return redirect('mensajePermiso')



from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Solicitud

@login_required
@permission_required('App_Municipal.delete_solicitud', raise_exception=True)
def eliminar_solicitud(request, id):
    """
    Vista para eliminar una solicitud.
    """
    solicitud = get_object_or_404(Solicitud, id=id)

    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, 'La solicitud ha sido eliminada correctamente.')
        return redirect('gestionar_solicitudes')

    return render(request, 'InterfazAdmin/Solicitudes/EliminacionConfirm.html', {'solicitud': solicitud})


@login_required
@permission_required('App_Municipal.change_solicitud', raise_exception=True)
def editar_estado_solicitud(request, id):
    """
    Vista para editar el estado de una solicitud.
    """
    solicitud = get_object_or_404(Solicitud, id=id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado').lower()  # Convertir a minúsculas
        solicitud.estado = nuevo_estado

        # Actualizar la fecha de aceptación si el estado es "aceptada"
        if nuevo_estado == 'aceptada':
            solicitud.fecha_aceptacion = now()
        else:
            solicitud.fecha_aceptacion = None

        solicitud.save()
        messages.success(request, 'El estado de la solicitud ha sido actualizado.')
        return redirect('gestionar_solicitudes')

    return render(request, 'InterfazAdmin/Solicitudes/EditarSolicitud.html', {'solicitud': solicitud})


@login_required
@permission_required('App_Municipal.view_solicitud', raise_exception=True)
def listar_solicitudes(request):
    """
    Lista todas las solicitudes y las organiza por estado.
    """
    solicitudes = Solicitud.objects.all()

    # Actualizar estado a 'expirada' si ha pasado el tiempo permitido
    for solicitud in solicitudes:
        if solicitud.estado != 'expirada' and now() > solicitud.fecha_solicitud + timedelta(days=30):
            solicitud.estado = 'expirada'
            solicitud.save()

    # Dividir solicitudes por estado
    solicitudes_pendientes = solicitudes.filter(estado='pendiente')
    solicitudes_aceptadas = solicitudes.filter(estado='aceptada')
    solicitudes_rechazadas = solicitudes.filter(estado='rechazada')
    solicitudes_expiradas = solicitudes.filter(estado='expirada')

    return render(request, 'InterfazAdmin/Solicitudes/listar_solicitud.html', {
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aceptadas': solicitudes_aceptadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
        'solicitudes_expiradas': solicitudes_expiradas,
    })


@login_required
@permission_required('App_Municipal.view_solicitud', raise_exception=True)
def detalles_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    return render(request, 'InterfazAdmin/Solicitudes/detalle_solicitud.html', {'solicitud': solicitud})




@login_required
@permission_required('App_Municipal.view_solicitud', raise_exception=True)
def gestionar_solicitudes(request):
    """
    Lista todas las solicitudes registradas con opciones de edición, eliminación y detalle.
    """
    solicitudes = Solicitud.objects.all()
    return render(request, 'InterfazAdmin/Gestion_Solicitud.html', {'solicitudes': solicitudes})