# flake8: noqa

"""
Script to generate many fat links for load testing.

This script can be executed directly from shell.
"""

# Standard Library
import os
import sys
from datetime import timedelta
from pathlib import Path

# Django
from django.utils.crypto import get_random_string

myauth_dir = Path(__file__).parent.parent.parent.parent.parent / "myauth"
sys.path.insert(0, str(myauth_dir))

# Django
import django

# init and setup django project
os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="myauth.settings.local")
django.setup()

# Standard Library
import random

# Django
from django.contrib.auth.models import User
from django.utils.timezone import now

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter

# Alliance Auth AFAT
from afat.models import Fat, FatLink, Log
from afat.tests.fixtures.utils import RequestStub
from afat.utils import write_log

LINKS_NUMBER = 100
MAX_PILOTS_IN_FLEET = 256


characters = list(EveCharacter.objects.all())

print(
    f"Adding {LINKS_NUMBER:,} FAT links with up to {MAX_PILOTS_IN_FLEET} characters each"
)

user = User.objects.first()
creator = user.profile.main_character
fleet_type = "Generated Fleet"

for _ in range(LINKS_NUMBER):
    fat_link = FatLink.objects.create(
        fleet=f"Generated Fleet #{random.randint(a=1, b=1000000000)}",
        hash=get_random_string(length=30),
        creator=user,
        character=creator,
        fleet_type=fleet_type,
        created=now() - timedelta(days=random.randint(a=0, b=365)),
    )

    write_log(
        request=RequestStub(user=user),
        log_event=Log.Event.CREATE_FATLINK,
        log_text=(
            f'FAT link with name "{fat_link.fleet}" '
            f'(Fleet type: "{fleet_type}") was created'
        ),
        fatlink_hash=fat_link.hash,
    )

    for character in random.sample(
        population=characters, k=random.randint(a=1, b=MAX_PILOTS_IN_FLEET)
    ):
        Fat.objects.create(
            character_id=character.id,
            fatlink=fat_link,
            system="Jita",
            shiptype="Ibis",
        )

    print(".", end="", flush=True)


print("")
print("DONE")
