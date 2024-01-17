from django.db import models
from .user_client import Client

class Game(models.Model):
    GAME_TYPES = (
        ('UTR', 'UTR'),
        ('normal', 'Normal'),
   
    )
    GAME_ENDING_TYPE = (
        ('third_set_normal', 'Third Set Normal'),
        ('super_tie_break', 'Super Tie Break'),
    )
    # user_company = models.ForeignKey(Client, on_delete=models.CASCADE)
    user_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    game_type = models.CharField(max_length=50, choices=GAME_TYPES)
    game_ending_type = models.CharField(max_length=50, choices=GAME_ENDING_TYPE,default='third_set_normal')
    won = models.BooleanField()

    def __str__(self):
        return f"Game {self.game_type} date {self.start_time} of {self.user_client.user_client.username}"
