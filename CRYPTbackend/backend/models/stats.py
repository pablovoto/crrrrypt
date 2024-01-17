
from django.db import models
from . import Client, Game, TypeStat
class Stat(models.Model):
    
    stat_type = models.ForeignKey(TypeStat, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    # value = models.IntegerField()

    def __str__(self):
        return f"{self.client.user_client.first_name} {self.client.user_client.last_name}'s {self.stat_type.name} in {self.game.game_type} between {self.game.start_time} and {self.game.end_time} at {self.created_at}"
