from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil


# Cuando un usuario sea creado, guardará esta señal (signal) con el siguiente receiver, que creara por defecto un
# perfil al usuario
@receiver(post_save, sender=User)  # post_save significa que se ejecutará después del .save()
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


post_save.connect(crear_perfil, sender=User)
