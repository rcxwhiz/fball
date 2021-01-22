"""fball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from fball_app.views import (
	Index,
	EnterGame,
	ViewRankings,
	FindRankings,
	ViewSeasonRankings,
	ViewPlayer,
	ViewPlayerRecord,
	FindPlayer,
	AddPlayer,
	AddSeason
)

urlpatterns = [
	path('admin/', admin.site.urls),

	path('', Index.as_view(), name='index'),
	path('enter_game/', EnterGame.as_view(), name='enter_game'),
	path('view_rankings/', ViewRankings.as_view(), name='view_rankings'),
	path('find_rankings/', FindRankings.as_view(), name='find_rankings'),
	path('view_rankings/<int:season>', ViewSeasonRankings.as_view(), name='view_season_rankings'),
	path('view_player/', ViewPlayer.as_view(), name='view_player'),
	path('view_player/<str:player>/', ViewPlayerRecord.as_view(), name='view_player_record'),
	path('find_player/', FindPlayer.as_view(), name='find_player'),
	path('add_player/', AddPlayer.as_view(), name='add_player'),
	path('add_season/', AddSeason.as_view(), name='add_season')
]
