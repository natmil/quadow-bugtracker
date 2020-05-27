from django.db import models
from django.contrib.auth.models import User
from PIL import Image

TAMANO_MAX = 512  # Tamaño máximo para la imagen de perfil


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(default='defecto.webp', upload_to='imagenes_perfil')

    def __str__(self):
        return f'{self.usuario.username} Perfil'

    # Sobreescribiremos la función de guardado
    '''def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Guardaremos la imagen reduciendo su resolución
        img = Image.open(self.imagen.path)

        # Solo si esta es mayor al tamaño deseado de nuestra constante
        if img.height > TAMANO_MAX or img.width > TAMANO_MAX:
            tamano_salida = (TAMANO_MAX, TAMANO_MAX)
            img.thumbnail(tamano_salida)
            img.save(self.imagen.path, quality=80)'''
