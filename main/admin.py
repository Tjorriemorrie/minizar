import logging
from collections import Counter

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html

from main.config import init_config
from main.models import Game, Player, Config, Building, Stock, Cost, Fig

logger = logging.getLogger(__name__)


@admin.action(description='Init config')
def act_init_config(modeladmin, request, queryset):
    logger.info('Taking action init config')
    for obj in queryset:
        init_config(obj)


class PlayerInline(admin.TabularInline):
    model = Player
    fields = ['user']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'player_names', 'play_admin', 'started_at', 'ended_at', 'config', 'init_at', 'buildings_col')
    inlines = [PlayerInline]
    actions = [act_init_config]

    def buildings_col(self, game: Game):
        return ', '.join(str(b) for b in game.buildings.all())

    def player_names(self, game: Game) -> str:
        names = [p.user.username for p in game.players.all()]
        return format_html(', '.join(names))

    def play_admin(self, game: Game) -> str:
        return format_html(f'<a href="{game.get_absolute_url()}" target="_blank">Play page</a>')

    def save_form(self, request, form, change):
        unique_users = Counter([v for k, v in form.data.items() if v and k.endswith('-user')])
        if unique_users.most_common()[0][1] > 1:
            raise ValidationError('Cannot duplicate the same user.')
        return super().save_form(request, form, change)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'game')


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'amount', 'stock']


class CostInline(admin.TabularInline):
    model = Cost
    fields = ['stock', 'name', 'amount']


class StockInline(admin.TabularInline):
    model = Stock
    fields = ['name', 'quantity', 'available']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'quantity', 'available', 'building', 'costs_col']
    inlines = [CostInline]

    def costs_col(self, stock: Stock):
        costs = ', '.join([str(c) for c in stock.costs.all()])
        return costs


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'game', 'config', 'name', 'fig_spots', 'duration', 'owner', 'stocks_col']
    list_select_related = ['game', 'config', 'owner']
    inlines = [StockInline]

    def stocks_col(self, building: Building):
        stocks = ', '.join([str(s) for s in building.stocks.all()])
        return stocks


class BuildingInline(admin.TabularInline):
    model = Building
    fields = ['name']


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'money', 'show_money']
    inlines = [BuildingInline]


@admin.register(Fig)
class FigAdmin(admin.ModelAdmin):
    list_display = ['pk', 'config', 'player', 'building']
