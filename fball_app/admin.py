from django.contrib import admin

from fball_app.models import (
	Season,
	Player,
	PlayerSeasonRecord,
	Game
)

admin.site.register(Season)
admin.site.register(Player)
admin.site.register(PlayerSeasonRecord)
admin.site.register(Game)
