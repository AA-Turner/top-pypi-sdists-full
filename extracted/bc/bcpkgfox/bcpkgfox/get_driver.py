RESET, GR, ORANGE, DK_ORANGE, RD = "\033[0m", "\033[38;5;34m", "\033[38;5;214m", "\033[38;5;130m", "\033[38;5;196m"
from .find_elements import Elements

from .find_elements import Elements, backcode__dont_use__find_element_with_wait_backcode, By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome
from selenium import webdriver

import subprocess
import logging
import random
import time
import sys
import os
from typing import Optional

class Instancedriver:
    """
    **PARAMETROS**:
        - **Version**: Versão específica do browser (pega a instalada na sua máquina por padrão)
        - **Subprocess**: Roda o browser em um processo separado
        - **Selenoid**: Ativa configurações de compatiblidade com Selenoid
        - **Navegador**: Qual navegador deve iniciar (Coloque o nome)
        - **Driver_path**: Path personalizado do executável
        - **Stealth_min**: Caso você tenha o arquivo _stealh_min.js_
        - **Timeout**: Tempo máximo que o navegador deve aguardar em caso de congelamento (coloque 0 para infinito)
---
    Args:
        *INICIAR_DRIVER*: Retorna a instância do navegador iniciado.
            - self.driver = bcpkgfox.initialize_driver()
            ---

        *OPTIONS*: Inicialize as opções primeiro e depois use a classe **_arguments_** para adicionar (antes de iniciar o driver)
            - bcpkgfox.initialize_options()
            - bcpkgfox.arguments.add_new_argument()
            ---

        *ELEMENTS*: Retorna a instancia de manipulação de elementos (já iniciada e configurada)
            - self.Elements = bcpkgfox.elemets
            ---
    """

    def __init__(self,
        Version: Optional[str | int] = "latest",
        Subprocess: Optional[bool] = False,
        Selenoid: Optional[str] = None,
        Navegador: Optional[str] = "chrome",
        Driver_path: Optional[str] = None,
        Stealth_min: Optional[str] = None,
        Timeout: Optional[int] = 180
        ):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
        )
        self.timeout_page = Timeout if Timeout != 0 else 999999999
        self.version_main = Version
        self.options = None
        self.version = Version
        self.subprocess = Subprocess
        self.selenoid = Selenoid
        self.stealth_min = Stealth_min
        self.nav = Navegador
        self.driver_path = Driver_path

        self.stealth_js_code = None
        self.captcha_api_key = None
        self.extension_path = None
        self.captcha_name = None
        self.driver = None

        self.arguments = self._Arguments(self)
        self.elements = None #FIX: Instance of .get_driver

    def initialize_options(self):

        if self.nav.lower() in ["firefox", "fox", "fire", "mozila", "mozila firefox"]:
            self.options = webdriver.FirefoxOptions()
            self.options.add_argument("--disable-blink-features=AutomationControlled")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")

        elif self.nav.lower() == "edge":
            from selenium.webdriver.edge.options import Options

            self.options = Options()

            self.options.add_argument("--disable-blink-features=AutomationControlled")
            self.options.add_argument("start-maximized")

        elif self.nav.lower() == "chrome":
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--disable-blink-features=AutomationControlled")

        elif self.nav.lower() in ["un", "chromeun", "undetected-chrome", "undetected chrome", "undetected_chrome", "un-chrome", "un_chrome", "un chrome", "undetected", "stealth" "stealth chrome", "google stealth", "stealth google", "stealth_google", "undetected_google"]:
            import undetected_chromedriver as uc
            self.options = uc.ChromeOptions()

        return self.options

    def initialize_driver(self,
        maximize: Optional[bool] = True,
        Active_logs: Optional[bool] = True
        ):

        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service

        self.version_main = self._get_chrome_version() if self.version == "latest" else self.version

        if self.selenoid:
            if self.nav.lower() == "firefox":
                self.options = webdriver.FirefoxOptions()
            elif self.nav.lower() == "opera":
                self.options = webdriver.OperaOptions()
            else:
                self.options = webdriver.ChromeOptions()

            self.options.set_capability("browserVersion", "128.0")
            self.options.set_capability("selenoid:options", {"enableVNC": True})

            self.driver = webdriver.Remote(
                command_executor='http://host.docker.internal:4444/wd/hub',
                options=self.options,
            )

        else:
            if not self.options: self.options = self.initialize_options()

            # Internet explorer
            if self.nav.lower() in ["ie", "internet_explorer", "internet explorer", "explorer"]:
                self.nav = "Internet explorer"
                self.iniciate_internet_explorer(Active_logs)

            # Edge
            elif self.nav.lower() == "edge":
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                from selenium.webdriver.edge.service import Service
                from selenium import webdriver

                service = Service(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=self.options)

            # Firefox
            elif self.nav.lower() in ["firefox", "fox", "fire", "mozila", "mozila firefox"]:
                from selenium import webdriver

                self.options.set_preference("dom.webdriver.enabled", False)
                self.options.set_preference("useAutomationExtension", False)
                self.options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/115.0")

                self.driver = webdriver.Firefox(options=self.options)

            # Opera
            elif self.nav.lower() == "opera":
                self.options = webdriver.OperaOptions()

            # Un-chrome
            elif self.nav.lower() in ["undetected-chrome", "un", "chromeun", "unchrome", "undetected chrome", "undetected_chrome", "un-chrome", "un_chrome", "un chrome", "undetected", "stealth" "stealth chrome", "google stealth", "stealth google", "stealth_google", "undetected_google"]:
                from webdriver_manager.chrome import ChromeDriverManager
                import undetected_chromedriver as uc

                import subprocess
                import pyautogui
                import psutil

                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                comando = [
                    chrome_path,
                    "--remote-debugging-port=8888",
                ]

                self.options.debugger_address = "127.0.0.1:8888"

                self.driver = uc.Chrome(
                    options=self.options,
                    driver_executable_path=ChromeDriverManager().install()
                )

            elif self.nav.lower() == "stealth max":
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                import undetected_chromedriver as uc  # Recommended over standard driver
                import random
                import time
                # from fake_useragent import UserAgent

                # Configure options
                options = uc.ChromeOptions()

                # Basic arguments
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-infobars")
                options.add_argument("--disable-popup-blocking")
                options.add_argument("--disable-notifications")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-logging")
                options.add_argument("--log-level=3")
                options.add_argument("--output=/dev/null")

                # Headless customization (avoid if possible)
                # options.add_argument("--headless=new")
                # options.add_argument("--window-size=1920,1080")

                # Proxy example (recommended for heavy usage)
                # options.add_argument(f"--proxy-server=http://user:pass@ip:port")

                # Randomize user agent
                # ua = UserAgent(browsers=['chrome'], platforms=['win32', 'linux', 'macos'])
                # user_agent = ua.random
                # options.add_argument(f"user-agent={user_agent}")

                # Experimental options
                # options.add_experimental_option("excludeSwitches", ["enable-automation"])
                # options.add_experimental_option("useAutomationExtension", False)

                # Configure capabilities
                caps = DesiredCapabilities.CHROME.copy()
                caps['goog:loggingPrefs'] = {'performance': 'ALL'}

                self.driver = uc.Chrome(
                    options=options,
                    desired_capabilities=caps,
                    use_subprocess=True,
                    suppress_welcome=True,
                    version_main=self.version_main
                )

                # Advanced JavaScript evasions
                stealth_js = """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                """

                # Execute evasions
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                })

                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": stealth_js
                })

                self.driver.execute_cdp_cmd('Browser.grantPermissions', {
                    'origin': 'https://www.detran.pe.gov.br/',
                    'permissions': ['geolocation']
                })

                # Randomize browser features
                self.driver.execute_script(f"""
                    Object.defineProperty(navigator, 'plugins', {{
                        get: () => [{{
                            description: 'PDF Viewer',
                            filename: 'internal-pdf-viewer',
                            length: 1
                        }}]
                    }});

                    Object.defineProperty(navigator, 'languages', {{
                        get: () => ['en-US', 'en', '{random.choice(["de", "es", "fr"])}']
                    }});

                    window.chrome = {{
                        app: {{
                            isInstalled: false,
                        }},
                        webstore: {{}},
                        runtime: {{}},
                    }};
                """)

                # Human-like mouse movement
                self.driver.execute_script("""
                    window.addEventListener('mousemove', function(e) {
                        window.mouseX = e.clientX;
                        window.mouseY = e.clientY;
                    });
                """)

                # Disable sensors
                self.driver.execute_cdp_cmd('Emulation.setSensorOverrideEnabled', {
                    'enabled': True,
                    'type': 'gyroscope',
                    'metadata': {'available': False}
                })

            # Chrome
            else:
                self.options.add_argument("--disable-blink-features=AutomationControlled")
                self.options.add_argument("--no-sandbox")
                self.options.add_argument("--disable-dev-shm-usage")

                # Automatically download and use the correct ChromeDriver
                service = Service(ChromeDriverManager().install())

                # Initialize Chrome
                self.driver = Chrome(service=service, options=self.options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.driver.get("about:blank")
        self.driver.set_page_load_timeout(self.timeout_page)
        # if self.nav != "Internet explorer": self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        if self.stealth_min: self.driver.execute_script(self.stealth_js_code) ; print(self.stealth_js_code)
        if maximize: self.driver.maximize_window()
        self.elements = Elements(self.driver)
        print(f" {DK_ORANGE}> {ORANGE}{self.nav[0].upper()}{self.nav[1:].lower()}{RESET} instânciado com sucesso.") if Active_logs else None
        return self.driver

    def iniciate_internet_explorer(self, Active_logs):
        powershell_script = """
            $zones = @("1", "2", "3", "4")
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Zones\\"

            foreach ($zone in $zones) {
                Set-ItemProperty -Path ($path + $zone) -Name 2500 -Value 0 -Type DWord
            }

            Write-Output "Modo Protegido ativado para todas as zonas de segurança do Internet Explorer."
        """

        process = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True
        ) # ; print(process.stdout, process.stderr)
        print(f" {DK_ORANGE}>{RESET} Modo Protegido ativado para todas as zonas de segurança do Internet Explorer.") if Active_logs else None

        options = webdriver.IeOptions()
        options.ignore_protected_mode_settings = True
        options.require_window_focus = True
        service = IEService(executable_path=self.driver_path)
        self.driver = webdriver.Ie(service=service, options=options)

    def add_extension(self, extension_folder: str,
        config: Optional[bool] = False,
        key: Optional[str|int] = None
        ):
        """ Inicia o navegador com uma extensão, o 'config' ele identifica o nome da pasta e se for uma conhecida (capmonster, twocaptcha) configura automaticamente

        - OBS: Caso a extensão precise de alguma KEY, declare ela também na variavel "key"

        - Exemplo: add_extension("capmonster", config=True)"""
        try:
            extensao_caminho = self.__resource_path(extension_folder)
            if not os.path.exists(extensao_caminho): extensao_caminho = os.path.abspath(extension_folder)
            self.arguments.add_new_argument(f'--load-extension={extensao_caminho}')
        except Exception as e:
            logging.error("Erro ao verificar pasta da extensão", exc_info=True)
            raise SystemError("Verificar pasta da extensão") from e

        if key:
            key = str(key) ; cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]
            for name in cap_monster_names:
                if name in extension_folder.lower(): self._config_capmonster(key)

    def _get_chrome_version(self) -> int:
        """Get major Chrome version"""
        try:
            if os.name == 'nt':
                return self._get_windows_chrome_version()
            return self._get_linux_chrome_version()
        except Exception as e:
            logging.error("Chrome version detection failed", exc_info=True)
            raise SystemError("Chrome version detection failed") from e

    @staticmethod
    def _get_windows_chrome_version() -> int:
        registry_paths = [
            r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome',
            r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome'
        ]
        for path in registry_paths:
            try:
                result = subprocess.check_output(
                    ['reg', 'query', path, '/v', 'DisplayVersion'],
                    stderr=subprocess.DEVNULL,
                    universal_newlines=True
                )
                version = result.split()[-1].split('.')[0]
                return int(version)
            except subprocess.CalledProcessError:
                continue
        raise SystemError("Chrome registry entry not found")

    @staticmethod
    def _get_linux_chrome_version() -> int:
        try:
            output = subprocess.check_output(
                ['google-chrome', '--version'],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            return int(output.strip().split()[-1].split('.')[0])
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise SystemError("Chrome not found in PATH")

    def _config_capmonster(self, api_key: str) -> None:
        self.driver.get("chrome://extensions/") ; time.sleep(5)

        # Shadow-doom
        id_extension = self.driver.execute_script("""
            return document.querySelector('extensions-manager')
            .shadowRoot.querySelector('extensions-item-list')
            .shadowRoot.querySelector('extensions-item').id;
        """) ; print(f" {DK_ORANGE}>{RESET} ID extensão extraido: ", id_extension)

        self.driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-input").send_keys(api_key) ; time.sleep(2.5)
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click()
        backcode__dont_use__find_element_with_wait_backcode(self.driver, By.ID, "client-key-save-btn").click()
        print(" {DK_ORANGE}>{RESET} Capmonter configurado.")

    @staticmethod
    def __resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and for PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def __check_selenoid_connection(selenoid_url: str):
        import requests
        try:
            response = requests.get(selenoid_url)
            if response.status_code != 200:
                raise ConnectionError(f"Falha na conexão com o Selenoid. Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise SystemError(f"Erro ao conectar ao servidor do Selenoid: {e}")

    @staticmethod
    def create_temp(folder_dir, txt_file: Optional[str] = None):
        """ folder_dir: coloque a pasta e subpastas que você quer criar.
            text_file: Coloque o que você quer que esteja escrito se tiver um .txt dentro (opcional).
        """
        import tempfile

        # Define a persistent temporary folder in the system temp directory.
        persistent_temp_folder = os.path.join(tempfile.gettempdir(), folder_dir)
        if not os.path.exists(persistent_temp_folder):
            os.makedirs(persistent_temp_folder)
            print(f" {ORANGE}>{RESET} Diretório temp criado:", file_path)
        else:
            print(f" {ORANGE}>{RESET} Diretório temp identificado:", file_path)

        # Define the path for the text file.
        file_path = os.path.join(persistent_temp_folder, folder_dir)

        # Write some content to the text file.
        with open(file_path, "w") as file:
            file.write(txt_file)

    @staticmethod
    def read_temp_file(temp_path, file_path):
        import tempfile
        # Define the persistent temporary folder and file path (same as in Script 1).
        persistent_temp_folder = os.path.join(tempfile.gettempdir(), temp_path)
        file_path = os.path.join(persistent_temp_folder, file_path)

        # Read the content from the file.
        with open(file_path, "r") as file:
            content = file.read()

        return content

    class _Arguments:
        def __init__(self, self_bot):
            self.web = self_bot

        def add_new_argument(self, args: str | list):
            """Add arguments to the driver options.

            Example single: add_new_argument("--headless")
            Example list: add_new_argument(["--headless", "--disable-gpu"])"""

            if isinstance(args, list):
                for arg in args:
                    self.web.options.add_argument(arg)
            else:
                self.web.options.add_argument(args)

        def add_experimental_option(self, name: str, value):
            """Add an experimental option.

            Example: add_experimental_option("prefs", profile_dict)"""

            self.web.options.add_experimental_option(name, value)

        # Or if you need to add multiple:
        def add_experimental_options(self, options: dict):
            """Add multiple experimental options.

            Example: add_experimental_options({"prefs": profile_dict, "detach": True})"""

            for name, value in options.items():
                self.web.options.add_experimental_option(name, value)

    class Selenoid:
        def __init__(self, self_bot):
            self.web = self_bot
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[logging.StreamHandler(), logging.FileHandler(f'{self.__class__.__name__}.log')]
            )
            self.capabilities = DesiredCapabilities.CHROME.copy()

        def add_capabilities(self, capabilities: str | list):

            if isinstance(capabilities, list) == True:
                for cap in capabilities: self.web.options.add_experimental_option [arg]
            else: self.web.options.add_experimental_option[Args]

            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities["browserName"] = "chrome"
            capabilities["version"] = "122.0"
            capabilities["enableVNC"] = True

            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                desired_capabilities=capabilities
            )

            driver.get("https://www.google.com")

            import time
            time.sleep(10)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def backcode__dont_use__set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

