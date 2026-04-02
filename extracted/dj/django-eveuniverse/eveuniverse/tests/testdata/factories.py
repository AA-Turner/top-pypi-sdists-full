from eveuniverse.models import EveEntity

_items = {
    40170698: {
        "itemID": 40170698,
        "itemName": "Colelie VI - Asteroid Belt 1",
        "typeID": 15,
        "typeName": "Asteroid Belt",
        "groupID": 9,
        "groupName": "Asteroid Belt",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "392074567680",
        "y": "78438850560",
        "z": "-199546920960",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.69249999999999989341858963598497211933135986328125,
        "distanceKm": 701983769,
    },
    50011472: {
        "itemID": 50011472,
        "itemName": "Stargate (Deltole)",
        "typeID": 3875,
        "typeName": "Stargate (Gallente System)",
        "groupID": 10,
        "groupName": "Stargate",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "390678650880",
        "y": "78437130240",
        "z": "-199573463040",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.6958999999999999630517777404747903347015380859375,
        "distanceKm": 702495020,
    },
    40170697: {
        "itemID": 40170697,
        "itemName": "Colelie VI",
        "typeID": 13,
        "typeName": "Planet (Gas)",
        "groupID": 7,
        "groupName": "Planet",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "390691127743",
        "y": "78438936622",
        "z": "-199521990101",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.69620000000000015205614545266143977642059326171875,
        "distanceKm": 702535753,
    },
    40170699: {
        "itemID": 40170699,
        "itemName": "Colelie VI - Moon 1",
        "typeID": 14,
        "typeName": "Moon",
        "groupID": 8,
        "groupName": "Moon",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "390796699186",
        "y": "78460132168",
        "z": "-199482549699",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.69620000000000015205614545266143977642059326171875,
        "distanceKm": 702535998,
    },
    40170700: {
        "itemID": 40170700,
        "itemName": "Colelie VI - Moon 2",
        "typeID": 14,
        "typeName": "Moon",
        "groupID": 8,
        "groupName": "Moon",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "390287025280",
        "y": "78357805096",
        "z": "-199058647578",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.699799999999999755573298898525536060333251953125,
        "distanceKm": 703071835,
    },
    40170701: {
        "itemID": 40170701,
        "itemName": "Colelie VI - Moon 3",
        "typeID": 14,
        "typeName": "Moon",
        "groupID": 8,
        "groupName": "Moon",
        "solarSystemID": "30002682",
        "regionID": 10000032,
        "constellationID": 10000032,
        "x": "390135687385",
        "y": "78327421033",
        "z": "-198566076258",
        "security": 0.51238882808862296069918329521897248923778533935546875,
        "distance": 4.70300000000000029132252166164107620716094970703125,
        "distanceKm": 703551499,
    },
}


def _create_evemicros_item(item_id):
    return _items[item_id]


def create_evemicros_response(*item_ids, ok=True):
    return {
        "ok": ok,
        "result": [_create_evemicros_item(item_id) for item_id in item_ids],
    }


def create_eve_entity(**kwargs):
    if "category" not in kwargs:
        kwargs["category"] = EveEntity.CATEGORY_CHARACTER
    return EveEntity.objects.create(**kwargs)


def create_evesdeapi_response(*item_ids):
    return [_create_evesdeapi_item(item_id) for item_id in item_ids]


def _create_evesdeapi_item(item_id):
    item = _items[item_id]
    return {
        "distance": item["distanceKm"],
        "group_id": item["groupID"],
        "group_name": item["groupName"],
        "item_id": item["itemID"],
        "name": item["itemName"],
        "position": {
            "x": item["x"],
            "y": item["y"],
            "z": item["z"],
        },
        "type_id": item["typeID"],
        "type_name": item["typeName"],
    }
