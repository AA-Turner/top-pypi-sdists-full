from django.db import migrations, models
from django.db.models import Count, F


def resolve_duplicate_uids(apps, schema_editor):
    """Enforce one Auth account per Discord account (#1408).

    Keeps the most recently activated link for each duplicated Discord uid,
    removes the stale links, and notifies each affected user.
    """
    DiscordUser = apps.get_model("discord", "DiscordUser")
    Notification = apps.get_model("notifications", "Notification")
    db = schema_editor.connection.alias

    duplicate_uids = (
        DiscordUser.objects.using(db)
        .values("uid")
        .annotate(count=Count("uid"))
        .filter(count__gt=1)
        .values_list("uid", flat=True)
    )

    for uid in duplicate_uids:
        links = list(
            DiscordUser.objects.using(db)
            .filter(uid=uid)
            .order_by(F("activated").desc(nulls_last=True), "-user_id")
        )
        for stale in links[1:]:
            Notification.objects.using(db).create(
                user_id=stale.user_id,
                level="warning",
                title="Discord account unlinked",
                message=(
                    "Your Discord account was linked to more than one Alliance "
                    "Auth account. Alliance Auth now allows a Discord account to "
                    "be linked to only one Auth account, so this duplicate link "
                    "was removed. Please reactivate the Discord service if you "
                    "still need access."
                ),
            )
            stale.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("discord", "0005_alter_discorduser_user"),
        ("notifications", "0007_alter_notification_user"),
    ]

    operations = [
        migrations.RunPython(resolve_duplicate_uids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="discorduser",
            name="uid",
            field=models.BigIntegerField(
                help_text="user's ID on Discord", unique=True
            ),
        ),
    ]