def _get_chrome_version() -> int:
    """Get major Chrome version"""
    try:
        if os.name == 'nt':
            return _get_windows_chrome_version()
        return _get_linux_chrome_version()
    except Exception as e:
        logging.error("Chrome version detection failed", exc_info=True)
        raise SystemError("Chrome version detection failed") from e

def _get_windows_chrome_version() -> int:
    registry_paths = [
        r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome',
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome'
    ]
    for path in registry_paths:
        try:
            result = subprocess.check_output(
                ['reg', 'query', path, '/v', 'DisplayVersion'],
                stderr=subprocess.DEVNULL,
                universal_newlines=True
            )
            version = result.split()[-1].split('.')[0]
            return int(version)
        except subprocess.CalledProcessError:
            continue
    raise SystemError("Chrome registry entry not found")

def _get_linux_chrome_version() -> int:
    try:
        output = subprocess.check_output(
            ['google-chrome', '--version'],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return int(output.strip().split()[-1].split('.')[0])
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise SystemError("Chrome not found in PATH")

def backcode__dont_use__launch_browser(download_dir: str, extension_path, captcha_name, captcha_api_key) -> WebElement:

    global driver

    # Configurações para o Chrome
    import undetected_chromedriver as uc
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={backcode__dont_use__set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.default_directory': download_dir,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
    }
    options.add_experimental_option("prefs", profile)
    # options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')

    if extension_path:
        extensao_caminho = resource_path(extension_path)
        if not os.path.exists(extensao_caminho):
            extensao_caminho = os.path.abspath(extension_path)

        options.add_argument(f'--load-extension={extensao_caminho}')

    # options.add_argument('--disable-extensions') # Fix: Possibilita ter extensões ou não, nunca influenciou na detecção

    # Inicializar o navegador com undetected_chromedriver
    try:
        driver = uc.Chrome(
            options=options,
            driver_executable_path=ChromeDriverManager().install()
        )
    except:
        driver = uc.Chrome(
            options=options,
            version_main=_get_chrome_version(),
        )

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if captcha_name:
        cap_monster_names = ["capmonster", "captchamonster", "monster", "cap-monster", "captcha monster", "captcha-monster", "cmonster", "cap monster"]

        for name in cap_monster_names:
            if captcha_name.lower() == name:
                backcode__dont_use__capmonster(captcha_api_key)

    driver.maximize_window()
    return driver

def backcode__dont_use__get(driver, link) -> WebElement:
    driver.get(link)

def backcode__dont_use__capmonster(api_key) -> None:
    global driver

    driver.get("chrome://extensions/")
    time.sleep(5)

    # Pega por JS pois está dentro da shadow
    id_extension = driver.execute_script("""
        return document.querySelector('extensions-manager')
        .shadowRoot.querySelector('extensions-item-list')
        .shadowRoot.querySelector('extensions-item').id;
    """)

    print("ID extensão extraido:", id_extension)
    driver.get(f"chrome-extension://{id_extension.lower()}/popup.html")

    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-input").send_keys(api_key)
    time.sleep(2.5)
    backcode__dont_use__find_element_with_wait_backcode(driver, By.XPATH, '//label[span[input[@id="captcha-radio-token-ReCaptcha2"]]]').click() # icone salvar
    backcode__dont_use__find_element_with_wait_backcode(driver, By.ID, "client-key-save-btn").click() # icone salvar
    print(" - Capmonter configurado.")