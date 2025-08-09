import sys
from orionis.console.dynamic.contracts.progress_bar import IProgressBar

class ProgressBar(IProgressBar):
    """
    Console-based progress bar for tracking and displaying progress.

    Parameters
    ----------
    total : int, optional
        The maximum value representing 100% progress. Default is 100.
    width : int, optional
        The width of the progress bar in characters. Default is 50.

    Attributes
    ----------
    total : int
        The maximum progress value.
    bar_width : int
        The width of the progress bar in characters.
    progress : int
        The current progress value.
    """

    def __init__(self, total=100, width=50) -> None:
        """
        Initialize a new ProgressBar instance.

        Parameters
        ----------
        total : int, optional
            The maximum value representing 100% progress. Default is 100.
        width : int, optional
            The width of the progress bar in characters. Default is 50.
        """
        self.total = total
        self.bar_width = width
        self.progress = 0

    def __updateBar(self) -> None:
        """
        Update the visual representation of the progress bar in the console.

        Calculates the percentage of completion and redraws the progress bar
        in place, overwriting the previous output.
        """
        percent = self.progress / self.total
        filled_length = int(self.bar_width * percent)
        bar = f"[{'█' * filled_length}{'░' * (self.bar_width - filled_length)}] {int(percent * 100)}%"

        # Move the cursor to the start of the line and overwrite it
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()

    def start(self) -> None:
        """
        Reset and display the progress bar at the starting state.

        Sets the progress to zero and renders the initial progress bar.
        """
        self.progress = 0
        self.__updateBar()

    def advance(self, increment=1) -> None:
        """
        Advance the progress bar by a specified increment.

        Parameters
        ----------
        increment : int, optional
            The value by which to increase the progress. Default is 1.

        Notes
        -----
        Progress will not exceed the total value.
        """
        self.progress += increment
        if self.progress > self.total:
            self.progress = self.total
        self.__updateBar()

    def finish(self) -> None:
        """
        Complete the progress bar and move to a new line.

        Sets progress to the maximum value, updates the bar, and moves the
        cursor to a new line for cleaner output.
        """
        self.progress = self.total
        self.__updateBar()
        sys.stdout.write("\n")
        sys.stdout.flush()
