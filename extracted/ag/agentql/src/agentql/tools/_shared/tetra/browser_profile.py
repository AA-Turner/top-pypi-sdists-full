from enum import Enum


class BrowserProfile(Enum):
    """
    Browser profile presets for different use cases.

    - LIGHT: Basic browser profile with standard configurations
    - STEALTH: Enhanced profile with advanced stealth measures
    - TF_BROWSER: TinyFish Browser, an agent-focused browser with advanced anti-detection
    """

    LIGHT = "light"
    STEALTH = "stealth"
    TF_BROWSER = "tf-browser"
