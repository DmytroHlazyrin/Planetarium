from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from shows.models import Ticket, Reservation, ShowSession, AstronomyShow, PlanetariumDome, ShowTheme
from user.serializers import UserSerializer

class ShowThemeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=ShowTheme.objects.all())])

    class Meta:
        model = ShowTheme
        fields = ("id", "name")

class PlanetariumDomeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[RegexValidator(regex=r'^[A-Za-z0-9\s.,!?;:\'"]+$', message="Invalid characters in name")],
        help_text="Only English characters and spaces are allowed in the name."
    )
    rows = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    seats_in_row = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    capacity = serializers.IntegerField()

    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")

class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "show_theme")

class ShowSessionSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('1000.00'))])
    show_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S"
    )

    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time", "price")

class TicketSerializer(serializers.ModelSerializer):
    row = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    seat = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

class TicketListSerializer(TicketSerializer):
    show_session = serializers.CharField(source="show_session.astronomy_show.title", read_only=True)
    reservation = serializers.CharField(source="reservation.user.username", read_only=True)
    planetarium_dome = serializers.CharField(source="show_session.planetarium_dome.name", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation", "planetarium_dome")

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["row", "seat"]
            )
        ]

    def validate(self, attrs):
        Ticket.validate_seats_row(
            attrs["row"],
            attrs["show_session"].planetarium_dome.rows,
            attrs["seat"],
            attrs["show_session"].planetarium_dome.seats_in_row,
            serializers.ValidationError,
        )
        return attrs

class UserTicketSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email",)

class ReservationDetailSerializer(ReservationSerializer):
    tickets = serializers.SerializerMethodField()
    user = UserTicketSerializer()


    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at", "tickets"]

    def get_tickets(self, obj):
        tickets = Ticket.objects.filter(reservation=obj)
        return TicketDetailSerializer(tickets, many=True).data


class PlanetariumDomeTicketSerializer(PlanetariumDomeSerializer):
    planetarium_name = serializers.CharField(source="name")

    class Meta:
        model = PlanetariumDome
        fields = ("planetarium_name",)

class AstronomyShowTicketSerializer(AstronomyShowSerializer):
    show_name = serializers.CharField(source="title")
    show_theme = serializers.SerializerMethodField()

    class Meta:
        model = AstronomyShow
        fields = ("show_name", "show_theme")

    @staticmethod
    def get_show_theme(obj):
        return [theme.name for theme in obj.show_theme.all()]

class ShowSessionTicketSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeTicketSerializer()
    astronomy_show = AstronomyShowTicketSerializer()

    class Meta:
        model = ShowSession
        fields = ("show_time", "planetarium_dome", "astronomy_show", "price")

class TicketDetailSerializer(serializers.ModelSerializer):
    reservation = serializers.SlugRelatedField(slug_field="user", read_only=True)
    show_session = ShowSessionTicketSerializer()

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "reservation", "show_session")

class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_theme = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "show_theme", "image")

class AstronomyShowCreateSerializer(AstronomyShowSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "show_theme", "image")

class AstronomyShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "image")

class PlanetariumDomeListSerializer(PlanetariumDomeSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")

class PlanetariumDomeCreateSerializer(PlanetariumDomeSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")

class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = serializers.SlugRelatedField(slug_field="title", read_only=True)
    planetarium_dome = serializers.SlugRelatedField(slug_field="name", read_only=True)
    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time", "price")

class ShowSessionCreateSerializer(ShowSessionSerializer):
    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time", "price")

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id"]

    def create(self, validated_data):
        return Reservation.objects.create(user=self.context['request'].user, **validated_data)
