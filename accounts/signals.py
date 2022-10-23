from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage, BadHeaderError
from django.core.mail.backends.smtp import EmailBackend
from django.contrib.sites.shortcuts import get_current_site
import string
import random

User = get_user_model()
site = get_current_site()


def get_random_password(password_length=20):
    # get random password pf length 8 with letters, digits, and symbols
    include = set(("ascii", "digits"))
    options = {
        "ascii": string.ascii_letters,
        "digits": string.digits,
    }
    characters = []
    for inc in include:
        characters += options[inc]
    return "".join(random.choice(characters) for i in range(password_length))


# send email to user after sign up to verify email
@receiver(post_save, sender=User)
def send_email_after_signup(instance, created, **kwargs):
    if not instance.is_active and not instance.activation_code:
        activation_code = get_random_password(40)
        instance.activation_code = activation_code
        instance.save()

        backend = EmailBackend(
            host='smtp.google.com',
            port='587',
            username='saied.notifier@gmail.com',
            password='ahmed7said',
            use_tls=True,
        )
        email = EmailMessage(
            'Confirm sign up', f'<p>we send this email to confirm your sign up pleaser click on this<a href="{site.domain}/confirm_signup/{activation_code}"><strong>link</strong></a></p>', to=[instance.email], connection=backend, from_email='saied.notifier@gmail.com'
        )
        email.content_subtype = "html"
        email.send()
