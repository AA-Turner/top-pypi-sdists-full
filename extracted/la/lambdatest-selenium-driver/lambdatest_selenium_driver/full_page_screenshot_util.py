import os
import time
import tempfile
from typing import List, Dict, Any, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from lambdatest_sdk_utils.logger import get_logger

logger = get_logger('lambdatest-selenium-driver')

# Constants
DEFAULT_PAGE_COUNT = 20
MAX_PAGE_COUNT = 30
SCROLL_DELAY_MS = 0.2
WEB_SCROLL_PAUSE_MS = 1.0
IOS_SCROLL_DURATION_MS = 1500
ANDROID_SCROLL_SPEED = 1500
PAGE_SOURCE_CHECK_DELAY_MS = 0.1

# Scroll percentages
ANDROID_SCROLL_END_PERCENT = 0.3
ANDROID_SCROLL_HEIGHT_PERCENT = 0.35
IOS_SCROLL_HEIGHT_PERCENT = 0.3
IOS_START_Y_PERCENT = 0.7
IOS_END_Y_PERCENT = 0.4
WEB_SCROLL_HEIGHT_PERCENT = 0.4


class FullPageScreenshotUtil:
    """Utility class for capturing full-page screenshots with scrolling."""
    
    def __init__(self, driver: WebDriver, save_directory_name: str, 
                 test_type: str = "app", precise_scroll: bool = False):
        """
        Initialize the full page screenshot utility.
        
        Args:
            driver: Selenium WebDriver instance
            save_directory_name: Directory name to save screenshots
            test_type: Test type ("app" or "web")
            precise_scroll: Whether to use precise scrolling
        """
        self.driver = driver
        self.save_directory_name = save_directory_name
        self.test_type = test_type
        self.precise_scroll = precise_scroll
        self.platform = self._detect_platform()
        self.device_name = self._detect_device_name()
        self.prev_page_source = ""
        self.default_page_count = DEFAULT_PAGE_COUNT
        
        self._create_directory_if_needed()
    
    def _create_directory_if_needed(self):
        """Create directory for saving screenshots if it doesn't exist."""
        if not os.path.exists(self.save_directory_name):
            os.makedirs(self.save_directory_name)
            logger.info(f"Created directory: {self.save_directory_name}")
    
    def capture_full_page_screenshot(self, page_count: int) -> Dict[str, Any]:
        """
        Capture full-page screenshot by scrolling and taking multiple screenshots.
        
        Args:
            page_count: Maximum number of pages to capture (0 means use default)
            
        Returns:
            Dictionary containing list of screenshot file paths
        """
        self._initialize_page_count(page_count)
        
        screenshot_files = []
        chunk_count = 0
        is_last_scroll = False
        
        while not is_last_scroll and chunk_count < self.default_page_count:
            screenshot_file = self._capture_and_save_screenshot(chunk_count)
            screenshot_files.append(screenshot_file)
            
            chunk_count += 1
            self._scroll_down()
            is_last_scroll = self._has_reached_bottom()
        
        return {
            "screenshots": screenshot_files
        }
    
    def _initialize_page_count(self, page_count: int):
        """Initialize page count with validation."""
        if page_count == 0:
            self.default_page_count = DEFAULT_PAGE_COUNT
        elif page_count > MAX_PAGE_COUNT:
            logger.warning(f"Page count {page_count} exceeds maximum {MAX_PAGE_COUNT}, "
                          f"using {MAX_PAGE_COUNT}")
            self.default_page_count = MAX_PAGE_COUNT
        else:
            self.default_page_count = page_count
        
        logger.info(f"Page count set to: {self.default_page_count}")
    
    def _capture_and_save_screenshot(self, index: int) -> str:
        """Capture and save a screenshot."""
        screenshot_file_path = os.path.join(
            self.save_directory_name, 
            f"{self.save_directory_name}_{index}.png"
        )
        
        try:
            # Take screenshot
            screenshot = self.driver.get_screenshot_as_png()
            
            # Save to file
            with open(screenshot_file_path, 'wb') as f:
                f.write(screenshot)
            
            logger.info(f"Saved screenshot: {screenshot_file_path}")
            return screenshot_file_path
        except Exception as e:
            logger.error(f"Error saving screenshot: {e}")
            raise
    
    def _scroll_down(self) -> int:
        """Scroll down the page."""
        try:
            time.sleep(SCROLL_DELAY_MS)
            if self.test_type.lower() == "app":
                if self.platform == "ios":
                    return self._scroll_ios()
                else:
                    return self._scroll_android()
            else:
                return self._scroll_web()
        except Exception as e:
            logger.error(f"Error in scroll_down: {e}")
            return 0
    
    def _scroll_ios(self) -> int:
        """Scroll on iOS platform."""
        try:
            # Get window size
            rect = self.driver.get_window_rect()
            scroll_height = int(rect['height'] * IOS_SCROLL_HEIGHT_PERCENT)
            
            # Try primary scroll method using JavaScript
            if self._try_touch_swipe_ios():
                time.sleep(0.5)
                return scroll_height
            
            # Fallback methods
            if self._try_drag_from_to_ios(rect):
                time.sleep(0.5)
                return scroll_height
            
            if self._try_javascript_scroll_ios(scroll_height):
                time.sleep(0.5)
                return scroll_height
            
            logger.warning("All iOS scroll methods failed")
            return 0
        except Exception as e:
            logger.error(f"iOS scroll failed: {e}")
            return 0
    
    def _scroll_android(self) -> int:
        """Scroll on Android platform."""
        try:
            # Get window size
            rect = self.driver.get_window_rect()
            scroll_height = int(rect['height'] * ANDROID_SCROLL_HEIGHT_PERCENT)
            
            # Try primary scroll method
            if self._try_touch_swipe_android():
                time.sleep(0.2)
                return scroll_height
            
            # Fallback methods
            if self._try_drag_from_to_android(rect):
                time.sleep(0.2)
                return scroll_height
            
            if self._try_javascript_scroll_android(scroll_height):
                time.sleep(0.2)
                return scroll_height
            
            logger.warning("All Android scroll methods failed")
            return 0
        except Exception as e:
            logger.error(f"Android scroll failed: {e}")
            return 0
    
    def _scroll_web(self) -> int:
        """Scroll on web platform."""
        try:
            # Get window size
            rect = self.driver.get_window_rect()
            scroll_height = int(rect['height'] * WEB_SCROLL_HEIGHT_PERCENT)
            
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(WEB_SCROLL_PAUSE_MS)
            return scroll_height
        except Exception as e:
            logger.error(f"Web JavaScript scroll failed: {e}")
            return 0
    
    def _try_touch_swipe_ios(self) -> bool:
        """Try iOS touch swipe method."""
        try:
            params = {
                "start": "50%,70%",
                "end": "50%,40%",
                "duration": "2"
            }
            self.driver.execute_script("mobile:touch:swipe", params)
            return True
        except Exception as e:
            logger.debug(f"iOS touch:swipe failed: {e}")
            return False
    
    def _try_drag_from_to_ios(self, rect: Dict[str, int]) -> bool:
        """Try iOS drag from to method."""
        try:
            center_x = rect["width"] // 2
            start_y = int(rect["height"] * IOS_START_Y_PERCENT)
            end_y = int(rect["height"] * IOS_END_Y_PERCENT)
            
            swipe_obj = {
                "fromX": center_x,
                "fromY": start_y,
                "toX": center_x,
                "toY": end_y,
                "duration": 2.0
            }
            self.driver.execute_script("mobile:dragFromToForDuration", swipe_obj)
            return True
        except Exception as e:
            logger.debug(f"iOS dragFromToForDuration failed: {e}")
            return False
    
    def _try_javascript_scroll_ios(self, scroll_height: int) -> bool:
        """Try JavaScript scroll for iOS."""
        try:
            self.driver.execute_script(
                f"window.scrollTo({{top: window.pageYOffset + {scroll_height}, behavior: 'smooth'}});"
            )
            return True
        except Exception as e:
            logger.debug(f"iOS JavaScript scroll failed: {e}")
            return False
    
    def _try_touch_swipe_android(self) -> bool:
        """Try Android touch swipe method."""
        try:
            params = {
                "start": "50%,70%",
                "end": "50%,30%",
                "duration": "2"
            }
            self.driver.execute_script("mobile:touch:swipe", params)
            return True
        except Exception as e:
            logger.debug(f"Android touch:swipe failed: {e}")
            return False
    
    def _try_drag_from_to_android(self, rect: Dict[str, int]) -> bool:
        """Try Android drag from to method."""
        try:
            center_x = rect["width"] // 2
            start_y = int(rect["height"] * ANDROID_SCROLL_END_PERCENT)
            end_y = int(rect["height"] * ANDROID_SCROLL_HEIGHT_PERCENT)
            
            swipe_obj = {
                "fromX": center_x,
                "fromY": start_y,
                "toX": center_x,
                "toY": end_y,
                "duration": 2.0
            }
            self.driver.execute_script("mobile:dragFromToForDuration", swipe_obj)
            return True
        except Exception as e:
            logger.debug(f"Android dragFromToForDuration failed: {e}")
            return False
    
    def _try_javascript_scroll_android(self, scroll_height: int) -> bool:
        """Try JavaScript scroll for Android."""
        try:
            self.driver.execute_script(
                f"window.scrollTo({{top: window.pageYOffset + {scroll_height}, behavior: 'smooth'}});"
            )
            return True
        except Exception as e:
            logger.debug(f"Android JavaScript scroll failed: {e}")
            return False
    
    def _has_reached_bottom(self) -> bool:
        """Check if the bottom of the page has been reached."""
        try:
            time.sleep(PAGE_SOURCE_CHECK_DELAY_MS)
            
            if self.test_type.lower() == "web":
                return self._has_reached_bottom_web()
            else:
                return self._has_reached_bottom_mobile()
        except Exception as e:
            logger.warning(f"Error checking if reached bottom: {e}")
            return True
    
    def _has_reached_bottom_web(self) -> bool:
        """Check if bottom reached for web."""
        try:
            current_scroll_y = self.driver.execute_script(
                "return window.pageYOffset || document.documentElement.scrollTop || "
                "document.body.scrollTop || 0;"
            )
            
            page_height = self.driver.execute_script(
                "return Math.max("
                "document.body.scrollHeight, "
                "document.body.offsetHeight, "
                "document.documentElement.clientHeight, "
                "document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight);"
            )
            
            viewport_height = self.driver.execute_script(
                "return window.innerHeight || document.documentElement.clientHeight || "
                "document.body.clientHeight;"
            )
            
            is_at_bottom = (current_scroll_y + viewport_height) >= page_height
            return is_at_bottom
        except Exception as e:
            logger.warning(f"Error checking web bottom: {e}")
            return True
    
    def _has_reached_bottom_mobile(self) -> bool:
        """Check if bottom reached for mobile by comparing page source."""
        try:
            current_page_source = self.driver.page_source
            
            if self.prev_page_source == current_page_source:
                return True
            
            self.prev_page_source = current_page_source
            return False
        except Exception as e:
            logger.warning(f"Error checking mobile bottom: {e}")
            return True
    
    def _detect_platform(self) -> str:
        """Detect the platform (ios, android, or web)."""
        try:
            if hasattr(self.driver, 'capabilities'):
                caps = self.driver.capabilities
                platform_name = caps.get("platformName", "").lower() or caps.get("platform", "").lower()
                
                if "ios" in platform_name:
                    return "ios"
                elif "android" in platform_name:
                    return "android"
                else:
                    return "web"
            else:
                return "web"
        except Exception as e:
            logger.warning(f"Failed to detect platform: {e}")
            return "web"
    
    def _detect_device_name(self) -> str:
        """Detect the device name from capabilities."""
        try:
            if hasattr(self.driver, 'capabilities'):
                caps = self.driver.capabilities
                device_keys = ["deviceName", "device", "deviceModel", "deviceType"]
                
                for key in device_keys:
                    desired = caps.get("desired", {})
                    if key in desired and desired[key]:
                        return str(desired[key])
                for key in device_keys:
                    if key in caps and caps[key]:
                        return str(caps[key])
                
                logger.info("No device name capability found, using platform as device identifier")
                return self.platform
            else:
                return self.platform
        except Exception as e:
            logger.warning(f"Failed to detect device name: {e}")
            return self.platform

