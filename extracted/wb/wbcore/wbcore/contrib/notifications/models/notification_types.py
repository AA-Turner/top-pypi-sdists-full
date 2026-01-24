from contextlib import suppress

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.utils import get_anonymous_user

from wbcore.contrib.authentication.models.users import User
from wbcore.models import WBModel


class NotificationType(WBModel):
    code = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128, default="")
    help_text = models.CharField(max_length=512, default="")

    stale = models.BooleanField(default=False)
    contenttype = models.ForeignKey(
        to="contenttypes.ContentType", related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    resource_button_label = models.CharField(max_length=128)

    default_enable_web = models.BooleanField(default=False)
    default_enable_mobile = models.BooleanField(default=False)
    default_enable_email = models.BooleanField(default=False)
    is_lock = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.resource_button_label:
            if self.contenttype:
                self.resource_button_label = f"Open {self.contenttype.name}"
            else:
                self.resource_button_label = "Open Resource"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Notification Type"
        verbose_name_plural = "Notification Types"

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:notifications:notification_type"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:notifications:notification_type_representation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"


class NotificationTypeSetting(WBModel):
    notification_type = models.ForeignKey(
        to="notifications.NotificationType", related_name="user_settings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(to=User, related_name="wbnotification_user_settings", on_delete=models.CASCADE)

    enable_web = models.BooleanField(default=False)
    enable_mobile = models.BooleanField(default=False)
    enable_email = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user}: {self.notification_type} ({self.enable_web}/{self.enable_mobile}/{self.enable_email})"

    class Meta:
        verbose_name = "Notification Type Setting"
        verbose_name_plural = "Notification Type Settings"
        constraints = [
            UniqueConstraint(
                name="unique_notification_setting",
                fields=["user", "notification_type"],
            )
        ]

    def save(self, *args, **kwargs):
        if self.notification_type.is_lock:
            self.enable_web = self.notification_type.default_enable_web
            self.enable_mobile = self.notification_type.default_enable_mobile
            self.enable_email = self.notification_type.default_enable_email

        super().save(*args, **kwargs)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:notifications:notification_type_setting"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:notifications:notification_type_setting_representation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{notification_type}}"


@receiver(post_save, sender="notifications.NotificationType")
def post_save_notification_type(instance, **kwargs):
    anonymous_user = get_anonymous_user()

    objs = []
    for user in User.objects.filter(~models.Q(pk=anonymous_user.pk)):
        try:
            existing_setting = NotificationTypeSetting.objects.get(user=user, notification_type=instance)
            enable_web = existing_setting.enable_web if not instance.is_lock else instance.default_enable_web
            enable_mobile = existing_setting.enable_mobile if not instance.is_lock else instance.default_enable_mobile
            enable_email = existing_setting.enable_email if not instance.is_lock else instance.default_enable_email
        except NotificationTypeSetting.DoesNotExist:
            enable_web = instance.default_enable_web
            enable_mobile = instance.default_enable_mobile
            enable_email = instance.default_enable_email

        objs.append(
            NotificationTypeSetting(
                notification_type=instance,
                user=user,
                enable_web=enable_web,
                enable_mobile=enable_mobile,
                enable_email=enable_email,
            )
        )
    if objs:
        NotificationTypeSetting.objects.bulk_create(
            objs,
            unique_fields=["notification_type", "user"],
            update_fields=["enable_web", "enable_mobile", "enable_email"],
            update_conflicts=True,
        )


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, raw, **kwargs):
    if created:
        with suppress(User.DoesNotExist):
            anonymous_user = get_anonymous_user()
            if instance.pk == anonymous_user.pk:
                return

        objs = []
        for notification_type in NotificationType.objects.all():
            objs.append(
                NotificationTypeSetting(
                    notification_type=notification_type,
                    user=instance,
                    enable_web=notification_type.default_enable_web,
                    enable_mobile=notification_type.default_enable_mobile,
                    enable_email=notification_type.default_enable_email,
                )
            )
        if objs:
            NotificationTypeSetting.objects.bulk_create(objs, unique_fields=["notification_type", "user"])
