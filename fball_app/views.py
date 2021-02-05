from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView

from fball_app.dao import add_player, add_game, add_season
from fball_app.forms import EnterGameForm, ChooseSeasonForm, ChoosePlayerForm, AddPlayerForm
from fball_app.models import Season, PlayerSeasonRecord, Player, Game


class Index(TemplateView):
	season = Season.objects.order_by('num').first()
	template_name = 'fball_app/index/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = self.season
		return context


class EnterGame(TemplateView):
	season = Season.objects.order_by('-num').first()
	template_name = 'fball_app/enter_game/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = self.season
		context['form'] = EnterGameForm()
		return context

	def post(self, request, *args, **kwargs):
		form = EnterGameForm(request.POST)
		if form.is_valid():
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			result = add_game(form, ip)
			if result['success']:
				return render(request, 'fball_app/success/index.html', {'success_msg': result['msg'], 'return_url': '/enter_game/'})
			elif result['msg'] == 'forbidden':
				return render(request, 'fball_app/not_allowed/index.html', {'return_url': '/enter_game/'})
			else:
				return render(request, 'fball_app/failure/index.html', {'failure_msg': result['msg'], 'return_url': '/enter_game/'})
		return render(request, self.template_name, {'form': form})


class ViewRankings(RedirectView):
	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		season_num = Season.objects.order_by('-num').first().num
		return f'/view_rankings/{season_num}'


class FindRankings(RedirectView):
	permanent = False

	def get(self, request, *args, **kwargs):
		form = ChooseSeasonForm(request.GET)
		if form.is_valid():
			return super().get(self, request, *args, **kwargs)
		return render(request, 'fball_app/view_rankings/index.html', {'form': form})

	def get_redirect_url(self, *args, **kwargs):
		return f'/view_rankings/{self.request.GET.get("season")}'


class ViewSeasonRankings(TemplateView):
	template_name = 'fball_app/view_rankings/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		season_num = self.kwargs['season']
		season = Season.objects.get(num=season_num)
		player_records = PlayerSeasonRecord.objects.filter(season=season).order_by('-power_index', '-goal_differential')
		context['season'] = season
		context['player_records'] = player_records
		context['form'] = ChooseSeasonForm()
		return context


class ViewPlayer(TemplateView):
	season = Season.objects.order_by('-num').first()
	template_name = 'fball_app/view_player/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = self.season
		context['form'] = ChoosePlayerForm()
		return context


class ViewPlayerRecord(TemplateView):
	template_name = 'fball_app/view_player/player.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		player_name = self.kwargs['player']
		player = Player.objects.get(name=player_name)
		player_records = PlayerSeasonRecord.objects.order_by('-season').filter(player=player)
		player_games = Game.objects.filter(Q(winner=player) | Q(loser=player)).order_by('-time')
		context['player'] = player
		context['player_records'] = player_records
		context['player_games'] = player_games
		return context


class FindPlayer(RedirectView):
	permanent = False

	def get(self, request, *args, **kwargs):
		form = ChoosePlayerForm(request.GET)
		if form.is_valid():
			return super().get(self, request, *args, **kwargs)
		return render(request, 'fball_app/view_player/index.html', {'form': form})

	def get_redirect_url(self, *args, **kwargs):
		return f'/view_player/{self.request.GET.get("player")}'


class AddPlayer(TemplateView):
	season = Season.objects.order_by('-num').first()
	template_name = 'fball_app/add_player/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = self.season
		context['form'] = AddPlayerForm()
		return context

	def post(self, request, *args, **kwargs):
		form = AddPlayerForm(request.POST)
		if form.is_valid():
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			result = add_player(form, ip)
			if result['success']:
				return render(request, 'fball_app/success/index.html', {'success_msg': result['msg'], 'return_url': '/add_player/'})
			elif result['msg'] == 'forbidden':
				return render(request, 'fball_app/not_allowed/index.html', {'return_url': '/add_player/'})
			else:
				return render(request, 'fball_app/failure/index.html', {'failure_msg': result['msg'], 'return_url': '/add_player/'})
		return render(request, self.template_name, {'form': form})


class AddSeason(TemplateView):
	season = Season.objects.order_by('-num').first()
	template_name = 'fball_app/add_season/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['season'] = self.season
		context['next_season_num'] = self.season.num + 1
		context['form'] = AddPlayerForm()
		return context

	def post(self, request, *args, **kwargs):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		result = add_season(ip)
		if result['success']:
			return render(request, 'fball_app/success/index.html', {'success_msg': result['msg'], 'return_url': '/add_season/'})
		elif result['msg'] == 'forbidden':
			return render(request, 'fball_app/not_allowed/index.html', {'return_url': '/add_season/'})
		else:
			return render(request, 'fball_app/failure/index.html', {'failure_msg': result['msg'], 'return_url': '/add_season/'})
