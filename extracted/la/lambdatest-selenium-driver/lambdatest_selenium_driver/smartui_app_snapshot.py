import os
import uuid
import tempfile
import shutil
from typing import Dict, Optional, List
from selenium.webdriver.remote.webdriver import WebDriver
from lambdatest_sdk_utils.logger import setup_logger, get_logger
from lambdatest_sdk_utils.git_utils import get_git_info
from lambdatest_sdk_utils.models import BuildData, UploadSnapshotRequest
from lambdatest_sdk_utils.app_api import create_build, upload_screenshot, stop_build
from lambdatest_sdk_utils.rest import fetch_build_info
from lambdatest_selenium_driver.full_page_screenshot_util import FullPageScreenshotUtil

# Setup logger
setup_logger()
logger = get_logger('lambdatest-selenium-driver')

# Constants
DEFAULT_TEST_TYPE = "app"
OPTION_DEVICE_NAME = "deviceName"
OPTION_PLATFORM = "platform"
OPTION_TEST_TYPE = "testType"
OPTION_FULL_PAGE = "fullPage"
OPTION_PRECISE_SCROLL = "preciseScroll"
OPTION_PAGE_COUNT = "pageCount"
OPTION_NAVIGATION_BAR_HEIGHT = "navigationBarHeight"
OPTION_STATUS_BAR_HEIGHT = "statusBarHeight"
OPTION_IS_CLI_ENABLED = "isCliEnabled"

BROWSER_IOS = "safari"
BROWSER_ANDROID = "chrome"
PLATFORM_IOS = "iOS"
PLATFORM_ANDROID = "Android"

PROJECT_TOKEN_KEY = "projectToken"
PROJECT_TOKEN_ENV = "PROJECT_TOKEN"


class SnapshotConfig:
    """Configuration object for snapshot capture."""
    
    def __init__(self, device_name: str, platform: str, test_type: str, 
                 page_count: int, full_page: bool, precise_scroll: bool, is_cli_enabled: bool):
        self.device_name = device_name
        self.platform = platform
        self.test_type = test_type
        self.page_count = page_count
        self.full_page = full_page
        self.precise_scroll = precise_scroll
        self.is_cli_enabled = is_cli_enabled


