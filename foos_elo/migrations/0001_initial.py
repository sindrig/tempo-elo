# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('team_1_score', models.CharField(max_length=2)),
                ('team_2_score', models.CharField(max_length=2)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('username', models.TextField(unique=True)),
                ('current_points', models.DecimalField(decimal_places=0, max_digits=5, default=1600)),
                ('previous_points', models.DecimalField(decimal_places=0, max_digits=5, default=1600)),
                ('wins', models.DecimalField(decimal_places=0, max_digits=4, default=0)),
                ('losses', models.DecimalField(decimal_places=0, max_digits=4, default=0)),
                ('draws', models.DecimalField(decimal_places=0, max_digits=4, default=0)),
                ('win_streak', models.DecimalField(decimal_places=0, max_digits=4, default=0)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='team_1_player_1',
            field=models.ForeignKey(to='foos_elo.Player', related_name='aurochs'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1_player_2',
            field=models.ForeignKey(to='foos_elo.Player', related_name='beasts'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2_player_1',
            field=models.ForeignKey(to='foos_elo.Player', related_name='goers'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2_player_2',
            field=models.ForeignKey(to='foos_elo.Player', related_name='fangs'),
        ),
    ]
