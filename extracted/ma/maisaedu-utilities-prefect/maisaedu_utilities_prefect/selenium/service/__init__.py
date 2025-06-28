from pydantic import BaseModel
from typing import Optional, Any

from selenium import webdriver

from maisaedu_utilities_prefect.constants.selenium import (
    SELENIUM_HUB_URL
)

class ScraperService(BaseModel):
    options: Any
    driver: Any
    
    def __init__(self, options: Optional[webdriver.ChromeOptions] = None, url = SELENIUM_HUB_URL, profile_directory = None, user_data_dir = None):
        if options is None:
            options = webdriver.ChromeOptions()
            if profile_directory is not None:
                options.add_argument(f"profile-directory={profile_directory}") 
            if user_data_dir is not None:
                options.add_argument(f"user-data-dir={user_data_dir}")
            options.add_argument("start-maximized")

        driver = webdriver.Remote(
            command_executor=url,
            options=options
        )

        super().__init__(options=options, driver=driver)

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def __del__(self):
        self.driver.close()
        self.driver.quit()
