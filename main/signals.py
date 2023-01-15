from typing import Type, Counter

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from main.models import Game


# @receiver(pre_save, sender=Game)
# def check_game_player_uniqueness(sender: Type[Game], instance: Game, **kwargs):
#     unique_users = Counter([p.user.id for p in instance.players.all()])
#     if unique_users.most_common()[0][1] > 1:
#         raise ValidationError('Cannot duplicate the same user.')
#
