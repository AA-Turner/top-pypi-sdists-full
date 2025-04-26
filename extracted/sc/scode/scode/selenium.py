import os
import sys
import shutil
import time
import pyperclip
import random
import requests
import subprocess
import chromedriver_autoinstaller as AutoChrome
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import glob


def get_status(driver: WebDriver):
    """
    If the driver can get the title of the page, it's alive, otherwise it's dead
    
    :param driver: The webdriver object
    :type driver: WebDriver
    :return: The status of the driver.
    """
    try:
        driver.title
    except:
        return "Dead"
    else:
        return "Alive"

def find_testdriver():

    import zipfile

    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    zip_link = get_chromedriver_url(AutoChrome.get_chrome_version())

    if zip_link:
        zip_response = requests.get(zip_link)
        with open("chromedriver.zip", "wb") as zip_file:
            zip_file.write(zip_response.content)

        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall(f"C:\\chromedriver\\{chrome_ver}\\")

        os.remove("chromedriver.zip")
        for directory in glob.glob(f"C:\\chromedriver\\{chrome_ver}\\*"):
            if 'chromedriver' in directory:
                os.rename(directory, f"C:\\chromedriver\\{chrome_ver}\\chromedriver")

        source_path = f"C:\\chromedriver\\{chrome_ver}\\chromedriver\\chromedriver.exe"
        target_path = f"C:\\chromedriver\\{chrome_ver}\\chromedriver.exe"
        shutil.move(source_path, target_path)

def get_chromedriver_url(chromedriver_version, no_ssl=False):

    try:
        from packaging import version
    except:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'packaging'])
        from packaging import version

    platform, architecture = AutoChrome.utils.get_platform_architecture()
    if chromedriver_version >= "115":  
        versions_url = "googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
        versions_url = "http://" + versions_url if no_ssl else "https://" + versions_url
        response = requests.get(versions_url)
        download_version_list = response.json()

        for good_version in download_version_list["versions"]:
            if version.parse(good_version["version"]) > version.parse(chromedriver_version):
                try: download_urls = last_version["downloads"]["chromedriver"]
                except: download_urls = good_version["downloads"]["chromedriver"]
                for url in download_urls:
                    if url["platform"] == platform + architecture:
                        return url['url']
            last_version = good_version
    else:  
        base_url = "chromedriver.storage.googleapis.com/"
        base_url = "http://" + base_url if no_ssl else "https://" + base_url
        return base_url + chromedriver_version + "/chromedriver_" + platform + architecture + ".zip"


