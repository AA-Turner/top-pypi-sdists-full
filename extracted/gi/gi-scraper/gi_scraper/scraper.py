from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from urllib import parse
from queue import Queue

from .util import disable_safesearch, cleanup, scroll_range
from .stream import QueueStream, CacheStream
from .handler import Lookup, Response
from .cache import Cache


class Scraper:
    """
    A class for scraping image search results from Google using Selenium.

    Parameters:
    - workers (int): The number of worker threads to use for scraping. Default is 4.
    - headless (bool): Whether to run the Chrome browser in headless mode. Default is True.
    - cache (Cache): Cache instance with a custom path and timeout. If not specified, the default settings of the Cache class are used.

    Attributes:
    - __workers (int): The number of worker threads to use for scraping.
    - __queue (Queue): A queue for storing scraped responses.
    - __headless (bool): Whether to run the Chrome browser in headless mode.
    - __drivers (list[webdriver.Chrome]): List of Chrome WebDriver instances for parallel scraping.
    - __url_frame (str): The base URL for constructing image search URLs.
    - __current_url (str | None): The current URL being processed.
    - __current_count (int): The current count of scraped images.
    - __terminate (bool): Flag to indicate whether scraping should be terminated.
    - __pool (ThreadPoolExecutor | None): Thread pool for parallel scraping.
    - __cache (Cache): Cache instance for storing and retrieving scraped responses.

    Methods:
    - scrape(query: str, count: int) -> CacheStream | QueueStream:
        Scrapes image search results for a given query and count.

    - terminate_query() -> None:
        Terminates the current query scraping, committing the cache and shutting down the thread pool.

    - terminate() -> None:
        Terminates the scraper, committing the cache, shutting down the thread pool and exiting all webdrivers.

    - __del__() -> None:
        Destructor to ensure proper termination of the scraper.

    Private Methods:
    - __setup() -> list[webdriver.Chrome]:
        Sets up Chrome WebDriver instances with specified options.

    - __task(thread_id: int, driver: webdriver.Chrome, lookup: Lookup) -> None:
        Task for each worker thread to perform the actual scraping.

    """

    def __init__(self, workers: int = 4, headless: bool = True, cache=Cache()) -> None:
        self.__workers = workers
        self.__queue = Queue()
        self.__headless = headless
        self.__drivers = self.__setup()
        self.__url_frame = "https://www.google.com/search?{}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR5qK3rcbxAhXYF3IKHYiBDf8Q_AUoAXoECAEQAw&biw=1291&bih=590"
        self.__current_url: str | None = None
        self.__current_count = 0
        self.__terminate = False
        self.__pool: ThreadPoolExecutor | None = None
        self.__cache = cache
        self.__lock = Lock()

    def __setup(self) -> list[webdriver.Chrome]:
        """
        Sets up Chrome WebDriver instances with specified options.

        Returns:
        - list[webdriver.Chrome]: List of Chrome WebDriver instances.
        """

        driver_path = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("ignore-certificate-errors")
        options.add_argument("incognito")
        if self.__headless:
            options.add_argument("headless")
        options.add_argument("log-level=3")
        options.add_argument("disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        return [
            webdriver.Chrome(service=Service(driver_path), options=options)
            for _ in range(self.__workers)
        ]

    def scrape(self, query: str, count: int) -> CacheStream | QueueStream:
        """
        Scrapes image search results for a given query and count.

        Parameters:
        - query (str): The query string for image search.
        - count (int): The number of images to scrape.

        Returns:
        - CacheStream | QueueStream: A stream of scraped responses.
        """

        self.__terminate = False

        query = query.lower()
        self.__cache.commit()
        lookup = Lookup(query, count)

        if not self.__cache.is_stale(lookup=lookup):
            stream = CacheStream(self.__cache, lookup)
        else:
            self.__queue = Queue()
            stream = QueueStream(self.__queue, self.__cache)
            self.__current_url = self.__url_frame.format(parse.urlencode({"q": query}))
            self.__current_count = 0

            arguments = []

            for index, driver in enumerate(self.__drivers):
                arguments.append(
                    {
                        "thread_id": index,
                        "driver": driver,
                        "lookup": lookup,
                    }
                )

            self.__pool = ThreadPoolExecutor(max_workers=self.__workers)
            self.__pool.map(lambda x: self.__task(**x), arguments)

        return stream

    def __task(self, thread_id: int, driver: webdriver.Chrome, lookup: Lookup) -> None:
        """
        Task for each worker thread to perform the actual scraping.

        Parameters:
        - thread_id (int): The identifier of the worker thread.
        - driver (webdriver.Chrome): The Chrome WebDriver instance for scraping.
        - lookup (Lookup): The lookup object containing query and count information.
        """

        driver.get(self.__current_url)
        driver.maximize_window()

        delay = 3  # seconds

        action = ActionChains(driver)
        wait = WebDriverWait(driver, delay)

        if not disable_safesearch(driver, action, wait):
            return

        scroll_range(action, 5)

        image_elements = driver.find_elements(By.CLASS_NAME, "rg_i")

        batch = 20
        lower_bound = thread_id * batch
        upper_bound = lower_bound + batch

        element_counter = lower_bound

        while not self.__terminate:
            if (
                element_counter == upper_bound
            ):  # Next batch if target count not achieved
                lower_bound += batch * self.__workers
                upper_bound = lower_bound + batch
                element_counter = lower_bound

            thumbnail_element = image_elements[element_counter]
            element_counter += 1

            img_name = None
            img_thumb = None
            img_url = None
            page_name = None
            page_url = None
            img_width = None
            img_height = None

            try:
                img_thumb = thumbnail_element.get_attribute("src")
                img_name = thumbnail_element.get_attribute("alt")
            except Exception as e:
                # print(f"T_{thread_id}", ":", "Image Thumbnail and Image Name", e)
                pass

            try:
                img_width = thumbnail_element.get_attribute("width")
                img_height = thumbnail_element.get_attribute("height")

                img_width, img_height = map(cleanup, [img_width, img_height])
            except Exception as e:
                # print(f"T_{thread_id}", ":", "Image Dimension", e)
                pass

            try:
                action.click(thumbnail_element).perform()

                elements = wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "iPVvYb"))
                )

                img_element = elements[-1]
                img_url = img_element.get_attribute("src")
            except Exception as e:
                # print(f"T_{thread_id}", ":", "Image URL", e)
                pass

            if all(var is not None for var in [img_url, img_width, img_height]):
                try:
                    selector = "#Sva75c > div.A8mJGd.NDuZHe.CMiV2d.OGftbe-N7Eqid-H9tDt > div.dFMRD > div.AQyBn > div.tvh9oe.BIB1wf.hVa2Fd > c-wiz > div > div > div > div > div.trXfzf > div.h11UTe > a.Hnk30e.indIKd"

                    url_element = driver.find_element(By.CSS_SELECTOR, selector)
                    page_url = url_element.get_attribute("href")

                    header_element = url_element.find_element(By.TAG_NAME, "h1")
                    page_name = header_element.text

                except Exception as e:
                    # print(f"T_{thread_id}", ":", "Page Name and Page Link", e)
                    pass

                response = Response(
                    query=lookup.query,
                    name=img_name,
                    thumbnail=img_thumb,
                    image=img_url,
                    src_name=page_name,
                    src_page=page_url,
                    width=img_width,
                    height=img_height,
                )

                with self.__lock:
                    if not self.__current_count < lookup.count:
                        # Close stream immediately on completing count
                        self.__queue.put(None)
                        break

                    self.__queue.put(response)
                    self.__cache.feed(lookup, response)
                    self.__current_count += 1

    def terminate_query(self) -> None:
        """
        Terminates the current query being scraped and syncs all the worker threads.
        """

        self.__terminate = True
        self.__queue.put(None)

        if self.__pool is not None:
            self.__pool.shutdown()
        self.__pool = None

        self.__cache.commit()

    def terminate(self) -> None:
        """
        Terminates the scraper, committing the cache, shutting down the thread pool and quitting webdriver instances.
        """

        self.terminate_query()

        if self.__drivers is not None:
            for driver in self.__drivers:
                driver.quit()

    def __del__(self) -> None:
        """
        Destructor to ensure proper termination of the scraper.
        """

        if not self.__terminate:
            self.terminate()
