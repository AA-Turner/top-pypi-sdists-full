"""
Automatic extraction of default parameters from all PySpark functions.

This module inspects all functions in pyspark.sql.functions and automatically
extracts their default parameter values to build the FUNCTION_DEFAULTS dictionary.
"""

import inspect
import logging
from typing import Dict, List, Tuple, Any, Optional
import pyspark.sql.functions as F
from pyspark.sql.types import DataType

logger = logging.getLogger(__name__)


def get_literal_type_from_python_value(value: Any) -> Optional[str]:
    """
    Map Python default values to protobuf literal types.
    
    Args:
        value: The Python default value
        
    Returns:
        str: The corresponding protobuf literal type, or None if unsupported
    """
    if isinstance(value, bool):
        return "literal_bool"
    elif isinstance(value, int):
        return "literal_int"
    elif isinstance(value, float):
        return "literal_double"
    elif isinstance(value, str):
        return "literal_string"
    elif value is None:
        return "literal_null"
    elif isinstance(value, DataType):
        # Handle PySpark DataType defaults - convert to string representation
        return "literal_string"
    else:
        # For complex types, try to serialize as string
        logger.debug(f"Unsupported default type {type(value)}: {value}")
        return None


def extract_function_defaults() -> Dict[str, List[Tuple[int, Any, str]]]:
    """
    Extract default parameters from all PySpark functions.
    
    Returns:
        Dict mapping function names to list of (param_index, default_value, literal_type)
    """
    function_defaults = {}
    
    # Get all functions from pyspark.sql.functions
    for name in dir(F):
        if name.startswith('_'):  # Skip private functions
            continue
            
        obj = getattr(F, name)
        
        # Only process callable functions
        if not callable(obj):
            continue
            
        try:
            # Get function signature
            sig = inspect.signature(obj)
            defaults_found = []
            
            for param_index, (param_name, param) in enumerate(sig.parameters.items()):
                # Skip *args and **kwargs
                if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    continue
                    
                # Check if parameter has a default value
                if param.default != inspect.Parameter.empty:
                    literal_type = get_literal_type_from_python_value(param.default)
                    
                    if literal_type:
                        # Convert DataType defaults to their string representation
                        if isinstance(param.default, DataType):
                            default_value = param.default.simpleString()
                        else:
                            default_value = param.default
                            
                        defaults_found.append((param_index, default_value, literal_type))
                        logger.debug(f"{name}[{param_index}] {param_name} = {param.default} ({literal_type})")
            
            # Only add function if it has defaults
            if defaults_found:
                function_defaults[name.lower()] = defaults_found
                logger.info(f"Registered {len(defaults_found)} defaults for {name}")
                
        except (ValueError, TypeError) as e:
            # Some functions might not have inspectable signatures
            logger.debug(f"Could not inspect {name}: {e}")
            continue
    
    return function_defaults


def print_discovered_defaults(function_defaults: Dict[str, List[Tuple[int, Any, str]]]) -> None:
    """Print all discovered function defaults in a readable format."""
    print(f"\n=== Discovered {len(function_defaults)} PySpark functions with defaults ===\n")
    
    for func_name, defaults in sorted(function_defaults.items()):
        print(f"{func_name}:")
        for param_index, default_value, literal_type in defaults:
            print(f"  [{param_index}] = {default_value} ({literal_type})")
        print()


def get_critical_functions_with_defaults() -> List[str]:
    """
    Return a list of functions that are critical for Spark Connect compatibility.
    These are functions commonly used where Scala clients might omit defaults.
    """
    return [
        'locate', 'overlay', 'substring', 'regexp_extract', 'regexp_replace',
        'split', 'lag', 'lead', 'nth_value', 'first', 'last',
        'round', 'bround', 'format_number', 'format_string',
        'date_add', 'date_sub', 'add_months', 'months_between',
        'from_unixtime', 'unix_timestamp', 'to_timestamp', 'to_date',
        'array_repeat', 'array_position', 'array_remove', 'array_distinct',
        'map_from_arrays', 'map_from_entries', 'struct',
        'when', 'coalesce', 'greatest', 'least',
        'rand', 'randn', 'monotonically_increasing_id',
        'conv', 'bin', 'hex', 'unhex', 'base64', 'unbase64'
    ]