def load_driver(chrome_options=None, mode=None, userId=None, port=9222, **kwargs) -> WebDriver:
    """
    It opens a Chrome browser with the specified options
    
    :param chrome_options: This is an instance of the ChromeOptions class. You can pass an existing
    instance of ChromeOptions to this parameter, or you can create a new instance of ChromeOptions
    :param mode: This is the mode you want to use. You can use multiple modes at once
    :param userId: This is the user ID that you want to use. This is used to create a cache folder for
    the user
    :param port: The port number that the Chrome browser will be running on, defaults to 9222 (optional)
    :return: A WebDriver object.
    """

    # userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    # userAgentMo = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    # userAgent = UserAgent().random

    valid_mode_lst = [
        'fast',
        'cache',
        'debug',
        'secret',
        'android',
        'ios'
    ]

    ios_agent = ['Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A432 Safari/604.1']
    
    and_agent = ['Mozilla/5.0 (Linux; Android 11; SM-G973W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; SM-N960U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G930F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36']

    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    chrome_driver_path = 'C:\\chromedriver\\'

    if not os.path.isdir('c:\\chromedriver'):
        os.mkdir('c:\\chromedriver')
    
    if chrome_options is None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--window-position=850,0')
    
    chrome_options.add_argument('--disable-features=ChromeWhatsNewUI')
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    if not mode:

        pass

    else:

        if isinstance(mode, str):

            md = mode
            
            if md == 'fast':

                prefs = {"profile.managed_default_content_settings.images": 2}
                chrome_options.add_experimental_option("prefs", prefs)
                
            if md == 'cache':
                
                userDataFolder = 'c:/cache/{}'.format(userId)
                chrome_options.add_argument('--user-data-dir=' + userDataFolder)
                chrome_options.add_argument('--disk-cache-dir=' + userDataFolder)
            
            if md == 'debug':
                import subprocess
                try:
                    subprocess.Popen(rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')
                except:
                    subprocess.Popen(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')

                chrome_options = Options()                                                                    # 옵션객체 생성
                chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
            
            if md == 'secret':
                chrome_options.add_argument('--incognito')
            
            if md == 'android':
                user_agent = random.choice(and_agent)
                chrome_options.add_argument("user-agent=" + user_agent)
            
            if md == 'ios':
                user_agent = random.choice(ios_agent)
                chrome_options.add_argument("user-agent=" + user_agent)
            
            if md not in valid_mode_lst:
                modes_text = ", ".join(valid_mode_lst)
                raise ValueError(f"Invalid Value : {mode}\nPlease Use below instead of {mode}\n\n{modes_text}\n\nUsage : load_driver(mode=['{random.choice(valid_mode_lst)}'])")
        else:
            for md in mode:
        
                if md == 'fast':

                    prefs = {"profile.managed_default_content_settings.images": 2}
                    chrome_options.add_experimental_option("prefs", prefs)
                    
                if md == 'cache':
                    
                    userDataFolder = 'c:/cache/{}'.format(userId)
                    chrome_options.add_argument('--user-data-dir=' + userDataFolder)
                    chrome_options.add_argument('--disk-cache-dir=' + userDataFolder)
                
                if md == 'debug':
                    import subprocess
                    try:
                        subprocess.Popen(rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')
                    except:
                        subprocess.Popen(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')

                    chrome_options = Options()                                                                    # 옵션객체 생성
                    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
                
                if md == 'secret':
                    chrome_options.add_argument('--incognito')

                if md == 'android':
                    user_agent = random.choice(and_agent)
                    chrome_options.add_argument("user-agent=" + user_agent)
                
                if md == 'ios':
                    user_agent = random.choice(ios_agent)
                    chrome_options.add_argument("user-agent=" + user_agent)
                
                if md not in valid_mode_lst:
                    modes_text = ", ".join(valid_mode_lst)
                    raise ValueError(f"Invalid Value : {mode}\nPlease Use below instead of {mode}\n\n{modes_text}\n\nUsage : load_driver(mode=['{random.choice(valid_mode_lst)}'])")
    
    if os.path.isfile(f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe'):
        driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options, **kwargs)
    else:
        try:
            driver = webdriver.Chrome(executable_path=AutoChrome.install(path=chrome_driver_path), options=chrome_options, **kwargs)
        except:
            find_testdriver()
            driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options, **kwargs)

    while len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return driver


def load_driver2(port=9222):
    import subprocess
    
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
    chrome_driver_path = 'C:\\chromedriver\\'

    if not os.path.isdir('c:\\chromedriver'):
        os.mkdir('c:\\chromedriver')

    # userAgent = UserAgent().random
    try:
        subprocess.Popen(rf'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')
    except:
        subprocess.Popen(rf'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port={port} --user-data-dir="C:\chrometemp"')

    # d = DesiredCapabilities.CHROME
    # d['goog:loggingPrefs'] = { 'browser':'ALL' }
    chrome_options = Options()                                                                    # 옵션객체 생성
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    # chrome_options.add_argument(f"user-agent={userAgent}")
    try:
        driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options)
    except:
        AutoChrome.install(path=chrome_driver_path)
        driver = webdriver.Chrome(executable_path=f'c:\\chromedriver\\{chrome_ver}\\chromedriver.exe', options=chrome_options)
    
    if len(driver.window_handles) > 1:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return driver


def load_cache_driver(userId, chrome_options = None, **kwargs):
    import warnings
    warnings.warn("load_cache_driver is deprecated. Use load_driver instead.", DeprecationWarning)
    return load_driver(chrome_options=chrome_options, mode=['cache'], userId=userId, **kwargs)


def n_login(driver: WebDriver, nid: str, pwd: str, keep_login: bool=True, ip_safe: bool=False, force: bool=False, mobile: bool=False, as_tuple: tuple=False):
    """
    It logs in to Naver.com and returns True if it was successful, False if it wasn't, and a string if
    there was a problem
    
    :param driver: WebDriver
    :type driver: WebDriver
    :param nid: Naver ID
    :type nid: str
    :param pwd: str
    :type pwd: str
    :param keep_login: If True, the account will be kept logged in. If False, the account will be logged
    out after closing the browser, defaults to True
    :type keep_login: bool (optional)
    :param ip_safe: If True, the login will be done with IP Safe, defaults to False
    :type ip_safe: bool (optional)
    :param force: If True, it will try to login even if it's already logged in, defaults to False
    :type force: bool (optional)
    :param mobile: bool=False, defaults to False
    :type mobile: bool (optional)
    :param as_tuple: If True, returns a tuple of (bool, str), defaults to False
    :type as_tuple: tuple (optional)
    :return: A tuple of two values.
    """
    
    flag = None
    
    try:
        
        if mobile:
            
            if force:
                pass
            else:
                
                try:
                    driver.get('https://m.naver.com/aside/')
                except TimeoutException:
                    try:
                        driver.refresh()
                    except TimeoutException:
                        sys.stdout.write('네트워크 문제로 로그인 되어있는지 확인이 불가합니다.\n')
                        flag = "네트워크 문제"
                        return
                except Exception as e:
                    sys.stdout.write(f'{e}\n')
                    flag = ' '.join(str(e).splitlines())
                    return
                
                time.sleep(.5)
                
                try:
                    check_login = driver.execute_script('return document.querySelector("div[class*=footer]").innerText')
                    if '로그아웃' in check_login:
                        flag = True
                        return
                except:
                    try:
                        driver.find_element(By.XPATH, f"//a[contains(.,'로그아웃')]")
                        flag = True
                        return
                    except:
                        pass
            
            driver.header_overrides = {'Referer': 'http://m.naver.com/aside/'}
            driver.get('https://nid.naver.com/nidlogin.login?svctype=262144&amp;url=http://m.naver.com/aside/')

            origin_clip = pyperclip.paste()
            try:
                pyperclip.copy(nid)
                driver.find_elements(By.CSS_SELECTOR, '#id')[0].send_keys(Keys.CONTROL, 'v')
                time.sleep(0.5)

                pyperclip.copy(pwd)
                driver.find_elements(By.CSS_SELECTOR, '#pw')[0].send_keys(Keys.CONTROL, 'v')
            finally:
                pyperclip.copy(origin_clip)

            if keep_login:
                if driver.find_element(By.CSS_SELECTOR, 'input#stay').get_attribute('value').lower() == 'off':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#stay'))
            else:
                if driver.find_element(By.CSS_SELECTOR, 'input#stay').get_attribute('value').lower() == 'on':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#stay'))

            driver.find_elements(By.CSS_SELECTOR, 'button[class="btn_check"]')[0].click()
            time.sleep(1)
        
        else:
            
            if force:
                pass
            else:
                try:
                    driver.get('https://www.naver.com')
                except TimeoutException:
                    try:
                        driver.refresh()
                    except TimeoutException:
                        sys.stdout.write('네트워크 문제로 로그인 되어있는지 확인이 불가합니다.\n')
                        flag = "네트워크 문제"
                        return
                except Exception as e:
                    sys.stdout.write(f'{e}\n')
                    flag = ' '.join(str(e).splitlines())
                    return
                time.sleep(.5)
                try:
                    logout_iframe = driver.find_element(By.CSS_SELECTOR, 'iframe#minime')
                    driver.switch_to.frame(logout_iframe)
                    driver.find_element(By.CSS_SELECTOR, 'a.btn_logout')
                except:
                    pass
                else:
                    try:
                        sys.stdout.write(f'''{driver.find_element(By.CSS_SELECTOR, 'div.email.MY_EMAIL').text.split('@')[0]} : 이미 로그인 되어있습니다.\n''')
                    except:
                        pass
                    finally:
                        flag = True
                        return
                finally:
                    driver.switch_to.default_content()

            # driver.header_overrides = {'Referer': 'https://www.naver.com/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
            driver.header_overrides = {'Referer': 'https://www.naver.com/'}
            driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
            
            time.sleep(.5)

            origin_clip = pyperclip.paste()
            try:
                pyperclip.copy(nid)
                driver.find_element(By.CSS_SELECTOR, 'input#id').send_keys(Keys.CONTROL, 'v')
                time.sleep(.5)
                pyperclip.copy(pwd)
                driver.find_element(By.CSS_SELECTOR, 'input#pw').send_keys(Keys.CONTROL, 'v')
            finally:
                pyperclip.copy(origin_clip)
            
            if keep_login:
                if driver.find_element(By.CSS_SELECTOR, 'input#keep').get_attribute('value').lower() == 'off':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#keep'))
            else:
                if driver.find_element(By.CSS_SELECTOR, 'input#keep').get_attribute('value').lower() == 'on':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#keep'))

            time.sleep(1)

            if ip_safe:
                if driver.find_element(By.CSS_SELECTOR, 'input#smart_LEVEL').get_attribute('value') == '-1':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#switch'))
            else:
                if driver.find_element(By.CSS_SELECTOR, 'input#smart_LEVEL').get_attribute('value') == '1':
                    driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'input#switch'))
            
            time.sleep(1)

            # 로그인 버튼 클릭
            try:
                driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][id="log.login"]').click()
            except:
                driver.execute_script('arguments[0].click();', driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][id="log.login"]'))

        try:
            WebDriverWait(driver, 2.5).until(expected_conditions.staleness_of(driver.find_element(By.TAG_NAME, 'html')))
        except:
            pass
        try:
            WebDriverWait(driver, 2.5).until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'html')))
        except:
            pass

        now_url = driver.current_url
        source = driver.page_source

        if 'https://m.naver.com/aside/' == now_url:
            flag = True
        
        elif 'https://www.naver.com/' == now_url:
            flag = True
        
        elif 'https://m.naver.com/' == now_url:
            flag = True
        
        elif 'idRelease' in now_url and '대량생성' in source:
            flag = '로그인제한(대량생성ID)'

        elif 'sleepId' in now_url and '최근 1년 동안 로그인하지 않아 휴면 상태입니다.' in source:
            flag = '휴면'
        
        elif 'https://nid.naver.com/nidlogin.login' == now_url and '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.' in source:
            flag = False
        
        elif 'https://nid.naver.com/nidlogin.login' == now_url and '스팸성 홍보활동' in source:
            flag = '보호조치(스팸성 홍보활동)'
        
        elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '개인정보보호 및 도용' in source:
            flag = '보호조치(개인정보보호및도용)'
        
        elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '타인으로 의심' in source:
            flag = '보호조치(타인의심)'
        
        elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source:
            flag = '보호조치'

        elif 'https://nid.naver.com/user2/help/contactInfo?m=viewPhoneInfo' == now_url and '회원정보에 사용할 휴대 전화번호를 확인해 주세요.' in source:
            flag = True

        elif 'deviceConfirm' in now_url and '자주 사용하는 기기라면 등록해 주세요.' in source:
            flag = True

        else:
            flag = False
        
        if flag is not True and flag is not False:
            import requests
            requests.get(f'http://aaa.e-e.kr/problemid/insert.php?id={nid}&desc={flag}')
    finally:
        
        if as_tuple:
            if flag == True:
                return True, "로그인 성공"
            
            elif isinstance(flag, str):
                return False, flag
            
            else:
                return False, "로그인 실패"
        else:
            return flag


