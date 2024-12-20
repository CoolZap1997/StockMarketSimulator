from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def prevent_multiple_superusers(sender, instance, **kwargs):
    if instance.is_superuser and User.objects.filter(is_superuser=True).exists() and not instance.pk:
        # Raise an error if there’s already a superuser and we’re trying to create a new one
        raise ValidationError("Only one superuser is allowed in this system.")
