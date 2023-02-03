from django.urls import path
# Импортируем созданное нами представление
from .views import (BoardFiltered, BoardMy, AnnDetail, AnnCreate, AnnUpdate, RespCreate, RespDetail, RespMy,
                    resp_acc, resp_rej, mass_mail)

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', BoardFiltered.as_view(), name='board'),
   path('my/', BoardMy.as_view(), name='my_ann'),
   path('<int:pk>/', AnnDetail.as_view(), name='detail'),
   path('create/', AnnCreate.as_view(), name='create'),
   path('<int:pk>/update', AnnUpdate.as_view(), name='update'),
   path('<int:pk>/response', RespCreate.as_view(), name='response'),
   path('response/<int:pk>', RespDetail.as_view(), name='resp_det'),
   path('response/<int:pk>/acc', resp_acc, name='accept'),
   path('response/<int:pk>/rej', resp_rej, name='reject'),
   path('response/my', RespMy.as_view(), name='resp_my'),
   path('massmail/', mass_mail, name='massmail'),
   ]
