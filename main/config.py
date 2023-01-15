import logging
from copy import deepcopy

from django.utils.timezone import now

from main.models import Config, Game, Resource, Player


logger = logging.getLogger(__name__)


def init_config(game: Game):
    """Init config for a new game."""
    logger.info(f'Init config ({game.config}) for {game}')
    if not game.config:
        logging.info(f'No config for {game}')
        return
    resources = {}
    for field in Resource._meta.get_fields():
        field_name = field.name
        if v := getattr(game.config, field_name):
            resources[field_name] = v
    Player.objects.filter(game=game).update(**resources)

    # clone buildings from config to game
    game.buildings.all().delete()
    for building in game.config.buildings.all():
        fig_copy = deepcopy(building)
        fig_copy.pk = None
        fig_copy.config = None
        fig_copy.game = game
        fig_copy.save()
        for stock in building.stocks.all():
            stock_copy = deepcopy(stock)
            stock_copy.pk = None
            stock_copy.building = fig_copy
            stock_copy.save()
            for cost in stock.costs.all():
                cost_copy = deepcopy(cost)
                cost_copy.pk = None
                cost_copy.stock = stock_copy
                cost_copy.save()

    # mini figs
    # clone figs from config to game
    for player in game.players.all():
        player.figs.all().delete()
        for fig in game.config.figs.all():
            fig_copy = deepcopy(fig)
            fig_copy.pk = None
            fig_copy.config = None
            fig_copy.player = player
            fig_copy.save()

    game.init_at = now()
    game.save()
    logger.info('Set up the config for game')

