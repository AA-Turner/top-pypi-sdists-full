from django.db import migrations
from game.level_management import set_blocks_inner
import json


def new_level(apps, schema_editor):
    Level = apps.get_model("game", "Level")
    Character = apps.get_model("game", "Character")
    Theme = apps.get_model("game", "Theme")
    LevelDecor = apps.get_model("game", "LevelDecor")
    LevelBlock = apps.get_model("game", "LevelBlock")
    Block = apps.get_model("game", "Block")

    def set_decor(level, decor):
        """Helper method creating LevelDecor objects given a list of decor in dictionary form."""
        LevelDecor.objects.filter(level=level).delete()

        level_decors = []
        for data in decor:
            level_decors.append(
                LevelDecor(
                    level_id=level.id, x=data["x"], y=data["y"], decorName=data[
                        "decorName"]
                )
            )
        LevelDecor.objects.bulk_create(level_decors)

    def set_blocks(level, blocks):
        set_blocks_inner(level, blocks, LevelBlock, Block)

    level79 = Level.objects.get(name="79", default=1)
    level78 = Level(
        name="78",
        default=True,
        path='[{"coordinate":[2,7],"connectedNodes":[1]},{"coordinate":[3,7],"connectedNodes":[0,2]},{"coordinate":[4,7],"connectedNodes":[1,3]},{"coordinate":[5,7],"connectedNodes":[2,4]},{"coordinate":[6,7],"connectedNodes":[3,5]},{"coordinate":[7,7],"connectedNodes":[4,6]},{"coordinate":[8,7],"connectedNodes":[5,7]},{"coordinate":[9,7],"connectedNodes":[6,8]},{"coordinate":[9,6],"connectedNodes":[7,9]},{"coordinate":[9,5],"connectedNodes":[8,10]},{"coordinate":[9,4],"connectedNodes":[9,11]},{"coordinate":[9,3],"connectedNodes":[10,12]},{"coordinate":[9,2],"connectedNodes":[11,13]},{"coordinate":[9,1],"connectedNodes":[12,14]},{"coordinate":[9,0],"connectedNodes":[15,13]},{"coordinate":[8,0],"connectedNodes":[16,14]},{"coordinate":[8,1],"connectedNodes":[17,15]},{"coordinate":[8,2],"connectedNodes":[18,16]},{"coordinate":[8,3],"connectedNodes":[19,17]},{"coordinate":[8,4],"connectedNodes":[20,18]},{"coordinate":[8,5],"connectedNodes":[22,21,19]},{"coordinate":[8,6],"connectedNodes":[20]},{"coordinate":[7,5],"connectedNodes":[23,20]},{"coordinate":[6,5],"connectedNodes":[24,22]},{"coordinate":[5,5],"connectedNodes":[25,23]},{"coordinate":[4,5],"connectedNodes":[26,24]},{"coordinate":[3,5],"connectedNodes":[27,25]},{"coordinate":[2,5],"connectedNodes":[62,53,26]},{"coordinate":[1,4],"connectedNodes":[29]},{"coordinate":[1,3],"connectedNodes":[54,28,30]},{"coordinate":[1,2],"connectedNodes":[29,60]},{"coordinate":[1,0],"connectedNodes":[65,60,32]},{"coordinate":[2,0],"connectedNodes":[31,33]},{"coordinate":[3,0],"connectedNodes":[32,34]},{"coordinate":[4,0],"connectedNodes":[33,35]},{"coordinate":[5,0],"connectedNodes":[34,36]},{"coordinate":[6,0],"connectedNodes":[35,38,37]},{"coordinate":[7,0],"connectedNodes":[36]},{"coordinate":[6,1],"connectedNodes":[39,36]},{"coordinate":[6,2],"connectedNodes":[40,38]},{"coordinate":[6,3],"connectedNodes":[42,41,39]},{"coordinate":[6,4],"connectedNodes":[40]},{"coordinate":[5,3],"connectedNodes":[43,44,40,45]},{"coordinate":[4,3],"connectedNodes":[42]},{"coordinate":[5,4],"connectedNodes":[42]},{"coordinate":[5,2],"connectedNodes":[42,46]},{"coordinate":[5,1],"connectedNodes":[47,45]},{"coordinate":[4,1],"connectedNodes":[48,46]},{"coordinate":[3,1],"connectedNodes":[49,47]},{"coordinate":[2,1],"connectedNodes":[50,48]},{"coordinate":[2,2],"connectedNodes":[51,49]},{"coordinate":[2,3],"connectedNodes":[52,50]},{"coordinate":[2,4],"connectedNodes":[51]},{"coordinate":[2,6],"connectedNodes":[27]},{"coordinate":[0,3],"connectedNodes":[55,29,64]},{"coordinate":[0,4],"connectedNodes":[56,54]},{"coordinate":[0,5],"connectedNodes":[57,55]},{"coordinate":[0,6],"connectedNodes":[58,59,56]},{"coordinate":[0,7],"connectedNodes":[57]},{"coordinate":[1,6],"connectedNodes":[57,63,62]},{"coordinate":[1,1],"connectedNodes":[61,30,31]},{"coordinate":[0,1],"connectedNodes":[60]},{"coordinate":[1,5],"connectedNodes":[59,27]},{"coordinate":[1,7],"connectedNodes":[59]},{"coordinate":[0,2],"connectedNodes":[54]},{"coordinate":[0,0],"connectedNodes":[31]}]',
        traffic_lights="[]",
        destinations="[[2,3]]",
        origin='{"coordinate":[2,7],"direction":"E"}',
        max_fuel=99,
        blocklyEnabled=True,
        pythonEnabled=False,
        theme=Theme.objects.get(id=4),
        character=Character.objects.get(id="6"),
        model_solution="[12]",
        next_level=level79,
        disable_route_score=True,
    )
    level78.save()
    set_decor(
        level78,
        json.loads(
            '[{"x":453,"y":592,"decorName":"tree1"},{"x":355,"y":593,"decorName":"tree1"},{"x":729,"y":67,"decorName":"tree2"}]'
        ),
    )
    set_blocks(
        level78,
        json.loads(
            '[{"type":"move_forwards","number":2},{"type":"turn_left"},{"type":"turn_right","number":1},{"type":"turn_around","number":3},{"type":"controls_repeat_while","number":4},{"type":"controls_repeat_until","number":1},{"type":"logic_negate","number":1},{"type":"at_destination","number":1},{"type":"road_exists","number":2},{"type":"dead_end","number":2}]'
        ),
    )

    level77 = Level.objects.get(name="77", default=1)
    level77.next_level = level78
    level77.save()


class Migration(migrations.Migration):
    dependencies = [("game", "0033_recursion_level")]

    operations = [migrations.RunPython(new_level)]
