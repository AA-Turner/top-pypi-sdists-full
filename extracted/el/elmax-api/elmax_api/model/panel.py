import json
from enum import Enum
from typing import Dict, List, Any

import packaging.version

from elmax_api.model.actuator import Actuator
from elmax_api.model.area import Area
from elmax_api.model.cover import Cover
from elmax_api.model.endpoint import DeviceEndpoint
from elmax_api.model.goup import Group
from elmax_api.model.scene import Scene
from elmax_api.model.zone import Zone


class PanelEntry:
    """Representation of an available control panel."""

    def __init__(self, devicehash: str, online: bool, name_by_user: Dict[str, str]):
        """Initialize the new control panel."""
        self._hash = devicehash
        self._online = online
        self._names = name_by_user

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def online(self) -> bool:
        return self._online

    def get_name_by_user(self, username: str) -> str:
        if username not in self._names:
            ValueError(
                "Cannot find the name associated by user %s to device %s",
                username,
                self._hash,
            )
        return self._names.get(username)

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'PanelEntry':
        """Create a new control panel from the API json response"""
        # Convert the data structure so that we have a dictionary of names by user
        name_by_user = dict()
        for entry in response_entry.get("username", []):
            username = entry.get("name")
            name = entry.get("label")
            name_by_user[username] = name

        control_panel = PanelEntry(
            devicehash=response_entry["hash"],
            online=bool(response_entry["centrale_online"]),
            name_by_user=name_by_user,
        )
        return control_panel


class PanelStatus:
    """Representation of a panel status"""

    def __init__(self,
                 panel_id: str,
                 user_email: str,
                 release: str,
                 cover_feature: bool,
                 scene_feature: bool,
                 zones: List[Zone],
                 actuators: List[Actuator],
                 areas: List[Area],
                 groups: List[Group],
                 scenes: List[Scene],
                 covers: List[Cover],
                 push_feature: bool,
                 accessory_type: str,
                 accessory_release: str,
                 *args,
                 **kwargs
                 ):

        self._panel_id = panel_id
        self._user_email = user_email
        self._release = release
        self._cover_feature = cover_feature
        self._scene_feature = scene_feature
        self._zones = zones
        self._actuators = actuators
        self._areas = areas
        self._groups = groups
        self._scenes = scenes
        self._covers = covers
        self._push_feature = push_feature
        self._accessory_type = accessory_type
        self._accessory_release = accessory_release

    @property
    def panel_id(self) -> str:
        return self._panel_id

    @property
    def user_email(self) -> str:
        return self._user_email

    @property
    def release(self) -> str:
        return self._release

    @property
    def cover_feature(self) -> bool:
        return self._cover_feature

    @property
    def scene_feature(self) -> bool:
        return self._scene_feature

    @property
    def zones(self) -> List[Zone]:
        return self._zones

    @property
    def actuators(self) -> List[Actuator]:
        return self._actuators

    @property
    def areas(self) -> List[Area]:
        return self._areas

    @property
    def groups(self) -> List[Group]:
        return self._groups

    @property
    def scenes(self) -> List[Scene]:
        return self._scenes

    @property
    def covers(self) -> List[Cover]:
        return self._covers

    @property
    def all_endpoints(self) -> List[DeviceEndpoint]:
        res = []
        res.extend(self.actuators)
        res.extend(self.areas)
        res.extend(self.groups)
        res.extend(self.scenes)
        res.extend(self.zones)
        res.extend(self.covers)
        return res

    @property
    def push_feature(self) -> bool:
        return self._push_feature

    @property
    def accessory_type(self) -> str:
        return self._accessory_type

    @property
    def accessory_release(self) -> str:
        return self._accessory_release

    def __repr__(self):
        def inspectobj(obj):
            if isinstance(obj,Enum):
                return obj.name
            elif hasattr(obj, "__dict__"):
                return vars(obj)
            else:
                return str(obj)

        return json.dumps(self, default=inspectobj)

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'PanelStatus':
        """Create a new panel status object from the API json response"""
        panel_status = PanelStatus(
            panel_id=response_entry.get('centrale'),
            user_email=response_entry.get('utente'),
            release=response_entry.get('release'),
            cover_feature=response_entry.get('tappFeature'),
            scene_feature=response_entry.get('sceneFeature'),
            push_feature=response_entry.get('pushFeature', False),
            accessory_type=response_entry.get('tipo_accessorio', 'Unknown'),
            accessory_release=response_entry.get('release_accessorio', 'Unknown'),
            zones=[Zone.from_api_response(x) for x in response_entry.get('zone', [])],
            actuators=[Actuator.from_api_response(x) for x in response_entry.get('uscite', [])],
            areas=[Area.from_api_response(x) for x in response_entry.get('aree', [])],
            covers=[Cover.from_api_response(x) for x in response_entry.get('tapparelle', [])],
            groups=[Group.from_api_response(x) for x in response_entry.get('gruppi', [])],
            scenes=[Scene.from_api_response(x) for x in response_entry.get('scenari', [])]
        )
        return panel_status

