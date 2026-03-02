from pydantic import BaseModel

class Display(BaseModel):
    """
    The Display object contains information about the physical or virtual display
    connected to a computer system.
    """

    # Optional:
    color_depth: int | None = None
    physical_height: int | None = None
    physical_orientation: int | None = None
    physical_width: int | None = None
    scale_factor: int | None = None
