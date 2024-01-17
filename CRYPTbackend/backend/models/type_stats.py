from django.db import models
from . import Company

class TypeStat(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # parent_stat = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_stat')
    name = models.CharField(max_length=255)
    def __str__(self):
       return self.name 

