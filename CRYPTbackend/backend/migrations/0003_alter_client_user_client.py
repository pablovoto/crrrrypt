# Generated by Django 4.2.3 on 2023-12-06 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_client_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='user_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
