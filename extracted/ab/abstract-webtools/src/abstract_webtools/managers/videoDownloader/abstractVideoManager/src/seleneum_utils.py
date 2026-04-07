from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
def make_driver():
    opts = Options()
    opts.binary_location = '/usr/bin/chromium-browser'
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')

    service = Service('/usr/local/bin/chromedriver')
    return webdriver.Chrome(service=service, options=opts)
def get_url_source(url):
    driver = make_driver()
    driver.get(url)
    return driver.page_source