class SmartUIAppSnapshot:
    """Main class for SmartUI App Snapshot functionality."""
    
    def __init__(self):
        """Initialize SmartUIAppSnapshot without proxy support."""
        self.project_token: Optional[str] = None
        self.build_data: Optional[BuildData] = None
    
    def start(self, options: Optional[Dict[str, str]] = None):
        """
        Initialize the SmartUI session and create a build.
        
        Args:
            options: Dictionary containing configuration options:
                - projectToken: LambdaTest project token (required)
                - buildName: Optional build name (auto-generated if not provided)
        
        Raises:
            Exception: If initialization fails
        """
        if options is None:
            options = {}
        
        self._initialize_project_token(options)
        self._create_build(options)
    
    def _initialize_project_token(self, options: Dict[str, str]):
        """Initialize project token from options or environment."""
        try:
            self.project_token = self._get_project_token(options)
            logger.info(f"Project token set")
        except Exception as e:
            logger.error("Project token is a mandatory field")
            raise Exception("Project token is a mandatory field", e)
    
    def _get_project_token(self, options: Dict[str, str]) -> str:
        """Get project token from options or environment variable."""
        # Check options first
        if self._is_valid_option_value(options, PROJECT_TOKEN_KEY):
            return options[PROJECT_TOKEN_KEY].strip()
        
        # Check environment variable
        env_token = os.getenv(PROJECT_TOKEN_ENV)
        if env_token and env_token.strip():
            return env_token.strip()
        
        raise ValueError("projectToken can't be empty")
    
    def _create_build(self, options: Dict[str, str]):
        """Create a build in SmartUI."""
        try:
            env_vars = dict(os.environ)
            git_info = get_git_info(env_vars)
            build_response = create_build(git_info, self.project_token, options)
            self.build_data = build_response.data
            
            if self.build_data:
                logger.info(f"Build ID set: {self.build_data.build_id} for build name: {self.build_data.name}")
                options["buildName"] = self.build_data.name
            else:
                raise Exception("Build not created")
        except Exception as e:
            logger.error(f"Couldn't create smartui build: {e}")
            raise Exception(f"Couldn't create smartui build: {e}")
    
    def smartui_app_snapshot(self, driver: WebDriver, screenshot_name: str, 
                            options: Optional[Dict[str, str]] = None):
        """
        Capture and upload a screenshot.
        
        Args:
            driver: Selenium WebDriver instance (required)
            screenshot_name: Unique name for the screenshot (required)
            options: Configuration options:
                - deviceName: Device name (required)
                - platform: Platform (iOS/Android) (required)
                - testType: "app" or "web" (default: "app")
                - fullPage: "true" to enable full-page screenshot (default: "false")
                - pageCount: Maximum pages for full-page (default: 20, max: 30)
                - preciseScroll: "true" to use precise scrolling (default: "false")
                - navigationBarHeight: Navigation bar height in pixels
                - statusBarHeight: Status bar height in pixels
        
        Raises:
            Exception: If screenshot capture or upload fails
        """
        if options is None:
            options = {}
        
        try:
            config = self._parse_snapshot_config(options)
            self._validate_mandatory_params(driver, screenshot_name, config.device_name)

            upload_request = self._create_upload_request(driver, screenshot_name, config)
            self._process_screenshot_capture(driver, screenshot_name, config, upload_request, options)
        except Exception as e:
            logger.error(f"Upload snapshot failed due to: {e}")
            raise Exception(f"Couldn't upload image to Smart UI due to: {e}")
    
    def _parse_snapshot_config(self, options: Dict[str, str]) -> SnapshotConfig:
        """Parse snapshot configuration from options."""
        test_type = self._get_option_value(options, OPTION_TEST_TYPE, DEFAULT_TEST_TYPE)
        if test_type not in ["app", "web"]:
            test_type = DEFAULT_TEST_TYPE
        
        return SnapshotConfig(
            device_name=self._get_option_value(options, OPTION_DEVICE_NAME),
            platform=self._get_option_value(options, OPTION_PLATFORM),
            test_type=test_type,
            page_count=self._parse_int_option(options, OPTION_PAGE_COUNT, 0),
            full_page=self._parse_boolean_option(options, OPTION_FULL_PAGE, False),
            precise_scroll=self._parse_boolean_option(options, OPTION_PRECISE_SCROLL, False),
            is_cli_enabled=self._parse_boolean_option(options, OPTION_IS_CLI_ENABLED, False)
        )
    
    def _validate_mandatory_params(self, driver: WebDriver, screenshot_name: str, device_name: str):
        """Validate mandatory parameters."""
        if driver is None:
            raise ValueError("An instance of the selenium driver object is required.")
        if not screenshot_name or screenshot_name.strip() == "":
            raise ValueError("The `snapshotName` argument is required.")
    
    def _create_upload_request(self, driver: WebDriver, screenshot_name: str, 
                               config: SnapshotConfig) -> UploadSnapshotRequest:
        """Create upload request object."""
        # Get window size
        rect = driver.get_window_rect()
        viewport_string = f"{rect['width']}x{rect['height']}"
        
        request = self._initialize_upload_request(screenshot_name, viewport_string, config)
        request.screenshot_hash = str(uuid.uuid4())
        
        return request
    
    def _initialize_upload_request(self, screenshot_name: str, viewport: str, config: SnapshotConfig) -> UploadSnapshotRequest:
        """Initialize upload request with base values."""
        request = UploadSnapshotRequest()
        if config.is_cli_enabled:
            build_info = fetch_build_info()
            if build_info and "data" in build_info:
                self.build_data = BuildData.from_dict(build_info["data"])
                self.project_token = self.build_data.project_token
                
        request.screenshot_name = screenshot_name
        request.project_token = self.project_token
        request.viewport = viewport
        
        return request
    
    def _configure_device_and_platform(self, request: UploadSnapshotRequest, 
                                      device_name: str):
        """Configure device and platform information."""
        browser_name = self._determine_default_browser(device_name)
        platform_name = self._determine_platform_name(browser_name)
        
        request.os = platform_name
        request.device_name = f"{device_name} {platform_name}"
        request.browser_name = self._determine_actual_browser(platform_name)
    
    def _determine_default_browser(self, device_name: str) -> str:
        """Determine default browser based on device name."""
        return PLATFORM_IOS if device_name.lower().startswith("i") else PLATFORM_ANDROID
    
    def _determine_platform_name(self, default_browser: str) -> str:
        """Determine platform name."""
        return default_browser
    
    def _determine_actual_browser(self, platform_name: str) -> str:
        """Determine actual browser name."""
        return BROWSER_IOS if "ios" in platform_name.lower() else BROWSER_ANDROID
    
    def _process_screenshot_capture(self, driver: WebDriver, screenshot_name: str,
                                    config: SnapshotConfig, upload_request: UploadSnapshotRequest,
                                    options: Dict[str, str]):
        """Process screenshot capture (full-page or single)."""
        self._process_upload_options(upload_request, options)
        
        page_count = config.page_count if config.full_page else 1
        if config.full_page:
            upload_request.full_page = "true"
        
        self._handle_screenshot_capture(driver, screenshot_name, config, upload_request, page_count)
    
    def _process_upload_options(self, upload_request: UploadSnapshotRequest, options: Dict[str, str]):
        """Process upload-related options."""
        self._set_upload_chunk_options(upload_request, options)
        self._set_navigation_options(upload_request, options)
        upload_request.crop_footer = "false"
        upload_request.crop_status_bar = "false"

    def _set_upload_chunk_options(self, upload_request: UploadSnapshotRequest, options: Dict[str, str]):
        """Set upload chunk related options."""
        #get boolean value for upload chunk from options
        upload_chunk = self._parse_boolean_option(options, "uploadChunk", False)
        if upload_chunk:
            upload_request.upload_chunk = "true"
    
    def _set_navigation_options(self, upload_request: UploadSnapshotRequest, options: Dict[str, str]):
        """Set navigation bar and status bar height options."""
        nav_bar_height = self._get_option_value(options, OPTION_NAVIGATION_BAR_HEIGHT)
        status_bar_height = self._get_option_value(options, OPTION_STATUS_BAR_HEIGHT)
        
        if nav_bar_height:
            upload_request.navigation_bar_height = nav_bar_height
        if status_bar_height:
            upload_request.status_bar_height = status_bar_height
    
    def _handle_screenshot_capture(self, driver: WebDriver, screenshot_name: str,
                                   config: SnapshotConfig, upload_request: UploadSnapshotRequest,
                                   page_count: int):
        """Handle screenshot capture (full-page or single)."""
        # Create temporary directory for screenshots
        temp_dir = tempfile.mkdtemp(prefix=f"smartui_{screenshot_name}_")
        
        try:
            full_page_util = FullPageScreenshotUtil(
                    driver, temp_dir, config.test_type, config.precise_scroll
            )
            upload_request.device_name = full_page_util.device_name
            self._configure_device_and_platform(upload_request, full_page_util.device_name)
            if config.full_page:
                # Full-page screenshot
                result = full_page_util.capture_full_page_screenshot(page_count)
                screenshots = result["screenshots"]
                self._validate_screenshots(screenshots)
                self._upload_screenshots(screenshots, upload_request)
            else:
                # Single screenshot
                screenshot_path = os.path.join(temp_dir, f"{screenshot_name}.png")
                screenshot_png = driver.get_screenshot_as_png()
                with open(screenshot_path, 'wb') as f:
                    f.write(screenshot_png)
                upload_request.full_page = "false"
                upload_screenshot(screenshot_path, upload_request, self.build_data)
        finally:
            # Clean up temporary directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def _validate_screenshots(self, screenshots: List[str]):
        """Validate that screenshots were captured."""
        if not screenshots:
            raise RuntimeError("SmartUI snapshot failed")
    
    def _upload_screenshots(self, screenshots: List[str], upload_request: UploadSnapshotRequest):
        """Upload screenshots (single or multiple)."""
        if len(screenshots) == 1:
            self._upload_single_screenshot(screenshots[0], upload_request)
        else:
            self._upload_multiple_screenshots(screenshots, upload_request)
    
    def _upload_single_screenshot(self, screenshot_path: str, upload_request: UploadSnapshotRequest):
        """Upload a single screenshot."""
        upload_request.full_page = "false"
        upload_screenshot(screenshot_path, upload_request, self.build_data)
    
    def _upload_multiple_screenshots(self, screenshots: List[str], upload_request: UploadSnapshotRequest):
        """Upload multiple screenshots as chunks."""
        total_screenshots = len(screenshots)
        
        # Upload all but last screenshot
        for i in range(total_screenshots - 1):
            upload_request.is_last_chunk = "false"
            upload_request.chunk_count = i
            upload_screenshot(screenshots[i], upload_request, self.build_data)
        
        # Upload last screenshot
        upload_request.is_last_chunk = "true"
        upload_request.chunk_count = total_screenshots - 1
        upload_screenshot(screenshots[total_screenshots - 1], upload_request, self.build_data)
    
    def stop(self):
        """Finalize the build and stop the SmartUI session."""
        try:
            if self.build_data and self.build_data.build_id:
                logger.info(f"Stopping session for buildId: {self.build_data.build_id}")
                stop_build(self.build_data.build_id, self.project_token)
                logger.info(f"Session ended for token: {self.project_token}")
            else:
                logger.info(f"Build ID not found to stop build for {self.project_token}")
        except Exception as e:
            logger.error(f"Couldn't stop the build due to an exception: {e}")
            raise Exception(f"Failed to stop build due to: {e}")
    
    def _get_option_value(self, options: Dict[str, str], key: str, default: str = "") -> str:
        """Get option value from options dictionary."""
        if options and key in options:
            value = options[key]
            return value.strip() if value else default
        return default
    
    def _is_valid_option_value(self, options: Dict[str, str], key: str) -> bool:
        """Check if option value is valid."""
        return options and key in options and options[key] and options[key].strip() != ""
    
    def _parse_int_option(self, options: Dict[str, str], key: str, default: int) -> int:
        """Parse integer option from options dictionary."""
        value = self._get_option_value(options, key)
        if not value:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Invalid integer value for {key}: {value}, using default: {default}")
            return default
    
    def _parse_boolean_option(self, options: Dict[str, str], key: str, default: bool) -> bool:
        """Parse boolean option from options dictionary."""
        value = self._get_option_value(options, key)
        if not value:
            return default
        return value.lower() == "true"

