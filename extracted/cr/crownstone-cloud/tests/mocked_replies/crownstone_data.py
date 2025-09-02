"""Mock replies from the cloud for Crownstone data."""

crownstone_data = [
    {
        "name": "my_awesome_crownstone",
        "address": "address",
        "type": "PLUG",
        "dimmingEnabled": "false",
        "major": 69,
        "minor": 69,
        "uid": 1,
        "icon": "fiCS1-desk-lamp-2",
        "tapToToggle": "true",
        "firmwareVersion": "5.0.1",
        "bootloaderVersion": "2.1.0",
        "hardwareVersion": "101020100000000000000000000QFAAB0",
        "hidden": "false",
        "locked": "false",
        "id": "my_awesome_crownstone_id",
        "locationId": "location_id",
        "sphereId": "my_awesome_sphere_id",
        "createdAt": "date_created",
        "updatedAt": "date_updated",
        "currentSwitchStateId": "switch_state_id",
        "currentSwitchState": {
            "timestamp": "date_updated",
            "switchState": 0
        },
        "abilities": [
            {
                "type": "dimming",
                "enabled": True,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_1",
                "stoneId": "my_awesome_crownstone_id",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": [
                    {
                        "type": "softOnSpeed",
                        "value": "5",
                        "id": "my_awesome_property_id_1",
                        "abilityId": "my_awesome_ability_id_1",
                        "sphereId": "my_awesome_sphere_id",
                        "createdAt": "date_created",
                        "updatedAt": "date_updated"
                    }
                ]
            },
            {
                "type": "switchcraft",
                "enabled": False,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_2",
                "stoneId": "my_awesome_crownstone_id",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": []
            },
            {
                "type": "tapToToggle",
                "enabled": False,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_3",
                "stoneId": "my_awesome_crownstone_id",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": []
            }
        ]
    },
    {
        "name": "my_awesome_crownstone_2",
        "address": "address",
        "type": "PLUG",
        "dimmingEnabled": "false",
        "major": 69,
        "minor": 69,
        "uid": 1,
        "icon": "fiCS1-desk-lamp-2",
        "tapToToggle": "true",
        "firmwareVersion": "5.0.1",
        "bootloaderVersion": "2.1.0",
        "hardwareVersion": "101020100000000000000000000QFAAB0",
        "hidden": "false",
        "locked": "false",
        "id": "my_awesome_crownstone_id_2",
        "locationId": "location_id",
        "sphereId": "my_awesome_sphere_id",
        "createdAt": "date_created",
        "updatedAt": "date_updated",
        "currentSwitchStateId": "switch_state_id",
        "currentSwitchState": {
            "timestamp": "date_updated",
            "switchState": 0
        },
        "abilities": [
            {
                "type": "dimming",
                "enabled": False,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_4",
                "stoneId": "my_awesome_crownstone_id_2",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": []
            },
            {
                "type": "switchcraft",
                "enabled": False,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_5",
                "stoneId": "my_awesome_crownstone_id_2",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": []
            },
            {
                "type": "tapToToggle",
                "enabled": True,
                "syncedToCrownstone": True,
                "id": "my_awesome_ability_id_6",
                "stoneId": "my_awesome_crownstone_id_2",
                "sphereId": "my_awesome_sphere_id",
                "createdAt": "date_created",
                "updatedAt": "date_updated",
                "properties": [
                    {
                        "type": "rssiOffset",
                        "value": "-10",
                        "id": "my_awesome_property_id_2",
                        "abilityId": "my_awesome_ability_id_6",
                        "sphereId": "my_awesome_sphere_id",
                        "createdAt": "date_created",
                        "updatedAt": "date_updated"
                    }
                ]
            }
        ]
    },
]
