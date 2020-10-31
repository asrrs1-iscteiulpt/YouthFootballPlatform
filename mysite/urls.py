from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from content.views import *

urlpatterns = [
    path('content/', include('content.urls')),
    path('admin/', admin.site.urls),
    url(r'^$', homepage, name='homepage'),
    url(r'^contacts', contacts, name="contacts"),
    url(r'^classoptions', classoptions, name="classoptions"),
    url(r'^statoptions', statoptions, name="statoptions"),
    url(r'^options', options, name="options"),
    url(r'^yfpplayers', yfpplayers, name="yfpplayers"),
    url(r'^players', players, name="players"),
    url(r'^insert_player', insert_player, name="insert_player"),
    url(r'^classification', classification, name="classification"),
    url(r'^matches', matches, name="matches"),
    url(r'^statistics', statistics, name="statistics"),
    url(r'^yfpstats', yfpstats, name="yfpstats"),    
    url(r'^archive', archive, name="archive"),
    url(r'^signup', signup, name="signup")
]