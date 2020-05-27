from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Proyecto, RolesProyecto


# Cuando un usuario sea creado, guardará esta señal (signal) con el siguiente receiver, que creara por defecto un
# perfil al usuario
@receiver(post_save, sender=Proyecto)  # post_save signifixa que se ejecutará después del .save()
def asignar_proyect_manager(sender, instance, created, **kwargs):
    if created:
        RolesProyecto.objects.create(proyecto=instance, usuario=instance.usuario_creador, tipo='PROJECT MANAGER')


post_save.connect(asignar_proyect_manager, sender=Proyecto)
