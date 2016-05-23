from django.db import models


ECOSYSTEMS = [
    ('fifa', 'FIFA'),
    ('rocket', 'Rocket League'),
    ('foos', 'Foosball')
]


class Player(models.Model):
    username = models.TextField()
    ecosystem = models.TextField(choices=ECOSYSTEMS)
    enabled = models.BooleanField(default=True)

    current_points = models.DecimalField(
        decimal_places=0, max_digits=5, default=1600)
    previous_points = models.DecimalField(
        decimal_places=0, max_digits=5, default=1600)
    wins = models.DecimalField(decimal_places=0, max_digits=4, default=0)
    losses = models.DecimalField(decimal_places=0, max_digits=4, default=0)
    draws = models.DecimalField(decimal_places=0, max_digits=4, default=0)
    win_streak = models.DecimalField(decimal_places=0, max_digits=4, default=0)

    class Meta:
        unique_together = 'username', 'ecosystem'

    def __str__(self):
        return '%s in [%s]' % (self.username, self.ecosystem)


class Match(models.Model):
    team_1_player_1 = models.ForeignKey(Player, on_delete=models.PROTECT,
                                        related_name='aurochs')
    team_1_player_2 = models.ForeignKey(Player, on_delete=models.PROTECT,
                                        related_name='beasts')
    team_2_player_1 = models.ForeignKey(Player, on_delete=models.PROTECT,
                                        related_name='goers')
    team_2_player_2 = models.ForeignKey(Player, on_delete=models.PROTECT,
                                        related_name='fangs')
    team_1_score = models.CharField(max_length=2)
    team_2_score = models.CharField(max_length=2)
    date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)
