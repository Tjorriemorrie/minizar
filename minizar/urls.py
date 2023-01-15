"""minizar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),

    path('game/<slug:slug>', views.GameDetailView.as_view(), name='game_detail'),
    path('hxg/<slug:slug>/status', views.HxGameStatusFormView.as_view(), name='hxg_status'),
    path('hxg/<slug:slug>/players', views.HxGamePlayersView.as_view(), name='hxg_players'),
    path('hxg/<slug:slug>/buildings', views.HxGameBuildingsView.as_view(), name='hxg_buildings'),

    path('player/<slug:slug>', views.PlayerDetailView.as_view(), name='player_detail'),
    path('hxp/<slug:slug>/resources', views.HxPlayerResourcesView.as_view(), name='hxp_resources'),
    path('hxp/<slug:slug>/fig/<int:pk>', views.HxPlayerFigView.as_view(), name='hxp_fig'),

]
