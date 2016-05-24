from datetime import date
from decimal import Decimal

from django.shortcuts import redirect, render

from .models import Match, Player
from .utils import validate_ecosystem_exists

K = 40


def home(request, ecosystem):
    validate_ecosystem_exists(ecosystem)
    players = Player.objects.filter(
        ecosystem=ecosystem
    ).order_by('-current_points')
    recent_matches = Match.objects.filter(
        team_1_player_1__ecosystem=ecosystem
    ).order_by('-timestamp')[:5]

    return render(
        request,
        'home.html',
        {'players': players, 'matches': recent_matches, 'game': ecosystem}
    )


def create_player(request, ecosystem, username):
    validate_ecosystem_exists(ecosystem)
    try:
        Player.objects.get(username=username, ecosystem=ecosystem)
    except Player.DoesNotExist:
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
            ecosystem=ecosystem,
            current_points=initial_elo,
            previous_points=initial_elo
        )

    return redirect_to_ecosystem_home(ecosystem)


def create_match(request, ecosystem, player1, player2, player3, player4,
                 score1, score2):
    validate_ecosystem_exists(ecosystem)
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
        player = Player.objects.get(
            username=i,
            ecosystem=ecosystem
        )
        elo = 0
        for j in team2:
            opposing_player = Player.objects.get(
                username=j,
                ecosystem=ecosystem
            )
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
        player = Player.objects.get(
            username=i,
            ecosystem=ecosystem
        )
        elo = 0
        for j in team1:
            opposing_player = Player.objects.get(
                username=j,
                ecosystem=ecosystem
            )
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

    save_match(ecosystem, team1, team2, score1, score2)
    return redirect_to_ecosystem_home(ecosystem)


def delete_player(request, ecosystem, username):
    validate_ecosystem_exists(ecosystem)
    player = Player.objects.get(
        username=username,
        ecosystem=ecosystem
    )
    player.delete()

    return redirect_to_ecosystem_home(ecosystem)


def reset_score(request, ecosystem):
    validate_ecosystem_exists(ecosystem)
    players = Player.objects.filter(ecosystem=ecosystem)
    for player in players:
        player.current_points = 1600
        player.previous_points = 1600
        player.wins = 0
        player.losses = 0
        player.draws = 0
        player.win_streak = 0

        player.save()

    return redirect_to_ecosystem_home(ecosystem)


def redirect_to_ecosystem_home(ecosystem):
    return redirect('/%s' % ecosystem)


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


def save_match(ecosystem, team1, team2, score1, score2):
    Match.objects.create(
        team_1_player_1=Player.objects.get(
            username=team1[0],
            ecosystem=ecosystem
        ),
        team_1_player_2=Player.objects.get(
            username=team1[1],
            ecosystem=ecosystem
        ),
        team_2_player_1=Player.objects.get(
            username=team2[0],
            ecosystem=ecosystem
        ),
        team_2_player_2=Player.objects.get(
            username=team2[1],
            ecosystem=ecosystem
        ),
        team_1_score=score1,
        team_2_score=score2,
        date=date.today()
    )
