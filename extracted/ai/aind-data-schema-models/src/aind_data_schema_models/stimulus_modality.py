"""Stimulus modalities"""

from enum import Enum


class StimulusModality(str, Enum):
    """Stimulus modalities"""

    AUDITORY = "Auditory"
    FREE_MOVING = "Free moving"
    NO_STIMULUS = "No stimulus"
    OLFACTORY = "Olfactory"
    OPTOGENETICS = "Optogenetics"
    VIRTUAL_REALITY = "Virtual reality"
    VISUAL = "Visual"
    WHEEL_FRICTION = "Wheel friction"
