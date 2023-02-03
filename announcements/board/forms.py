from django import forms
from .models import Announcement, Response

class AnnForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'type',
            'title',
            'text',
        ]
class RespForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

class MailForm(forms.Form):
    subject = forms.CharField(label='Тема', required=True)
    text = forms.CharField(label='Сообщение', required=True)
