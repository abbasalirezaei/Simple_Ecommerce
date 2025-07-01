# rest_framework imports


from rest_framework import exceptions, serializers

# third party imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# django import
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


from django.utils import timezone
from datetime import timedelta
# locals import

from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, max_length=128)
    password = serializers.CharField(write_only=True, max_length=128)
    full_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password", "password1", "full_name"]

    def validate(self, attrs):
        # Run default validations
        attrs = super().validate(attrs)

        password = attrs.get("password")
        password1 = attrs.get("password1")
        errors = {}

        # Check if both passwords match
        if password != password1:
            errors["password1"] = "Passwords do not match"

        # Validate password strength using Django's built-in validators
        try:
            dummy_user = User(email=attrs.get("email", ""))
            validate_password(password=password, user=dummy_user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        # Remove password1 as it's not a User model field
        validated_data.pop("password1", None)

        # Extract full_name to use for profile after user is saved
        full_name = validated_data.pop("full_name", "")

        # Create the user instance
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            role="reader",
            verified=False,
            is_active=False
        )

        # Update the related profile with full_name
        if hasattr(user, "profile"):
            user.profile.full_name = full_name
            user.profile.save()

        return user


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)

        if not self.user.verified:
            msg = "Unable to log in with provided credentials, first you have to verify your account."
            raise serializers.ValidationError(msg)
        validate_data["user_id"] = self.user.id
        validate_data["user_email"] = self.user.email

        return validate_data


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Ensure the email exists in the system before resending activation.
        """
        user_obj = User.objects.filter(email=value).first()

        if not user_obj:
            raise serializers.ValidationError(
                "No account found with this email.")

        # Store the user instance for later access in the view
        self.user_obj = user_obj
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        errors = {}
        new_password1 = attrs.get("new_password1")
        new_password = attrs.get("new_password")
        if new_password1 != new_password:
            errors["new_passwords"] = ["New Passwords do not match."]

        try:
            validate_password(password=new_password, user=None)
        except exceptions.ValidationError as e:
            errors["new_password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(attrs)

