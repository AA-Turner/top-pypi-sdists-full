from django.db import migrations


def migrate_forward(apps, schema_editor):
    import inspect
    import json
    import os

    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    path = f"{currentdir}/industry_activities.json"
    with open(path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    IndustryActivity = apps.get_model("eveuniverse", "EveIndustryActivity")
    for id, row in data.items():
        args = {
            "id": id,
            "defaults": {
                "description": row["description"],
                "name": row["activityName"],
            },
        }
        IndustryActivity.objects.update_or_create(**args)


class Migration(migrations.Migration):
    dependencies = [
        (
            "eveuniverse",
            "0008_eveindustryactivity_alter_evetype_enabled_sections_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(migrate_forward),
    ]
