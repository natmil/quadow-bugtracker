from django import forms

from tracker.models import Proyecto, AdjuntosTicket, ComentariosTicket


class FormularioActualizarProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ('nombre', 'descripcion', 'estado')


class FormularioActualizarImagenProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['imagen']


class FormularioSubirAdjunto(forms.ModelForm):
    class Meta:
        model = AdjuntosTicket
        fields = ['fichero']


class FormularioComentarTicket(forms.ModelForm):
    class Meta:
        model = ComentariosTicket
        fields = ['texto']