def daum_mail_login(driver, did, pwd):

    try:
        driver.get('https://logins.daum.net/accounts/signinform.do?url=https%3A%2F%2Fmail.daum.net%2F')
    except:
        driver.refresh()
    driver.implicitly_wait(5)
    time.sleep(1)

    pyperclip.copy(did)
    driver.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys(Keys.CONTROL + 'v')
    pyperclip.copy(pwd)
    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(Keys.CONTROL + 'v')
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, 'label[class="lab_check"]').click()
    time.sleep(.5)
    driver.find_element(By.CSS_SELECTOR, 'button[id="loginBtn"]').click()
    driver.implicitly_wait(5)
    time.sleep(1)

    now_url = driver.current_url

    # 카카오 통합계정이면 
    if now_url == 'https://logins.daum.net/accounts/login.do?slevel=1':

        # 로그인 창
        driver.get('https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fmail.daum.net%252F')
        driver.implicitly_wait(3)
        time.sleep(1)

        # 아이디 비밀번호 입력
        pyperclip.copy(did)
        driver.find_element(By.CSS_SELECTOR, 'input[validator="email_or_phone_or_kakaoid"]').send_keys(Keys.CONTROL + 'v')
        pyperclip.copy(pwd)
        driver.find_element(By.CSS_SELECTOR, 'input[validator="password"]').send_keys(Keys.CONTROL + 'v')
        time.sleep(.5)
        driver.execute_script(""" document.querySelector('input[name="stay_signed_in"]').click() """)
        time.sleep(.5)
        driver.find_element(By.CSS_SELECTOR, 'button[class="btn_g btn_confirm submit"]').click()
        driver.implicitly_wait(5)

        # 메일쓰기 버튼 나올때까지 대기
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn_comm btn_write"]')))
        time.sleep(1)

    else:

        try:
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn_comm btn_write"]')))
            time.sleep(1)
        except:
            driver.find_element(By.CSS_SELECTOR, 'a[id="afterBtn"]').click()
            driver.implicitly_wait(10)
            time.sleep(2)


