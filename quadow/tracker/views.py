from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from django.contrib import messages

from .formulario import FormularioActualizarImagenProyecto, FormularioSubirAdjunto, FormularioComentarTicket
from .models import Proyecto, Ticket, ComentariosTicket, RolesProyecto, AdjuntosTicket

import datetime


def mensaje_error(request):
    messages.error(request, f'Ha ocurrido un error. Por favor, revise los datos.')


# Vista para ir al inicio
@login_required
def inicio(request):
    # Gráfico de tarta
    labels_roles = ['ADMIN', 'DEVELOPER', 'PROJECT MANAGER', 'BETA TESTER', 'NS/NC']
    data_roles = []

    for i in range(len(labels_roles)):
        data_roles.append(Proyecto.objects.filter(
            Q(rolesproyecto__in=RolesProyecto.objects.filter(usuario=request.user, tipo=labels_roles[i]))).count())

    # Gráfico de área
    data_tickets = []
    anyo_actual = datetime.datetime.now().year
    proyectos_del_usuario = RolesProyecto.objects.filter(usuario=request.user).values_list('proyecto').distinct()

    for i in range(12):
        data_tickets.append(Ticket.objects.filter(Q(fecha_creacion__year=anyo_actual),
                                                  Q(fecha_creacion__month=i + 1),
                                                  Q(proyecto_id__in=proyectos_del_usuario)).count())

    # Tipo de tickets
    tipo_tickets = []
    from .models import TIPO_TICKET
    for i in range(len(TIPO_TICKET)):
        tipo_tickets.append(Ticket.objects.filter(Q(tipo=TIPO_TICKET[i][0]),
                                                  Q(proyecto_id__in=proyectos_del_usuario)).count())

    numero_tickets_usuario = sum(tipo_tickets)
    for i in range(len(tipo_tickets)):
        tipo_tickets[i] = round((tipo_tickets[i] * 100) / numero_tickets_usuario) if numero_tickets_usuario > 0 else 0

    # Porcentaje proyectos finalizados
    numero_roles_del_usuario = RolesProyecto.objects.filter(usuario=request.user).distinct('proyecto').all().count()
    proyectos_finalizados_porcentaje = round((Proyecto.objects.filter(usuario_creador=request.user,
                                                                      estado="FINALIZADO").all().count() * 100) /
                                             numero_roles_del_usuario) if numero_roles_del_usuario > 0 else 0

    contexto = {
        'titulo': 'Dashboard',
        'labels_roles': labels_roles,
        'data_roles': data_roles,
        'data_tickets': data_tickets,
        'proyectos': Proyecto.objects.all(),
        'proyectos_asignados': RolesProyecto.objects.filter(usuario=request.user).distinct('proyecto').all(),
        'tipo_tickets': tipo_tickets,
        'roles_asignados': RolesProyecto.objects.filter(usuario=request.user).all().count(),
        'proyectos_finalizados_porcentaje': proyectos_finalizados_porcentaje
    }
    return render(request, 'tracker/index.html', contexto)


# Vista para ver los proyectos
@login_required
def retornar_proyectos(request):
    contexto = {
        # Le pasamos todos los objetos de la tabla Proyecto de la base de datos ordenados por fecha
        'proyectos': Proyecto.objects.all().order_by("fecha_creacion"),
        'titulo': "Proyectos"
    }
    return render(request, "tracker/lista-proyectos.html", contexto)


