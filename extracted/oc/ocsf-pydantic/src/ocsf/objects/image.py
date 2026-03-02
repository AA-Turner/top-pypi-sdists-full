
from ._entity import Entity


class Image(Entity):
    """
    The Image object provides a description of a specific Virtual Machine (VM) or
    Container image.
    """

    uid: str # The unique image ID. For example: `77af4d6b9913`.


    # Optional:
    labels: list[str] | None = None # The image labels.
    name: str | None = None # The image name. For example: `elixir`.
    path: str | None = None # The full path to the image file.
    tag: str | None = None
