from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nome', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Informações adicionais sobre seu pedido (opcional)'}),
        }