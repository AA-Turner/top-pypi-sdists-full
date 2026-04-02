from enum import Enum


class LOGINPAGELAYOUTEnum(str, Enum):
    ANIMATED_GRADIENT = "animated-gradient"
    BOTTOM_SHEET = "bottom-sheet"
    BRAND_PATTERN = "brand-pattern"
    CAROUSEL = "carousel"
    CENTERED_CARD = "centered-card"
    DIAGONAL = "diagonal"
    DUOTONE = "duotone"
    FULL_HERO = "full-hero"
    GLASSMORPHISM = "glassmorphism"
    GRADIENT = "gradient"
    LOGO_WATERMARK = "logo-watermark"
    MINIMAL = "minimal"
    NEUMORPHISM = "neumorphism"
    NEWS = "news"
    RIGHT_SPLIT = "right-split"
    SEASONAL = "seasonal"
    SPLIT_SCREEN = "split-screen"
    STACKED = "stacked"
    STATS = "stats"
    TABBED = "tabbed"
    TIME_BASED = "time-based"
    VIDEO_BACKGROUND = "video-background"
    WEATHER = "weather"
    WIZARD = "wizard"

    def __str__(self) -> str:
        return str(self.value)
