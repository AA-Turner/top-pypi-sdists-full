# src/matrice/data_processing/augmentation_utils/strategies/__init__.py

# Manual imports - more reliable and explicit
from .bit_depth_reduction import BitDepthReductionAugmentation
from .blur import BlurAugmentation  # Replace with actual class name
from .brightness_contrast import BrightnessContrastAugmentation  # Replace with actual class name
from .color_jitter import ColorJitterAugmentation  # Replace with actual class name
from .compression_artifacts import CompressionArtifactsAugmentation  # Replace with actual class name
from .downscale_upscale import DownscaleUpscaleAugmentation  # Replace with actual class name
from .film_grain import FilmGrainAugmentation  # Replace with actual class name
from .flip import HorizontalFlipAugmentation  # Replace with actual class name
from .fog import FogAugmentation  # Replace with actual class name
from .horizontal_flip import HorizontalFlipAugmentation  # Replace with actual class name
from .hsv import HueSaturationValueAugmentation  # Replace with actual class name
from .iso_noise import ISONoiseAugmentation  # Replace with actual class name
from .low_light import LowLightSimulationAugmentation  # Replace with actual class name
from .posterize import PosterizeAugmentation  # Replace with actual class name
from .rain import RainAugmentation  # Replace with actual class name
from .random_affine import RandomAffineAugmentation  # Replace with actual class name
from .salt_pepper import SaltAndPepperNoiseAugmentation  # Replace with actual class name
from .shadows import ShadowAugmentation  # Replace with actual class name
from .snow import SnowAugmentation  # Replace with actual class name
from .speckle import SpeckleNoiseAugmentation  # Replace with actual class name
from .sunflare import SunFlareAugmentation  # Replace with actual class name

__all__ = [
    'BitDepthReductionAugmentation',
    'BlurAugmentation',
    'BrightnessContrastAugmentation',
    'ColorJitterAugmentation',
    'CompressionArtifactsAugmentation',
    'DownscaleUpscaleAugmentation',
    'FilmGrainAugmentation',
    'HorizontalFlipAugmentation',
    'FogAugmentation',
    'HueSaturationValueAugmentation',
    'ISONoiseAugmentation',
    'LowLightSimulationAugmentation',
    'PosterizeAugmentation',
    'RainAugmentation',
    'RandomAffineAugmentation',
    'SaltAndPepperNoiseAugmentation',
    'ShadowAugmentation',
    'SnowAugmentation',
    'SpeckleNoiseAugmentation',
    'SunFlareAugmentation',
]