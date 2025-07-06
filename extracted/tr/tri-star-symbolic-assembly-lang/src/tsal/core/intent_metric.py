"""Intent-Driven Metric calculation."""

def calculate_idm(
    info_quality: float,
    info_quantity: float,
    accuracy: float,
    complexity: float,
    time_taken: float,
) -> float:
    """Return the IDM score.

    IDM = (info_quality * info_quantity * accuracy) / (complexity * time_taken)
    """
    if complexity <= 0 or time_taken <= 0:
        raise ValueError("complexity and time_taken must be > 0")
    info_power = info_quality * info_quantity * accuracy
    return info_power / (complexity * time_taken)
