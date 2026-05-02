"""
WorkdayReport Component

Automated extraction of Workday custom reports with dynamic dates and Excel download.
"""
import asyncio
import shutil
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from ..exceptions import ComponentError, ConfigError
from ..interfaces.credentials import CredentialsInterface
from .flow import FlowComponent

try:
    from parrot.tools.scraping import WebScrapingTool
except ModuleNotFoundError as exc:
    WebScrapingTool = None
    _IMPORT_ERROR: Optional[ModuleNotFoundError] = exc
else:
    _IMPORT_ERROR = None


class WorkdayReport(CredentialsInterface, FlowComponent):
    """
    Workday Report Extraction Component

    Automates the process of:
    1. Logging into Workday
    2. Navigating to a custom report
    3. Filling date parameters
    4. Downloading the Excel export
    5. Loading the data with Pandas

    **Features**
    - Dynamic date support (masks or fixed dates)
    - Configurable report URLs
    - Automatic download detection
    - Pandas DataFrame output
    - Browser automation (headless or visible)

    **Example Usage with Fixed Dates**

    ```yaml
    WorkdayReport:
      credentials:
        username: WORKDAY_REPORT_USERNAME
        password: WORKDAY_REPORT_PASSWORD
      report_url: "https://wd501.myworkday.com/troc/d/task/1422$594.htmld"
      start_date: "11/07/2025"
      end_date: "11/07/2025"
      headless: false
    ```

    **Example Usage with Dynamic Dates (Masks)**

    ```yaml
    WorkdayReport:
      credentials:
        username: WORKDAY_REPORT_USERNAME
        password: WORKDAY_REPORT_PASSWORD
      report_url: "https://wd501.myworkday.com/troc/d/task/1422$594.htmld"
      start_date: "{start_date}"
      end_date: "{end_date}"
      masks:
        "{start_date}":
          - yesterday
          - days_offset: -7
          - mask: "%m/%d/%Y"
        "{end_date}":
          - yesterday
          - mask: "%m/%d/%Y"
      headless: true
    ```

    **Example with Data Processing Pipeline**

    ```yaml
    name: WorkdayCustomPunchReport
    steps:
      - WorkdayReport:
          credentials:
            username: WORKDAY_REPORT_USERNAME
            password: WORKDAY_REPORT_PASSWORD
          report_url: "https://wd501.myworkday.com/troc/d/task/1422$594.htmld"
          start_date: "11/07/2025"
          end_date: "11/07/2025"

      - FilterRows:
          filter_conditions:
            clean_empty:
              columns: ["Worker", "Date"]

      - CopyToPg:
          credentials:
            host: DB_HOST
            port: 5432
            username: DB_USER
            password: DB_PASS
            database: analytics
          table_name: workday_custom_punch
          schema: workday
    ```

    **Parameters**

    - **credentials** (required): Dict with username and password (env var names)
    - **report_url** (required): Full URL of the Workday report
    - **start_date** (optional): Start date in MM/DD/YYYY format or "{placeholder}" for masks
    - **end_date** (optional): End date in MM/DD/YYYY format or "{placeholder}" for masks
    - **masks** (optional): Dynamic date masks (keys must match placeholders with braces)
    - **requires_supervisory** (optional): Add supervisory organization selection steps (default: False)
    - **supervisory_name** (optional): Name to search for in supervisory organizations (e.g., "Bret")
    - **headless** (optional): Run browser in headless mode (default: True)
    - **browser** (optional): Browser type: chrome, firefox, edge (default: chrome)
    - **driver_type** (optional): Driver type: selenium or playwright (default: selenium)
    - **download_directory** (optional): Where to download files (default: /tmp/workday_downloads)
    - **report_generation_wait** (optional): Seconds to wait after submitting dates before clicking download (default: 5). Increase for large date ranges that take longer to generate.
    - **download_timeout** (optional): Seconds to wait for download (default: 60)
    - **filename** (optional): Expected filename or pattern (e.g., "Custom_Punch*.xlsx")
    - **rename** (optional): Rename file with masks (e.g., "workday_{date}.xlsx")
    - **destination_directory** (optional): Move/copy file to different directory (like FileCopy)
    - **remove_source** (optional): Remove original file after rename/move (default: True)
    - **move** (optional): Alias for remove_source (like FileCopy)
    - **pandas_kwargs** (optional): Arguments to pass to pd.read_excel()
    - **cleanup_downloads** (optional): Delete downloaded files after loading (default: False)

    **Returns**

    pathlib.Path to the downloaded (and optionally renamed) file
    """

    _credentials: dict = {
        "username": str,
        "password": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs: Any,
    ) -> None:
        # Required parameters
        self.report_url: str = kwargs.get("report_url")
        if not self.report_url:
            raise ConfigError("WorkdayReport: 'report_url' is required")

        # Date parameters
        self.start_date: Optional[str] = kwargs.get("start_date")
        self.end_date: Optional[str] = kwargs.get("end_date")

        # Flow configuration flags
        self.requires_supervisory: bool = kwargs.get("requires_supervisory", False)
        self.supervisory_name: Optional[str] = kwargs.get("supervisory_name")  # Name to search for

        # Browser configuration
        self.headless: bool = kwargs.get("headless", True)
        self.browser: str = kwargs.get("browser", "chrome")
        self.driver_type: str = kwargs.get("driver_type", "selenium")

        # Download configuration
        download_dir = kwargs.get("download_directory", "/tmp/workday_downloads")
        self.download_directory: Path = Path(download_dir)
        self.download_timeout: int = int(kwargs.get("download_timeout", 60))
        self.cleanup_downloads: bool = kwargs.get("cleanup_downloads", False)
        self.filename: Optional[str] = kwargs.get("filename")  # Expected filename or pattern
        self.rename: Optional[str] = kwargs.get("rename")  # Optional rename with masks
        self.remove_source: bool = kwargs.get("remove_source", True)  # Remove original after rename (like FileCopy)

        # Destination directory (like FileCopy pattern)
        dest_dir = kwargs.get("destination_directory")
        self.destination_directory: Optional[Path] = Path(dest_dir) if dest_dir else None

        # Support 'move' as alias for remove_source (like FileCopy)
        if "move" in kwargs:
            self.remove_source = kwargs.get("move")

        # Wait before download button (seconds) — configurable from YAML for slow reports
        self.report_generation_wait: int = int(kwargs.get("report_generation_wait", 5))

        # Pandas configuration
        self.pandas_kwargs: Dict[str, Any] = kwargs.get("pandas_kwargs", {
            "sheet_name": 0,
            "header": 0,
        })

        # Internal state
        self._scraping_tool: Optional[Any] = None
        self._driver = None
        self._downloaded_file: Optional[Path] = None

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def _format_date_for_input(self, date_str: str) -> str:
        """
        Convert date from MM/DD/YYYY to MMDDYYYY for keyboard input.

        Example: "11/07/2025" -> "11072025"
        """
        return date_str.replace("/", "")

    def _get_supervisory_steps(self) -> List[Dict[str, Any]]:
        """Build supervisory organization selection steps based on actual HTML structure."""
        steps = [
            {
                "action": "wait",
                "timeout": 5,
                "condition_type": "simple",
                "description": "Wait for Supervisory Organizations field"
            },
            {
                "action": "click",
                "selector": "//label[text()='Supervisory Organizations']/ancestor::li//span[@data-automation-id='promptIcon']",
                "selector_type": "xpath",
                "description": "Click Supervisory Organizations icon to activate list"
            },
            {
                "action": "wait",
                "timeout": 2,
                "condition_type": "simple",
                "description": "Wait for supervisory menu to appear"
            },
            {
                "action": "click",
                "selector": "//div[@data-automation-id='promptOption' and @data-automation-label='Supervisory Organization']",
                "selector_type": "xpath",
                "description": "Select 'Supervisory Organization' option (singular)"
            },
            {
                "action": "wait",
                "timeout": 2,
                "condition_type": "simple",
                "description": "Wait for organization list"
            },
        ]

        # If supervisory_name is specified, search and select it
        if self.supervisory_name:
            steps.extend([
                {
                    "action": "click",
                    "selector": f"//div[@data-automation-id='promptOption' and contains(@data-automation-label, '{self.supervisory_name}')]/..//input[@type='checkbox']",
                    "selector_type": "xpath",
                    "description": f"Select '{self.supervisory_name}' checkbox"
                },
                {
                    "action": "click",
                    "selector": "button[data-automation-id='wd-CommandButton_uic_okButton']",
                    "description": "Click OK to confirm supervisory selection"
                },
                {
                    "action": "wait",
                    "timeout": 2,
                    "condition_type": "simple",
                    "description": "Wait for form to process supervisory selection"
                },
                {
                    "action": "click",
                    "selector": "//div[@data-automation-id='checkboxPanel']/input[@type='checkbox']",
                    "selector_type": "xpath",
                    "description": "Click additional checkbox (Include Subordinate Organizations)"
                },
            ])

        return steps

    def _get_identity_login_url(self) -> str:
        """
        Derive the Workday Identity login URL from the report URL.

        Example:
            report_url:  https://wd501.myworkday.com/troc/d/task/1422$845.htmld
            identity_url: https://identity.wd501.myworkday.com/wday/authgwy/troc/upc/login
        """
        from urllib.parse import urlparse
        parsed = urlparse(self.report_url)
        # hostname: wd501.myworkday.com  →  prefix: wd501
        host_prefix = parsed.hostname.split(".")[0]
        # path: /troc/d/task/...  →  tenant: troc
        tenant = parsed.path.lstrip("/").split("/")[0]
        return f"https://identity.{host_prefix}.myworkday.com/wday/authgwy/{tenant}/upc/login"

    def _build_flow(self) -> List[Dict[str, Any]]:
        """
        Build the WebScrapingTool flow with dynamic dates and URL.

        The flow is based on the successful workday_login.json pattern.
        Uses flags to conditionally add steps.
        """
        start_date_input = self._format_date_for_input(self.start_date)
        end_date_input = self._format_date_for_input(self.end_date)

        username = self.credentials.get("username")
        password = self.credentials.get("password")
        identity_url = self._get_identity_login_url()

        flow = [
            {
                # Navigate directly to the identity login page instead of the report URL.
                # The report URL redirects to identity, but that redirect can timeout (8-10s)
                # and leave Chrome stuck. Going directly is faster and more reliable.
                "action": "navigate",
                "url": identity_url,
                "description": "Navigate directly to Workday identity login page"
            },
            {
                "action": "wait",
                "timeout": 15,
                "condition_type": "selector",
                "condition": "[data-testid='username-password-button']",
                "description": "Wait for Username and Password auth button (new UPC SPA)"
            },
            {
                "action": "click",
                "selector": "[data-testid='username-password-button']",
                "description": "Click Username and Password option"
            },
            {
                "action": "wait",
                "timeout": 5,
                "condition_type": "simple",
                "description": "Wait for login form to render after clicking auth option"
            },
            {
                "action": "fill",
                "selector": "input[data-testid='username']",
                "value": username,
                "description": "Fill username"
            },
            {
                "action": "fill",
                "selector": "input[data-testid='password']",
                "value": password,
                "description": "Fill password"
            },
            {
                "action": "click",
                "selector": "button[data-testid='login-button']",
                "description": "Click Sign In button"
            },
            {
                "action": "wait",
                "timeout": 5,
                "condition_type": "simple",
                "description": "Wait after login"
            },
            {
                # TrustDevice page: new UPC renders Skip as [data-testid='btn-skip'].
                # Old xpath with data-automation-id='linkButton' no longer exists.
                "action": "click",
                "selector": "[data-testid='btn-skip']",
                "optional": True,
                "description": "Click Skip on 'Remember this device' screen (if shown)"
            },
        ]

        # After login, navigate to the report URL.
        # (We logged in via the identity URL directly, so Workday lands on home — not the report.)
        flow.append({
            "action": "navigate",
            "url": self.report_url,
            "description": "Navigate to report after login"
        })

        # Add supervisory steps if required
        if self.requires_supervisory:
            flow.extend(self._get_supervisory_steps())

        # Continue with date steps
        flow.extend([
            {
                "action": "wait",
                "timeout": 5,
                "condition_type": "simple",
                "description": "Wait for date popup"
            },
            {
                "action": "click",
                "selector": "(//input[@aria-label='Month'])[1]",
                "selector_type": "xpath",
                "description": "Click Start Date - Month field"
            },
            {
                "action": "press_key",
                "keys": list(start_date_input),
                "sequential": True,
                "description": f"Type Start Date: {self.start_date}"
            },
            {
                "action": "wait",
                "timeout": 1,
                "condition_type": "simple",
                "description": "Wait after filling Start Date"
            },
            {
                "action": "click",
                "selector": "(//input[@aria-label='Month'])[2]",
                "selector_type": "xpath",
                "description": "Click To Date - Month field (second date field)"
            },
            {
                "action": "press_key",
                "keys": list(end_date_input),
                "sequential": True,
                "description": f"Type End Date: {self.end_date}"
            },
            {
                "action": "click",
                "selector": "button[data-automation-id='wd-CommandButton_uic_okButton']",
                "description": "Click OK button"
            },
            {
                "action": "wait",
                "timeout": self.report_generation_wait,
                "condition_type": "simple",
                "description": f"Wait for report to generate ({self.report_generation_wait}s — set via report_generation_wait)"
            },
            {
                "action": "click",
                "selector": "div[data-automation-id='excelIconButton']",
                "description": "Click Excel export button"
            },
            {
                "action": "wait",
                "timeout": 3,
                "condition_type": "simple",
                "description": "Wait for download modal"
            },
            {
                "action": "click",
                "selector": "button[data-automation-id='uic_downloadButton']",
                "description": "Click Download button"
            },
            {
                "action": "wait",
                "timeout": 5,
                "condition_type": "simple",
                "description": "Wait for download to start"
            }
        ])

        return flow

    async def start(self, **kwargs: Any) -> bool:
        """Initialize component and process credentials/dates"""
        await super().start(**kwargs)

        if WebScrapingTool is None:
            raise ComponentError(
                f"WorkdayReport requires ai-parrot's WebScrapingTool. "
                f"Install ai-parrot package: {_IMPORT_ERROR}"
            )

        # Process credentials
        self.processing_credentials()

        if not self.credentials.get("username"):
            raise ConfigError("WorkdayReport: Missing WORKDAY_REPORT_USERNAME credential")
        if not self.credentials.get("password"):
            raise ConfigError("WorkdayReport: Missing WORKDAY_REPORT_PASSWORD credential")

        # Process dates with mask replacement
        # This handles both fixed dates ("11/07/2025") and masked dates ("{start_date}")
        if self.start_date:
            self.start_date = self.mask_replacement(self.start_date)
            self._logger.info(f"Start date: {self.start_date}")
        if self.end_date:
            self.end_date = self.mask_replacement(self.end_date)
            self._logger.info(f"End date: {self.end_date}")

        # Validate that we have dates
        if not self.start_date:
            raise ConfigError("WorkdayReport: 'start_date' is required (or define in masks)")
        if not self.end_date:
            raise ConfigError("WorkdayReport: 'end_date' is required (or define in masks)")

        # Ensure download_directory is a Path object (may have been overwritten as string)
        if not isinstance(self.download_directory, Path):
            self.download_directory = Path(self.download_directory)

        # Create download directory
        self.download_directory.mkdir(parents=True, exist_ok=True)
        self._logger.info(f"Download directory: {self.download_directory}")

        # Ensure destination_directory is a Path and create it if specified
        if self.destination_directory:
            if not isinstance(self.destination_directory, Path):
                self.destination_directory = Path(self.destination_directory)
            self.destination_directory.mkdir(parents=True, exist_ok=True)
            self._logger.info(f"Destination directory: {self.destination_directory}")

        return True

    def _is_download_complete(self, file_path: Path) -> bool:
        """
        Check if file download is complete.

        Returns True if:
        - File exists
        - Not a temp file (.crdownload, .part)
        - Size is stable (same size after 1 second)
        """
        if not file_path.exists():
            return False

        # Check for temp extensions
        if file_path.suffix in {'.crdownload', '.part', '.tmp'}:
            return False

        # Check if size is stable
        try:
            size1 = file_path.stat().st_size
            time.sleep(1)
            size2 = file_path.stat().st_size
            return size1 == size2 and size1 > 0
        except Exception:
            return False

    async def _wait_for_download(self, timeout: int) -> Path:
        """
        Wait for a file to appear in the download directory.

        If filename is specified, looks for that specific file or pattern.
        Otherwise, looks for any new files.

        Args:
            timeout: Maximum seconds to wait

        Returns:
            Path to the downloaded file (renamed if rename_to is specified)

        Raises:
            ComponentError: If download times out or fails
        """
        start_time = time.time()

        if self.filename:
            # Look for specific filename or pattern
            self._logger.info(f"Looking for file: {self.filename} in {self.download_directory}")

            while time.time() - start_time < timeout:
                matching_files = list(self.download_directory.glob(self.filename))

                if matching_files:
                    # Take the most recent file if multiple matches
                    file_path = max(matching_files, key=lambda p: p.stat().st_mtime)

                    if self._is_download_complete(file_path):
                        self._logger.info(f"Found file: {file_path.name}")

                        # Determine destination (like FileCopy pattern)
                        if self.rename or self.destination_directory:
                            # Determine new filename
                            new_name = self.mask_replacement(self.rename) if self.rename else file_path.name

                            # Determine destination directory
                            dest_dir = self.destination_directory if self.destination_directory else file_path.parent
                            new_path = dest_dir / new_name

                            if self.remove_source:
                                # Move (removes original)
                                self._logger.info(f"Moving {file_path} -> {new_path}")
                                shutil.move(str(file_path), str(new_path))
                            else:
                                # Copy (keeps original)
                                self._logger.info(f"Copying {file_path} -> {new_path}")
                                shutil.copy2(str(file_path), str(new_path))

                            return new_path

                        return file_path

                await asyncio.sleep(1)

            raise ComponentError(
                f"WorkdayReport: Download timeout after {timeout} seconds. "
                f"File matching '{self.filename}' not found in {self.download_directory}"
            )
        else:
            # Look for any new files (original behavior)
            initial_files = set(self.download_directory.glob("*"))
            self._logger.info(f"Monitoring {self.download_directory} for new files...")

            while time.time() - start_time < timeout:
                current_files = set(self.download_directory.glob("*"))
                new_files = current_files - initial_files

                if new_files:
                    # Found a new file, check if it's complete
                    for file_path in new_files:
                        if self._is_download_complete(file_path):
                            self._logger.info(f"Download complete: {file_path.name}")

                            # Determine destination (like FileCopy pattern)
                            if self.rename or self.destination_directory:
                                # Determine new filename
                                new_name = self.mask_replacement(self.rename) if self.rename else file_path.name

                                # Determine destination directory
                                dest_dir = self.destination_directory if self.destination_directory else file_path.parent
                                new_path = dest_dir / new_name

                                if self.remove_source:
                                    # Move (removes original)
                                    self._logger.info(f"Moving {file_path} -> {new_path}")
                                    shutil.move(str(file_path), str(new_path))
                                else:
                                    # Copy (keeps original)
                                    self._logger.info(f"Copying {file_path} -> {new_path}")
                                    shutil.copy2(str(file_path), str(new_path))

                                return new_path

                            return file_path

                await asyncio.sleep(1)

            raise ComponentError(
                f"WorkdayReport: Download timeout after {timeout} seconds. "
                f"No new files detected in {self.download_directory}"
            )

    async def _load_excel_file(self, file_path: Path) -> pd.DataFrame:
        """
        Load Excel file with Pandas.

        Uses pandas_kwargs from configuration for customization.
        """
        try:
            self._logger.info(f"Loading Excel file: {file_path.name}")
            df = pd.read_excel(file_path, **self.pandas_kwargs)
            self._logger.info(f"Loaded DataFrame with shape: {df.shape}")
            return df
        except Exception as exc:
            raise ComponentError(
                f"WorkdayReport: Failed to load Excel file {file_path}: {exc}"
            ) from exc

    async def _execute_flow(self) -> None:
        """Execute the WebScrapingTool flow"""
        if self._scraping_tool is None:
            tool_args = {
                "headless": self.headless,
                "browser": self.browser,
                "driver_type": self.driver_type,
                "download_directory": str(self.download_directory),
            }
            try:
                self._scraping_tool = WebScrapingTool(**tool_args)
            except Exception as exc:
                raise ComponentError(
                    f"WorkdayReport: Unable to initialize WebScrapingTool: {exc}"
                ) from exc

        # Build flow with current dates
        flow_steps = self._build_flow()

        try:
            result = await self._scraping_tool._execute(steps=flow_steps)
        except Exception as exc:
            raise ComponentError(
                f"WorkdayReport: WebScrapingTool flow failed: {exc}"
            ) from exc

        try:
            # Capture driver reference for cleanup
            self._driver = getattr(self._scraping_tool, "driver", None)
        except Exception:
            pass

        return result

    async def run(self) -> Path:
        """
        Execute the complete workflow:
        1. Run WebScrapingTool flow (login, dates, download)
        2. Wait for file download
        3. Rename if requested
        4. Return Path to downloaded file
        """
        # Execute the scraping flow
        try:
            await self._execute_flow()
        except Exception as exc:
            raise ComponentError(
                f"WorkdayReport: Failed to execute flow: {exc}"
            ) from exc

        # Wait for download and get file path
        try:
            self._downloaded_file = await self._wait_for_download(self.download_timeout)
        except Exception as exc:
            raise ComponentError(
                f"WorkdayReport: Failed to detect download: {exc}"
            ) from exc

        self._logger.info(f"Successfully downloaded: {self._downloaded_file}")
        self._result = self._downloaded_file

        return self._result

    async def close(self) -> None:
        """Cleanup resources"""
        if self._scraping_tool:
            close_method = getattr(self._scraping_tool, "close", None)
            if close_method:
                try:
                    if asyncio.iscoroutinefunction(close_method):
                        await close_method()
                    else:
                        close_method()
                except Exception:
                    pass

        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass

        self._scraping_tool = None
        self._driver = None
