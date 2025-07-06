import subprocess
import threading
import argparse
import time
import sys
import os


class clean_main:

    def __init__(self):
        self.current_dir = os.getcwd()
        self.args = None
        self.file = None

    def main(self):

        # Detect the user input
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
                print(f"{self.visuals.bold}{self.visuals.RD} > Error: You need to use one function that installs imports before verifying them.{self.visuals.RESET}")
                print("\033[J", end='', flush=True)

        self.clean_terminal()



class Visual():
    def __init__(self):


        # Colors
        self.DK_ORANGE = "\033[38;5;130m"
        self.ORANGE = "\033[38;5;214m"
        self.YL = "\033[38;5;226m"
        self.RD = "\033[38;5;196m"
        self.GR = "\033[38;5;34m"
        self.RESET = "\033[0m"
        self.bold = "\033[1m"

class Visual(clean_main):
    def __init__(self):
        super().__init__()

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

    def main():

        class visual():
            def __init__(self):
                self.RESET = "\033[0m"
                self.DK_ORANGE = "\033[38;5;130m"
                self.Neg = "\033[1m"
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

        class exec_gen():
            def __init__(self):
                self.current_dir = None
                self.target_file = None
                self.file_name = None

            def preparations(self):
                self.current_dir = os.getcwd()

                parser = argparse.ArgumentParser(description="Script to generate .exe and preventing bugs")
                parser.add_argument("file", type=str, help="Put the name of file after the command (with the extension '.py')")

                args = parser.parse_args()
                self.file_name = args.file
                self.target_file = os.path.join(self.current_dir, self.file_name)

                if not os.path.exists(self.target_file):
                    print(f"Error: File '{self.target_file}' does not exist.")
                    return

            def run_pyinstaller(self):
                global process_finished

                def print_footer():
                    """Função que mantém a mensagem 'Aguarde download' na última linha."""
                    while not process_finished:
                        sys.stdout.write(f"\r \033[F\r\033[K\033[E {visuals.animate_rgb_text(f"   {visuals.Neg}| Gerando executável do '{self.file_name}', aguarde finalização. |{visuals.RESET}")}\n\033[F")
                        sys.stdout.flush()

                process_finished = False

                command = ["pyinstaller", self.target_file]
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                footer_thread = threading.Thread(target=print_footer)
                footer_thread.start()

                # Lê a saída do PyInstaller em tempo real
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        sys.stdout.write(f"\033[F\r\033[K{output.strip()}\033[K\n\n")
                        sys.stdout.flush()

                process_finished = True
                footer_thread.join()

                print(f"\r \033[F\r\033[K\033[f\r\033[K\033[2E{visuals.Neg}{visuals.DK_ORANGE}>{visuals.RESET}{visuals.Neg} Executável gerado com sucesso!\n{visuals.RESET}\033[3E")

        script = exec_gen()
        visuals = visual()
        script.preparations()
        script.run_pyinstaller()
