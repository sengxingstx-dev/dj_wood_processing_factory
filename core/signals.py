from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from core.models import WoodInventory


@receiver(pre_save, sender=WoodInventory)
def handle_wood_image_on_update(sender, instance, **kwargs):
    if not instance.image:
        return

    image_changed = False

    if instance.pk:
        try:
            old_instance = sender.objects.only("image").get(pk=instance.pk)
            image_changed = old_instance.image != instance.image
            if image_changed and old_instance.image:
                old_instance.image.delete(save=False)
        except sender.DoesNotExist:
            pass  # Old instance does not exist, this must be a new instance


@receiver(pre_delete, sender=WoodInventory)
def delete_wood_inventory_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
