from typing import Any, Optional, List, Type
import asyncio
from collections.abc import Callable
import importlib
import pandas as pd
from parrot.tools.scraping import WebScrapingTool
from pydantic import BaseModel
from bs4 import BeautifulSoup
from ..interfaces.ParrotTool import ParrotTool
from ..interfaces.credentials import CredentialsInterface
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class ScrapTool(CredentialsInterface, ParrotTool, FlowComponent):
    """
    ScrapTool Component

    **Overview**

    This component uses Parrot's WebScrapingTool to perform automated web scraping
    with programmable browser flows defined in JSON files.

    The component is generic and can scrape any website by defining different flow
    configurations in JSON files stored in the `flows/` directory.

    **Features**

    - Programmable browser automation via JSON flow files
    - Support for navigation, clicking, filling forms, scrolling, screenshots, etc.
    - Loop support for iterating over data (e.g., multiple URLs, zipcodes, products)
    - Human-in-the-loop with await_browser_event for manual interactions
    - Variable replacement from flow variables into JSON configurations
    - Can enrich existing dataframes or generate new data
    - Support for both Selenium and Playwright drivers
    - Optional authentication credentials (username/password) with env var support

       :widths: auto

    |   flow_file                | Yes      | Path to JSON file with scraping flow (relative to taskstorage/flows/)          |
    |                            |          | Example: `consumeraffairs_reviews.json`                                         |
    |   output_column            | No       | Column name to store scraped data (default: `scraped_data`)                     |
    |   parser_function          | No       | Custom parser function. Format: `filename.function_name`                        |
    |                            |          | Loads from taskstorage/{program}/parsers/filename.py                            |
    |   parser_model             | No       | Pydantic model for validation. Format: `filename.ClassName`                     |
    |                            |          | Loads from taskstorage/{program}/parsers/filename.py                            |
    |   extract_name             | No       | Name of extracted data in result (from get_html action)                         |
    |   auto_expand              | No       | Auto-expand extracted data into columns (default: `true`)                       |
    |   headless                 | No       | Run browser in headless mode (default: `true`)                                  |
    |   browser                  | No       | Browser type: chrome, firefox, edge, safari, undetected (default: `chrome`)     |
    |   driver_type              | No       | Driver type: selenium or playwright (default: `selenium`)                       |
    |   iterate_over             | No       | Column name to iterate over (for scraping multiple items from previous data)    |
    |   user_data_dir            | No       | Directory for persistent browser profile (for SSO sessions)                     |
    |   debugger_address         | No       | Chrome debugger address for remote debugging (e.g., `127.0.0.1:9222`)          |
    |   username                 | No       | Username for authentication. Can be env var name (e.g., `MY_USERNAME`)          |
    |                            |          | Available in flow as `{username}` variable                                      |
    |   password                 | No       | Password for authentication. Can be env var name (e.g., `MY_PASSWORD`)          |
    |                            |          | Available in flow as `{password}` variable. Use env vars for security.          |

    **Returns**

    A pandas DataFrame with scraped data. If `previous=True`, enriches the input DataFrame
    with new columns. Otherwise, returns a new DataFrame with the scraped data.

    **Flow JSON Structure**

    The flow file must contain:
    - `steps`: List of browser actions to execute
    - `selectors`: (Optional) Content selectors for data extraction

    Example flow file (`flows/product_scraper.json`):

    ```json
    {
      "steps": [
        {
          "action": "navigate",
          "url": "{product_url}",
          "description": "Navigate to product page"
        },
        {
          "action": "wait",
          "selector": ".product-details",
          "timeout": 10,
          "description": "Wait for product details to load"
        },
        {
          "action": "scroll",
          "direction": "bottom",
          "description": "Scroll to load all content"
        }
      ],
      "selectors": [
        {
          "name": "product_name",
          "selector": "h1.product-title",
          "extract_type": "text"
        },
        {
          "name": "price",
          "selector": ".price",
          "extract_type": "text"
        },
        {
          "name": "reviews",
          "selector": ".review-item",
          "extract_type": "text",
          "multiple": true
        }
      ]
    }
    ```

    **Example YAML Configuration**

    Basic scraping without input:


    Scraping with iteration over dataframe:


    Scraping with authentication (credentials from env vars):


    Or with direct values (not recommended for passwords):


    **Variable Replacement**

    Variables from the flow can be used in the JSON file.
    Credentials (username/password) are automatically available:


    In the JSON flow:
    ```json
    {
      "steps": [
        {
          "action": "navigate",
          "url": "{base_url}/login"
        },
        {
          "action": "authenticate",
          "method": "form",
          "username_selector": "input[name='email']",
          "username": "{username}",
          "password_selector": "input[name='password']",
          "password": "{password}",
          "submit_selector": "button[type='submit']"
        }
      ]
    }
    ```

    **Advanced: Custom Parser with Pydantic Models**

    For complex scraping where you need custom data processing:

    1. Create a parser file in your task's parsers directory:

    **taskstorage/{program}/parsers/dispatch.py:**

    ```python
    from pydantic import BaseModel, Field
    from typing import List, Optional
    from bs4 import Tag

    class Provider(BaseModel):
        name: Optional[str] = None
        rating: Optional[float] = None
        distance: Optional[str] = None
        address: Optional[str] = None
        trades: List[str] = Field(default_factory=list)

    def parse_provider_div(tag: Tag) -> Provider:
        # Custom BeautifulSoup parsing logic
        name = tag.find('h2').get_text() if tag.find('h2') else None
        rating_text = tag.find(attrs={'class': 'rating'})
        rating = float(rating_text.get_text()) if rating_text else None

        return Provider(
            name=name,
            rating=rating,
            # ... more parsing logic
        )
    ```

    2. Use in YAML configuration:


    **Directory structure:**
    ```
    taskstorage/{program}/
      flows/
        dispatch_scraper.json
      parsers/
        dispatch.py
    ```

    This will:
    - Load parser from taskstorage (no changes to flowtask code needed!)
    - Extract HTML using `get_html` action in the JSON flow
    - Parse each element with your custom function
    - Validate with Pydantic model
    - Return a clean DataFrame with all Provider fields as columns

    **Human-in-the-Loop Workflows**

    For sites requiring manual interaction (captchas, complex forms):

    ```json
    {
      "steps": [
        {
          "action": "navigate",
          "url": "https://example.com/login"
        },
        {
          "action": "await_browser_event",
          "timeout": 600,
          "wait_condition": {
            "key_combo": "ctrl_enter",
            "show_overlay_button": true
          },
          "description": "Wait for human to login, then press Ctrl+Enter"
        },
        {
          "action": "loop",
          "values": ["{zipcode1}", "{zipcode2}"],
          "actions": [
            {
              "action": "fill",
              "selector": "input[name='zip']",
              "value": "{value}"
            },
            {
              "action": "get_html",
              "selector": "div.provider-card",
              "multiple": true,
              "extract_name": "providers"
            }
          ]
        }
      ]
    }
    ```

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ScrapTool:
          flow_file: "consumeraffairs_reviews.json"
          output_column: "reviews_data"
          headless: true
        ```
    """
    _version = "1.0.0"
    
    # Optional credentials for authentication flows
    _credentials: dict = {
        "username": str,
        "password": str,
    }
    
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Handle credentials - support both formats:
        # 1. credentials: {username: "...", password: "..."}
        # 2. username: "...", password: "..." (direct)
        if 'credentials' not in kwargs:
            # Build credentials dict from direct username/password
            creds = {}
            if 'username' in kwargs:
                creds['username'] = kwargs.pop('username')
            if 'password' in kwargs:
                creds['password'] = kwargs.pop('password')
            if creds:
                kwargs['credentials'] = creds
        
        # WebScraping specific configuration
        self.headless: bool = kwargs.get('headless', True)
        self.browser: str = kwargs.get('browser', 'chrome')
        self.driver_type: str = kwargs.get('driver_type', 'selenium')
        self.user_data_dir: Optional[str] = kwargs.get('user_data_dir', None)
        self.debugger_address: Optional[str] = kwargs.get('debugger_address', None)
        self.full_page: bool = kwargs.get('full_page', False)
        self.mobile: bool = kwargs.get('mobile', False)
        self.mobile_device: Optional[str] = kwargs.get('mobile_device', None)
        
        # Iteration configuration
        self.iterate_over: Optional[str] = kwargs.get('iterate_over', None)
        
        # Output configuration
        self.output_column: Optional[str] = kwargs.get('output_column', None)
        self.auto_expand: bool = kwargs.get('auto_expand', True)
        
        # Advanced parsing configuration
        self.parser_function: Optional[str] = kwargs.get('parser_function', None)
        self.parser_model: Optional[str] = kwargs.get('parser_model', None)
        self.extract_name: Optional[str] = kwargs.get('extract_name', None)
        
        # Will be set during initialization
        self._parser_fn: Optional[Callable] = None
        self._model_class: Optional[Type[BaseModel]] = None
        
        # Call parent constructors
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        
        # Set the tool class AFTER calling super().__init__
        # This prevents ParrotTool.__init__ from overwriting it
        self._tool_class = WebScrapingTool
        self._tool_name = 'WebScrapingTool'
        
        # Storage for scraped results
        self._scraped_results: List[dict] = []

    def _extract_tool_params(self) -> dict:
        """Extract WebScrapingTool initialization parameters"""
        params = {
            'headless': self.headless,
            'browser': self.browser,
            'driver_type': self.driver_type,
            'full_page': self.full_page,
            'mobile': self.mobile,
        }
        
        # Add optional parameters
        if self.mobile_device:
            params['mobile_device'] = self.mobile_device
        if self.user_data_dir:
            params['user_data_dir'] = self.user_data_dir
        if self.debugger_address:
            params['debugger_address'] = self.debugger_address
        
        return params

    def _load_parser_from_file(self, parser_path):
        """
        Load parser from a Python file in taskstorage
        
        Args:
            parser_path: Path to the Python file containing the parser
        
        Returns:
            Module object
        """
        import sys
        from importlib import util
        
        # Create a unique module name based on the file path
        module_name = f"_scrap_parser_{self._program}_{parser_path.stem}"
        
        # Load the module from file
        spec = util.spec_from_file_location(module_name, parser_path)
        if spec is None or spec.loader is None:
            raise ConfigError(f"ScrapTool: Could not load parser from {parser_path}")
        
        module = util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return module
    
    def _load_custom_parser(self):
        """
        Load custom parser function
        
        Supports two formats:
        1. File-based (in taskstorage): "parser_file.function_name"
        2. Module-based (importable): "module.submodule.function_name"
        """
        if not self.parser_function:
            return
        
        try:
            # Check if it's a simple "filename.function" format
            if '.' in self.parser_function and self.parser_function.count('.') == 1:
                # Try to load from taskstorage parsers directory
                parsers_path = self._taskstore.path.joinpath(self._program, 'parsers')
                
                if parsers_path.exists():
                    file_name, func_name = self.parser_function.split('.')
                    parser_file = parsers_path / f"{file_name}.py"
                    
                    if parser_file.exists():
                        # Load from file in taskstorage
                        module = self._load_parser_from_file(parser_file)
                        self._parser_fn = getattr(module, func_name)
                        self._logger.info(
                            f"Loaded parser from taskstorage: {parser_file.name}.{func_name}"
                        )
                        return
            
            # Fallback: try to import as a regular module
            module_path, func_name = self.parser_function.rsplit('.', 1)
            module = importlib.import_module(module_path)
            self._parser_fn = getattr(module, func_name)
            self._logger.info(f"Loaded parser from module: {self.parser_function}")
            
        except Exception as err:
            raise ConfigError(
                f"ScrapTool: Failed to load parser function '{self.parser_function}': {err}"
            ) from err
    
    def _load_custom_model(self):
        """
        Load custom Pydantic model
        
        Supports two formats:
        1. File-based (in taskstorage): "parser_file.ClassName"
        2. Module-based (importable): "module.submodule.ClassName"
        """
        if not self.parser_model:
            return
        
        try:
            # Check if it's a simple "filename.ClassName" format
            if '.' in self.parser_model and self.parser_model.count('.') == 1:
                # Try to load from taskstorage parsers directory
                parsers_path = self._taskstore.path.joinpath(self._program, 'parsers')
                
                if parsers_path.exists():
                    file_name, class_name = self.parser_model.split('.')
                    parser_file = parsers_path / f"{file_name}.py"
                    
                    if parser_file.exists():
                        # Load from file in taskstorage
                        module = self._load_parser_from_file(parser_file)
                        self._model_class = getattr(module, class_name)
                        
                        # Verify it's a Pydantic model
                        if not issubclass(self._model_class, BaseModel):
                            raise ConfigError(
                                f"ScrapTool: {self.parser_model} is not a Pydantic BaseModel"
                            )
                        
                        self._logger.info(
                            f"Loaded model from taskstorage: {parser_file.name}.{class_name}"
                        )
                        return
            
            # Fallback: try to import as a regular module
            module_path, class_name = self.parser_model.rsplit('.', 1)
            module = importlib.import_module(module_path)
            self._model_class = getattr(module, class_name)
            
            # Verify it's a Pydantic model
            if not issubclass(self._model_class, BaseModel):
                raise ConfigError(
                    f"ScrapTool: {self.parser_model} is not a Pydantic BaseModel"
                )
            
            self._logger.info(f"Loaded model from module: {self.parser_model}")
            
        except Exception as err:
            raise ConfigError(
                f"ScrapTool: Failed to load parser model '{self.parser_model}': {err}"
            ) from err

    async def start(self, **kwargs):
        """
        Initialize the ScrapTool component
        
        - Validates configuration
        - Loads flow from JSON file
        - Initializes WebScrapingTool
        - Loads custom parsers/models if specified
        - Processes authentication credentials if provided
        """
        # Process credentials (resolves environment variables)
        # This will populate self.credentials dict with actual values
        self.processing_credentials()
        
        # Make credentials available as flow variables
        if hasattr(self, 'credentials') and self.credentials:
            for key, value in self.credentials.items():
                if value:  # Only add non-empty credentials
                    self._variables[key] = value
                    # Log without revealing password
                    if key == 'password':
                        self._logger.info(f"Credential 'password' loaded (***)")
                    else:
                        self._logger.info(f"Credential '{key}' = {value}")
        
        # Check if we have input data
        if self.previous:
            self.data = self.input
            self._logger.info(f"Received input data with {len(self.data)} rows")
            
            # Auto-convert DataFrame columns to lists for flow variables
            # This allows using {column_name} in loops within the JSON flow
            self._convert_dataframe_columns_to_variables()
        
        # Load custom parser and model if specified
        self._load_custom_parser()
        self._load_custom_model()
        
        # Call parent start to load config and initialize tool
        await super().start(**kwargs)
        
        return True
    
    def _convert_dataframe_columns_to_variables(self):
        """
        Convert DataFrame columns to list variables for use in flow
        
        This enables patterns like:
        1. QueryToPandas returns DataFrame with 'zipcode' column
        2. Flow JSON can use {zipcodes} in a loop
        3. Component auto-converts 'zipcode' column to 'zipcodes' list
        
        Handles both singular and plural column names.
        """
        if not hasattr(self, 'data') or self.data is None or self.data.empty:
            return
        
        for col in self.data.columns:
            # Convert column to list (drop NaN values)
            col_list = self.data[col].dropna().astype(str).tolist()
            
            # Make available as both singular and plural
            # e.g., 'zipcode' column -> {zipcode} and {zipcodes} variables
            self._variables[col] = col_list
            
            # Also add plural version if not already exists
            if not col.endswith('s'):
                plural = f"{col}s"
                self._variables[plural] = col_list
                self._logger.info(
                    f"DataFrame column '{col}' available as {{{col}}} and {{{plural}}} "
                    f"({len(col_list)} items)"
                )
            else:
                self._logger.info(
                    f"DataFrame column '{col}' available as {{{col}}} ({len(col_list)} items)"
                )

    def _parse_extracted_data(self, raw_result: dict, local_vars: dict | None = None) -> List[dict]:
        """
        Parse extracted data using custom parser if available

        Args:
            raw_result: Raw result from WebScrapingTool
            local_vars: Variables de la iteración actual (por ejemplo {value}, {i}, etc.)

        Returns:
            List of parsed dictionaries
        """
        parsed_items = []

        if not raw_result.get('result'):
            return parsed_items

        # Combinar variables globales con las locales de la iteración
        vars_for_parser = dict(getattr(self, "_variables", {}) or {})
        if local_vars:
            vars_for_parser.update(local_vars)

        # Procesar cada paso del scraping
        for idx, step_result in enumerate(raw_result['result']):
            # DEBUG: Log what we're processing
            self._logger.debug(f"Processing step_result {idx}: has content={bool(step_result.get('content'))}, has extracted_data={bool(step_result.get('extracted_data'))}, extracted_data keys={list(step_result.get('extracted_data', {}).keys())}")

            # Merge extracted_data AND loop context from this step into vars (generic approach)
            step_vars = vars_for_parser.copy()

            # First, merge extracted_data if present
            if 'extracted_data' in step_result:
                step_vars.update(step_result['extracted_data'])

            # Then, merge loop context from metadata (this is where Parrot stores it)
            if 'metadata' in step_result and 'data' in step_result['metadata']:
                loop_context = step_result['metadata']['data']
                step_vars.update(loop_context)

            # Si hay un BeautifulSoup y tenemos parser
            # Si no existe 'bs' pero tenemos 'content', crear BeautifulSoup
            # SOLO para pasos de extracción (que tienen extracted_data no vacío)
            bs_object = None
            if 'bs' in step_result:
                bs_object = step_result['bs']
            elif self._parser_fn and 'content' in step_result and step_result.get('content'):
                # Verificar que este step tenga extracted_data con contenido real
                extracted = step_result.get('extracted_data', {})
                if extracted and isinstance(extracted, dict) and len(extracted) > 0:
                    # FILTRAR: Ignorar step_results de _extract_full_content
                    # que tienen keys genéricos como 'title', 'body_text', 'links', 'images'
                    generic_keys = {'title', 'body_text', 'links', 'images'}
                    extracted_keys = set(extracted.keys())

                    # Solo procesar si NO tiene SOLO keys genéricos
                    if not extracted_keys.issubset(generic_keys):
                        # Solo procesar si tiene algún contenido extraído (indicador de get_html/get_text)
                        # Verificar que el valor extraído no sea None o vacío
                        has_real_data = any(v is not None and v != '' for v in extracted.values())
                        if has_real_data:
                            # Crear BeautifulSoup desde el HTML content solo para pasos de extracción
                            try:
                                bs_object = BeautifulSoup(step_result['content'], 'html.parser')
                                self._logger.debug("Created BeautifulSoup from content field for extraction step")
                            except Exception as err:
                                self._logger.warning(f"Failed to create BeautifulSoup from content: {err}")
                    else:
                        self._logger.debug(f"Skipping generic _extract_full_content result with keys: {extracted_keys}")

            if bs_object and self._parser_fn:
                try:
                    import inspect
                    sig = inspect.signature(self._parser_fn)

                    if len(sig.parameters) > 1:
                        parsed = self._parser_fn(bs_object, step_vars)
                    else:
                        parsed = self._parser_fn(bs_object)

                    # Manejo de retorno
                    if isinstance(parsed, BaseModel):
                        parsed_items.append(parsed.model_dump())
                    elif isinstance(parsed, dict):
                        parsed_items.append(parsed)
                    elif isinstance(parsed, list):
                        for item in parsed:
                            if isinstance(item, BaseModel):
                                parsed_items.append(item.model_dump())
                            elif isinstance(item, dict):
                                parsed_items.append(item)
                            else:
                                self._logger.warning(
                                    f"Parser returned list with unexpected item type: {type(item)}"
                                )
                    else:
                        self._logger.warning(
                            f"Parser returned unexpected type: {type(parsed)}"
                        )
                except Exception as err:
                    self._logger.error(f"Error parsing with custom function: {err}")

            # Si no hay parser, usar extracted_data
            elif 'extracted_data' in step_result:
                # Aplicar el mismo filtro: ignorar resultados genéricos de _extract_full_content
                extracted = step_result.get('extracted_data', {})
                if extracted and isinstance(extracted, dict):
                    generic_keys = {'title', 'body_text', 'links', 'images'}
                    extracted_keys = set(extracted.keys())

                    # Solo agregar si NO tiene SOLO keys genéricos
                    if not extracted_keys.issubset(generic_keys):
                        parsed_items.append(step_result['extracted_data'])
                    else:
                        self._logger.debug(f"Skipping generic _extract_full_content data in fallback path")

        return parsed_items


    async def _scrape_single(self, **variables) -> Any:
        """
        Execute a single scraping operation
        
        Args:
            **variables: Additional variables to merge into the flow
        
        Returns:
            Scraped data - can be dict, list of dicts, or DataFrame
        """
        # Merge additional variables into config
        flow_config = self._tool_config.copy()
        
        # Replace variables in the flow config with current iteration values
        if variables:
            flow_config = self._replace_iteration_variables(flow_config, variables)
        
        try:
            result = await self._tool._execute(**flow_config)
            
            if result.get('status'):
                # If we have a custom parser, use it
                if self._parser_fn:
                    parsed_data = self._parse_extracted_data(result, variables)
                    return parsed_data if parsed_data else []
                
                # Otherwise, extract data normally
                extracted_data = {}
                
                if result.get('result'):
                    # Combine all extracted data from all steps
                    for step_result in result['result']:
                        if 'extracted_data' in step_result:
                            extracted_data.update(step_result['extracted_data'])
                
                return extracted_data
            else:
                self._logger.warning("Scraping operation failed")
                return {} if not self._parser_fn else []
                
        except Exception as err:
            self._logger.error(f"Error during scraping: {err}")
            raise ComponentError(
                f"ScrapTool: Scraping failed: {err}"
            ) from err

    def _replace_iteration_variables(self, obj: Any, variables: dict) -> Any:
        """
        Replace iteration variables ({value}, {index}, etc.) in flow config
        
        Args:
            obj: Object to process (dict, list, str, etc.)
            variables: Variables to replace
        
        Returns:
            Processed object with variables replaced
        """
        if isinstance(obj, str):
            for var_name, var_value in variables.items():
                obj = obj.replace(f"{{{var_name}}}", str(var_value))
            return obj
        elif isinstance(obj, dict):
            return {k: self._replace_iteration_variables(v, variables) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_iteration_variables(item, variables) for item in obj]
        else:
            return obj

    def _process_config_variables(self):
        """
        Override to prevent processing variables that will be used in iterations.

        When iterate_over is set, we want to preserve column placeholders (e.g., {url})
        so they can be replaced per-iteration instead of with the entire column list.
        """
        if self.iterate_over and hasattr(self, 'data'):
            # Skip processing config variables - will be done per-iteration
            self._logger.debug(f"Skipping config variable processing because iterate_over='{self.iterate_over}'")
            return

        # Otherwise, use parent's implementation
        super()._process_config_variables()

    async def run(self):
        """
        Execute the web scraping workflow

        If iterate_over is specified and input data exists, scrapes for each row.
        Otherwise, performs a single scraping operation.
        """
        results = []

        if self.iterate_over and self.previous and hasattr(self, 'data'):
            # Iterate over each row in the input dataframe
            self._logger.info(f"Iterating over column '{self.iterate_over}' ({len(self.data)} rows)")

            for idx, row in self.data.iterrows():
                iteration_value = row.get(self.iterate_over)

                if pd.isna(iteration_value):
                    self._logger.warning(f"Skipping row {idx}: {self.iterate_over} is NaN")
                    results.append([])
                    continue

                self._logger.info(f"Scraping {idx + 1}/{len(self.data)}: {iteration_value}")

                # Prepare variables for this iteration
                iteration_vars = {
                    'value': iteration_value,
                    'index': idx,
                    'i': idx,  # 0-based index
                    self.iterate_over: iteration_value,
                }
                for col_name, col_value in row.items():
                    if not pd.isna(col_value):
                        iteration_vars[col_name] = col_value

                try:
                    scraped_data = await self._scrape_single(**iteration_vars)
                    # Normalizamos: listas vacías -> [], dict -> [dict], None -> []
                    if isinstance(scraped_data, dict):
                        scraped_data = [scraped_data]
                    elif scraped_data is None:
                        scraped_data = []
                    results.append(scraped_data)
                except Exception as err:
                    self._logger.error(f"Error scraping row {idx}: {err}")
                    results.append([{'error': str(err), self.iterate_over: iteration_value}])

            # --- Aplanado inteligente ---
            # Caso 1: todas las iteraciones devolvieron listas de dicts -> concatenamos filas
            if all(isinstance(r, list) for r in results) and all(
                all(isinstance(x, dict) for x in r) for r in results
            ):
                flat = [item for sub in results for item in sub]
                self._result = pd.DataFrame(flat) if flat else pd.DataFrame()

            # Caso 2: todas son dicts -> expandimos columnas por fila original (comportamiento anterior)
            elif all(isinstance(r, dict) for r in results):
                results_df = pd.DataFrame(results)
                if self.auto_expand and len(results_df.columns) > 1:
                    for col in results_df.columns:
                        self.data[col] = results_df[col]
                else:
                    output_col = self.output_column or 'scraped_data'
                    for col in results_df.columns:
                        new_col_name = f"{output_col}_{col}" if len(results_df.columns) > 1 else output_col
                        self.data[new_col_name] = results_df[col]
                self._result = self.data

            # Caso 3: mixto o no dicts -> deja como una columna por iteración
            else:
                output_col = self.output_column or 'scraped_data'
                self.data[output_col] = results
                self._result = self.data

        else:
            # Single scraping operation (no iteration)
            self._logger.info("Performing single scraping operation")
            scraped_data = await self._scrape_single()

            if isinstance(scraped_data, list) and scraped_data:
                if all(isinstance(item, dict) for item in scraped_data):
                    self._result = pd.DataFrame(scraped_data)
                else:
                    output_col = self.output_column or 'scraped_data'
                    self._result = pd.DataFrame({output_col: scraped_data})
            elif isinstance(scraped_data, dict):
                max_len = 1
                for value in scraped_data.values():
                    if isinstance(value, list):
                        max_len = max(max_len, len(value))
                normalized_data = {}
                for key, value in scraped_data.items():
                    if isinstance(value, list) and len(value) == max_len:
                        normalized_data[key] = value
                    else:
                        normalized_data[key] = [value] * max_len if max_len > 1 else [value]
                self._result = pd.DataFrame(normalized_data)
            elif not scraped_data:
                self._result = pd.DataFrame()
            else:
                output_col = self.output_column or 'scraped_data'
                self._result = pd.DataFrame([{output_col: scraped_data}])

        # Print summary
        self._logger.info(f"Scraping completed. Result shape: {self._result.shape}")
        if len(self._result) <= 10:
            self._print_data_(self._result, 'ScrapTool')

        return self._result

    async def close(self):
        """Clean up resources"""
        # WebScrapingTool handles its own cleanup
        pass

