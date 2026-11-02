"""Type Lightning's dynamically initialized public callback collection."""

from typing import Protocol

from lightning.pytorch import Callback


class LightningCallbacks(Protocol):
    """Trainer's callback connector installs this attribute after constructing the Trainer."""

    callbacks: list[Callback]
