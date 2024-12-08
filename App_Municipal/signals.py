from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from .models import Solicitud


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Crear roles/grupos predeterminados en el sistema.
    """
    roles = ['Administrador', 'Vendedor']
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f'Rol "{role}" creado.')
        else:
            print(f'Rol "{role}" ya existe.')


@receiver(post_migrate)
def assign_permissions(sender, **kwargs):
    """
    Asignar permisos predeterminados a los grupos Administrador y Vendedor.
    """
    # Content types
    solicitud_content_type = ContentType.objects.get_for_model(Solicitud)
    user_content_type = ContentType.objects.get_for_model(User)

    # Permisos específicos del modelo Solicitud para el grupo Administrador
    admin_solicitud_permissions = [
        ('list_solicitud', 'Puede listar solicitudes'),
        ('view_solicitud', 'Puede ver detalles de una solicitud'),
        ('change_solicitud', 'Puede cambiar el estado de una solicitud'),
        ('delete_solicitud', 'Puede eliminar solicitudes'),
    ]

    # Permisos específicos del modelo User para el grupo Administrador
    admin_user_permissions = [
        ('view_user', 'Puede ver detalles de un usuario'),
        ('change_user', 'Puede modificar usuarios'),
        ('create_user', 'Puede crear usuarios'),
        ('list_user', 'Puede listar usuarios'),
        ('delete_user', 'Puede eliminar usuarios'),
        ('change_password', 'Puede restablecer contraseña usuario'),
    ]

    # Asignar permisos al grupo Administrador
    admin_group, created = Group.objects.get_or_create(name='Administrador')

    for codename, name in admin_solicitud_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=solicitud_content_type
        )
        admin_group.permissions.add(permission)
        print(f'Permiso "{name}" asignado al grupo "Administrador".')

    for codename, name in admin_user_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=user_content_type
        )
        admin_group.permissions.add(permission)
        print(f'Permiso "{name}" asignado al grupo "Administrador".')

    # Permisos específicos para el grupo Vendedor
    vendedor_permissions = [
        ('buscar_solicitud', 'Puede buscar solicitudes'),
    ]

    # Asignar permisos al grupo Vendedor
    vendedor_group, created = Group.objects.get_or_create(name='Vendedor')
    for codename, name in vendedor_permissions:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=solicitud_content_type
        )
        vendedor_group.permissions.add(permission)
        print(f'Permiso "{name}" asignado al grupo "Vendedor".')


@receiver(post_migrate)
def create_default_admin_user(sender, **kwargs):
    """
    Crear un superusuario predeterminado con contraseña fija.
    """
    admin_email = "admin@gmail.com"
    admin_password = "123456"  # Contraseña fija

    if not User.objects.filter(email=admin_email).exists():
        # Crear superusuario con la contraseña fija
        admin_user = User.objects.create_superuser(
            username="admin",
            email=admin_email,
            password=admin_password,
            first_name="Administrador",
            last_name="Principal"
        )
        # Asignar al grupo "Administrador"
        admin_group = Group.objects.get(name="Administrador")
        admin_user.groups.add(admin_group)

        print(f'Superusuario predeterminado creado: {admin_email} con contraseña: {admin_password}')
    else:
        print(f'Superusuario predeterminado ya existe: {admin_email}')
