from django.db import models


class Season(models.Model):
	num = models.IntegerField(verbose_name='Season Number', unique=True)

	def __str__(self):
		return f'Season {self.num}'


class Player(models.Model):
	name = models.CharField(verbose_name='Name', unique=True, max_length=128)
	nickname = models.CharField(verbose_name='Nickname', unique=True, max_length=128)

	def __str__(self):
		return f'{self.name} - {self.nickname}'


class PlayerSeasonRecord(models.Model):
	player = models.ForeignKey(Player, verbose_name='Player', on_delete=models.CASCADE)
	season = models.ForeignKey(Season, verbose_name='Season', on_delete=models.CASCADE)
	played = models.IntegerField(verbose_name='Played')
	wins = models.IntegerField(verbose_name='Wins')
	losses = models.IntegerField(verbose_name='Losses')
	goals_forced = models.IntegerField(verbose_name='Goals Forced')
	goals_allowed = models.IntegerField(verbose_name='Goals Allowed')
	goal_differential = models.IntegerField(verbose_name='Goal Differential')
	power_index = models.FloatField(verbose_name='Power Index')

	def __str__(self):
		return f'{self.season} {self.player.name} {self.wins}-{self.losses}'


class Game(models.Model):
	winner = models.ForeignKey(Player, verbose_name='Winner', on_delete=models.CASCADE, related_name='game_winner', db_column='game_winner')
	loser = models.ForeignKey(Player, verbose_name='Loser', on_delete=models.CASCADE, related_name='game_loser', db_column='game_loser')
	season = models.ForeignKey(Season, verbose_name='Season', on_delete=models.CASCADE)
	winning_score = models.IntegerField(verbose_name='Winning Score')
	losing_score = models.IntegerField(verbose_name='Losing Score')
	time = models.DateTimeField(verbose_name='Time')

	def __str__(self):
		return f'{self.winner} {self.winning_score} - {self.loser} {self.losing_score}'
