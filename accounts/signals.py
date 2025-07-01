from django.db.models.signals import post_save
from django.dispatch import receiver

# local imports
from .models.users import User
from .models.profiles import Profile
from .tasks import send_activation_email_task

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_activation_email_signal(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        send_activation_email_task.delay(instance.id, instance.email)