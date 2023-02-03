from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Announcement(models.Model):
    tank = 'TN'
    hil = 'HL'
    dd = 'DD'
    torg = 'TG'
    gildm = 'GM'
    kvestg = 'KG'
    kuzn = 'KZ'
    kozhev = 'KV'
    zelev = 'ZL'
    zakl = 'MZ'
    POSITIONS = [
        (tank, 'Танк'),
        (hil, 'Хил'),
        (dd, 'ДД'),
        (torg, 'Торговец'),
        (gildm, 'Гилдмастер'),
        (kvestg, 'Квестгивер'),
        (kuzn, 'Кузнец'),
        (kozhev, 'Кожевник'),
        (zelev, 'Зельевар'),
        (zakl, 'Мастер заклинаний'),
    ]
    type = models.CharField(max_length=2, choices=POSITIONS, default=tank)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_creating = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

class Response(models.Model):
    waiting = 'W'
    accepted = 'A'
    rejected = 'R'
    POSITIONS = [
        (waiting, 'На рассмотрении'),
        (accepted, 'Принят'),
        (rejected, 'Удален'),
    ]
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    responser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=1, choices=POSITIONS, default=waiting)
    time_creating = models.DateTimeField(auto_now_add=True)

