# Generated by Django 4.2 on 2023-06-15 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baseApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
