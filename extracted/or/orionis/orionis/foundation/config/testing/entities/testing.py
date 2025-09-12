from dataclasses import dataclass, field
from orionis.support.entities.base import BaseEntity
from orionis.foundation.config.testing.enums import ExecutionMode, PersistentDrivers, VerbosityMode
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.services.system.workers import Workers

@dataclass(unsafe_hash=True, kw_only=True)
class Testing(BaseEntity):
    """
    Configuration dataclass for test execution options.

    Parameters
    ----------
    verbosity : int or VerbosityMode, optional
        Verbosity level for test output. 0 = silent, 1 = minimal, 2 = detailed (default: 2).
    execution_mode : str or ExecutionMode, optional
        Mode of test execution. 'SEQUENTIAL' runs tests one after another, 'PARALLEL' runs tests in parallel (default: 'SEQUENTIAL').
    max_workers : int, optional
        Maximum number of worker threads/processes for parallel execution (default: calculated by Workers).
    fail_fast : bool, optional
        If True, stop execution after the first test failure (default: False).
    throw_exception : bool, optional
        If True, raise an exception on test failure (default: False).
    base_path : str, optional
        Base directory where tests are located (default: 'tests').
    folder_path : str or list of str, optional
        Folder path pattern(s) to search for tests (default: '*').
    pattern : str, optional
        Filename pattern to identify test files (default: 'test_*.py').
    test_name_pattern : str or None, optional
        Pattern to match specific test names (default: None).
    persistent : bool, optional
        If True, keep test results persistent (default: False).
    persistent_driver : str or PersistentDrivers, optional
        Driver to use for persisting test results. Supported: 'sqlite', 'json' (default: 'json').
    web_report : bool, optional
        If True, generate a web report for test results (default: False).

    Notes
    -----
    This class validates all configuration options on initialization and raises an exception if any value is invalid.
    """

    verbosity: int | VerbosityMode = field(
        default = VerbosityMode.DETAILED.value,
        metadata = {
            "description": "The verbosity level of the test output. Default is 2.",
            "default": VerbosityMode.DETAILED.value
        }
    )

    execution_mode : str | ExecutionMode = field(
        default = ExecutionMode.SEQUENTIAL.value,
        metadata = {
            "description": "The mode of test execution. Default is SEQUENTIAL",
            "default": ExecutionMode.SEQUENTIAL.value
        }
    )

    max_workers: int = field(
        default = 4,
        metadata = {
            "description": "The maximum number of worker threads/processes to use when running tests in parallel.",
            "default": 4
        }
    )

    fail_fast: bool = field(
        default = False,
        metadata = {
            "description": "Whether to stop execution after the first test failure. Default is False.",
            "default": False
        }
    )

    throw_exception: bool = field(
        default = False,
        metadata = {
            "description": "Whether to throw an exception if a test fails. Default is False.",
            "default": False
        }
    )

    folder_path: str | list = field(
        default = '*',
        metadata = {
            "description": "The folder path pattern to search for tests. Default is '*'.",
            "default": '*'
        }
    )

    pattern: str = field(
        default = 'test_*.py',
        metadata = {
            "description": "The filename pattern to identify test files. Default is 'test_*.py'.",
            "default": 'test_*.py'
        }
    )

    test_name_pattern: str | None = field(
        default = None,
        metadata = {
            "description": "A pattern to match specific test names. Default is None.",
            "default": None
        }
    )

    persistent: bool = field(
        default = False,
        metadata = {
            "description": "Whether to keep the test results persistent. Default is False.",
            "default": False
        }
    )

    persistent_driver: str | PersistentDrivers = field(
        default = PersistentDrivers.JSON.value,
        metadata = {
            "description": "Specifies the driver to use for persisting test results. Supported values: 'sqlite', 'json'. Default is 'sqlite'.",
            "default": PersistentDrivers.JSON.value
        }
    )

    web_report: bool = field(
        default = False,
        metadata = {
            "description": "Whether to generate a web report for the test results. Default is False.",
            "default": False
        }
    )

    def __post_init__(self):
        super().__post_init__()
        """
        Validate and normalize configuration options after initialization.

        This method checks the types and values of all configuration attributes of the Testing class.
        If any attribute is invalid, an OrionisIntegrityException is raised with a descriptive error message.
        It also normalizes enum/string values to their canonical forms where appropriate.

        Raises
        ------
        OrionisIntegrityException
            If any configuration option is invalid or inconsistent.
        """

        # Validate the attributes of the Testing dataclass
        if not isinstance(self.verbosity, (int, VerbosityMode)):
            raise OrionisIntegrityException(
                f"Invalid type for 'verbosity': {type(self.verbosity).__name__}. It must be an integer or an instance of VerbosityMode."
            )

        if isinstance(self.verbosity, int):
            if (self.verbosity < 0 or self.verbosity > 2):
                raise OrionisIntegrityException(
                    f"Invalid value for 'verbosity': {self.verbosity}. It must be an integer between 0 (silent) and 2 (detailed output)."
                )
        elif isinstance(self.verbosity, VerbosityMode):
                self.verbosity = self.verbosity.value


        # Validate the Excecution Mode
        if not isinstance(self.execution_mode, (str, ExecutionMode)):
            raise OrionisIntegrityException(
                f"Invalid type for 'execution_mode': {type(self.execution_mode).__name__}. It must be a string or an instance of ExecutionMode."
            )

        if isinstance(self.execution_mode, str):
            options_modes = ExecutionMode._member_names_
            _value = str(self.execution_mode).upper().strip()
            if _value not in options_modes:
                raise OrionisIntegrityException(
                    f"Invalid value for 'execution_mode': {self.execution_mode}. It must be one of: {str(options_modes)}."
                )
            else:
                self.execution_mode = ExecutionMode[_value].value
        elif isinstance(self.execution_mode, ExecutionMode):
            self.execution_mode = self.execution_mode.value

        # Validate Max Workers
        if not isinstance(self.max_workers, int) or self.max_workers < 1:
            raise OrionisIntegrityException(
                f"Invalid value for 'max_workers': {self.max_workers}. It must be a positive integer greater than 0."
            )

        # Real max working calculation
        real_max_working = Workers().calculate()
        if self.max_workers > real_max_working:
            raise OrionisIntegrityException(
                f"Invalid value for 'max_workers': {self.max_workers}. It must be less than or equal to the real maximum workers available: {real_max_working}."
            )

        # Validate fail_fast attribute
        if not isinstance(self.fail_fast, bool):
            raise OrionisIntegrityException(
                f"Invalid type for 'fail_fast': {type(self.fail_fast).__name__}. It must be a boolean (True or False)."
            )

        # Validate throw_exception attribute
        if not isinstance(self.throw_exception, bool):
            raise OrionisIntegrityException(
                f"Invalid type for 'throw_exception': {type(self.throw_exception).__name__}. It must be a boolean (True or False)."
            )

        # Validate folder_path attribute
        if not (isinstance(self.folder_path, str) or isinstance(self.folder_path, list)):
            raise OrionisIntegrityException(
            f"Invalid type for 'folder_path': {type(self.folder_path).__name__}. It must be a string or a list of strings representing the folder path pattern."
            )

        # If folder_path is a list, ensure all elements are strings
        if isinstance(self.folder_path, list):
            for i, folder in enumerate(self.folder_path):
                if not isinstance(folder, str):
                    raise OrionisIntegrityException(
                        f"Invalid type for folder at index {i} in 'folder_path': {type(folder).__name__}. Each folder path must be a string."
                    )

        # Validate pattern attribute
        if not isinstance(self.pattern, str):
            raise OrionisIntegrityException(
                f"Invalid type for 'pattern': {type(self.pattern).__name__}. It must be a string representing the filename pattern for test files."
            )

        # Validate test_name_pattern attribute
        if self.test_name_pattern is not None and not isinstance(self.test_name_pattern, str):
            raise OrionisIntegrityException(
                f"Invalid type for 'test_name_pattern': {type(self.test_name_pattern).__name__}. It must be a string or None."
            )

        # Validate persistent attribute
        if not isinstance(self.persistent, bool):
            raise OrionisIntegrityException(
                f"Invalid type for 'persistent': {type(self.persistent).__name__}. It must be a boolean (True or False)."
            )

        # Validate persistent_driver attribute
        if self.persistent:

            # Validate persistent_driver type and value
            if not isinstance(self.persistent_driver, (str, PersistentDrivers)):
                raise OrionisIntegrityException(
                    f"Invalid type for 'persistent_driver': {type(self.persistent_driver).__name__}. It must be a string or an instance of PersistentDrivers."
                )

            # If persistent_driver is a string, convert it to PersistentDrivers enum
            if isinstance(self.persistent_driver, str):
                options_drivers = PersistentDrivers._member_names_
                _value = str(self.persistent_driver).upper().strip()
                if _value not in options_drivers:
                    raise OrionisIntegrityException(
                        f"Invalid value for 'persistent_driver': {self.persistent_driver}. It must be one of: {str(options_drivers)}."
                    )
                else:
                    self.persistent_driver = PersistentDrivers[_value].value
            else:
                self.persistent_driver = self.persistent_driver.value

        # Validate web_report attribute
        if not isinstance(self.web_report, bool):
            raise OrionisIntegrityException(
                f"Invalid type for 'web_report': {type(self.web_report).__name__}. It must be a boolean (True or False)."
            )