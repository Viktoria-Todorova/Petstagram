
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_profile(sender:UserModel, instance:UserModel, created:bool, **kwargs:dict):
    if created:
        Profile.objects.create(user=instance)

        send_mail(
            subject='New account created',
            message='Hello! Congrats on your new profile at Petstagram.',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )