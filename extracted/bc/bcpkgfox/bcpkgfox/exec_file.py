import subprocess
import threading
import argparse
import time
import sys
import os

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