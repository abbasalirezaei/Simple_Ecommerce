import pytest

from rest_framework.test import APIClient
from .factories import UserFactory

# Fixtures for reusability
@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def verified_active_user():
    """Create and return a verified, active user."""
    user = UserFactory()
    return user
