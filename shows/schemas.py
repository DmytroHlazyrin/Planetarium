from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter, OpenApiExample
)

ticket_list_schema = extend_schema(
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

astronomy_show_list_schema = extend_schema(
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
                description="An example response body for list astronomy show",
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
                description="An example request body for "
                            "creating an astronomy show.",
                value={
                    "title": "Galactic Journey",
                    "description": "Explore the galaxy...",
                    "show_theme": [1, 2],
                    "image": "base64_image_data"
                }
            ),
        ]
    )

planetarium_dome_list_schema = extend_schema(
        parameters=[
            OpenApiParameter(name="planetarium_name", type=OpenApiTypes.STR,
                             description="Filter by planetarium_name(name)"),
            OpenApiParameter(name="rows", type=OpenApiTypes.INT,
                             description="Filter by rows(rows)"),
            OpenApiParameter(name="seats_in_row", type=OpenApiTypes.INT,
                             description="Filter by seats_in_row"),
        ],
        examples=[
            OpenApiExample(
                "List Example",
                summary="Example of listing planetarium domes",
                description="An example response body "
                            "for listing planetarium domes.",
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
                description="An example request body "
                            "for creating a planetarium dome.",
                value={
                    "name": "Main Dome",
                    "rows": 20,
                    "seats_in_row": 30
                }
            ),
        ]
    )

show_session_list_schema = extend_schema(
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
                description="An example response body "
                            "for listing show sessions.",
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
                description="An example request body "
                            "for creating a show session.",
                value={
                    "astronomy_show": 1,
                    "planetarium_dome": 1,
                    "show_time": "2024-06-10T14:00:00Z",
                    "price": "20.00"
                }
            ),
        ]
    )

show_theme_list_schema = extend_schema(
        parameters=[
            OpenApiParameter(name="show_theme_name", type=OpenApiTypes.STR,
                             description="Filter by theme name"),
        ],
    )

reservation_list_schema = extend_schema(
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
                description="An example response body "
                            "for listing reservations.",
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
                description="An example request body "
                            "for creating a reservation.",
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
