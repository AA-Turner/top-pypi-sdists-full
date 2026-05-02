from abc import abstractmethod
from typing import Any, Type, Optional
from pathlib import Path
from navconfig.logging import logging
import orjson
from ..exceptions import ConfigError, ComponentError


class ParrotTool:
    """ParrotTool.

    Interface for integrating Parrot Tools into Flowtask Components
    
    This interface provides a consistent pattern for using any Parrot tool
    (WebScrapingTool, SearchTool, etc.) as a FlowTask component.
    
    Features:
    - Load tool configuration from JSON files stored in taskstorage
    - Lazy initialization (tool setup happens in start(), not __init__)
    - Support for dynamic variable replacement in configurations
    - Consistent error handling and logging
    
    Usage:
        class MyScrapingComponent(ParrotTool, FlowComponent):
            def __init__(self, *args, **kwargs):
                self._tool_class = WebScrapingTool
                super().__init__(*args, **kwargs)
            
            async def start(self, **kwargs):
                await super().start(**kwargs)
                # Additional initialization
            
            async def run(self):
                result = await self._tool._execute(**self._tool_config)
                return result
    """
    
    def __init__(self, *args, **kwargs):
        self._tool_name = kwargs.get('tool_name', 'ParrotTool')
        self._tool: Any = None
        self._tool_class: Optional[Type] = None  # Must be set by subclass
        self._logger = logging.getLogger(f'Tool.{self._tool_name.lower()}')
        
        # Configuration file for the tool (e.g., JSON with flow/config)
        self._config_file: Optional[str] = kwargs.get('config_file', None)
        self._flow_file: Optional[str] = kwargs.get('flow_file', None)  # Alias for config_file
        
        # Tool-specific configuration
        self._tool_config: dict = kwargs.get('tool_config', {})
        
        # Output configuration
        self.output_column: Optional[str] = kwargs.get('output_column', None)
        
        super(ParrotTool, self).__init__(*args, **kwargs)

    async def start(self, **kwargs):
        """
        Initialize the Parrot Tool
        
        This method:
        1. Loads configuration from JSON file if specified
        2. Initializes the Parrot tool with configuration
        3. Validates required parameters
        
        Override this method in subclasses to add custom initialization logic.
        Make sure to call super().start(**kwargs) first.
        """
        # Determine which config file to use
        config_file = self._flow_file or self._config_file
        
        if config_file:
            # Load configuration from taskstorage
            await self._load_tool_config(config_file)
        
        # Initialize the Parrot tool
        if self._tool_class is None:
            raise ComponentError(
                f"{self._tool_name}: _tool_class must be set by subclass"
            )
        
        # Extract tool initialization parameters from attributes
        tool_params = self._extract_tool_params()
        
        try:
            self._logger.info(f"Initializing {self._tool_name} with params: {list(tool_params.keys())}")
            self._tool = self._tool_class(**tool_params)
        except Exception as err:
            raise ComponentError(
                f"{self._tool_name}: Error initializing tool: {err}"
            ) from err
        
        return True

    async def _load_tool_config(self, config_file: str):
        """
        Load tool configuration from JSON file
        
        Args:
            config_file: Path to JSON file relative to taskstorage flows directory
        """
        # Find in the taskstorage, the "flows" directory
        flows_path = self._taskstore.path.joinpath(self._program, 'flows')
        
        if not flows_path.exists():
            # Try to create it
            try:
                flows_path.mkdir(parents=True, exist_ok=True)
                self._logger.warning(
                    f"Created flows directory: {flows_path}"
                )
            except Exception as err:
                raise ConfigError(
                    f"{self._tool_name}: Flows Path Not Found and could not be created: {flows_path}"
                ) from err
        
        # Build full path to config file
        config_path = flows_path / config_file
        
        if not config_path.exists():
            raise ConfigError(
                f"{self._tool_name}: Config File Not Found: {config_path}"
            )
        
        # Read and parse JSON config
        try:
            with open(config_path, 'rb') as f:
                config_data = orjson.loads(f.read())
            
            self._logger.info(f"Loaded config from {config_file}")
            
            # Merge with existing tool_config
            self._tool_config = {**self._tool_config, **config_data}
            
            # Process variable replacements in config
            self._process_config_variables()
            
        except orjson.JSONDecodeError as err:
            raise ConfigError(
                f"{self._tool_name}: Invalid JSON in config file {config_file}: {err}"
            ) from err
        except Exception as err:
            raise ConfigError(
                f"{self._tool_name}: Error loading config file {config_file}: {err}"
            ) from err

    def _process_config_variables(self):
        """
        Replace variables in tool configuration with values from:
        - self._variables
        - self._mask
        - self._attributes

        Supports {variable} syntax in strings throughout the config.
        Preserves Python types (lists, dicts) instead of converting to strings.
        """
        import re

        def replace_vars(obj):
            """Recursively replace variables in nested structures"""
            if isinstance(obj, str):
                # Check if the entire string is just a variable placeholder
                # e.g., "{zipcodes}" should be replaced with the actual list
                match = re.match(r'^\{(\w+)\}$', obj)
                if match:
                    var_name = match.group(1)
                    # Direct replacement - preserve type (list, dict, etc.)
                    if var_name in self._variables:
                        return self._variables[var_name]
                    elif var_name in self._mask:
                        return self._mask[var_name]

                # Otherwise, do string replacement for embedded variables
                for var_name, var_value in self._variables.items():
                    placeholder = f"{{{var_name}}}"
                    if placeholder in obj:
                        # Only convert to string if it's embedded in a larger string
                        obj = obj.replace(placeholder, str(var_value))

                # Also check masks
                for mask_name, mask_value in self._mask.items():
                    if mask_name in obj:
                        obj = obj.replace(mask_name, str(mask_value))

                return obj
            elif isinstance(obj, dict):
                return {k: replace_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_vars(item) for item in obj]
            else:
                return obj

        self._tool_config = replace_vars(self._tool_config)

    @abstractmethod
    def _extract_tool_params(self) -> dict:
        """
        Extract tool initialization parameters from component attributes
        
        This method should return a dictionary of parameters to pass
        to the tool's __init__ method.
        
        Example:
            def _extract_tool_params(self) -> dict:
                return {
                    'headless': self.headless,
                    'browser': self.browser,
                    'driver_type': self.driver_type,
                }
        
        Returns:
            dict: Parameters for tool initialization
        """
        pass

    async def close(self):
        """
        Close the tool and clean up resources
        
        Override in subclasses if tool requires special cleanup.
        """
        # Default implementation - tools may not need explicit cleanup
        pass

