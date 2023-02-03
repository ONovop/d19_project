from django import forms
from .models import Announcement

class AnnForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'type',
            'title',
            'text',
        ]
