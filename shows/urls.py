from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    TicketViewSet,
    ReservationViewSet
)

router = DefaultRouter()
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("show-themes", ShowThemeViewSet)
router.register("planetarium-domes", PlanetariumDomeViewSet)
router.register("show-sessions", ShowSessionViewSet)
router.register("tickets", TicketViewSet)
router.register("reservations", ReservationViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "shows"
