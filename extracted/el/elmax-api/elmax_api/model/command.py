from enum import Enum


class Command(Enum):
    pass


class SwitchCommand(Command):
    TURN_ON = "on"
    TURN_OFF = "off"


class CoverCommand(Command):
    UP = 1
    DOWN = 2


class AreaCommand(Command):
    ARM_TOTALLY = 4
    ARM_P1_P2 = 3
    ARM_P2 = 2
    ARM_P1 = 1
    DISARM = 0


class SceneCommand(Command):
    TRIGGER_SCENE = "on"

