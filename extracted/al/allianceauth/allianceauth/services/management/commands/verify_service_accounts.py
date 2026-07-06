from django.core.management.base import BaseCommand

from allianceauth.authentication.models import User
from allianceauth.services.tasks import validate_services


class Command(BaseCommand):
    help = "Ensures all service accounts belong to users with required permissions."

    def handle(self, *args, **options):
        for u in User.objects.all():
            validate_services(u.pk)
        self.stdout.write(self.style.SUCCESS('Verified all user service accounts.'))
