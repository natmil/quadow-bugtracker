from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Importamos los usuarios de django
from django.urls import reverse
from PIL import Image

ESTADO_PROYECTO = (
    ("ACTIVO", "Activo"),
    ("FINALIZADO", "Finalizado"),
)

PRIORIDAD_TICKET = (
    (0, "Urgente"),
    (1, "Alta"),
    (2, "Media"),
    (3, "Baja"),
)

# https://support.euphoria.co.za/support/solutions/articles/60399-what-do-the-ticket-statuses-mean-
ESTADO_TICKET = (
    (0, "Abierto"),  # El usuario ha abierto el ticket y aún no ha sido procesado
    (1, "Pendiente"),  # El ticket está siendo procesado
    (2, "Resuelto"),  # El ticket ha sido resuelto
    (3, "Cerrado"),  # El ticket ha sido cerrado, generalmente ha sido aceptado por el usuario
)

TIPO_TICKET = (
    ("BUG", "Bug"),
    ("CONSULTA", "Consulta"),
    ("FEATURE REQUEST", "Solicitud de función"),
    ("OTROS", "Otros"),
)

ROL_EMPLEADO = (
    ("ADMIN", "Admin"),
    ("DEVELOPER", "Developer"),
    ("PROJECT MANAGER", "Project Manager"),
    ("BETA TESTER", "Beta Tester"),
    ("NS/NC", "NS/NC"),
)

TAMANO_MAX = 512


class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    usuario_creador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_PROYECTO, default="ACTIVO")
    imagen = models.ImageField(default='interr.jpg', upload_to='imagenes_proyectos')

    def __str__(self):
        return self.nombre

    '''def save(self, **kwargs):
        super().save()

        img = Image.open(self.imagen.path)

        if img.height > TAMANO_MAX or img.width > TAMANO_MAX:
            tamano_salida = (TAMANO_MAX, TAMANO_MAX)
            img.thumbnail(tamano_salida)
            img.save(self.imagen.path, quality=80)'''

    def get_absolute_url(self):
        return reverse('detalle-proyecto', kwargs={'pk_proyecto': self.pk})

    class Meta:
        ordering = ['fecha_creacion', '-estado']


class RolesProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=ROL_EMPLEADO, default="NS/NC")

    def __str__(self):
        return f'{self.proyecto} - {self.usuario} - {self.tipo}'

    def get_absolute_url(self):
        return reverse('detalle-proyecto', kwargs={'pk_proyecto': self.proyecto.pk})


class Ticket(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    usuario_creador = models.ForeignKey(User, on_delete=models.CASCADE)
    prioridad = models.IntegerField(choices=PRIORIDAD_TICKET, default=3)
    estado = models.IntegerField(choices=ESTADO_TICKET, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_TICKET, default="OTROS")

    def __str__(self):
        return self.titulo

    # Para ordenar los tickets primero por prioridad y después por estado
    class Meta:
        ordering = ['estado', 'prioridad']

    def get_absolute_url(self):
        return reverse('detalle-ticket', kwargs={'pk_proyecto': self.proyecto.pk, 'pk_ticket': self.pk})


class ComentariosTicket(models.Model):
    texto = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comentario {self.autor} #{self.id}'


class AdjuntosTicket(models.Model):
    fichero = models.FileField(upload_to='adjuntos')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    fecha_subida = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.ticket} - {self.autor} - {self.fichero.name}'
