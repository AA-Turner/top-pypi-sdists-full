import sys
import threading
import time


SPINNER_STYLES = {
    "dots": ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    "line": ['|', '/', '-', '\\'],
    "grow_vertical": ['▁', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃'],
    "grow_horizontal": ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'],
    "bounce": ['⠁','⠂','⠄','⠂'],
    "circle": ['◐', '◓', '◑', '◒'],
}


class Spinner:
    def __init__(self, message="Processing", delay=0.25, style="dots"):
        self.message = message
        self.delay = delay
        self.spinner = SPINNER_STYLES.get(style, SPINNER_STYLES["line"])
        self.stop_spinner = threading.Event()
        self.thread = threading.Thread(target=self._spin)

    def _spin(self):
        idx = 0
        while not self.stop_spinner.is_set():
            sys.stdout.write(f"\r{self.message} {self.spinner[idx % len(self.spinner)]}")
            sys.stdout.flush()
            time.sleep(self.delay)
            idx += 1
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")  # Clear line

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_spinner.set()
        self.thread.join()
        
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
