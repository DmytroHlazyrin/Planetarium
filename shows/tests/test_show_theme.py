from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ValidationError

from rest_framework.test import APIClient
from rest_framework import status

from shows.models import ShowTheme
from shows.serializers import ShowThemeSerializer
from shows.tests.default_test_data import user_test, sample_show_theme, admin_test

ShowTheme_URL = reverse("shows:showtheme-list")


class UnauthenticatedShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()

    def test_auth_required(self):
        res = self.client.get(ShowTheme_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowThemeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.admin = admin_test()
        self.client.force_authenticate(self.user)

    def test_list_show_theme(self):
        sample_show_theme()
        sample_show_theme(name="default_theme")
        res = self.client.get(ShowTheme_URL)
        show_theme = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(show_theme, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_create_show_theme(self):
        payload = {"name": "New Show Theme"}
        res = self.client.post(ShowTheme_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_show_theme(self):
        admin = self.admin
        self.client.force_authenticate(admin)

        payload = {"name": "New Show Theme"}
        res = self.client.post(ShowTheme_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class ShowThemeFilteringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_filter_show_theme_name(self):
        show_theme_1 = sample_show_theme(name="Test1")
        show_theme_2 = sample_show_theme(name="Test2")
        show_theme_3 = sample_show_theme(name="No Match")

        res = self.client.get(ShowTheme_URL, {"name": "test"})

        serializer1 = ShowThemeSerializer(show_theme_1)
        serializer2 = ShowThemeSerializer(show_theme_2)
        serializer3 = ShowThemeSerializer(show_theme_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)


class ShowThemeValidateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_validate_show_theme_name_models(self):
        with self.assertRaises(IntegrityError):
            show_theme_object2 = sample_show_theme(name="Test Astronomy")
            show_theme_object_3 = sample_show_theme(name="Test Astronomy")

    def test_validate_astronomy_show_name_serializer(self):
        with self.assertRaises(ValidationError):
            sample_show_theme()
            payload = {
                "name": "New ShowTheme",
            }
            serializer = ShowThemeSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            sample_show_theme(name="Test2")
            payload = {"name": "New ShowTheme"}
            serializer = ShowThemeSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()


class ShowThemeModelsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test()
        self.client.force_authenticate(self.user)

    def test_show_theme_str(self):
        show_theme_1 = sample_show_theme(name="Test1")
        self.assertEqual(show_theme_1.__str__(), "Test1")
