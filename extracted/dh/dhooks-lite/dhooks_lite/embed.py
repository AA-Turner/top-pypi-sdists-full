"""Discord Embed."""

import json
import logging
from datetime import datetime
from typing import Any, List, Optional, Union, get_type_hints

from .serializers import JsonDateTimeEncoder

logger = logging.getLogger(__name__)


class _EmbedObject:
    """base class for all Embed objects"""

    def __eq__(self, other: Any) -> bool:
        """enables comparing all objects by value, including nested objects"""
        if not isinstance(other, type(self)):
            return False
        return all(
            self.__dict__[key1] == other.__dict__[key2]
            for key1, key2 in zip(self.__dict__.keys(), other.__dict__.keys())
        )

    def __ne__(self, other: Any) -> bool:
        """enables comparing all objects by value, including nested objects"""
        return not self.__eq__(other)

    def asdict(self) -> dict:
        """returns a dict representation of this object

        will not include properties that are None
        """
        arr = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, list):
                    v_list = []
                    for elem in value:
                        if isinstance(elem, _EmbedObject):
                            v_list.append(elem.asdict())
                        else:
                            raise NotImplementedError()
                    arr[key[1:]] = v_list
                else:
                    if isinstance(value, _EmbedObject):
                        arr[key[1:]] = value.asdict()
                    else:
                        arr[key[1:]] = value
        return arr

    @classmethod
    def from_dict(cls, obj_dict: dict):
        """creates a new object from the given dict"""
        args = {}
        for param_name, param_type in get_type_hints(cls.__init__).items():
            if param_name in obj_dict and param_name != "return":
                if hasattr(param_type, "__origin__") and param_type.__origin__ == Union:
                    param_type = param_type.__args__[0]
                try:
                    origin_type = param_type.__origin__
                except AttributeError:
                    origin_type = param_type

                if issubclass(origin_type, list):
                    my_type = list(param_type.__args__).pop()
                    value = [my_type(**obj) for obj in obj_dict[param_name]]

                elif issubclass(origin_type, _EmbedObject):
                    value = param_type.from_dict(obj_dict[param_name])

                else:
                    value = obj_dict[param_name]

                args[param_name] = value

        return cls(**args)


class Author(_EmbedObject):
    """Author in an Embed"""

    def __init__(
        self,
        name: str,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ):
        if not name:
            raise ValueError("name can not be None")

        self._name = str(name)
        self._url = str(url) if url else None
        self._icon_url = str(icon_url) if icon_url else None
        self._proxy_icon_url = str(proxy_icon_url) if proxy_icon_url else None

    @property
    def name(self) -> str:
        """Return author name."""
        return self._name

    @property
    def url(self) -> Optional[str]:
        """Return author URL."""
        return self._url

    @property
    def icon_url(self) -> Optional[str]:
        """Return author's icon URL."""
        return self._icon_url

    @property
    def proxy_icon_url(self) -> Optional[str]:
        """Return author's proxy icon URL."""
        return self._proxy_icon_url


class Field(_EmbedObject):
    """Field in an Embed"""

    MAX_CHARACTERS_NAME = 256
    MAX_CHARACTERS_VALUE = 1024

    def __init__(self, name: str, value: str, inline: bool = True) -> None:
        if not name:
            raise ValueError("name can not be None")
        if not value:
            raise ValueError("value can not be None")
        if not isinstance(inline, bool):
            raise TypeError("inline must be of type bool")

        name = str(name)
        if len(name) > self.MAX_CHARACTERS_NAME:
            raise ValueError(
                f"name can not exceed {self.MAX_CHARACTERS_NAME} characters"
            )
        value = str(value)
        if len(value) > self.MAX_CHARACTERS_VALUE:
            raise ValueError(
                f"value can not exceed {self.MAX_CHARACTERS_VALUE} characters"
            )

        self._name = name
        self._value = value
        self._inline = inline

    @property
    def name(self) -> str:
        """Return field name."""
        return self._name

    @property
    def value(self) -> str:
        """Return field value."""
        return self._value

    @property
    def inline(self) -> Optional[bool]:
        """Return field inline."""
        return self._inline


class Footer(_EmbedObject):
    """Footer in an Embed"""

    def __init__(
        self,
        text: str,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ) -> None:
        if not text:
            raise ValueError("text can not be None")

        self._text = str(text)
        self._icon_url = str(icon_url) if icon_url else None
        self._proxy_icon_url = str(proxy_icon_url) if proxy_icon_url else None

    @property
    def text(self) -> str:
        """Return Footer text."""
        return self._text

    @property
    def icon_url(self) -> Optional[str]:
        """Return footer's icon URL."""
        return self._icon_url

    @property
    def proxy_icon_url(self) -> Optional[str]:
        """Return footer's proxy icon URL."""
        return self._proxy_icon_url


