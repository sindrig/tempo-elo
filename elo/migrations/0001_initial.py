# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion

from django.forms.models import model_to_dict

ECOSYSTEMS = [
    ('fifa', 'FIFA'),
    ('rocket', 'Rocket League'),
    ('foos', 'Foosball')
]


def transfer_all_data(apps, schema_editor):
    Player = apps.get_model('elo', 'Player')
    Match = apps.get_model('elo', 'Match')
    for ecosystem, pretty_name in ECOSYSTEMS:
        app_name = '%s_elo' % ecosystem
        OldPlayer = apps.get_model(app_name, 'Player')
        OldMatch = apps.get_model(app_name, 'Match')
        db_alias = schema_editor.connection.alias

        # Dict with "username: Player"
        created_players = {}

        for player in OldPlayer.objects.using(db_alias).all():
            new_player = Player(**model_to_dict(player))
            new_player.ecosystem = ecosystem
            new_player.pk = None
            new_player.save()
            created_players[new_player.username] = new_player
        for match in OldMatch.objects.using(db_alias).select_related().all():
            new_match = Match(
                team_1_score=match.team_1_score,
                team_2_score=match.team_2_score,
                date=match.date,
                timestamp=match.timestamp,
            )
            new_match.pk = None
            player_attrs = ('team_1_player_1', 'team_1_player_2',
                            'team_2_player_1', 'team_2_player_2')
            for attr in player_attrs:
                player_name = getattr(match, attr).username
                setattr(new_match, attr, created_players[player_name])
            new_match.save()


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_elo', '0001_initial'),
        ('rocket_elo', '0001_initial'),
        ('foos_elo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', primary_key=True,
                    serialize=False, auto_created=True)
                 ),
                ('team_1_score', models.CharField(max_length=2)),
                ('team_2_score', models.CharField(max_length=2)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', primary_key=True, serialize=False,
                    auto_created=True)
                 ),
                ('username', models.TextField()),
                ('ecosystem', models.TextField(choices=ECOSYSTEMS)),
                ('enabled', models.BooleanField(default=True)),
                ('current_points', models.DecimalField(
                    default=1600, decimal_places=0, max_digits=5)),
                ('previous_points', models.DecimalField(
                    default=1600, decimal_places=0, max_digits=5)),
                ('wins', models.DecimalField(
                    default=0, decimal_places=0, max_digits=4)),
                ('losses', models.DecimalField(
                    default=0, decimal_places=0, max_digits=4)),
                ('draws', models.DecimalField(
                    default=0, decimal_places=0, max_digits=4)),
                ('win_streak', models.DecimalField(
                    default=0, decimal_places=0, max_digits=4)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('username', 'ecosystem')]),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1_player_1',
            field=models.ForeignKey(
                to='elo.Player', related_name='aurochs',
                on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1_player_2',
            field=models.ForeignKey(
                to='elo.Player', related_name='beasts',
                on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2_player_1',
            field=models.ForeignKey(
                to='elo.Player', related_name='goers',
                on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2_player_2',
            field=models.ForeignKey(
                to='elo.Player', related_name='fangs',
                on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.RunPython(transfer_all_data, migrations.RunPython.noop),
    ]
