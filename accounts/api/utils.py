from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import threading
import logging

class EmailThread(threading.Thread):
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        try:
            self.email_obj.send()
            logging.info("Activation email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")



def get_tokens_for_user(user):
    """Generate and return a JWT access token for the given user."""
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)


def send_activation_email(user, email):
    """Generate activation token and send an activation email asynchronously."""
    # generate token
    token = get_tokens_for_user(user)
    # Define email parameters
    subject = "Activate Your Account"
    from_email = settings.EMAIL_HOST_USER
    activation_link = f"http://localhost:8000/accounts/api/v1/activation/confirm/{token}"
    context = {"activation_link": activation_link}

    # Render email content
    text_content = f"Your account activation link:\n{activation_link}"
    html_content = render_to_string("email/activation_email.html", context)

    # Create the email object
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, "text/html")

    # Send email asynchronously using threading
    EmailThread(msg).start()



def is_premium_user(user):
    """
    Check if the user has an active premium status.
    Works only if user has a related profile with is_premium and premium_expiry.
    """
    profile = getattr(user, "profile", None)
    if not profile:
        return False

    return profile.is_premium and (not profile.premium_expiry or profile.premium_expiry > timezone.now())
