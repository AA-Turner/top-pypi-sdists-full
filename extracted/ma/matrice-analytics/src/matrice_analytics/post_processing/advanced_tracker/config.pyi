"""Auto-generated stub for module: config."""

# Classes
class TrackerConfig:
    # Configuration for advanced tracker.
    #
    # This class contains all the parameters needed to configure the tracking algorithm,
    # including thresholds, buffer sizes, and algorithm-specific settings.
    #
    # Threshold Tuning Guide:
    # - Lower thresholds = more lenient matching = fewer new track IDs = more stable counts
    # - Higher thresholds = stricter matching = more new track IDs = potential count inflation
    #
    # Recommended defaults are optimized for count accuracy over precision.

    ...
