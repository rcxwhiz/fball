from datetime import datetime
from fball_app.models import Player, Season, PlayerSeasonRecord, Game

allowed_ip_addresses = [
	'66.219.252.33'
]


def get_power_change_win(player_record, opponent_record):
	return opponent_record.power_index / player_record.power_index


def get_power_change_loss(player_record, opponent_record):
	return player_record.power_index / opponent_record.power_index


def add_player(form, ip_address):
	if ip_address not in allowed_ip_addresses:
		return {'success': False, 'msg': 'forbidden'}
	try:
		data = form.cleaned_data
		player = Player()
		player.name = data.get('name')
		player.nickname = data.get('nickname')
		player.save()
		for season in Season.objects.all():
			record = PlayerSeasonRecord()
			record.player = player
			record.season = season
			record.played = 0
			record.wins = 0
			record.losses = 0
			record.goals_forced = 0
			record.goals_allowed = 0
			record.goal_differential = 0
			record.power_index = 1.0
			record.save()
		return {'success': True, 'msg': f'Successfully created player {player}'}
	except Exception:
		return {'success': False, 'msg': 'Failed to create player'}


def add_game(form, ip_address):
	if ip_address not in allowed_ip_addresses:
		return {'success': False, 'msg': 'forbidden'}
	try:
		data = form.cleaned_data
		winner = data.get('winner')
		loser = data.get('loser')
		season = Season.objects.order_by('-num').first()
		winning_score = data.get('winning_score')
		losing_score = data.get('losing_score')
		winner_record = PlayerSeasonRecord.objects.get(player=winner, season=season)
		loser_record = PlayerSeasonRecord.objects.get(player=loser, season=season)

		game = Game()
		game.winner = winner
		game.loser = loser
		game.winning_score = winning_score
		game.losing_score = losing_score
		game.season = season
		game.time = datetime.now()
		game.save()

		winner_record.played += 1
		winner_record.wins += 1
		winner_record.goals_forced += game.winning_score
		winner_record.goals_allowed += game.losing_score
		winner_record.goal_differential += game.winning_score
		winner_record.goal_differential -= game.losing_score
		winner_record.power_index += get_power_change_win(winner_record, loser_record)
		winner_record.save()

		loser_record.played += 1
		loser_record.losses += 1
		loser_record.goals_forced += game.losing_score
		loser_record.goals_allowed += game.winning_score
		loser_record.goal_differential += game.losing_score
		loser_record.goal_differential -= game.winning_score
		loser_record.power_index -= get_power_change_loss(loser_record, winner_record)
		if loser_record.power_index < 1.0:
			loser_record.power_index = 1.0
		loser_record.save()

		return {'success': True, 'msg': 'Successfully saved game'}
	except Exception:
		return {'success': False, 'msg': 'Failed to save game'}


def add_season(ip_address):
	if ip_address not in allowed_ip_addresses:
		return {'success': False, 'msg': 'forbidden'}
	try:
		current_season = Season.objects.order_by('-num').get()
		new_season = Season()
		new_season.num = current_season.num + 1
		new_season.save()

		players = Player.objects.all()
		for player in players:
			record = PlayerSeasonRecord()
			record.player = player
			record.season = new_season
			record.played = 0
			record.wins = 0
			record.losses = 0
			record.goals_forced = 0
			record.goals_allowed = 0
			record.goal_differential = 0
			record.power_index = 1.0
			record.save()
		return {'success': True, 'msg': f'Successfully created season {new_season.num}'}
	except Exception:
		return {'success': False, 'msg': 'Failed to create new season'}
