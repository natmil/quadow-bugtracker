from django.contrib import admin
from .models import Proyecto, Ticket, ComentariosTicket, RolesProyecto, AdjuntosTicket

admin.site.register(Proyecto)
admin.site.register(Ticket)
admin.site.register(ComentariosTicket)
admin.site.register(RolesProyecto)
admin.site.register(AdjuntosTicket)
