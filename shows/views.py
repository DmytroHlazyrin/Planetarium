from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiExample
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from shows.models import Ticket, AstronomyShow, PlanetariumDome, ShowSession, Reservation, ShowTheme
from shows.permissions import IsAdminOrIfAuthenticatedReadOnly
from shows.serializers import (
    TicketSerializer, TicketDetailSerializer, TicketCreateSerializer,
    TicketListSerializer,
    AstronomyShowListSerializer, AstronomyShowCreateSerializer,
    PlanetariumDomeListSerializer,
    PlanetariumDomeCreateSerializer, ShowSessionListSerializer,
    ShowSessionCreateSerializer,
    ShowThemeSerializer, AstronomyShowImageSerializer, AstronomyShowSerializer,
    PlanetariumDomeSerializer, ReservationSerializer,
    ReservationDetailSerializer, ReservationCreateSerializer,
    ShowSessionSerializer
)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        'show_session__astronomy_show',
        'show_session__planetarium_dome',
        'reservation__user'
    ).prefetch_related('show_session__astronomy_show__show_theme')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketDetailSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(reservation__user=self.request.user).distinct()
        show_session = self.request.query_params.get("show_session")
        reservation = self.request.query_params.get("reservation")
        planetarium_dome = self.request.query_params.get("planetarium_dome")

        if show_session:
            queryset = queryset.filter(show_session__astronomy_show__title__icontains=show_session)
        if reservation:
            queryset = queryset.filter(reservation__user__email__icontains=reservation)
        if planetarium_dome:
            queryset = queryset.filter(show_session__planetarium_dome__name__icontains=planetarium_dome)
        return queryset

    def perform_create(self, serializer):
        reservation_obj = Reservation.objects.create(user=self.request.user)
        serializer.save(reservation=reservation_obj)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="show_session", type=OpenApiTypes.STR,
                             description="Filter by show_session title"),
            OpenApiParameter(name="reservation", type=OpenApiTypes.STR,
                             description="Filter by reservation(username)"),
            OpenApiParameter(name="planetarium_dome", type=OpenApiTypes.STR,
                             description="Filter by planetarium_dome(name)"),
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing tickets",
                description="An example response body for listing tickets.",
                value=[
                    {
                        "id": 1,
                        "show_session": {
                            "astronomy_show": {
                                "title": "Galactic Journey",
                                "description": "Explore the galaxy...",
                                "image": "url_to_image",
                                "show_theme": [{"name": "Space"}]
                            },
                            "planetarium_dome": {
                                "name": "Main Dome",
                                "rows": 20,
                                "seats_in_row": 30
                            },
                            "show_time": "2024-06-10T14:00:00Z",
                            "price": "20.00"
                        },
                        "reservation": {
                            "user": {"email": "sample@email.com"},
                            "created_at": "2024-06-01T10:00:00Z"
                        }
                    }
                ]
            ),
            OpenApiExample(
                "Create Example",
                summary="Example of creating a ticket",
                description="An example request body for creating a ticket.",
                value={
                    "show_session": 1
                }
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all().prefetch_related("show_theme")
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        elif self.action == "upload_image":
            return AstronomyShowImageSerializer
        elif self.action == "create":
            return AstronomyShowCreateSerializer
        return AstronomyShowSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        astronomy_show = self.get_object()
        serializer = self.get_serializer(astronomy_show, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = self.queryset
        show_theme = self.request.query_params.get("show_theme")
        show_name = self.request.query_params.get("show_name")
        description = self.request.query_params.get("description")

        if show_theme:
            queryset = queryset.filter(show_theme__name__icontains=show_theme)
        if show_name:
            queryset = queryset.filter(title__icontains=show_name)
        if description:
            queryset = queryset.filter(description__icontains=description)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="show_theme", type=OpenApiTypes.STR,
                             description="Filter by show_theme(name)"),
            OpenApiParameter(name="show_name", type=OpenApiTypes.STR,
                             description="Filter by show_name(title)"),
            OpenApiParameter(name="description", type=OpenApiTypes.STR,
                             description="Filter by description(description)"),
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing astronomy shows",
                description="An example response body for listing astronomy shows.",
                value=[
                    {
                        "id": 1,
                        "title": "Galactic Journey",
                        "description": "Explore the galaxy...",
                        "show_theme": [{"name": "Space"}],
                        "image": "url_to_image"
                    }
                ]
            ),
            OpenApiExample(
                "Create Example",
                summary="Example of creating an astronomy show",
                description="An example request body for creating an astronomy show.",
                value={
                    "title": "Galactic Journey",
                    "description": "Explore the galaxy...",
                    "show_theme": [1, 2],
                    "image": "base64_image_data"
                }
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer
        elif self.action == "create":
            return PlanetariumDomeCreateSerializer
        return PlanetariumDomeSerializer

    def get_queryset(self):
        queryset = self.queryset
        planetarium_name = self.request.query_params.get("planetarium_name")
        rows = self.request.query_params.get("rows")
        seats_in_row = self.request.query_params.get("seats_in_row")

        if planetarium_name:
            queryset = queryset.filter(name__icontains=planetarium_name)
        if rows:
            queryset = queryset.filter(rows=rows)
        if seats_in_row:
            queryset = queryset.filter(seats_in_row=seats_in_row)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="planetarium_name", type=OpenApiTypes.STR,
                             description="Filter by planetarium_name(name)"),
            OpenApiParameter(name="rows", type=OpenApiTypes.INT,
                             description="Filter by rows(rows)"),
            OpenApiParameter(name="seats_in_row", type=OpenApiTypes.INT,
                             description="Filter by seats_in_row(seats_in_row)"),
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing planetarium domes",
                description="An example response body for listing planetarium domes.",
                value=[
                    {
                        "id": 1,
                        "name": "Main Dome",
                        "rows": 20,
                        "seats_in_row": 30
                    }
                ]
            ),
            OpenApiExample(
                "Create Example",
                summary="Example of creating a planetarium dome",
                description="An example request body for creating a planetarium dome.",
                value={
                    "name": "Main Dome",
                    "rows": 20,
                    "seats_in_row": 30
                }
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related("astronomy_show", "planetarium_dome")
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "create":
            return ShowSessionCreateSerializer
        return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        show_name = self.request.query_params.get("show_name")
        description = self.request.query_params.get("description")
        planetarium_dome = self.request.query_params.get("name")
        show_time = self.request.query_params.get("show_time")
        price = self.request.query_params.get("price")

        if show_name:
            queryset = queryset.filter(astronomy_show__title__icontains=show_name)
        if description:
            queryset = queryset.filter(astronomy_show__description__icontains=description)
        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__name__icontains=planetarium_dome)
        if show_time:
            queryset = queryset.filter(show_time__icontains=show_time)
        if price:
            queryset = queryset.filter(price=price)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="show_name", type=OpenApiTypes.STR,
                             description="Filter by show_name(name)"),
            OpenApiParameter(name="description", type=OpenApiTypes.STR,
                             description="Filter by description(description)"),
            OpenApiParameter(name="name", type=OpenApiTypes.STR,
                             description="Filter by name(name)"),
            OpenApiParameter(name="show_time", type=OpenApiTypes.DATE,
                             description="Filter by show_time(show_time)"),
            OpenApiParameter(name="price", type=OpenApiTypes.DECIMAL,
                             description="Filter by price"),
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing show sessions",
                description="An example response body for listing show sessions.",
                value=[
                    {
                        "astronomy_show": {
                            "title": "Galactic Journey",
                            "description": "Explore the galaxy...",
                            "show_theme": [{"name": "Space"}]
                        },
                        "planetarium_dome": {
                            "name": "Main Dome",
                            "rows": 20,
                            "seats_in_row": 30
                        },
                        "show_time": "2024-06-10T14:00:00Z",
                        "price": "20.00"
                    }
                ]
            ),
            OpenApiExample(
                "Create Example",
                summary="Example of creating a show session",
                description="An example request body for creating a show session.",
                value={
                    "astronomy_show": 1,
                    "planetarium_dome": 1,
                    "show_time": "2024-06-10T14:00:00Z",
                    "price": "20.00"
                }
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(name="show_theme_name", type=OpenApiTypes.STR,
                             description="Filter by theme name"),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all().select_related('user')
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReservationDetailSerializer
        elif self.action == "create":
            return ReservationCreateSerializer
        return ReservationSerializer

    def get_queryset(self):
        email = self.request.query_params.get("email")
        queryset = self.queryset
        if email:
            queryset = queryset.filter(user__email__icontains=email)
        return queryset.filter(user=self.request.user).distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                description="Filter by user(email)",
            )
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing reservations",
                description="An example response body for listing reservations.",
                value=[
                    {
                        "id": 1,
                        "user": {
                            "email": "john_doe@example.com",
                        },
                        "created_at": "2024-06-01T10:00:00Z",
                        "tickets": [
                            {
                                "id": 1,
                                "show_session": {
                                    "astronomy_show": {
                                        "title": "Galactic Journey",
                                        "description": "Explore the galaxy...",
                                        "image": "url_to_image",
                                        "show_theme": [{"name": "Space"}]
                                    },
                                    "planetarium_dome": {
                                        "name": "Main Dome",
                                        "rows": 20,
                                        "seats_in_row": 30
                                    },
                                    "show_time": "2024-06-10T14:00:00Z",
                                    "price": "20.00"
                                }
                            }
                        ]
                    }
                ]
            ),
            OpenApiExample(
                "Create Example",
                summary="Example of creating a reservation",
                description="An example request body for creating a reservation.",
                value={
                    "tickets": [
                        {
                            "show_session": 1
                        }
                    ]
                }
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
