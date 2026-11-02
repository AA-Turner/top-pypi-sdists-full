"""Keeping the goat on screen: it idles on its own, acts out each key and repeats what it knows."""

from __future__ import annotations

import shutil
import time
from collections.abc import Callable
from typing import IO, ClassVar

import click

from labqoat.cli.bleat_report import BleatReport
from labqoat.cli.key_queue import KeyQueue
from labqoat.cli.output.banner import Banner
from labqoat.cli.output.goat import Goat
from labqoat.json_document import JsonDocument


class BleatSession:
    """Redraw one block in place, moving between keys, until the watcher leaves."""

    BEAT = 0.13
    IDLE = 0.32
    FRESH = 60.0
    HINT = "[f] feed   [p] pet   [b] butt   [r] refresh   [q] quit"
    DOZING = ("z", "z z", "z z z", "z z")
    ACTS: ClassVar[dict[str, tuple[str, str]]] = {
        "f": ("feed", "nom nom."),
        "p": ("pet", "meeeh. The goat leans in."),
        "b": ("butt", "bonk!"),
    }
    ENCORE = 6
    LINGER = 3.0

    def __init__(
        self,
        stream: IO[str],
        read: Callable[[], JsonDocument],
        keys: Callable[[float], str | None],
        pause: Callable[[float], None] = time.sleep,
        width: Callable[[], int] | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        """Hold the screen, the way to ask the service again, the keyboard and the passing of time."""
        self.stream = stream
        self.read = read
        self.keys = keys
        self.pause = pause
        self.width = width or BleatSession.columns
        self.clock = clock
        self.height = 0
        self.fed = 0
        self.acts = 0
        self.letters = 0
        self.shown_at = 0.0
        self.beat = 0
        self.said = "meh."
        self.report = JsonDocument()
        self.read_at = 0.0

    @staticmethod
    def columns() -> int:
        """The width of the terminal being drawn on."""
        return shutil.get_terminal_size().columns

    def run(self, report: JsonDocument) -> None:
        """Greet, then idle and act on keys until one of them means leave; the cursor always comes back."""
        self.stream.write("\x1b[?25l")
        try:
            self.know(report)
            self.act("greet", "meh.")
            while (pressed := self.keys(self.IDLE)) not in KeyQueue.LEAVING:
                if pressed is None:
                    self.idle()
                else:
                    self.respond(pressed.lower())
        finally:
            self.stream.write("\x1b[?25h")
            self.stream.flush()

    def know(self, report: JsonDocument) -> None:
        """Take a report as current from this moment."""
        self.report = report
        self.read_at = self.clock()

    def current(self) -> JsonDocument:
        """What is known, with its durations moved on by the time since it was read."""
        return BleatReport.aged(self.report, int(self.clock() - self.read_at))

    def asleep(self) -> bool:
        """Whether the herd is resting, which puts the goat to sleep."""
        return self.report["longest_running"] is None

    def idle(self) -> None:
        """Draw the next pose of the goat's own rhythm, asking the service again once a minute."""
        if self.clock() - self.read_at >= self.FRESH:
            self.know(self.read())
        self.fade()
        self.beat += 1
        poses = Goat.scene("sleep" if self.asleep() else "idle")
        dozing = self.DOZING[(self.beat // 2) % len(self.DOZING)]
        self.show(poses[self.beat % len(poses)], dozing if self.asleep() else self.said)

    def respond(self, pressed: str) -> None:
        """Count again on r, play the act a key names, and leave the goat as it is for any other key."""
        self.fade()
        if pressed == "r":
            self.know(self.read())
            self.act("greet", "meh. Counted again.")
        elif pressed in self.ACTS:
            self.perform(pressed)

    def perform(self, pressed: str) -> None:
        """Feed, pet or butt; enough attention and the goat puts on a show."""
        scene, said = self.ACTS[pressed]
        if pressed == "f":
            self.fed += 1
            said = f"nom nom. Fed {self.fed} time{'' if self.fed == 1 else 's'}."
        self.act(scene, said)
        self.acts += 1
        if self.acts % self.ENCORE == 0:
            self.celebrate()

    def celebrate(self) -> None:
        """Dance, then spell the name out letter by letter and keep it on screen."""
        self.letters = 0
        self.act("dance", "The goat has something to show you.")
        self.said = "labqoat!"
        for letters in range(1, len(Banner.NAME) + 1):
            self.pause(self.BEAT)
            self.letters = letters
            self.show(Goat.frame(*Goat.REST), self.said)
        self.shown_at = self.clock()

    def fade(self) -> None:
        """Take the name down once it has been up long enough, and let the goat go back to its usual word."""
        if self.letters and self.clock() - self.shown_at >= self.LINGER:
            self.letters = 0
            self.said = "meh."

    def act(self, scene: str, said: str) -> None:
        """Play one act pose by pose and leave its last pose on screen for the idling to take over."""
        self.said = said
        frames = Goat.scene(scene)
        for index, frame in enumerate(frames):
            self.show(frame, said)
            if index < len(frames) - 1:
                self.pause(self.BEAT)

    def show(self, frame: list[str], said: str) -> None:
        """One pose with what the goat says, what it knows and which keys it answers."""
        facts = BleatReport.lines(self.current())
        name = [click.style(row, fg="green", bold=True) for row in Banner.rows(self.letters)]
        self.draw([*frame, "", click.style(said, bold=True), "", *name, *facts, "", click.style(self.HINT, dim=True)])

    def draw(self, lines: list[str]) -> None:
        """Replace the block drawn last time; lines end with a carriage return because reading keys keeps the terminal raw."""
        back = f"\x1b[{self.height}A\r" if self.height else ""
        self.stream.write(back + "\x1b[J" + "".join(f"{line}\r\n" for line in lines))
        self.stream.flush()
        self.height = sum(self.rows(line) for line in lines)

    def rows(self, line: str) -> int:
        """How many terminal rows a line takes once the terminal wraps it."""
        return max(-(-len(click.unstyle(line)) // self.width()), 1)
