import subprocess
import threading
import argparse
import shutil
import math
import time
import sys
import re
import os

def main(): cli().main()

class cli:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.file = None
        self.args = None

        self.visuals = self.visual(self)
        self.exec_gen = self.exec_gen_(self)
        self.find_imports = self.find_import(self)
        self.venv_manager = self.venv_mangt(self)

        self.parser = argparse.ArgumentParser(
            add_help=False,
            description=f"{self.visuals.bold}{self.visuals.DK_ORANGE} BCFOX Library \n You can use the arguments in any order you want.\n\n Most flags are independent, you can use it alone or combine them in a single command interacting with each other when applicable.{self.visuals.RESET}",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
            # formatter_class=argparse.RawTextHelpFormatter  # Formats the 'help' text manually
        )

        self._setup_arguments()

    def _setup_arguments(self):
        """Configure all CLI arguments"""
        venv_group = self.parser.add_argument_group(f'{self.visuals.ORANGE}{self.visuals.bold} Virtual Environment Options{self.visuals.RESET}')
        venv_group.add_argument(
            '-v', '--venv',
            action='store_true',
            help="Creates a new virtual environment with all dependencies installed\n"
        )

        venv_group.add_argument(
            '-vc', '--venv-clean',
            action='store_true',
            help="Creates a virtual environment without dependencies\n"
        )

        venv_group.add_argument(
            '-rv', '--recreate-venv',
            action='store_true',
            help="Recreates venv (without dependencies)\n"
        )

        venv_group.add_argument(
            '-dv', '--delete-venv',
            action='store_true',
            help="Deletes venv\n"
        )

        venv_group.add_argument(
            '-r', '--requirements',
            action='store_true',
            # nargs='?',
            # action=self.venv_manager.custom_action_requirements,
            # default=False,
            help="Create a requirements\n"
        )

        exe_group = self.parser.add_argument_group(f'{self.visuals.ORANGE}{self.visuals.bold} Exe options{self.visuals.RESET}')
        exe_group.add_argument(
            '-e', '--exe',
            action='store_true',
            help="Creates a .exe of the file\n"
        )

        exe_group.add_argument(
            '-nc', '--no-console',
            action='store_true',
            help="The exe don't open the console when started\n"
        )

        exe_group.add_argument(
            '-z', '--zip',
            action='store_true',
            help="Make a zip of the 'dist' and rename it to the name of the file\n"
        )

        exe_group.add_argument(
            '-ic', '--icon',
            type=str,
            nargs='+',
            help="Change the exe icon (put .ico path)\n"
        )

        exe_group.add_argument(
            '-ad', '--add-data',
            type=str,
            nargs='+',
            help="Add data(s) to .exe (similar of pyinstaller)\n"
        )

        file_group = self.parser.add_argument_group(f'{self.visuals.ORANGE}{self.visuals.bold} File Options{self.visuals.RESET}')
        file_group.add_argument(
            '-fi', '--find-imports',
            action='store_true',
            help="Finds all imports necessary for the lib to work\n"
        )

        file_group.add_argument(
            '-vi', '--verify-imports',
            action='store_true',
            help="Shows imports that were not installed automatically\n"
        )

        file_group.add_argument(
            '-i', '--install-imports',
            action='store_true',
            help="Installs all imports necessary for the lib to work\n"
        )

        self.parser.add_argument(
            'filename',
            type=str,
            nargs='?',
            help="Input file to process"
        )

        self.parser.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help="If you need more help contact guilherme"
        )

    def main(self):
        self.args = self.parser.parse_args()
        self.file = self.args.filename

        self.data_dict = []
        if self.args.exe:
            if self.args.add_data:
                for data in self.args.add_data:
                    self.data_dict.append(data)

        # Icon check
        if self.args.icon:
            if len(self.args.icon) > 1:
                raise ValueError("Put only one PATH in 'icon' argument.")

            if not os.path.exists(os.path.join(self.current_dir, self.args.icon[0])):
                raise ValueError(f"The path '{self.args.icon[0]}' not exists")

        # Venv
        if self.args.venv:
            self.venv_manager.main()
        elif self.args.venv_clean:
            self.venv_manager.create_venv()
        elif self.args.recreate_venv:
            self.venv_manager.recreate_venv()
        elif self.args.delete_venv:
            self.venv_manager.delete_venv()

        # Imports
        if self.args.find_imports:
            self.find_imports.main()
        elif self.args.install_imports:
            self.venv_manager.install_imports()

        # EXEC
        elif self.args.exe:
            self.exec_gen.main()

        if self.args.zip:
            self.exec_gen.zip_file()

        # LOG - Verify imports
        if self.args.verify_imports:
            if self.args.find_imports \
            or self.args.install_imports \
            or self.args.venv \
            or self.args.recreate_venv \
            or self.args.exe:
                self.find_imports.verify_imports()
            else:
                print(f"{self.visuals.bold}{self.visuals.RD} > Error: You need to use one function that installs imports before verifying them{self.visuals.RESET}")
                print("\033[J", end='', flush=True)

        # Requirements
        if self.args.requirements:
            self.venv_manager.requirements()

        self.clean_terminal()

    def clean_terminal(self):
        if self.exec_gen.error == 1 \
        or self.find_imports.error == 1 \
        or self.venv_manager.error == 1:
            print("\033[J", end='', flush=True)

        if self.exec_gen.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.exec_gen.descerror}")
        if self.find_imports.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.find_imports.descerror}")
        if self.venv_manager.descerror: print(f"\n {self.visuals.DK_ORANGE}>{self.visuals.RESET} {self.venv_manager.descerror}")

    class visual:
        def __init__(self, self_cli):
            self.cli = self_cli

            self.DK_ORANGE = "\033[38;5;130m"
            self.ORANGE = "\033[38;5;214m"
            self.YL = "\033[38;5;226m"
            self.RD = "\033[38;5;196m"
            self.GR = "\033[38;5;34m"
            self.RESET = "\033[0m"
            self.bold = "\033[1m"

            self.hue = 0

        def hsl_to_rgb(self, h, s, l):
            h = h % 360
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = l - c / 2

            if 0 <= h < 60: r, g, b = c, x, 0
            elif 60 <= h < 120: r, g, b = x, c, 0
            elif 120 <= h < 180: r, g, b = 0, c, x
            elif 180 <= h < 240: r, g, b = 0, x, c
            elif 240 <= h < 300: r, g, b = x, 0, c
            elif 300 <= h < 360: r, g, b = c, 0, x

            r = int((r + m) * 255) ; g = int((g + m) * 255) ; b = int((b + m) * 255)
            return r, g, b

        def rgb_text(self, text, r, g, b): return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        def animate_rgb_text(self, text, delay=0.01):
            r, g, b = self.hsl_to_rgb(self.hue, s=1.0, l=0.5)
            self.hue = (self.hue + 1) % 360
            time.sleep(delay)
            return f"    \033[1m{self.rgb_text(text, r, g, b)}\033[0m"

        class animation:
            def __init__(self, self_cli):
                self.cli = self_cli
                self.text = None
                self.braille_spinner = [
                    '\u280B',
                    '\u2809',
                    '\u2839',
                    '\u2838',
                    '\u283C',
                    '\u2834',
                    '\u2826',
                    '\u2827',
                    '\u2807',
                    '\u280F'
                ]

                self.retro_computer_style = [
                '\u23BA',  # ⎺
                '\u23BB',  # ⎻
                '\u23BC',  # ⎼
                '\u23BD',  # ⎽
                ]

                self.footer_thread = None
                self.process_finished = False

            def print_footer(self):
                s = 0
                n = 0
                while not self.process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(self.retro_computer_style): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.cli.visuals.animate_rgb_text(f"  {self.cli.visuals.bold} {self.retro_computer_style[n]} {self.text} {self.retro_computer_style[n]} {self.cli.visuals.RESET}")} \033[0J\n\033[F")
                    sys.stdout.flush()
                    s += 1

            def start(self, text):
                self.text = text
                self.footer_thread = threading.Thread(target=self.print_footer)
                self.footer_thread.start()

            def finish(self):
                self.process_finished = True
                self.footer_thread.join()

    class exec_gen_:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.current_dir = self.cli.current_dir
            self.target_file = self.cli.file
            self.error = 0
            self.descerror = ""
            self.visuals = self.cli.visuals
            self.ultimate_error = None

        def preparations(self):
            self.current_dir = os.getcwd()
            self.target_file = os.path.join(self.current_dir, self.cli.file)  #TODO

            if not os.path.exists(self.target_file):
                self.descerror = f"Error: File '{self.target_file}' does not exist."
                self.error = 1
                return

        def run_pyinstaller(self):
            global process_finished

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',
            '\u23BB',
            '\u23BC',
            '\u23BD',
            ]

            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Gerando executável do '{self.cli.file}', aguarde finalização. {braille_spinner[n]} {self.visuals.RESET}")} \033[0J\n\033[F")
                    sys.stdout.flush()
                    s += 1
                print("\033[1A \r\033[K \033[1B \r\033[K")  #\033[1B \r\033[K\033[1B \r\033[K\033[1B \r\033[K")

            try:
                process_finished = False
                python_executable = os.path.join(".venv", 'Scripts' if os.name == 'nt' else 'bin', 'python')
                command = [python_executable, "-m", "PyInstaller", "--onefile", "--clean"]
                if self.cli.data_dict:
                    for data in self.cli.data_dict:
                        if ":" in data or ";" in data: command.extend(["--add-data", data])
                        else: command.extend(["--add-data", f"{data}:{data}"])

                if self.cli.args.no_console:
                    command.append("--noconsole")

                if self.cli.args.icon:
                    command.extend(["--icon", f"{self.cli.args.icon[0]}"])

                command.append(self.target_file)

                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                footer_thread = threading.Thread(target=print_footer)
                footer_thread.start()

                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None: break
                    if output:
                        sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                        sys.stdout.flush()

                process_finished = True
                footer_thread.join()

            except Exception as e:
                process_finished = True
                self.descerror = e
                self.error = 1
            finally: process_finished = True

            rows = os.get_terminal_size().lines
            print(f"\033[F\033[K\033[f\033[K\033[f\033[K{self.visuals.bold}{self.visuals.GR}\033[{rows};1H > Executável gerado com sucesso!\n{self.visuals.RESET} \033[0J")

        def zip_file(self):

            animation = self.visuals.animation(self.cli)
            animation.start(text='Creating zip file')
            zip_log = False

            try:
                name_dir = self.current_dir.split("\\")
                print(name_dir)

                name_dir = [part for part in name_dir if part]

                target_name = name_dir[-1]

                dist_path = os.path.join(self.current_dir, "dist")
                temp_path = os.path.join(self.current_dir, f"{target_name}_temp")
                inner_path = os.path.join(temp_path, target_name)

                if os.path.isfile(os.path.join(self.current_dir, f"{target_name}.zip")):
                    os.remove(os.path.join(self.current_dir, f"{target_name}.zip"))

                if os.path.exists(os.path.join(self.current_dir, f"{target_name}")):
                    shutil.rmtree(os.path.join(self.current_dir, f"{target_name}"))

                if os.path.exists(dist_path):
                    if os.path.exists(temp_path):
                        shutil.rmtree(temp_path)
                    os.mkdir(temp_path)
                    shutil.move(dist_path, inner_path)
                else:
                    raise FileNotFoundError(f"{self.visuals.bold}{self.visuals.RD}Error: 'dist' directory not found!{self.visuals.RESET}")

                zip_path = shutil.make_archive(
                    os.path.join(self.current_dir, target_name),
                    'zip',
                    root_dir=temp_path,
                    base_dir=target_name
                )

                # Espera o sistema liberar o zip
                wait = 0
                while True:
                    try:
                        with open(zip_path, 'rb'):
                            break
                    except (PermissionError, OSError):
                        time.sleep(0.1)
                        wait += 1
                        if wait >= 600:
                            raise TimeoutError("Timeout while waiting for zip file to be accessible.")

                shutil.rmtree(temp_path)
                zip_log = True

            except Exception as e:
                self.ultimate_error = e

            finally:
                animation.finish()

                if zip_log:
                    print(f"{self.visuals.bold}{self.visuals.GR} > Zip file created successfully {self.visuals.RESET}\033[J\n\033[J")
                else:
                    print(f"{self.visuals.bold}{self.visuals.RD} > Error creating zip file:\033[J")
                    print(f"{self.ultimate_error}{self.visuals.RESET}")
                    sys.exit(1)

        def main(self):
            script = self.cli.exec_gen
            script.preparations()
            script.run_pyinstaller()

    class find_import:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.visuals = self.cli.visuals

            self.error = 0
            self.descerror = ""

            self.imports = None
            self.error_libs = []

        def hsl_to_rgb(self, h, s, l):
            h = h % 360
            c = (1 - abs(2 * l - 1)) * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = l - c / 2

            if 0 <= h < 60: r, g, b = c, x, 0
            elif 60 <= h < 120: r, g, b = x, c, 0
            elif 120 <= h < 180: r, g, b = 0, c, x
            elif 180 <= h < 240: r, g, b = 0, x, c
            elif 240 <= h < 300: r, g, b = x, 0, c
            elif 300 <= h < 360: r, g, b = c, 0, x

            r = int((r + m) * 255) ; g = int((g + m) * 255) ; b = int((b + m) * 255)
            return r, g, b

        def rgb_text(self, text, r, g, b): return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

        def animate_rgb_text(self, text, delay=0.01):
            import time
            from bcpkgfox import DK_ORANGE
            hue = 0
            print(f" {DK_ORANGE}>{self.visuals.RESET} Dependências do arquivo {self.visuals.DK_ORANGE}'{self.target_file}'{self.visuals.RESET} identificadas com sucesso")
            time.sleep(2)
            print(f"{DK_ORANGE} PIP:{self.visuals.RESET}\n\n\033[s")
            while True:
                r, g, b = self.hsl_to_rgb(hue, s=1.0, l=0.5)
                terminal_width = shutil.get_terminal_size().columns
                num_lines = math.floor(len(text) / terminal_width)
                if num_lines == 0: print("\033[1B", end="\r")
                print(f"\033[{num_lines}A\033[0J {DK_ORANGE}---> \033[1m{self.rgb_text(text, r, g, b)}\033[0m (CTRL + C)", end="\r")
                hue = (hue + 1) % 360
                time.sleep(delay)

        def verify_imports(self):
            if self.error_libs:
                print(f"{self.visuals.bold}{self.visuals.YL} WARNING: \n The libraries below can't be installed. This is not necessarily an error, just an alert.{self.visuals.RESET}")
                for lib in self.error_libs:
                    print(f" {self.visuals.bold}{self.visuals.YL}   - {lib} {self.visuals.RESET}")

        def main(self, return_=False):
            self.target_file = self.cli.file

            if not self.target_file:
                print(f"{self.visuals.bold}{self.visuals.RD} > Error: Please pass your 'target_file' to detect the libraries.{self.visuals.RESET}")
                sys.exit(1)

            if not os.path.exists(self.target_file):
                print(f"{self.visuals.bold}{self.visuals.RD} > Error: Your 'target_file' does not exist or can't be accessed.{self.visuals.RESET}")
                sys.exit(1)

            try:
                with open(self.target_file, "r", encoding="utf-8", errors="replace") as file:
                    file_content = file.read()
            except Exception as e:
                print(f"Error reading file: {e}")
                return

            if not file_content:
                print(f"Erro: Não foi possível ler o arquivo '{self.target_file}' com nenhuma codificação testada.")
                return

            self.imports = ["bcpkgfox"]
            import_data = {
                "extract_pdf": "PyMuPDF",
                "import requests": "requests",
                "import pyautogui": "pyautogui",
                "import cv2": "opencv-python",
                "fitz": "PyMuPDF",
                "from PIL": "Pillow",
                "from reportlab.lib import utils": "reportlab",
                "from PyPDF2 import PdfMerger": "PyPDF2",
                "PdfWriter": "pypdf",
                "import PyPDF2": "PyPDF2",
                "invoke_api_": "requests",
                "wait_for": "pygetwindow",
                "from selenium_stealth import stealth": "selenium-stealth",
                "capmonstercloudclient": "bcpkgfox[capmonstercloudclient]",
                "capmonstercloud_client": "bcpkgfox[capmonstercloudclient]",
                "import undetected_chromedriver": "undetected-chromedriver",
                "webdriver_manager": "webdriver-manager",
                "move_to_image": ["pyscreeze", "pyautogui", "Pillow", "opencv-python"],
                "move_mouse_smoothly": ["pyscreeze", "pyautogui", "Pillow"],
                "initialize_driver": ["webdriver-manager", "undetected-chromedriver", "pyautogui", "psutil"],
                "stealth max": ["webdriver-manager", "undetected-chromedriver"],
                "bs4": "beautifulsoup4", "beautifulsoup":"beautifulsoup4",
                "psutil": "bcpkgfox[psutil]",
                "screeninfo": "bcpkgfox[screeninfo]", "get_monitors": "bcpkgfox[screeninfo]",
                "pynput": "bcpkgfox[pynput]", "pynput.mouse": "bcpkgfox[pynput]",
                "pynput.keyboard": "bcpkgfox[pynput]",
                "pywinauto": "bcpkgfox[pywinauto]",
                "pdfplumber": "pdfplumber",
                "twocaptcha": "bcpkgfox[twocaptcha]", "TwoCaptcha": "bcpkgfox[twocaptcha]",
            }

            for name, import_name in import_data.items():
                if re.search(fr"\b{name}\b", file_content):
                    if isinstance(import_name, list):
                        self.imports.extend(import_name)
                    else: self.imports.append(import_name)

            IMPORT_PATTERN = re.compile(r'^(?:from|import)\s+([A-Za-z0-9_\.]+)', re.MULTILINE)

            # Encontra outras libs por regex
            for match in IMPORT_PATTERN.finditer(file_content):
                módulo = match.group(1).split('.')[0]  # pega o pacote raiz
                if módulo not in self.imports:
                    self.imports.append(módulo)

            self.imports = list(set(self.imports))
            import pyperclip

            from bcpkgfox import DK_ORANGE, ORANGE, RESET
            if self.imports:
                if not return_:
                    pyperclip.copy(f"pip install {' '.join(self.imports)}")

                    # try: self.animate_rgb_text(f'pip install {" ".join(self.imports)}', delay=0.002)
                    text = f"pip install {' '.join(self.imports)}"
                    terminal_width = shutil.get_terminal_size().columns
                    num_lines = math.floor(len(text) / terminal_width)

                    try: self.animate_rgb_text(text, delay=0.002)
                    except KeyboardInterrupt: print(f"\033[{num_lines}A\033[0J {DK_ORANGE}--->{RESET} {ORANGE}pip install {' '.join(self.imports)}{RESET}                   \n\n {DK_ORANGE}>{RESET} Copiado para sua área de transferencia. \n(obs: só identifica as libs que são pertencentes da bibliotca bcfox) \n")
                else: return self.imports
            else: print("No libraries from the list were found in the script.")

    class venv_mangt:
        def __init__(self, self_cli):
            self.cli = self_cli
            self.current_dir = self.cli.current_dir
            self.target_file = self.cli.file
            self.error = 0
            self.descerror = ""
            self.visuals = self.cli.visuals

        def delete_venv(self):

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Deleting virtual environment {braille_spinner[n]} {self.visuals.RESET}")} \033[0J\n\033[F")
                    sys.stdout.flush()
                    s += 1

            try:
                footer_thread = threading.Thread(target=print_footer)
                footer_thread.start()

                if os.path.exists(os.path.join(self.current_dir, ".venv")):
                    try:
                        shutil.rmtree(".venv")
                    except Exception as e:
                        print(f"{self.visuals.RD} > Failed to remove venv: {e} {self.visuals.RESET}")
                        return False
                process_finished = True
                footer_thread.join()

                print(f"{self.visuals.bold}{self.visuals.GR} > Oldest virtual environment deleted with sucessfuly {self.visuals.RESET}\n")
            except Exception as e:
                process_finished = True
                self.descerror = e
                self.error = 1
                sys.exit()
                raise SystemExit()
            finally: process_finished = True

        def create_venv(self):

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Generating virtual environment {braille_spinner[n]} {self.visuals.RESET}")} \033[0J\n\033[F")
                    sys.stdout.flush()
                    s += 1

            try:
                process_finished = False
                command = [sys.executable, '-m', 'venv', ".venv"]
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                footer_thread = threading.Thread(target=print_footer)
                footer_thread.start()

                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                        sys.stdout.flush()

                process_finished = True
                footer_thread.join()

                print(f"{self.visuals.bold}{self.visuals.GR} > Virtual environment created successfully {self.visuals.RESET}\n")
            except Exception as e:
                process_finished = True
                self.descerror = e
                self.error = 1
            finally: process_finished = True

        def install_imports(self):
            pip_path = os.path.join(".venv", 'Scripts' if os.name == 'nt' else 'bin', 'pip')
            librarys = self.cli.find_imports.main(return_=True)

            braille_spinner = [
                '\u280B',
                '\u2809',
                '\u2839',
                '\u2838',
                '\u283C',
                '\u2834',
                '\u2826',
                '\u2827',
                '\u2807',
                '\u280F'
            ]

            retro_computer_style = [
            '\u23BA',  # ⎺
            '\u23BB',  # ⎻
            '\u23BC',  # ⎼
            '\u23BD',  # ⎽
            ]

            process_finished = False
            def print_footer():
                s = 0
                n = 0
                while not process_finished:
                    if s % 10 == 0: n += 1
                    if n == len(braille_spinner): n = 0

                    sys.stdout.write(f"\r \033[F\r\033[K\033[E {self.visuals.animate_rgb_text(f"  {self.visuals.bold} {braille_spinner[n]} Installing all dependencies {braille_spinner[n]} {self.visuals.RESET}")} \033[0J\n\033[F")
                    sys.stdout.flush()
                    s += 1

            try:
                log_animation = threading.Thread(target=print_footer)
                log_animation.start()

                process_finished = False
                for lib in librarys:
                    result = subprocess.run(
                        [pip_path, 'install', lib],
                        # check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    if result.returncode != 0:
                        if isinstance(lib, list):
                            self.cli.find_imports.error_libs.extend(lib)
                        else: self.cli.find_imports.error_libs.append(lib)
                        continue


                    elif result.stdout:
                        print(f"\033[0J{result.stdout.strip()}\033[0J")

                process_finished = True
                log_animation.join()
                print(f" {self.visuals.bold}{self.visuals.GR} > All packages installed successfully {self.visuals.RESET}\n\n")

            except Exception as e:
                process_finished = True
                self.descerror = e
                self.error = 1
                print(e)
                sys.exit()

        def recreate_venv(self):
            self.delete_venv()
            self.create_venv()

        class custom_action_requirements(argparse.Action):
            ''' This is necessary to define a new action and the parser identifies it as valid '''

            def __call__(self, parser, namespace, values, option_string=None):
                if values is None:
                    setattr(namespace, self.dest, 'requirements.txt')
                else:
                    setattr(namespace, self.dest, values)

        def requirements(self):

            # # Identifies endwish
            # if '.' in self.cli.args.requirements:
            #     name = self.cli.args.requirements
            # else:
            #     name = self.cli.args.requirements + '.txt'

            # FIX: name is always 'requirements.txt'
            name = 'requirements.txt'

            # Attempt of recreate
            try:
                os.remove(os.path.join(self.current_dir, name))
            except:
                pass

            # Creates a new one
            subprocess.run(f"pip freeze > {name}", shell=True)

            # Read
            with open(f'{name}', 'r') as f:
                lines = f.readlines()

            # Re-write
            add_list = []
            imports = self.cli.find_imports.main(return_=True)
            imports_lower = {imp.lower() for imp in imports}
            with open(f'{name}', 'w') as f:

                for line in lines:

                    # Formats
                    if '\n' in line:
                        line_for_print = line.replace('\n', '').strip()

                    # Compares
                    pkg = line.split('==')[0].strip().lower()
                    if pkg in imports_lower:
                        f.write(line)
                        add_list.append(line_for_print)

            print(f"\n{self.visuals.bold}{self.visuals.GR} > Requirements created with sucessfuly {self.visuals.RESET}\n")
            print(f"{self.visuals.bold}{self.visuals.YL} Libraries installed: {self.visuals.RESET}{self.visuals.YL}" + "".join(f"\n   {lib}" for lib in add_list) + f"{self.visuals.RESET}")

        def main(self):
            try: self.delete_venv()
            except: pass
            self.create_venv()
            self.install_imports()