class Image(_EmbedObject):
    """Image in an Embed"""

    def __init__(
        self,
        url: str,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ) -> None:
        if not url:
            raise ValueError("url can not be None")
        if width and width <= 0:
            raise ValueError("width must be > 0")
        if height and height <= 0:
            raise ValueError("height must be > 0")

        self._url = str(url)
        self._proxy_url = str(proxy_url) if proxy_url else None
        self._height = int(height) if height else None
        self._width = int(width) if width else None

    @property
    def url(self) -> str:
        """Return image URL."""
        return self._url

    @property
    def proxy_url(self) -> Optional[str]:
        """Return image's proxy URL."""
        return self._proxy_url

    @property
    def height(self) -> Optional[int]:
        """Return image height."""
        return self._height

    @property
    def width(self) -> Optional[int]:
        """Return image width."""
        return self._width


class Thumbnail(Image):
    """Thumbnail in an Embed."""


class Embed(_EmbedObject):
    """Embedded content for a message."""

    # pylint: disable=too-many-instance-attributes

    MAX_CHARACTERS = 6000
    MAX_TITLE = 256
    MAX_DESCRIPTION = 2048
    MAX_FIELDS = 25

    def __init__(
        self,
        description: Optional[str] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        color: Optional[int] = None,
        footer: Optional[Footer] = None,
        image: Optional[Image] = None,
        thumbnail: Optional[Thumbnail] = None,
        author: Optional[Author] = None,
        fields: Optional[List[Field]] = None,
    ) -> None:
        """Initialize an Embed object

        Args:
            description: message text for this embed
            title: title of embed
            url: url of embed
            timestamp: timestamp of embed content
            color: color code of the embed
            footer: footer information
            image: image within embed
            thumbnail: thumbnail for this embed
            author: author information
            fields: fields information

        Exceptions:
            TypeException: when passing variables of wrong type
            ValueException: when embed size exceeds hard limit

        """
        if timestamp and not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime object")

        if footer and not isinstance(footer, Footer):
            raise TypeError("footer must be a Footer object")

        if image and not isinstance(image, Image):
            raise TypeError("image must be an Image object")

        if thumbnail and not isinstance(thumbnail, Thumbnail):
            raise TypeError("thumbnail must be a Thumbnail object")

        if author and not isinstance(author, Author):
            raise TypeError("author must be a Author object")

        if fields and not isinstance(fields, list):
            raise TypeError("fields must be a list")

        if fields:
            if len(fields) > self.MAX_FIELDS:
                raise ValueError(f"Fields can not exceed {self.MAX_FIELDS} objects")
            for field in fields:
                if not isinstance(field, Field):
                    raise TypeError("all elements in fields must be a Field")

        if description and len(description) > self.MAX_DESCRIPTION:
            raise ValueError(
                f"description exceeds max length of {self.MAX_DESCRIPTION} characters"
            )

        if title and len(title) > self.MAX_TITLE:
            raise ValueError(f"title exceeds max length of {self.MAX_TITLE} characters")

        self._title = str(title) if title else None
        self._type = "rich"
        self._description = str(description) if description else None
        self._url = str(url) if url else None
        self._timestamp = timestamp
        self._color = int(color) if color else None
        self._footer = footer
        self._image = image
        self._thumbnail = thumbnail
        self._author = author
        self._fields = fields

        d_json = json.dumps(self.asdict(), cls=JsonDateTimeEncoder)
        if len(d_json) > self.MAX_CHARACTERS:
            limit = len(d_json) - self.MAX_CHARACTERS
            raise ValueError(
                f"Embed exceeds maximum allowed char size of {self.MAX_CHARACTERS} "
                f"by {limit}"
            )

    @property
    def description(self) -> Optional[str]:
        """Return embed's description."""
        return self._description

    @property
    def title(self) -> Optional[str]:
        """Return embed's title or None."""
        return self._title

    @property
    def type(self) -> Optional[str]:
        """Return embed's type or None."""
        return self._type

    @property
    def url(self) -> Optional[str]:
        """Return embed's URL or None."""
        return self._url

    @property
    def timestamp(self) -> Optional[datetime]:
        """Return embed's timestamp or None."""
        return self._timestamp

    @property
    def color(self) -> Optional[int]:
        """Return embed's color or None."""
        return self._color

    @property
    def footer(self) -> Optional[Footer]:
        """Return embed's footer or None."""
        return self._footer

    @property
    def image(self) -> Optional[Image]:
        """Return embed's image or None."""
        return self._image

    @property
    def thumbnail(self) -> Optional[Thumbnail]:
        """Return embed's thumbnail or None."""
        return self._thumbnail

    @property
    def author(self) -> Optional[Author]:
        """Return embed's author or None."""
        return self._author

    @property
    def fields(self) -> Optional[List[Field]]:
        """Return embed's fields or None."""
        return self._fields
