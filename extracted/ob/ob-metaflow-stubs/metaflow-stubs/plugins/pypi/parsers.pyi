######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.869076                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class ParserValueError(metaflow.exception.MetaflowException, metaclass=type):
    ...

def requirements_txt_parser(content: str):
    """
    Parse non-comment lines from a requirements.txt file as strictly valid
    PEP 508 requirements.
    
    Recognizes direct references (e.g. "my_lib @ git+https://..."), extras
    (e.g. "requests[security]"), and version specifiers (e.g. "==2.0"). If
    the package name is "python", its specifier is stored in the "python"
    key instead of "packages".
    
    Parameters
    ----------
    content : str
        Contents of a requirements.txt file.
    
    Returns
    -------
    dict
        A dictionary with two keys:
            - "packages": dict(str -> str)
              Mapping from package name (plus optional extras/references) to a
              version specifier string.
            - "python": str or None
              The Python version constraints if present, otherwise None.
    
    Raises
    ------
     ParserValueError
        If a requirement line is invalid PEP 508 or if environment markers are
        detected, or if multiple Python constraints are specified.
    """
    ...

def pyproject_toml_parser(content: str):
    """
    Parse a pyproject.toml file per PEP 621.
    
    Reads the 'requires-python' and 'dependencies' fields from the "[project]" section.
    Each dependency line must be a valid PEP 508 requirement. If the package name is
    "python", its specifier is stored in the "python" key instead of "packages".
    
    Parameters
    ----------
    content : str
        Contents of a pyproject.toml file.
    
    Returns
    -------
    dict
        A dictionary with two keys:
            - "packages": dict(str -> str)
              Mapping from package name (plus optional extras/references) to a
              version specifier string.
            - "python": str or None
              The Python version constraints if present, otherwise None.
    
    Raises
    ------
    RuntimeError
        If no TOML library (tomllib in Python 3.11+ or tomli in earlier versions) is found.
     ParserValueError
        If a dependency is not valid PEP 508, if environment markers are used, or if
        multiple Python constraints are specified.
    """
    ...

def conda_environment_yml_parser(content: str):
    """
    Parse a minimal environment.yml file under strict assumptions.
    
    The file must contain a 'dependencies:' line, after which each dependency line
    appears with a '- ' prefix. Python can appear as 'python=3.9', etc.; other
    packages as 'numpy=1.21.2' or simply 'numpy'. Non-compliant lines raise  ParserValueError.
    
    Parameters
    ----------
    content : str
        Contents of a environment.yml file.
    
    Returns
    -------
    dict
        A dictionary with keys:
        {
            "packages": dict(str -> str),
            "python": str or None
        }
    
    Raises
    ------
     ParserValueError
        If the file has malformed lines or unsupported sections.
    """
    ...