def get_manual_function_defaults() -> Dict[str, List[Tuple[int, Any, str]]]:
    """
    Return manually defined defaults for functions that don't have Python defaults
    but are commonly called with missing parameters by Scala Spark Connect clients.
    
    These are based on Spark SQL behavior and common usage patterns.
    NOTE: Only add functions here if they actually need defaults for Scala compatibility
    and don't have Python defaults. Verify with inspect.signature() first!
    """
    return {
        # NOTE: Most functions that seem like they need defaults actually require all parameters.
        # Only add functions here after verifying they have missing defaults in Python
        # that are needed for Scala Spark Connect compatibility.
        
        # Currently empty - PySpark automatic inspection covers most cases
        # Add functions here only if you've verified:
        # 1. The function doesn't have Python defaults (check with inspect.signature())
        # 2. Scala clients commonly call it with fewer parameters 
        # 3. There's a sensible default from Spark SQL documentation
    }


def filter_critical_functions(function_defaults: Dict[str, List[Tuple[int, Any, str]]]) -> Dict[str, List[Tuple[int, Any, str]]]:
    """Filter to only include critical functions to avoid over-injection."""
    critical_functions = set(func.lower() for func in get_critical_functions_with_defaults())
    
    filtered = {}
    for func_name, defaults in function_defaults.items():
        if func_name in critical_functions:
            filtered[func_name] = defaults
    
    return filtered


def validate_extracted_defaults() -> Dict[str, List[Tuple[int, Any, str]]]:
    """
    Extract and validate function defaults, with filtering for critical functions.
    
    Returns:
        Dict of validated function defaults
    """
    logger.info("Extracting defaults from all PySpark functions...")
    
    # Extract all defaults from PySpark inspection
    all_defaults = extract_function_defaults()
    
    # Filter to critical functions to avoid over-injection
    critical_defaults = filter_critical_functions(all_defaults)
    
    # Add manual defaults for functions that don't have Python defaults
    # but need them for Scala Spark Connect compatibility
    manual_defaults = get_manual_function_defaults()
    
    # Merge manual defaults with extracted defaults
    for func_name, defaults in manual_defaults.items():
        if func_name in critical_defaults:
            # Merge defaults, avoiding duplicates
            existing_params = {param_idx for param_idx, _, _ in critical_defaults[func_name]}
            for param_idx, default_val, literal_type in defaults:
                if param_idx not in existing_params:
                    critical_defaults[func_name].append((param_idx, default_val, literal_type))
                    critical_defaults[func_name].sort(key=lambda x: x[0])  # Sort by param index
        else:
            # Add entirely new function
            critical_defaults[func_name] = defaults
    
    logger.info(f"Found {len(all_defaults)} total functions with defaults")
    logger.info(f"Added {len(manual_defaults)} manual function defaults")
    logger.info(f"Final selection: {len(critical_defaults)} critical functions")
    
    return critical_defaults


def generate_defaults_dict_code(function_defaults: Dict[str, List[Tuple[int, Any, str]]]) -> str:
    """Generate Python code for the FUNCTION_DEFAULTS dictionary."""
    lines = ["# Auto-generated FUNCTION_DEFAULTS from PySpark inspection", "FUNCTION_DEFAULTS = {"]
    
    for func_name, defaults in sorted(function_defaults.items()):
        lines.append(f'    "{func_name}": [')
        for param_index, default_value, literal_type in defaults:
            # Properly format the default value for code generation
            if isinstance(default_value, str):
                formatted_value = f'"{default_value}"'
            elif default_value is None:
                formatted_value = "None"
            else:
                formatted_value = str(default_value)
            
            lines.append(f'        ({param_index}, {formatted_value}, "{literal_type}"),')
        lines.append("    ],")
    
    lines.append("}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Extract defaults
    defaults = validate_extracted_defaults()
    
    # Print discovered defaults
    print_discovered_defaults(defaults)
    
    # Generate code
    print("\n" + "="*80)
    print("GENERATED CODE FOR function_defaults.py:")
    print("="*80)
    print(generate_defaults_dict_code(defaults))
    
    print(f"\n✅ Successfully processed {len(defaults)} critical PySpark functions with defaults!")
