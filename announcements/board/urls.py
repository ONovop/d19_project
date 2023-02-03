from django.urls import path
# Импортируем созданное нами представление
from .views import (BoardFiltered, BoardMy, AnnDetail, AnnCreate)

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
#   path('board/<int:pk>/update', NewsUpdate.as_view(), name='update'),
#   path('response', NewsDelete.as_view(), name='response'),
#   path('response/my', ArticleCreate.as_view(), name='my_resp'),
#   path('user/', IndexView.as_view(), name='UserPage'),
#   path('user/upgrade', upgrade_me, name='Upgrade'),
#   path('user/subscribe/<int:pk>', subscribe_me, name='subscribe'),
   ]
