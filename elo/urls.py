from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^delete_player/(?P<username>\w+)', views.delete_player, name='delete_player'),
    url(r'^create_player/(?P<username>\w+)', views.create_player, name='create_player'),
    url(r'^create_match/(?P<player1>\w+)_(?P<player2>\w+)_(?P<player3>\w+)_(?P<player4>\w+)_(?P<score1>\d{1,2})_(?P<score2>\d{1,2})', views.create_match, name='create_match')
]