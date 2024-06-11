from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from rest_framework.test import APIClient
from rest_framework import status

from shows.models import PlanetariumDome
from shows.serializers import (
    PlanetariumDomeListSerializer,
    PlanetariumDomeCreateSerializer,
)
from shows.tests.default_test_data import (
    user_test,
    admin_test,
    sample_planetarium_dome,
)

Planetarium_Dome_URL = reverse("shows:planetariumdome-list")


class UnauthenticatedPlanetariumDomeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()

    def test_auth_required(self):
        res = self.client.get(Planetarium_Dome_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_list_planetarium_dome(self):
        res = self.client.get(Planetarium_Dome_URL)
        planetarium_dome = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeListSerializer(
            planetarium_dome, many=True
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_create_planetarium_dome(self):
        payload = {"name": "New Show Theme", "rows": 40, "seats_in_row": 50}
        res = self.client.post(Planetarium_Dome_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_planetarium_dome(self):
        admin = admin_test()
        self.client.force_authenticate(admin)

        payload = {"name": "New Show Theme", "rows": 40, "seats_in_row": 50}
        res = self.client.post(Planetarium_Dome_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class PlanetariumDomeFilteringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_filter_planetarium_dome_name(self):
        planetarium_dome_1 = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=200
        )

        planetarium_dome_2 = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=200
        )

        planetarium_dome_3 = sample_planetarium_dome(
            name="No Match", rows=40, seats_in_row=200
        )

        res = self.client.get(
            Planetarium_Dome_URL, {"planetarium_name": "planetarium"}
        )

        serializer1 = PlanetariumDomeListSerializer(planetarium_dome_1)
        serializer2 = PlanetariumDomeListSerializer(planetarium_dome_2)
        serializer3 = PlanetariumDomeListSerializer(planetarium_dome_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_planetarium_rows(self):
        planetarium_dome_1 = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=200
        )

        planetarium_dome_2 = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=200
        )

        planetarium_dome_3 = sample_planetarium_dome(
            name="Planetarium Dome Test3", rows=35, seats_in_row=200
        )

        res = self.client.get(Planetarium_Dome_URL, {"rows": 40})

        serializer1 = PlanetariumDomeListSerializer(planetarium_dome_1)
        serializer2 = PlanetariumDomeListSerializer(planetarium_dome_2)
        serializer3 = PlanetariumDomeListSerializer(planetarium_dome_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_planetarium_seats_rows(self):
        planetarium_dome_1 = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=200
        )

        planetarium_dome_2 = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=200
        )

        planetarium_dome_3 = sample_planetarium_dome(
            name="Planetarium Dome Test3", rows=35, seats_in_row=150
        )

        res = self.client.get(Planetarium_Dome_URL, {"seats_in_row": 200})
        serializer1 = PlanetariumDomeListSerializer(planetarium_dome_1)
        serializer2 = PlanetariumDomeListSerializer(planetarium_dome_2)
        serializer3 = PlanetariumDomeListSerializer(planetarium_dome_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)


class PlanetariumValidateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = admin_test()
        self.client.force_authenticate(self.test_user)

    def test_planetarium_validate_serializers_name(self):
        with self.assertRaises(IntegrityError):
            payload1 = {
                "name": "Test 1",
                "rows": 40,
                "seats_in_row": 50,
            }
            payload2 = {
                "name": "Test 1",
                "rows": 40,
                "seats_in_row": 50,
            }
            serializer1 = PlanetariumDomeCreateSerializer(data=payload1)
            serializer1.is_valid(raise_exception=True)
            serializer1.save()
            serializer2 = PlanetariumDomeCreateSerializer(data=payload2)
            serializer2.is_valid(raise_exception=True)
            serializer2.save()

    def test_planetarium_validate_serializers_rows_seats(self):
        with self.assertRaises(ValidationError):
            payload1 = {
                "name": "Test 1",
                "rows": 400,
                "seats_in_row": 50,
            }
            serializer1 = PlanetariumDomeCreateSerializer(data=payload1)
            serializer1.is_valid(raise_exception=True)

        with self.assertRaises(ValidationError):
            payload2 = {
                "name": "Test 1",
                "rows": 40,
                "seats_in_row": 500,
            }
            serializer2 = PlanetariumDomeCreateSerializer(data=payload2)
            serializer2.is_valid(raise_exception=True)



class PlanetariumModelsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_show_theme_str(self):
        planetarium_dome = sample_planetarium_dome()
        self.assertEqual(planetarium_dome.name.__str__(), "Sample Planetarium Dome")
        self.assertEqual(
            planetarium_dome.__str__(),
            f"name: {planetarium_dome.name}, rows: {planetarium_dome.rows}, seats_in_row: {planetarium_dome.seats_in_row}",
        )
