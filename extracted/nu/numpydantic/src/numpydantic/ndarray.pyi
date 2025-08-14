from dask.array.core import Array as DaskArrayCoreArray
from numpydantic.interface.hdf5 import H5ArrayPath
from numpydantic.interface.hdf5 import H5Proxy
from pathlib._local import Path as Pathlib_localPath
from cv2 import VideoCapture as Cv2VideoCapture
from numpydantic.interface.video import VideoProxy
from zarr.core import Array as ZarrCoreArray
from numpydantic.interface.zarr import ZarrArrayPath
from numpy import ndarray as Numpyndarray
import typing
import pathlib

# Add mypy-style generic params to a static type
# https://mypy.readthedocs.io/en/stable/generics.html#generic-type-aliases
TShape = typing.TypeVar('TShape')
TDtype = typing.TypeVar('TDtype')


NDArray = TShape | TDtype | DaskArrayCoreArray | H5ArrayPath | typing.Tuple[typing.Union[pathlib._local.Path, str], str] | H5Proxy | Pathlib_localPath | Cv2VideoCapture | VideoProxy | Pathlib_localPath | ZarrCoreArray | ZarrArrayPath | Numpyndarray