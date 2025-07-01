import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_can_register():
    client = APIClient()
    payload = {
        "email": "test@example.com",
        "password": "StrongPass123",
        "password1": "StrongPass123",
        "full_name": "ghezbas",
    }
    response = client.post("/accounts/api/v1/registration/", payload)

    assert response.status_code == 201
    assert User.objects.filter(email="test@example.com").exists()


@pytest.mark.django_db
def test_user_can_login():

    user = User.objects.create_user(
        email="testuser@example.com",
        password="StrongPass123"
    )
    user.verified = True
    user.is_active = True
    user.save()
    client = APIClient()
    payload = {
        "email": "testuser@example.com",
        "password": "StrongPass123",

    }
    response = client.post("/accounts/api/v1/jwt/token/create/", payload)

    assert response.status_code == 200
    assert "access" in response.data


