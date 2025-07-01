from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from accounts.models.profiles import Profile
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@shared_task
def send_activation_email_task(user_id, email):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return "User not found"

    token = get_tokens_for_user(user)
    activation_link = f"http://localhost:8000/accounts/api/v1/activation/confirm/{token}"
    context = {"activation_link": activation_link}

    subject = "Activate Your Account"
    from_email = settings.EMAIL_HOST_USER
    text_content = f"Your account activation link:\n{activation_link}"
    html_content = render_to_string("email/activation_email.html", context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
