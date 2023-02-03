from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from .models import Announcement, Response
from .filters import BoardFilter, RespFilter
from .forms import AnnForm, RespForm, MailForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.object.author == self.request.user or
                Response.objects.filter(announcement=self.object, responser=self.request.user).exists()):
            resp = False
        else:
            resp = True
        context['resp'] = resp
        return context

class AnnCreate(LoginRequiredMixin, CreateView):
    form_class = AnnForm
    model = Announcement
    template_name = 'ann_edit.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object.author = self.request.user
        self.object.save()
        return result

class AnnUpdate(LoginRequiredMixin, UpdateView):
    form_class = AnnForm
    model = Announcement
    template_name = 'ann_edit.html'

    def get_object(self, queryset=None):
        initial = super(AnnUpdate, self).get_object(queryset)
        if initial.author != self.request.user:
            raise PermissionDenied('Разрешено редактировать только свои объявления')
        return initial


class RespCreate(LoginRequiredMixin, CreateView):
    form_class = RespForm
    model = Response
    template_name = 'resp_edit.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        self.object.responser = self.request.user
        if Announcement.objects.filter(id=self.kwargs['pk']).exists():
            ann = Announcement.objects.get(id=self.kwargs['pk'])
        else:
            self.object.delete()
            raise Http404('Вы пытаетесь откликнуться на несуществующее объявление')
        self.object.announcement = ann
        if self.object.responser == self.object.announcement.author:
            self.object.delete()
            raise Http404('Вы пытаетесь откликнуться на собственное объявление')
        if Response.objects.filter(announcement=self.object.announcement, responser=self.object.responser):
            self.object.delete()
            raise Http404('Вы уже откликались на это объявление')
        self.object.save()
        lst=[]
        lst.append(self.object.announcement.author.email)
        send_mail(
            subject=f'Новый отклик!',
            message=f'Дорогой {self.object.announcement.author.username}, на ваше объявление'
                    f'{self.object.announcement.title} получен новый отклик от'
                    f'пользователя {self.object.responser.username}',
            from_email='da3c709e-298c-4bc6-98b5-30bfc7892069@debugmail.io',
            recipient_list=lst
        )
        return result

class RespDetail(DetailView):
    model = Response
    template_name = 'resp_d.html'
    context_object_name = 'resp'

class RespMy(LoginRequiredMixin, ListView):
    model = Response
    ordering = '-time_creating'
    template_name = 'respmy.html'
    context_object_name = 'resps'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RespFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['user_id'] = self.request.user.id
        return context

@login_required
def resp_acc(request, **kwargs):
    user = request.user
    resp_id = kwargs.get('pk')
    if Response.objects.filter(id=resp_id).exists():
        resp = Response.objects.get(id=resp_id)
    else:
        raise Http404('Такого отклика не существует')
    if resp.announcement.author == user:
        resp.status = Response.accepted
    else:
        raise PermissionDenied('У вас нет прав на изменение статуса этого отклика')
    resp.save()
    lst = []
    lst.append(resp.responser.email)
    send_mail(
        subject=f'Ваш отклик принят!',
        message=f'Дорогой {resp.responser.username}, ваш отклик на объявление {resp.announcement.title} принят'
                f'автором объявления {resp.announcement.author.username}',
        from_email='da3c709e-298c-4bc6-98b5-30bfc7892069@debugmail.io',
        recipient_list=lst
    )
    return redirect('resp_my')

@login_required
def resp_rej(request, **kwargs):
    user = request.user
    resp_id = kwargs.get('pk')
    if Response.objects.filter(id=resp_id).exists():
        resp = Response.objects.get(id=resp_id)
    else:
        raise Http404('Такого отклика не существует')
    if resp.announcement.author == user:
        resp.status = Response.rejected
    else:
        raise PermissionDenied('У вас нет прав на изменение статуса этого отклика')
    resp.save()
    return redirect('resp_my')

@login_required
def mass_mail(request, **kwargs):
    if not request.user.is_staff:
        raise PermissionDenied('У вас нет прав на это действие')
    if request.method == 'GET':
        form = MailForm()
    elif request.method == 'POST':
        form = MailForm(request.POST)
        lst = []
        users = User.objects.all()
        for i in users:
            lst.append(i.email)
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['text'],
                from_email='da3c709e-298c-4bc6-98b5-30bfc7892069@debugmail.io',
                recipient_list=lst
            )
        else:
            raise PermissionDenied('Неверный запрос')
        return redirect('board')
    return render(request, 'mail.html', {'form': form})
