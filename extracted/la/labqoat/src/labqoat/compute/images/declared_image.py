"""One importable callable and its authored image in an App-owned closure."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.compute.image import Image


@dataclass(frozen=True)
class DeclaredImage:
    """Keep source locations lexical until explicit publication captures their bytes."""

    module: str
    name: str
    source: Path
    image: Image

    @property
    def key(self) -> str:
        """Identify functions and class methods independently of their argument bindings."""
        return f"{self.module}:{self.name}"
