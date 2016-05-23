from django.shortcuts import render, redirect
from decimal import Decimal
from datetime import date

from .models import Player, Match


K = 40

def home(request):
    players = Player.objects.all().order_by('-current_points')
    recent_matches = Match.objects.all().order_by('-timestamp')[:5]

    return render(request, 'home.html', {'players': players, 'matches': recent_matches, 'game': 'rocketl'})


def create_player(request, username):
    try:
        Player.objects.get(username=username)
    except Exception:
        initial_elo = 0
        players = Player.objects.all()
        if len(players) == 0:
            initial_elo = 1600
        else:
            for player in players:
                initial_elo += player.current_points
            initial_elo /= len(players)

        Player.objects.create(
            username=username,
            current_points=initial_elo,
            previous_points=initial_elo
        )

    return redirect('/rocketl')


def create_match(request, player1, player2, player3, player4, score1, score2):
    score1 = int(score1)
    score2 = int(score2)

    if score1 > score2:
        team1_index = 1
        team2_index = 0
    elif score2 > score1:
        team1_index = 0
        team2_index = 1
    else:
        team1_index = 0.5
        team2_index = 0.5

    team1 = [player1, player2]
    team2 = [player3, player4]

    for i in team1:
        player = Player.objects.get(username=i)
        elo = 0
        for j in team2:
            opposing_player = Player.objects.get(username=j)
            elo += calculate(player, opposing_player, team1_index, 1)

        elo /= 2
        player.previous_points = player.current_points
        player.current_points = elo
        if team1_index == 1:
            player.wins += 1
            player.win_streak += 1
        elif team1_index == 0:
            player.losses += 1
            player.win_streak = 0
        else:
            player.draws += 1
            player.win_streak = 0

        player.save()

    for i in team2:
        player = Player.objects.get(username=i)
        elo = 0
        for j in team1:
            opposing_player = Player.objects.get(username=j)
            elo += calculate(player, opposing_player, team2_index, 2)

        elo /= 2
        player.previous_points = player.current_points
        player.current_points = elo
        if team2_index == 1:
            player.wins += 1
            player.win_streak += 1
        elif team2_index == 0:
            player.losses += 1
            player.win_streak = 0
        else:
            player.draws += 1
            player.win_streak = 0

        player.save()

    save_match(team1, team2, score1, score2)
    return redirect('/rocketl')


def delete_player(request, username):
    player = Player.objects.get(username=username)
    player.delete()

    return redirect('/rocketl')


def reset_score(request):
    players = Player.objects.all()
    for player in players:
        player.current_points = 1600
        player.previous_points = 1600
        player.wins = 0
        player.losses = 0
        player.draws = 0
        player.win_streak = 0

        player.save()

    return redirect('/rocketl')


def calculate(player, opposing_player, match_results, team):
    if team == 1:
        opposing_player_points = opposing_player.current_points
    else:
        opposing_player_points = opposing_player.previous_points

    match_results = Decimal(match_results)

    r1 = Decimal(10 ** (player.current_points / 400))
    r2 = Decimal(10 ** (opposing_player_points / 400))

    e1 = r1 / (r1 + r2)
    points = player.current_points + K * (match_results - e1)

    return points


def save_match(team1, team2, score1, score2):
    Match.objects.create(
        team_1_player_1=Player.objects.get(username=team1[0]),
        team_1_player_2=Player.objects.get(username=team1[1]),
        team_2_player_1=Player.objects.get(username=team2[0]),
        team_2_player_2=Player.objects.get(username=team2[1]),
        team_1_score=score1,
        team_2_score=score2,
        date=date.today()
    )