# Generated by Django 5.0.6 on 2024-06-10 17:24

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shows", "0002_showsession_price"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="astronomyshow",
            name="unique_title",
        ),
        migrations.RemoveConstraint(
            model_name="planetariumdome",
            name="unique_name_planetarium",
        ),
        migrations.RemoveConstraint(
            model_name="showtheme",
            name="unique_name",
        ),
        migrations.RemoveConstraint(
            model_name="ticket",
            name="unique_row_seats",
        ),
        migrations.AlterField(
            model_name="astronomyshow",
            name="show_theme",
            field=models.ManyToManyField(
                related_name="astronomy_shows", to="shows.showtheme"
            ),
        ),
        migrations.AlterField(
            model_name="astronomyshow",
            name="title",
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name="planetariumdome",
            name="name",
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name="planetariumdome",
            name="rows",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(50),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="planetariumdome",
            name="seats_in_row",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(50),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="showtheme",
            name="name",
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="shows.reservation",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="row",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="seat",
            field=models.PositiveIntegerField(),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("row", "seat", "show_session"), name="unique_ticket"
            ),
        ),
    ]
