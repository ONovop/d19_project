from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Announcement
from .filters import BoardFilter
from .forms import AnnForm

class BoardFiltered(ListView):
    model = Announcement
    ordering = '-time_creating'
    template_name = 'board.html'
    context_object_name = 'anns'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BoardFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class BoardMy(LoginRequiredMixin, ListView):
    model = Announcement
    ordering = '-time_creating'
    template_name = 'boardmy.html'
    context_object_name = 'anns'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BoardFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['user_id'] = self.request.user.id
        return context

class AnnDetail(DetailView):
    model = Announcement
    template_name = 'ann_d.html'
    context_object_name = 'ann'

class AnnCreate(LoginRequiredMixin, CreateView):
    form_class = AnnForm
    model = Announcement
    template_name = 'ann_edit.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object.author = self.request.user.id
        self.object.save()
        return result