class ListarProyectos(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = "tracker/lista-proyectos.html"
    context_object_name = 'proyectos'
    extra_context = {'titulo': 'Proyectos'}

    # Solo devuelve los proyectos donde estemos como personal autorizado, hayamos creado o seamos superusuario django
    def get_queryset(self):
        filtro = RolesProyecto.objects.filter(usuario=self.request.user)
        return Proyecto.objects.filter(
            Q(rolesproyecto__in=filtro)).distinct() if not self.request.user.is_superuser else self.model.objects.all()


class CrearProyecto(LoginRequiredMixin, CreateView):
    model = Proyecto
    fields = ['nombre', 'descripcion', 'imagen']
    template_name = "tracker/crear-proyecto.html"
    extra_context = {'titulo': 'Nuevo proyecto'}

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        messages.success(self.request, f'Proyecto creado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_error(self.request)
        return super().form_invalid(form)


class EditarProyecto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Proyecto
    fields = ['nombre', 'descripcion', 'imagen']
    template_name = "tracker/editar-proyecto.html"
    extra_context = {'titulo': 'Editar proyecto'}

    def test_func(self):
        proyecto = Proyecto.objects.filter(id=self.kwargs.get('pk')).first()
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=proyecto)
        return True if filtro_por_tipo.filter(
            Q(tipo='PROJECT MANAGER') | Q(tipo='ADMIN')) or self.request.user.is_superuser else False


class ActualizarRoles(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RolesProyecto
    fields = ['usuario', 'tipo']
    template_name = "tracker/asignar-rol.html"
    extra_context = {'titulo': 'Actualizar proyecto'}

    def form_valid(self, form):
        form.instance.proyecto_id = self.kwargs.get('pk')
        messages.success(self.request, f'Rol añadido al proyecto.')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_error(self.request)
        return super().form_invalid(form)

    def test_func(self):
        proyecto = Proyecto.objects.filter(id=self.kwargs.get('pk')).first()
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=proyecto)
        return True if filtro_por_tipo.filter(
            Q(tipo='PROJECT MANAGER') | Q(tipo='ADMIN')) or self.request.user.is_superuser else False


# Vista para ver los detalles de un proyecto
@login_required
def retornar_detalle_proyecto(request, pk_proyecto):
    objeto = get_object_or_404(Proyecto, pk=pk_proyecto)
    filtro_por_tipo = RolesProyecto.objects.filter(usuario=request.user, proyecto=pk_proyecto)

    if request.method == 'POST':
        if filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
                tipo='PROJECT MANAGER') or request.user.is_superuser:
            if 'cambiar_imagen' in request.POST:
                formulario_imagen = FormularioActualizarImagenProyecto(request.POST, request.FILES, instance=objeto)
                if formulario_imagen.is_valid():
                    formulario_imagen.save()
                    messages.success(request, f'Imagen actualizada.')
                    return redirect('detalle-proyecto', pk_proyecto)
                else:
                    mensaje_error(request)
                    return redirect('detalle-proyecto', pk_proyecto)
            elif 'eliminar_rol' in request.POST:
                rol_eliminar = request.POST.get('eliminar_rol')
                if rol_eliminar and filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
                        tipo='PROJECT MANAGER') or request.user.is_superuser:
                    RolesProyecto.objects.filter(id=rol_eliminar).delete()
                    messages.success(request, f'Rol eliminado.')
                    return redirect('detalle-proyecto', pk_proyecto) if RolesProyecto.objects.filter(usuario=request.user, proyecto=pk_proyecto) else redirect('tracker-proyectos')
                else:
                    mensaje_error(request)
                    return redirect('detalle-proyecto', pk_proyecto)
        else:
            mensaje_error(request)
            return redirect('detalle-proyecto', pk_proyecto)
    else:
        # Controlamos que solo pueda acceder al proyecto aquel que está como personal asignado
        if filtro_por_tipo or request.user.is_superuser:
            contexto = {
                'proyecto': objeto,
                'titulo': objeto.nombre + " - Detalles Proyecto",
                # Le pasamos todos los tickets que coincidan con la PK del proyecto
                'tickets': Ticket.objects.filter(proyecto=pk_proyecto),
                'roles': RolesProyecto.objects.filter(proyecto=pk_proyecto),
                'admins': RolesProyecto.objects.filter(proyecto=pk_proyecto, tipo='ADMIN', usuario=request.user),
                'proyect_managers': RolesProyecto.objects.filter(proyecto=pk_proyecto, tipo='PROJECT MANAGER',
                                                                 usuario=request.user)
            }
            return render(request, 'tracker/detalle-proyecto.html', contexto)
        else:
            raise Http404("No existe el proyecto.")


class AbrirTicket(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Ticket
    fields = ['titulo', 'descripcion', 'prioridad', 'tipo']
    template_name = "tracker/abrir-ticket.html"
    extra_context = {'titulo': 'Abrir ticket'}

    def form_valid(self, form):
        form.instance.usuario_creador = self.request.user
        form.instance.proyecto_id = self.kwargs.get('pk')
        messages.success(self.request, f'Ticket abierto.')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_error(self.request)
        return super().form_invalid(form)

    # Solo quien esté en la lista de personal asignado podrá crear tickets
    def test_func(self):
        proyecto = Proyecto.objects.filter(id=self.kwargs.get('pk')).first()
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=proyecto)
        return True if filtro_por_tipo or self.request.user.is_superuser else False


class EliminarProyecto(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proyecto
    template_name = "tracker/eliminar-proyecto.html"
    success_url = reverse_lazy('tracker-proyectos')
    extra_context = {'titulo': 'Eliminar proyecto'}

    def test_func(self):
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=self.get_object())
        return True if filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
            tipo='PROJECT MANAGER') or self.request.user.is_superuser else False


class EliminarTicket(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = "tracker/eliminar-ticket.html"
    extra_context = {'titulo': 'Eliminar ticket'}

    # Para redireccionar a los detalles del proyecto una vez eliminado el ticket
    def get_success_url(self):
        proyecto = self.object.proyecto
        return reverse_lazy('detalle-proyecto', kwargs={'pk_proyecto': proyecto.id})

    def test_func(self):
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=self.get_object().proyecto)
        return True if filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
            tipo='PROJECT MANAGER') or self.request.user.is_superuser else False


