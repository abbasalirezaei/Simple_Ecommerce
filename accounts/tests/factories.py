from django.contrib.auth import get_user_model
User = get_user_model()

import factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    email = factory.Sequence(lambda n: f"testuser{n}@example.com")
    password = "StrongPass123"
    verified = True
    is_active = True