def t_login(driver, tid, pwd):
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]').click()
        driver.implicitly_wait(5)
        time.sleep(.5)

        pyperclip.copy(tid)
        driver.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(.5)
        pyperclip.copy(pwd)
        driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(Keys.CONTROL, 'v')
        time.sleep(.5)

        driver.find_element(By.CSS_SELECTOR, 'div[role="button"]').click()
        driver.implicitly_wait(5)
        time.sleep(.5)
    except:
        print('로그인이 되어 있습니다.')
    driver.get('https://twitter.com')
    time.sleep(1)
    if driver.current_url == 'https://twitter.com/home':
        return True
    else:
        return False


def line_login(driver: WebDriver, line_email: str, line_passwd: str):
    login_flag = False
    driver.implicitly_wait(3)
    driver.get('https://m.naver.com/aside/')

    try:
        check_login = driver.execute_script('return document.querySelector("div[class*=footer]").innerText')
        if '로그아웃' in check_login:
            login_flag = True
            return login_flag
    except:
        try:
            driver.find_element(By.XPATH, f"//a[contains(.,'로그아웃')]")
            login_flag = True
            return login_flag
        except:
            pass

    try:
        driver.get('https://access.line.me/oauth2/v2.1/noauto-login?loginState=RqKRHGGcrATtnP3SI7gc3I&loginChannelId=1426360231&returnUri=%2Foauth2%2Fv2.1%2Fauthorize%2Fconsent%3Fscope%3Dprofile%2Bfriends%2Bmessage.write%2Btimeline.post%2Bphone%2Bemail%2Bopenid%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fnid.naver.com%252Foauth%252Fglobal%252FlineCallback%26state%3D0120522838%26client_id%3D1426360231#/')
    except WebDriverException:
        login_flag = '라인 로그인창 접속 실패'
        return login_flag

    try:
        email_input_el = WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[name="tid"]')))
        # print(2)
    except:
        try:
            c_bt_el = driver.find_element(By.CSS_SELECTOR, 'button.c-button.l-btn.c-button--allow')
            driver.execute_script("arguments[0].click();", c_bt_el)
            try:
                WebDriverWait(driver, 1.5).until(expected_conditions.alert_is_present())
            except:
                now_url = driver.current_url
                source = driver.page_source

                if 'https://www.naver.com/' in driver.current_url:
                    login_flag = True
                    # print(32)
                    return login_flag

                elif 'idRelease' in now_url and '대량생성' in source:
                    login_flag = '로그인제한(대량생성ID)'
                    return login_flag

                elif 'sleepId' in now_url and '최근 1년 동안 로그인하지 않아 휴면 상태입니다.' in source:
                    login_flag = '휴면'
                    return login_flag

                elif 'https://nid.naver.com/nidlogin.login' == now_url and '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.' in source:
                    login_flag = False
                    return login_flag

                elif 'https://nid.naver.com/nidlogin.login' == now_url and '스팸성 홍보활동' in source:
                    login_flag = '보호조치(스팸성 홍보활동)'
                    return login_flag

                elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '개인정보보호 및 도용' in source:
                    login_flag = '보호조치(개인정보보호및도용)'
                    return login_flag

                elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '타인으로 의심' in source:
                    login_flag = '보호조치(타인의심)'
                    return login_flag

                elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source:
                    login_flag = '보호조치'
                    return login_flag

                elif 'https://nid.naver.com/user2/help/contactInfo?m=viewPhoneInfo' == now_url and '회원정보에 사용할 휴대 전화번호를 확인해 주세요.' in source:
                    login_flag = True
                    return login_flag

                elif 'deviceConfirm' in now_url and '새로운 기기(브라우저) 로그인' in source:
                    login_flag = True
                    return login_flag

                else:
                    login_flag = 'Unknown Error'
                    return login_flag
            else:
                try:
                    fail_alert = driver.switch_to.alert
                    if '정상 처리가 안되었음' in fail_alert.text:
                        login_flag = fail_alert.text
                        fail_alert.dismiss()
                    else:
                        login_flag = fail_alert.text
                        fail_alert.dismiss()
                        print(login_flag)
                    return login_flag
                except:
                    login_flag = 'Unknown Error'
                    return login_flag

            # driver.find_elements(By.CSS_SELECTOR, 'button.c-button.l-btn.c-button--allow')[0].click()
            # print(3)
        except:
            print('이메일 입력창을 찾을 수 없습니다. 담당자에게 문의해주세요.')
            # print(4)
            login_flag = '아이디 창 오류'
            return login_flag
    else:
        try:
            password_input_el = WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'input[name="tpasswd"]')))
            # print(5)
        except:
            print('패스워드 입력창을 찾을 수 없습니다. 담당자에게 문의해주세요.')
            login_flag = '패스워드 창 오류'
            return login_flag

        else:
            email_input_el.send_keys(line_email)
            time.sleep(1)
            password_input_el.send_keys(line_passwd)
            time.sleep(1)
            submit_bt_el = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            try:
                driver.execute_script("arguments[0].click();", submit_bt_el)
            except:
                print('패스워드 입력창을 찾을 수 없습니다. 담당자에게 문의해주세요.')
                login_flag = '패스워드 창 오류'
                return login_flag
            else:
                time.sleep(3)

            try:
                WebDriverWait(driver, 1.5).until(expected_conditions.alert_is_present())
            except:
                pass
            else:
                try:
                    fail_alert = driver.switch_to.alert
                    if '정상 처리가 안되었음' in fail_alert.text:
                        login_flag = fail_alert.text
                        fail_alert.dismiss()
                    else:
                        login_flag = fail_alert.text
                        fail_alert.dismiss()
                        print(login_flag)
                    return login_flag
                except:
                    login_flag = 'Unknown Error'
                    return login_flag

            # print(6)
            try:
                if '필요한 권한' in driver.page_source or 'Naver Authorization' in driver.page_source:
                    # print(7)
                    try:
                        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]').click()
                        # print(8)
                    except:
                        auth_submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]')
                        driver.execute_script("arguments[0].click();", auth_submit_button)
                        # print(9)
                    finally:
                        auth_try_cnt = 0
                        while login_flag == False:
                            # print(10)
                            if auth_try_cnt > 2:
                                login_flag = alert_text
                                # print(11)
                                return login_flag
                            try:
                                # print(12)
                                WebDriverWait(driver, 1.5).until(expected_conditions.alert_is_present())
                                auth_alert = driver.switch_to.alert
                                # print(13)
                            except:
                                # print(14)
                                time.sleep(1.5)
                                if 'https://www.naver.com/' in driver.current_url:
                                    # print(15)
                                    login_flag = True
                                    return login_flag
                                else:
                                    # print(16)
                                    auth_try_cnt += 1
                                    continue
                            else:
                                time.sleep(1.5)
                                # print(17)
                                if '정상 처리가 안되었음' in auth_alert.text:
                                    alert_text = auth_alert.text
                                    # print(18)
                                    auth_alert.dismiss()
                                    time.sleep(1)
                                    try:
                                        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]').click()
                                        # print(19)
                                    except:
                                        auth_submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]')
                                        driver.execute_script("arguments[0].click();", auth_submit_button)
                                        # print(20)
                                    finally:
                                        try:
                                            WebDriverWait(driver, 1.5).until(expected_conditions.alert_is_present())
                                        except:
                                            if 'https://www.naver.com/' in driver.current_url:
                                                login_flag = True
                                                # print(22)
                                                return login_flag
                                            else:
                                                auth_try_cnt += 1
                                                continue
                                        else:
                                            auth_alert = driver.switch_to.alert
                                            alert_text = auth_alert.text
                                            auth_alert.dismiss()
                                        # print(21)
                                else:
                                    alert_text = auth_alert.text
                                    # print(23)
                                    auth_alert.dismiss()
                                    time.sleep(1)
                                    # print(24)
                                    try:
                                        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]').click()
                                        # print(25)
                                    except:
                                        # print(26)
                                        auth_submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"][class="c-button l-btn c-button--allow"]')
                                        driver.execute_script("arguments[0].click();", auth_submit_button)
                                        # print(27)
                                    finally:
                                        # print(28)
                                        time.sleep(1)
                                        if 'https://www.naver.com/' in driver.current_url:
                                            login_flag = True
                                            # print(29)
                                            return login_flag
                                auth_try_cnt += 1
                                # print(30)
                                continue
                else:
                    now_url = driver.current_url
                    source = driver.page_source

                    if 'https://www.naver.com/' in driver.current_url:
                        login_flag = True
                        # print(32)
                        return login_flag

                    elif 'idRelease' in now_url and '대량생성' in source:
                        login_flag = '로그인제한(대량생성ID)'
                        return login_flag

                    elif 'sleepId' in now_url and '회원님의 아이디는 휴면 상태로 전환되었습니다.' in source:
                        login_flag = '휴면'
                        return login_flag

                    elif 'https://nid.naver.com/nidlogin.login' == now_url and '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.' in source:
                        login_flag = '잘못입력'
                        return login_flag

                    elif 'https://nid.naver.com/nidlogin.login' == now_url and '스팸성 홍보활동' in source:
                        login_flag = '보호조치(스팸성 홍보활동)'
                        return login_flag

                    elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '개인정보보호 및 도용' in source:
                        login_flag = '보호조치(개인정보보호및도용)'
                        return login_flag

                    elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source and '타인으로 의심' in source:
                        login_flag = '보호조치(타인의심)'
                        return login_flag

                    elif 'idSafetyRelease' in now_url and '회원님의 아이디를 보호하고 있습니다.' in source:
                        login_flag = '보호조치'
                        return login_flag

                    elif 'https://nid.naver.com/user2/help/contactInfo?m=viewPhoneInfo' == now_url and '회원정보에 사용할 휴대 전화번호를 확인해 주세요.' in source:
                        login_flag = True
                        return login_flag
                    elif 'deviceConfirm' in now_url and '새로운 기기(브라우저) 로그인' in source:
                        login_flag = True
                        return login_flag
                    else:
                        login_flag = 'Unknown Error'
                        return login_flag

            except Exception as e:
                login_flag = 'Unknown Error'
                return login_flag
    return login_flag

    
