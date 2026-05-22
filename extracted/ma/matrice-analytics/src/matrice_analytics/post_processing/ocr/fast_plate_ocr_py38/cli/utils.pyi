"""Auto-generated stub for module: utils."""
from typing import Any, Callable, Optional

# Functions
def print_params(table_title: str = 'Parameters Table', c1_title: str = 'Variable', c2_title: str = 'Value') -> Callable:
    """
    A decorator that prints the parameters of a function in a formatted table
    using the rich library.
    
    Args:
        c1_title (str, optional): Title of the first column. Defaults to "Variable".
        c2_title (str, optional): Title of the second column. Defaults to "Value".
        table_title (str, optional): Title of the table. Defaults to "Parameters Table".
    
    Returns:
        Callable: The wrapped function with parameter printing functionality.
    """
    ...
def print_train_details(augmentation: Any.Any, config: dict[str, Any]) -> None: ...
def print_variables_as_table(c1_title: str, c2_title: str, title: str = 'Variables Table', **kwargs: Any) -> None:
    """
    Prints variables in a formatted table using the rich library.
    
    Args:
        c1_title (str): Title of the first column.
        c2_title (str): Title of the second column.
        title (str): Title of the table.
        **kwargs (Any): Variable names and values to be printed.
    """
    ...
def requires(*modules: Any) -> Callable:
    """
    Decorator that checks if given modules are importable. If not, raises ModuleNotFoundError with
    a hint to install the package(s).
    
    Args:
        modules (str): Names of modules to check (via importlib.util.find_spec).
        pkg_name (Optional[Sequence[str]]): Names of packages to suggest installing.
    
    Returns:
        Callable: The wrapped function that checks for module availability.
    """
    ...
def seed_everything(seed: int) -> None:
    """
    Seed random number generators for reproducibility.
    
    Args:
        seed (int): The seed value to set.
    """
    ...
