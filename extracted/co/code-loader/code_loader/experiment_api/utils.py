from dataclasses import asdict, is_dataclass
import random
import requests
from typing import Any, Dict, Union
from urllib.parse import urljoin
from code_loader.experiment_api.types import ApiMetricValue, MetricValue, NumericMetricValue, StringMetricValue


def upload_file(url: str, file_path: str)-> None:
    with open(file_path, "rb") as f:
        requests.put(url, data=f, timeout=12_000)

def to_dict_no_none(data: Any)-> Union[Dict[str, Any], Any]:
    if is_dataclass(data):
        data = asdict(data)
    if isinstance(data, dict):
        return {k: to_dict_no_none(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [to_dict_no_none(item) for item in data]
    else:
        return data

def join_url(base_url: str, post_path: str)-> str:
    if not base_url.endswith('/'):
        base_url += '/'
    if post_path.startswith('/'):
        post_path = post_path[1:]
    return urljoin(base_url, post_path)

def to_api_metric_value(value: MetricValue) -> ApiMetricValue:
    if isinstance(value, float) or isinstance(value, int):
        return NumericMetricValue(value=value)
    elif isinstance(value, str):
        return StringMetricValue(value=value)
    else:
        raise Exception(f"Unsupported metric value type: {type(value)}")


def generate_experiment_name() -> str:
    words = {
        "adjectives": [
            "Brave", "Clever", "Fierce", "Mysterious", "Swift", "Ancient", "Luminous", 
            "Bold", "Majestic", "Noble", "Silent", "Vibrant", "Eternal", "Mystic", 
            "Radiant", "Whimsical", "Serene", "Fabled", "Shadowy", "Enigmatic", "Fearless"
        ],
        "animals": [
            "Tiger", "Phoenix", "Dragon", "Griffin", "Falcon", "Wolf", "Eagle", 
            "Lion", "Panther", "Hawk", "Unicorn", "Bear", "Raven", "Fox", "Cobra", 
            "Leopard", "Serpent", "Shark", "Owl", "Stag", "Hound", "Basilisk"
        ],
        "colors": [
            "Crimson", "Azure", "Emerald", "Golden", "Silver", "Midnight", "Scarlet", 
            "Ivory", "Obsidian", "Sapphire", "Ruby", "Onyx", "Amber", "Copper", 
            "Pearl", "Amethyst", "Topaz", "Jade", "Bronze", "Verdant", "Indigo"
        ],
        "elements": [
            "Fire", "Water", "Earth", "Air", "Lightning", "Shadow", "Ice", 
            "Storm", "Light", "Darkness", "Sun", "Moon", "Void", "Spirit", 
            "Flame", "Ocean", "Wind", "Frost", "Thunder", "Blaze", "Mist"
        ],
        "objects": [
            "Blade", "Crown", "Shield", "Spear", "Wings", "Orb", "Heart", 
            "Soul", "Flame", "Key", "Ring", "Sword", "Chalice", "Banner", 
            "Gem", "Mirror", "Scroll", "Stone", "Throne", "Helm", "Talisman"
        ]
    }

    pattern = random.choice([
        "{adjectives} {animals}",
        "{colors} {animals}",
        "{elements} {animals}",
        "{adjectives} {objects}",
        "{colors} {objects}",
        "{elements} {objects}",
        "{adjectives} {elements}",
        "{adjectives} {colors}"
    ])

    return pattern.format(
        adjectives=random.choice(words["adjectives"]),
        animals=random.choice(words["animals"]),
        colors=random.choice(words["colors"]),
        elements=random.choice(words["elements"]),
        objects=random.choice(words["objects"])
    )