def scrollDownUntilPageEnd(driver, SCROLL_PAUSE_SEC = 1):
    """
    It scrolls down the page until the page height is the same as the last scroll height
    
    :param driver: the webdriver object
    :param SCROLL_PAUSE_SEC: The number of seconds to wait between each scroll, defaults to 1 (optional)
    :return: The return value is the height of the document in pixels.
    """
    
    # 스크롤 높이 가져옴
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
    except:
        return False
    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # 끝까지 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 1초 대기
            time.sleep(SCROLL_PAUSE_SEC)

            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            break
        last_height = new_height
    return True


def solve_reCAPTCHA(driver: WebDriver):
    """
    It takes a Selenium WebDriver object as an argument, and returns True if it successfully solves the
    reCAPTCHA on the current page, and False otherwise
    
    :param driver: WebDriver
    :type driver: WebDriver
    :return: A boolean value.
    """
    
    from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
    from urllib.parse import urlsplit

    try:
        target_site_url = driver.current_url
        target_site_key = driver.execute_script('''return document.querySelector('[data-sitekey]').getAttribute('data-sitekey');''')
    except:
        try:
            driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]')
        except:
            print('해당 사이트의 reCAPTCHA Key를 찾을 수 없습니다.')
            return False
        else:
            try:
                target_site_url = driver.current_url
                target_site_key = dict([x.split('=') for x in urlsplit(driver.find_element(By.CSS_SELECTOR, 'iframe[src*="recaptcha"]').get_attribute('src')).query.split('&')])['k']
            except:
                try:
                    print('해당 사이트의 reCAPTCHA Key를 찾을 수 없습니다.')
                    return False
                except:
                    try:
                        target_site_url = driver.current_url
                        target_site_key = dict([x.split('=') for x in urlsplit(driver.find_element(By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]').get_attribute('src')).query.split('&')])['k']
                    except:
                        print('해당 사이트의 reCAPTCHA Key를 찾을 수 없습니다.')
                        return False
    
    API_KEY = 'b336be7de932b65c877403893a382713'

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(API_KEY)
    solver.set_website_url(target_site_url)
    solver.set_website_key(target_site_key)
    #set optional custom parameter which Google made for their search page Recaptcha v2
    #solver.set_data_s('"data-s" token from Google Search results "protection"')

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        # print("g-response: "+g_response)
        pass
    else:
        print("task finished with error "+solver.error_code)
    
    try:
        driver.execute_script(f'''document.getElementById("g-recaptcha-response").innerHTML = "{g_response}"''')
    except:
        result_flag = False
    else:
        try:
            tmp = driver.execute_script('return document.querySelector("#g-recaptcha-response").innerHTML;')
        except:
            tmp = None
        result_flag = isinstance(tmp, str) and g_response == tmp.strip()

    return result_flag
