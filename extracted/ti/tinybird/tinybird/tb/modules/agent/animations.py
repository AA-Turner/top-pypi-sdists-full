import random
import sys
import threading
from time import sleep
from typing import Optional


class ThinkingAnimation:
    """Thinking animation that shows changing sparkles as a prefix."""

    def __init__(
        self,
        message: str = "Chirping",
        delay: float = 0.15,
        colors: bool = True,
        dots: bool = True,
    ):
        self.message = message
        self.delay = delay
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.colors = colors and sys.stdout.isatty()
        self.dots = dots

        # Default sparkle characters
        self.sparkle_chars = ["✧", "✦", "⋆", "✳", "✺", "✹", "*", "·"]

        # ANSI color codes
        self.colors_list = [
            "\033[33m",  # Yellow
            "\033[36m",  # Cyan
            "\033[35m",  # Magenta
            "\033[93m",  # Bright Yellow
            "\033[96m",  # Bright Cyan
        ]
        self.reset_color = "\033[0m"

    def start(self, message: Optional[str] = None):
        """Start the animation in a separate thread."""
        # Stop any existing animation first
        if self.running:
            self._stop_without_reset()

        if message:
            self.message = message
        self.running = True
        self.thread = threading.Thread(target=self._run_animation)
        self.thread.daemon = True

        # Clear the current line before starting new animation
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()
        self.thread.start()

    def stop(self):
        """Stop the animation."""
        self.message = "Chirping"
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the line and reset cursor position
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def _stop_without_reset(self):
        """Stop the animation without resetting the message."""
        self.running = False
        if self.thread:
            self.thread.join()
        # Clear the line and reset cursor position
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

    def _run_animation(self):
        """Run the animation until stopped."""
        frame_count = 0
        dots_count = 0

        while self.running:
            # Choose a random sparkle for this frame
            sparkle = random.choice(self.sparkle_chars)

            if self.colors:
                color = random.choice(self.colors_list)
                colored_sparkle = f"{color}{sparkle}{self.reset_color}"
            else:
                colored_sparkle = sparkle

            # Handle dots animation if enabled
            if self.dots:
                dots_count = (frame_count // 4) % 4  # Change dots every 4 frames
                dots = "." * dots_count
                display_message = f"{self.message}{dots}"
            else:
                display_message = self.message

            # Print the message with the prefix sparkle, padding to clear any leftover characters
            line_content = f"{colored_sparkle} {display_message}"
            # Pad with spaces to clear any leftover characters from longer previous messages
            padded_line = line_content.ljust(len(self.message) + 10)
            sys.stdout.write(f"\r{padded_line}")
            sys.stdout.flush()

            sleep(self.delay)
            frame_count += 1
