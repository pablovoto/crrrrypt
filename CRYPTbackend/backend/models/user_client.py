from django.db import models

from backend.models import CustomUser

class ClientType(models.TextChoices):
    TEACHER = "T", "Teacher"
    PARTICULAR = "P", "Particular"
    STUDENT = "S", "Student"

class Client(models.Model):
    user_client = models.ForeignKey(CustomUser, on_delete=models.CASCADE,unique=True, related_name='client')
    teacher = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    company= models.ForeignKey('Company', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=ClientType.choices, default=ClientType.PARTICULAR)
    
    class Meta:
        db_table = "client"
    
    def __str__(self):
        
        return self.user_client.first_name + " " + self.user_client.last_name + " " + self.type 
    
    