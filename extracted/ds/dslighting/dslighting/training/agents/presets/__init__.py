"""
DSLighting Training Agents - Presets

Preset training agent wrappers.
"""
from dslighting.training.agents.presets.aide import AIDETrainingAgent
from dslighting.training.agents.presets.autokaggle import AutoKaggleTrainingAgent
from dslighting.training.agents.presets.data_interpreter import DataInterpreterTrainingAgent

__all__ = [
    "AIDETrainingAgent",
    "AutoKaggleTrainingAgent",
    "DataInterpreterTrainingAgent",
]
