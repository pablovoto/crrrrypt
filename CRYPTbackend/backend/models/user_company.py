from django.db import models

from backend.models import CustomUser


class Company(models.Model):
    user_company = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=30,unique=True)
    lease_date = models.DateField()

    class Meta: #Esta clase es para que el modelo se llame en la base de datos como Company
        db_table = "company"
    def __str__(self):
        return self.company_name + " " + self.lease_date.strftime("%d/%m/%Y") + " " + self.user_company.first_name + " " + self.user_company.last_name

