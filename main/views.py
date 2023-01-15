from django.views.generic import TemplateView, DetailView, UpdateView

from main.forms import GameStatusForm
from main.models import Game, Player


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        ctx = {
            'nav': 'home',
        }
        return ctx


class GameDetailView(DetailView):
    template_name = 'main/game_detail.html'
    model = Game


class HxGamePlayersView(DetailView):
    model = Game

    def get_template_names(self):
        return 'main/hxg_players.html'


class HxGameStatusFormView(UpdateView):
    template_name = 'main/hxg_status.html'
    form_class = GameStatusForm
    model = Game

    def get_success_url(self) -> str:
        return self.request.path


class HxGameBuildingsView(DetailView):
    model = Game

    def get_template_names(self):
        return 'main/hxg_buildings.html'


class PlayerDetailView(DetailView):
    template_name = 'main/player_detail.html'
    model = Player


class HxPlayerResourcesView(DetailView):
    model = Player

    def get_template_names(self):
        return 'main/hxp_resources.html'


class HxPlayerFigView(DetailView):
    model = Player

    def get_template_names(self):
        return 'main/hxp_fig.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class HxPlayerFigsView(DetailView):
    model = Player

    def get_template_names(self):
        return 'main/hxp_fig.html'
