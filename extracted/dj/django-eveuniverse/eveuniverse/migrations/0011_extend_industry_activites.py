# A migration to add reactions with ID 11 to industry activites.

from django.db import migrations


def migrate_forward(apps, schema_editor):
    IndustryActivity = apps.get_model("eveuniverse", "EveIndustryActivity")
    args = {
        "id": 11,
        "defaults": {
            "description": "The process of combining raw and intermediate materials to create advanced components",
            "name": "Reactions2",
        },
    }
    IndustryActivity.objects.update_or_create(**args)


class Migration(migrations.Migration):

    dependencies = [
        ("eveuniverse", "0010_alter_eveindustryactivityduration_eve_type_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_forward),
    ]
