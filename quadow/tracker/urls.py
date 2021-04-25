from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (ListarProyectos, CrearProyecto, EliminarProyecto, EliminarTicket, AbrirTicket, EditarProyecto,
                    ActualizarRoles, EditarTicket)
from . import views

urlpatterns = [
    path('', views.inicio, name="tracker-inicio"),
    path('proyectos/', ListarProyectos.as_view(), name="tracker-proyectos"),
    path('proyectos/nuevo/', CrearProyecto.as_view(), name="crear-proyecto"),
    path('proyectos/<int:pk_proyecto>/cambiar-estado/', views.cambiar_estado_proyecto, name='cambiar-estado-proyecto'),
    # Para acceder a los detalles de un proyecto por su clave primaria (id)
    path('proyectos/<int:pk_proyecto>/', views.retornar_detalle_proyecto, name="detalle-proyecto"),
    path('proyectos/<int:pk>/editar/', EditarProyecto.as_view(), name="editar-proyecto"),
    path('proyectos/<int:pk>/asignar-rol/', ActualizarRoles.as_view(), name="roles-proyecto"),
    path('proyectos/<int:pk>/eliminar/', EliminarProyecto.as_view(), name="eliminar-proyecto"),
    path('proyectos/<int:pk>/abrir-ticket/', AbrirTicket.as_view(), name="abrir-ticket"),
    path('proyectos/<int:pk_proyecto>/ticket/<int:pk_ticket>/', views.retornar_detalle_ticket, name="detalle-ticket"),
    path('proyectos/<int:pk_proyecto>/ticket/<int:pk>/eliminar/', EliminarTicket.as_view(), name="eliminar-ticket"),
    path('proyectos/<int:pk_proyecto>/ticket/<int:pk>/editar/', EditarTicket.as_view(), name="editar-ticket"),
    path('proyectos/<int:pk_proyecto>/ticket/<int:pk>/cambiar-estado/<int:estado>/', views.cambiar_estado_ticket,
         name="cambiar-estado"),
]
