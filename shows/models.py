import pathlib
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import UniqueConstraint
from django.template.defaultfilters import slugify
from Planetarium import settings

def astronomy_show_image_path(instance, filename):
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{pathlib.Path(filename).suffix}"
    return pathlib.Path("upload/astronomy_show/") / filename

class AstronomyShow(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    show_theme = models.ManyToManyField("ShowTheme", related_name="astronomy_shows")
    image = models.ImageField(upload_to=astronomy_show_image_path, null=True)

    def __str__(self):
        return f"name_show: {self.title}, description: {self.description}"

class ShowTheme(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

def validate_price(value):
    if not 0 <= value <= 1000:
        raise ValidationError(_('Price must be between 0 and 1000'), params={'value': value})

class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name="show_sessions")
    planetarium_dome = models.ForeignKey("PlanetariumDome", on_delete=models.CASCADE, related_name="dome_sessions")
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price], default=0)

    def __str__(self):
        return f"Show session: {self.astronomy_show.title}, planetarium: {self.planetarium_dome.name}, show time: {self.show_time}"

class PlanetariumDome(models.Model):
    name = models.CharField(max_length=256, unique=True)
    rows = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    seats_in_row = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def clean(self):
        if not 1 <= self.rows <= 50:
            raise ValidationError("Rows must be in range (1, 50)")
        if not 1 <= self.seats_in_row <= 50:
            raise ValidationError("Seats in row must be in range (1, 50)")

    def __str__(self):
        return f"name: {self.name}, rows: {self.rows}, seats_in_row: {self.seats_in_row}"

class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"reservation for: {self.user}, created at: {self.created_at}"

class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "show_session"], name="unique_ticket")
        ]

    @staticmethod
    def validate_seats_row(
            row, num_row, seat, num_seats_in_row, error_to_raise
    ):
        if not 1 <= row <= num_row:
            raise error_to_raise(
                "the row must be from 1 to {}".format(num_row)
            )
        if not 1 <= seat <= num_seats_in_row:
            raise error_to_raise(
                "the seat must be from 1 to  {}".format(num_seats_in_row)
            )

    def clean(self):
        Ticket.validate_seats_row(
            self.row,
            self.show_session.planetarium_dome.rows,
            self.seat,
            self.show_session.planetarium_dome.seats_in_row,
            ValueError,
        )

    def __str__(self):
        return f"row: {self.row}, seat: {self.seat}, show_session: {self.show_session}, reservation: {self.reservation.user.email}"
