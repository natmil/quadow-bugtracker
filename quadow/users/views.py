from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .formulario import FormularioRegistro, FormularioActualizarUsuario, FormularioActualizarPerfil


def registro(request):
    if request.user.is_authenticated:  # Si el usuario ya está autentificado le redireccionará al inicio
        return redirect('tracker-inicio')
    else:
        # Si hay una petición POST se guardará el usuario, de lo contrario no
        if request.method == 'POST':
            formulario = FormularioRegistro(request.POST)
            # Aquí hace las validaciones pertinentes (que el usuario no exista, la contraseña sea la adeacuada, etc)
            if formulario.is_valid():
                formulario.save()  # Guardamos el nuevo usuario en la base de datos
                usuario = formulario.cleaned_data.get('username')
                # Si el usuario es correcto mostraremos un mensaje como tal con
                messages.success(request, f'Bienvenido {usuario}, tu cuenta ha sido creada.')
                return redirect('login')  # Redireccionamos al usuario al inicio
        else:
            formulario = FormularioRegistro()
        return render(request, 'users/registro.html', {'formulario': formulario, 'titulo': 'Registro'})


@login_required
def perfil(request):
    if request.method == 'POST' and 'editar_usuario' in request.POST:
        formulario_usuario = FormularioActualizarUsuario(request.POST, instance=request.user)
        if formulario_usuario.is_valid():
            formulario_usuario.save()
            messages.success(request, f'Tu perfil ha sido actualizado.')
            return redirect('perfil')
        else:
            messages.error(request, f'Ha ocurrido un error. Por favor, revise los datos.')
            return redirect('perfil')
    elif request.method == 'POST' and 'editar_perfil' in request.POST:
        formulario_perfil = FormularioActualizarPerfil(request.POST, request.FILES, instance=request.user.perfil)
        if formulario_perfil.is_valid():
            formulario_perfil.save()
            messages.success(request, f'Tu perfil ha sido actualizado.')
            return redirect('perfil')
        else:
            messages.error(request, f'Ha ocurrido un error. Por favor, revise los datos.')
            return redirect('perfil')

    contexto = {
        'titulo': request.user.get_full_name()
    }

    return render(request, 'users/perfil.html', contexto)
