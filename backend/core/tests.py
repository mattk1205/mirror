from django.urls import reverse
from rest_framework import status
from rest_framework.test import APISimpleTestCase


class HealthTests(APISimpleTestCase):
    def test_health_returns_ok(self):
        response = self.client.get(
            reverse("health"),
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})

