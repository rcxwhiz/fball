from django import forms

from fball_app.models import Player, Season


class EnterGameForm(forms.Form):
	winner = forms.ModelChoiceField(label='Winner', queryset=Player.objects.order_by('name'), to_field_name='name', empty_label='Choose a winner', required=False)
	winning_score = forms.IntegerField(label='Winning Score', min_value=1, required=False)
	loser = forms.ModelChoiceField(label='Loser', queryset=Player.objects.order_by('name'), to_field_name='name', empty_label='Choose a loser', required=False)
	losing_score = forms.IntegerField(label='Losing Score', min_value=0, required=False)

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get('winner') is None:
			self.add_error('winner', 'Choose a winner')
		if cleaned_data.get('loser') is None:
			self.add_error('loser', 'Choose a loser')
		if cleaned_data.get('winning_score') is None:
			self.add_error('winning_score', 'Enter a winning score')
		if cleaned_data.get('losing_score') is None:
			self.add_error('losing_score', 'Enter a losing score')
		if cleaned_data.get('winner') is not None and cleaned_data.get('winner') == cleaned_data.get('loser'):
			self.add_error('loser', 'Enter different winner and loser')
		if cleaned_data.get('winning_score') is not None and cleaned_data.get('losing_score') is not None and not cleaned_data.get('winning_score') > cleaned_data.get('losing_score'):
			self.add_error('winning_score', 'Winning score must be higher than losing score')
		return cleaned_data


class ChooseSeasonForm(forms.Form):
	season = forms.ModelChoiceField(label='', queryset=Season.objects.order_by('-num'), to_field_name='num', empty_label='Choose a season', required=False)

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get('season') is None:
			self.add_error('season', 'Choose a season')
		return cleaned_data


class ChoosePlayerForm(forms.Form):
	player = forms.ModelChoiceField(label='', queryset=Player.objects.order_by('name'), to_field_name='name', empty_label='Choose a player', required=False)

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get('player') is None:
			self.add_error('player', 'Choose a player')
		return cleaned_data


class AddPlayerForm(forms.Form):
	name = forms.CharField(label='Name', max_length=12, required=False)
	nickname = forms.CharField(label='Nickname', max_length=10, required=False)

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get('name') == '':
			self.add_error('name', 'Enter a name')
		elif Player.objects.filter(name=cleaned_data.get('name')).exists():
			self.add_error('name', 'Name taken')
		if cleaned_data.get('nickname') == '':
			self.add_error('nickname', 'Enter a nickname')
		elif Player.objects.filter(nickname=cleaned_data.get('nickname')).exists():
			self.add_error('nickname', 'Nickname taken')
		return cleaned_data
