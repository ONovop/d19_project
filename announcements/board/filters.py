import django_filters
from django_filters import FilterSet
from django import forms
from .models import Announcement, Response

class BoardFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    text = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.AllValuesFilter()
    time_creating = django_filters.DateFilter(lookup_expr='gt')
    time_creating.field.widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Announcement
        fields = [
            'title',
            'author',
            'text',
            'time_creating',
        ]

class RespFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'announcement__title': ['icontains'],
            'announcement__type': ['icontains'],
            'text' :['icontains'],
            'time_creating': ['gt'],
        }
