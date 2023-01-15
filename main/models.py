from collections import Counter
from random import choices

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from main.constants import STATUS_NEW, STATUS_BUSY, STATUS_DONE, SHOW_UNUSED, SHOW_HIDDEN, SHOW_NOT_EMPTY, SHOW_ALWAYS, \
    RESOURCE_MONEY


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Slugged(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=False)

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse(f'{type(self).__name__.casefold()}_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(6, '123456789')
        super().save(*args, **kwargs)


class Resource(models.Model):
    SHOW_CHOICES = (
        (0, SHOW_UNUSED),
        (10, SHOW_HIDDEN),
        (20, SHOW_NOT_EMPTY),
        (30, SHOW_ALWAYS),
    )
    money = models.IntegerField(null=True, blank=True)
    show_money = models.IntegerField(choices=SHOW_CHOICES, default=0)

    class Meta:
        abstract = True


class Config(Resource, Timestamp):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'<Config {self.name}>'


class Game(Slugged, Timestamp):
    STATUS_CHOICES = (
        (1, STATUS_NEW),
        (10, STATUS_BUSY),
        (20, STATUS_DONE),
    )
    config = models.ForeignKey(Config, on_delete=models.SET_NULL, null=True, related_name='games')
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)
    init_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = self.get_status_display()
        start = f'started={self.started_at}' if self.started_at else ''
        end = f'ended={self.ended_at}' if self.ended_at else ''
        return f'<Game #{self.pk} {status} {start} {end}>'

    def run_time(self) -> int:
        if not self.started_at:
            return 0
        end_time = self.ended_at or now()
        seconds = max(1, (end_time - self.started_at).seconds)
        return seconds


class Player(Resource, Slugged, Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='players')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return f'<Player #{self.slug} {self.user.username}>'


class Building(Timestamp):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='buildings', null=True, blank=True)
    config = models.ForeignKey(Config, on_delete=models.CASCADE, related_name='buildings', null=True, blank=True)
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='buildings', null=True, blank=True)
    fig_spots = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(default=30)

    def __str__(self):
        game_or_config = self.game or self.config
        owner = self.owner or ''
        stocks = ', '.join(str(s) for s in self.stocks.all())
        return f'<Building {self.name} {game_or_config} {owner} {stocks}>'


class Stock(Timestamp):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='stocks')
    name = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
    available = models.IntegerField(null=True, blank=True)

    def __str__(self):
        costs = ', '.join([str(c) for c in self.costs.all()])
        return f'<Stock {self.name}={self.quantity}, {costs}>'


class Cost(Timestamp):
    COST_CHOICES = [
        [RESOURCE_MONEY, RESOURCE_MONEY],
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='costs')
    name = models.CharField(max_length=250, choices=COST_CHOICES, default=RESOURCE_MONEY)
    amount = models.IntegerField()

    def __str__(self):
        return f'<Cost {self.name}={self.amount}>'


class Fig(Timestamp):
    name = models.CharField(max_length=50)
    config = models.ForeignKey(Config, on_delete=models.SET_NULL, related_name='figs', blank=True, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='figs', blank=True, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='figs', blank=True, null=True)

    def __str__(self):
        return f'<Fig '


class Tx(Timestamp):
    fig = models.ForeignKey(Fig, on_delete=models.CASCADE, related_name='txs')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='txs')
    tx_at = models.DateTimeField()


