from datetime import datetime, timedelta
from typing import Dict, Union, List, Tuple, Any, Callable

# Define time units as a data structure
# Each unit contains:
# - name: full name of the unit (e.g., "year") 
# - abbr: abbreviation (e.g., "y")
# - seconds: number of seconds in this unit (for reference)
# - extract: function to extract this unit's value from a timedelta
TIME_UNITS = [
    {
        "name": "year",
        "abbr": "y",
        "seconds": 31536000,
        "extract": lambda td: int(td.days / 365)
    },
    {
        "name": "day",
        "abbr": "d",
        "seconds": 86400,
        "extract": lambda td: int(td.days % 365)
    },
    {
        "name": "hour",
        "abbr": "h",
        "seconds": 3600,
        "extract": lambda td: int(td.seconds / 3600)
    },
    {
        "name": "minute",
        "abbr": "m",
        "seconds": 60,
        "extract": lambda td: int(td.seconds / 60) % 60
    },
    {
        "name": "second",
        "abbr": "s",
        "seconds": 1,
        "extract": lambda td: int(td.seconds % 60)
    },
    {
        "name": "millisecond",
        "abbr": "ms",
        "seconds": 0.001,
        "extract": lambda td: int(td.microseconds / 1000)
    },
    {
        "name": "microsecond",
        "abbr": "μs",
        "seconds": 0.000001,
        "extract": lambda td: int(td.microseconds % 1000)
    }
]

def get_delta_from_subject(subject: Union[datetime, timedelta, int, float]) -> Tuple[timedelta, bool]:
    """
    Convert various input types to a timedelta and determine if it's in the past.
    
    Args:
        subject: A datetime, timedelta, or timestamp (int/float)
        
    Returns:
        tuple: (timedelta object, is_past boolean)
    """
    if isinstance(subject, timedelta):
        return subject, subject >= timedelta(0)
    
    if isinstance(subject, datetime):
        delta = datetime.now(tz=subject.tzinfo) - subject
        return delta, delta >= timedelta(0)
    
    # Assume it's a timestamp
    try:
        dt = datetime.fromtimestamp(float(subject))
        delta = datetime.now() - dt
        return delta, delta >= timedelta(0)
    except (ValueError, TypeError, OverflowError):
        raise TypeError(f"Cannot convert {type(subject)} to a time delta")

def delta2dict(delta: timedelta) -> Dict[str, int]:
    """
    Accepts a delta, returns a dictionary of units.
    
    Args:
        delta: A timedelta object
        
    Returns:
        Dictionary with unit names as keys and their values
    """
    delta = abs(delta)
    result = {}
    
    for unit in TIME_UNITS:
        result[unit["name"]] = unit["extract"](delta)
    
    return result

def extract_components(delta: timedelta) -> List[Dict[str, Union[str, int]]]:
    """
    Extract time components from a timedelta, filtering out zero values.
    
    Args:
        delta: A timedelta object
        
    Returns:
        List of components with values > 0
    """
    # Use delta2dict to get all time values
    time_dict = delta2dict(delta)
    
    components = []
    # For each time unit, create a component if value > 0
    for unit in TIME_UNITS:
        unit_name = unit["name"]
        value = time_dict[unit_name]
        
        if value > 0:
            components.append({
                "unit": unit_name,
                "abbr": unit["abbr"],
                "value": value
            })
    
    return components

def format_components(
    components: List[Dict[str, Union[str, int]]],
    precision: int = 2,
    abbreviate: bool = False
) -> str:
    """
    Format the time components into a human-readable string.
    
    Args:
        components: List of time components with values
        precision: Number of units to include
        abbreviate: Whether to use abbreviations
        
    Returns:
        Formatted string (e.g., "2 years, 1 day" or "2y, 1d")
    """
    result = []
    
    # Only include up to 'precision' number of components
    for component in components[:precision]:
        if abbreviate:
            result.append(f"{component['value']}{component['abbr']}")
        else:
            unit_name = component["unit"]
            if component["value"] != 1:
                # Handle plurals
                unit_name += "s"
            result.append(f"{component['value']} {unit_name}")
    
    return ", ".join(result)

def human(
    subject: Union[datetime, timedelta, int, float],
    precision: int = 2,
    past_tense: str = "{} ago",
    future_tense: str = "in {}",
    abbreviate: bool = False
) -> str:
    """
    Accept a subject, return a human readable timedelta string.
    
    Args:
        subject: A datetime, timedelta, or timestamp (int/float)
        precision: The desired amount of unit precision (default: 2)
        past_tense: The format string used for past timedeltas (default: '{} ago')
        future_tense: The format string used for future timedeltas (default: 'in {}')
        abbreviate: Boolean to abbreviate units (default: False)
        
    Returns:
        Human readable timedelta string
    """
    # Convert input to timedelta and determine if it's in the past
    delta, is_past = get_delta_from_subject(subject)
    
    # Extract time components (e.g., years, days, hours)
    components = extract_components(delta)
    
    # Handle edge case: no components (very small time difference)
    if not components:
        return "just now"
    
    # Format the components into a readable string
    formatted = format_components(components, precision, abbreviate)
    
    # Apply the appropriate tense
    if is_past:
        return past_tense.format(formatted)
    else:
        return future_tense.format(formatted)