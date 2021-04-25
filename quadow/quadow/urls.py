"""Quadow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_view


def url_redirect(request):
    return HttpResponseRedirect("/login/")


urlpatterns = [
    path('admin/', admin.site.urls),
    # Si la url termina en 'tracker' llamará al fichero urls de la app tracker
    path('tracker/', include("tracker.urls")),
    path('registro/', user_view.registro, name='registro'),
    path('perfil/', user_view.perfil, name='perfil'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='users/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', next_page='/'), name='logout'),
    path('restablecer-contrasena/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('restablecer-contrasena/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('restablecer-contrasena-confirmado/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('restablecer-contrasena-completado/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', url_redirect),  # TEMPORAL
]

# Temporal, mientras estemos desarrollando dejaremos el acceso estático de /media de esta manera
# https://docs.djangoproject.com/en/3.0/howto/static-files/#serving-static-files-during-development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
