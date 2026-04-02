from django.db import migrations


def migrate_forward(apps, schema_editor):
    import inspect
    import json
    import os

    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    path = f"{currentdir}/eve_unit.json"
    with open(path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    EveUnit = apps.get_model("eveuniverse", "EveUnit")
    for row in data:
        args = {
            "id": row["unitID"],
            "defaults": {
                "name": row["unitName"],
                "display_name": row["displayName"] if row["displayName"] else "",
                "description": row["description"] if row["description"] else "",
            },
        }
        EveUnit.objects.update_or_create(**args)


class Migration(migrations.Migration):
    dependencies = [
        ("eveuniverse", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_forward),
    ]