class EndpointStatus:
    """Representation of an endpoint status"""

    def __init__(self,
                 release: str,
                 cover_feature: bool,
                 scene_feature: bool,
                 zones: List[Zone],
                 actuators: List[Actuator],
                 areas: List[Area],
                 groups: List[Group],
                 scenes: List[Scene],
                 covers: List[Cover],
                 push_feature: bool,
                 accessory_type: str,
                 accessory_release: str,
                 *args,
                 **kwargs):

        self._release = release
        self._cover_feature = cover_feature
        self._scene_feature = scene_feature
        self._zones = zones
        self._actuators = actuators
        self._areas = areas
        self._groups = groups
        self._scenes = scenes
        self._covers = covers
        self._push_feature = push_feature
        self._accessory_type = accessory_type
        self._accessory_release = accessory_release

    @property
    def release(self) -> str:
        return self._release

    @property
    def cover_feature(self) -> bool:
        return self._cover_feature

    @property
    def scene_feature(self) -> bool:
        return self._scene_feature

    @property
    def zones(self) -> List[Zone]:
        return self._zones

    @property
    def actuators(self) -> List[Actuator]:
        return self._actuators

    @property
    def areas(self) -> List[Area]:
        return self._areas

    @property
    def groups(self) -> List[Group]:
        return self._groups

    @property
    def scenes(self) -> List[Scene]:
        return self._scenes

    @property
    def covers(self) -> List[Cover]:
        return self._covers

    @property
    def all_endpoints(self) -> List[DeviceEndpoint]:
        res = []
        res.extend(self.actuators)
        res.extend(self.areas)
        res.extend(self.groups)
        res.extend(self.scenes)
        res.extend(self.zones)
        return res

    @property
    def push_feature(self) -> bool:
        return self._push_feature

    @property
    def accessory_type(self) -> str:
        return self._accessory_type

    @property
    def accessory_release(self) -> str:
        return self._accessory_release

    @staticmethod
    def from_api_response(response_entry: Dict) -> 'EndpointStatus':
        """Create a new endpoint status object from the API json response"""
        status = EndpointStatus(
            release=response_entry.get('release', 'Unknown'),
            cover_feature=response_entry.get('tappFeature', False),
            scene_feature=response_entry.get('sceneFeature', False),
            push_feature=response_entry.get('pushFeature', False),
            accessory_type=response_entry.get('tipo_accessorio', 'Unknown'),
            accessory_release=response_entry.get('release_accessorio', 'Unknown'),
            zones=[Zone.from_api_response(x) for x in response_entry.get('zone', [])],
            actuators=[Actuator.from_api_response(x) for x in response_entry.get('uscite', [])],
            areas=[Area.from_api_response(x) for x in response_entry.get('aree', [])],
            covers=[Cover.from_api_response(x) for x in response_entry.get('tapparelle', [])],
            groups=[Group.from_api_response(x) for x in response_entry.get('gruppi', [])],
            scenes=[Scene.from_api_response(x) for x in response_entry.get('scenari', [])]
        )
        return status