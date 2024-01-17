from django.contrib import admin

# Register your models here.
from .models import CustomUser, Company, Client, Game, Stat, TypeStat
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Game)
admin.site.register(Stat)
admin.site.register(TypeStat)