# Vista para ver los detalles de un proyecto
@login_required
def retornar_detalle_ticket(request, pk_proyecto, pk_ticket):
    objeto = get_object_or_404(Ticket.objects.filter(proyecto=pk_proyecto), pk=pk_ticket)

    if request.method == 'POST':
        # Controlamos que el proyecto no se encuentre cerrado
        if not Ticket.objects.filter(proyecto=pk_proyecto, pk=pk_ticket, estado=3):
            if 'subir_adjunto' in request.POST:
                formulario_adjunto = FormularioSubirAdjunto(request.POST, request.FILES)
                if formulario_adjunto.is_valid():
                    form = formulario_adjunto.save(commit=False)
                    form.autor = request.user
                    form.ticket = objeto
                    form.save()
                    messages.success(request, f'Adjunto subido.')
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
                else:
                    mensaje_error(request)
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
            elif 'comentar_ticket' in request.POST:
                formulario_comentario = FormularioComentarTicket(request.POST)
                if formulario_comentario.is_valid():
                    form = formulario_comentario.save(commit=False)
                    form.autor = request.user
                    form.ticket = objeto
                    form.save()
                    messages.success(request, f'Comentario publicado.')
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
                else:
                    mensaje_error(request)
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
            elif 'comentario' in request.POST:
                comentario_eliminar = request.POST.get('comentario')
                filtro_por_tipo = RolesProyecto.objects.filter(usuario=request.user, proyecto=pk_proyecto)
                if comentario_eliminar and filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
                        tipo='PROJECT MANAGER') or ComentariosTicket.objects.filter(autor=request.user,
                                                                                    id=comentario_eliminar) or request.user.is_superuser:
                    ComentariosTicket.objects.filter(id=comentario_eliminar).delete()
                    messages.success(request, f'Comentario eliminado.')
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
                else:
                    mensaje_error(request)
                    return redirect('detalle-ticket', pk_proyecto, objeto.id)
        else:
            mensaje_error(request)
            return redirect('detalle-ticket', pk_proyecto, objeto.id)
    else:
        contexto = {
            'ticket': objeto,
            'comentarios': ComentariosTicket.objects.filter(ticket=pk_ticket).order_by('-fecha_creacion'),
            'adjuntos': AdjuntosTicket.objects.filter(ticket=pk_ticket).order_by('fecha_subida'),
            'titulo': f"Ticket {pk_ticket}",
            'admins': RolesProyecto.objects.filter(proyecto=pk_proyecto, tipo='ADMIN', usuario=request.user),
            'proyect_managers': RolesProyecto.objects.filter(proyecto=pk_proyecto, tipo='PROJECT MANAGER',
                                                             usuario=request.user)
        }
        return render(request, 'tracker/detalle-ticket.html', contexto)


@login_required
def cambiar_estado_proyecto(request, pk_proyecto):
    filtro_por_tipo = RolesProyecto.objects.filter(usuario=request.user, proyecto=pk_proyecto)
    objeto = Proyecto.objects.filter(pk=pk_proyecto)

    if filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
            tipo='PROJECT MANAGER') or request.user.is_superuser:

        nuevo_estado = 'ACTIVO'

        if objeto.filter(Q(estado__contains='ACTIVO')):
            nuevo_estado = 'FINALIZADO'

        Proyecto.objects.filter(pk=pk_proyecto).update(estado=nuevo_estado)
        return redirect('detalle-proyecto', pk_proyecto)
    else:
        raise Http404("No existe la página.")


class EditarTicket(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ticket
    fields = ['titulo', 'prioridad', 'tipo', 'descripcion']
    template_name = "tracker/editar-ticket.html"
    extra_context = {'titulo': 'Editar ticket'}

    def form_valid(self, form):
        messages.success(self.request, f'Ticket editado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        mensaje_error(self.request)
        return super().form_invalid(form)

    def test_func(self):
        proyecto = Proyecto.objects.filter(id=self.kwargs.get('pk')).first()
        filtro_por_tipo = RolesProyecto.objects.filter(usuario=self.request.user, proyecto=proyecto)
        return True if filtro_por_tipo.filter(
            Q(tipo='PROJECT MANAGER') | Q(tipo='ADMIN')) or self.request.user.is_superuser else False


@login_required
def cambiar_estado_ticket(request, pk_proyecto, pk, estado):
    filtro_por_tipo = RolesProyecto.objects.filter(usuario=request.user, proyecto=pk_proyecto)

    if filtro_por_tipo.filter(tipo='ADMIN') or filtro_por_tipo.filter(
            tipo='PROJECT MANAGER') or request.user.is_superuser:

        from .models import ESTADO_TICKET
        if estado in [[x[0] for x in ESTADO_TICKET] for b in ESTADO_TICKET][0]:
            Ticket.objects.filter(proyecto=pk_proyecto, id=pk).update(estado=estado)
            messages.success(request, f'Estado cambiado.')
            return redirect('detalle-ticket', pk_proyecto, pk)
        else:
            mensaje_error(request)
            return redirect('detalle-ticket', pk_proyecto, pk)
    else:
        raise Http404("No existe la página.")
