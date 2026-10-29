from datetime import timedelta

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone


class ResolveDuplicateUidsMigrationTest(TransactionTestCase):
    """0006_discorduser_uid_unique deduplicates before adding the uid constraint (#1408)."""

    app = "discord"
    migrate_from = "0005_alter_discorduser_user"
    migrate_to = "0006_discorduser_uid_unique"

    def _migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([(self.app, target)])
        return executor.loader.project_state([(self.app, target)]).apps

    def setUp(self):
        old_apps = self._migrate(self.migrate_from)
        User = old_apps.get_model("auth", "User")
        DiscordUser = old_apps.get_model("discord", "DiscordUser")

        self.keep_user = User.objects.create(username="keep")
        self.stale_user = User.objects.create(username="stale")
        self.other_user = User.objects.create(username="other")

        shared_uid = 12345
        now = timezone.now()
        DiscordUser.objects.create(
            user=self.stale_user, uid=shared_uid, activated=now - timedelta(days=2)
        )
        DiscordUser.objects.create(
            user=self.keep_user, uid=shared_uid, activated=now
        )
        # a non-duplicated link that must survive untouched
        DiscordUser.objects.create(user=self.other_user, uid=999, activated=now)

    def tearDown(self):
        # restore the latest schema for the rest of the suite
        self._migrate(self.migrate_to)

    def test_keeps_most_recently_activated_and_notifies_the_rest(self):
        new_apps = self._migrate(self.migrate_to)
        DiscordUser = new_apps.get_model("discord", "DiscordUser")
        Notification = new_apps.get_model("notifications", "Notification")

        self.assertSetEqual(
            set(DiscordUser.objects.values_list("user_id", "uid")),
            {(self.keep_user.pk, 12345), (self.other_user.pk, 999)},
        )
        self.assertFalse(
            DiscordUser.objects.filter(user_id=self.stale_user.pk).exists()
        )
        self.assertTrue(
            Notification.objects.filter(user_id=self.stale_user.pk).exists()
        )
        self.assertFalse(
            Notification.objects.filter(user_id=self.keep_user.pk).exists()
        )
