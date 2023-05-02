from django.urls import path

from . import views

urlpatterns = [
    path('updatenews', views.updatenews, name='updatenews'),
    path('updateshorts', views.updateshorts, name='updateshorts'),
    path('updateadvise', views.updateadvise, name='updateadvise'),
    path('', views.index, name='index'),
]