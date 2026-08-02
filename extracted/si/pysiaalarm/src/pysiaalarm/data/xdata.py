"""SIA XData."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass
class SIAXData:
    """Class for Xdata."""

    identifier: str
    name: str
    description: str
    length: int
    characters: str
    value: str | None = None


XDATA: Final[dict[str, SIAXData]] = {
    "A": SIAXData(
        identifier="A",
        name="Authentication Hash",
        description="A hash of the message that allows the message to "
        "be authenticated.",
        length=12,
        characters="ASCII",
        value=None,
    ),
    "C": SIAXData(
        identifier="C",
        name="Supervision Category",
        description="An identifier for the number of communication "
        "paths and link supervision category",
        length=64,
        characters="ASCII",
        value=None,
    ),
    "H": SIAXData(
        identifier="H",
        name="Time of Occurence",
        description="Time that event occurred (may be different than "
        "message time stamp)",
        length=21,
        characters="ASCII",
        value=None,
    ),
    "I": SIAXData(
        identifier="I",
        name="Alarm Text",
        description="Alarm text which may be a description of the event "
        "or a comment regarding the event.",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "J": SIAXData(
        identifier="J",
        name="Network Path",
        description="Manufacturer specific identifier for the path that "
        "was used for the communication",
        length=1,
        characters="ASCII",
        value=None,
    ),
    "K": SIAXData(
        identifier="K",
        name="Encryption Key",
        description="Key exchange request from CSR to PE (up to 256 bits)",
        length=64,
        characters="ASCII",
        value=None,
    ),
    "L": SIAXData(
        identifier="L",
        name="Location",
        description="Location of event on site",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "M": SIAXData(
        identifier="M",
        name="MAC Address",
        description="MAC address of the PE.",
        length=12,
        characters="ASCII",
        value=None,
    ),
    "N": SIAXData(
        identifier="N",
        name="Network Address",
        description="Hardware network address associated with the "
        "communication on path used.",
        length=128,
        characters="ASCII",
        value=None,
    ),
    "O": SIAXData(
        identifier="O",
        name="Building Name",
        description="Building name.",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "P": SIAXData(
        identifier="P",
        name="Authentication Hash",
        description="contains a message used to support programming or "
        "other interactive operations with the receiver",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "R": SIAXData(
        identifier="R",
        name="Room",
        description="Room of the event.",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "S": SIAXData(
        identifier="S",
        name="Site name",
        description="Site name describing the premises.",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "T": SIAXData(
        identifier="T",
        name="Alarm Trigger",
        description="Trigger for the event.",
        length=1,
        characters="ASCII",
        value=None,
    ),
    "V": SIAXData(
        identifier="V",
        name="Verification",
        description="information about audio or video information that "
        "may be associated with the event report.",
        length=256,
        characters="Win1252",
        value=None,
    ),
    "X": SIAXData(
        identifier="X",
        name="Longitude",
        description="Location of event, longitude.",
        length=12,
        characters="ASCII",
        value=None,
    ),
    "Y": SIAXData(
        identifier="Y",
        name="Latitude",
        description="Location of event, latitude.",
        length=12,
        characters="ASCII",
        value=None,
    ),
    "Z": SIAXData(
        identifier="Z",
        name="Altitude",
        description="Location of event, altitude.",
        length=12,
        characters="ASCII",
        value=None,
    ),
}
