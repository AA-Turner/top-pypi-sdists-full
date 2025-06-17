######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.893111                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.cards.card_modules.card
    import typing
    import metaflow.plugins.cards.card_modules.components

from .basic import LogComponent as LogComponent
from .basic import ErrorComponent as ErrorComponent
from .basic import ArtifactsComponent as ArtifactsComponent
from .basic import TableComponent as TableComponent
from .basic import ImageComponent as ImageComponent
from .basic import SectionComponent as SectionComponent
from .basic import MarkdownComponent as MarkdownComponent
from .basic import PythonCodeComponent as PythonCodeComponent
from .card import MetaflowCardComponent as MetaflowCardComponent
from .card import with_default_component_id as with_default_component_id
from .convert_to_native_type import TaskToDict as TaskToDict
from .renderer_tools import render_safely as render_safely

class UserComponent(metaflow.plugins.cards.card_modules.card.MetaflowCardComponent, metaclass=type):
    def update(self, *args, **kwargs):
        ...
    ...

class StubComponent(UserComponent, metaclass=type):
    def __init__(self, component_id):
        ...
    def update(self, *args, **kwargs):
        ...
    ...

class Artifact(UserComponent, metaclass=type):
    """
    A pretty-printed version of any Python object.
    
    Large objects are truncated using Python's built-in [`reprlib`](https://docs.python.org/3/library/reprlib.html).
    
    Example:
    ```
    from datetime import datetime
    current.card.append(Artifact({'now': datetime.utcnow()}))
    ```
    
    Parameters
    ----------
    artifact : object
        Any Python object.
    name : str, optional
        Optional label for the object.
    compressed : bool, default: True
        Use a truncated representation.
    """
    def update(self, artifact):
        ...
    def __init__(self, artifact: typing.Any, name: typing.Optional[str] = None, compressed: bool = True):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class Table(UserComponent, metaclass=type):
    """
    A table.
    
    The contents of the table can be text or numerical data, a Pandas dataframe,
    or other card components: `Artifact`, `Image`, `Markdown` objects.
    
    Example: Text and artifacts
    ```
    from metaflow.cards import Table, Artifact
    current.card.append(
        Table([
            ['first row', Artifact({'a': 2})],
            ['second row', Artifact(3)]
        ])
    )
    ```
    
    Example: Table from a Pandas dataframe
    ```
    from metaflow.cards import Table
    import pandas as pd
    import numpy as np
    current.card.append(
        Table.from_dataframe(
            pd.DataFrame(
                np.random.randint(0, 100, size=(15, 4)),
                columns=list("ABCD")
            )
        )
    )
    ```
    
    Parameters
    ----------
    data : List[List[str or MetaflowCardComponent]], optional
        List (rows) of lists (columns). Each item can be a string or a `MetaflowCardComponent`.
    headers : List[str], optional
        Optional header row for the table.
    """
    def update(self, *args, **kwargs):
        ...
    def __init__(self, data: typing.Optional[typing.List[typing.List[typing.Union[str, metaflow.plugins.cards.card_modules.card.MetaflowCardComponent]]]] = None, headers: typing.Optional[typing.List[str]] = None, disable_updates: bool = False):
        ...
    @classmethod
    def from_dataframe(cls, dataframe = None, truncate: bool = True):
        """
        Create a `Table` based on a Pandas dataframe.
        
        Parameters
        ----------
        dataframe : Optional[pandas.DataFrame]
            Pandas dataframe.
        truncate : bool, default: True
            Truncate large dataframe instead of showing all rows (default: True).
        """
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class Image(UserComponent, metaclass=type):
    """
    An image.
    
    `Images can be created directly from PNG/JPG/GIF `bytes`, `PIL.Image`s,
    or Matplotlib figures. Note that the image data is embedded in the card,
    so no external files are required to show the image.
    
    Example: Create an `Image` from bytes:
    ```
    current.card.append(
        Image(
            requests.get("https://www.gif-vif.com/hacker-cat.gif").content,
            "Image From Bytes"
        )
    )
    ```
    
    Example: Create an `Image` from a Matplotlib figure
    ```
    import pandas as pd
    import numpy as np
    current.card.append(
        Image.from_matplotlib(
            pandas.DataFrame(
                np.random.randint(0, 100, size=(15, 4)),
                columns=list("ABCD"),
            ).plot()
        )
    )
    ```
    
    Example: Create an `Image` from a [PIL](https://pillow.readthedocs.io/) Image
    ```
    from PIL import Image as PILImage
    current.card.append(
        Image.from_pil_image(
            PILImage.fromarray(np.random.randn(1024, 768), "RGB"),
            "From PIL Image"
        )
    )
    ```
    
    Parameters
    ----------
    src : bytes
        The image data in `bytes`.
    label : str
        Optional label for the image.
    """
    @staticmethod
    def render_fail_headline(msg):
        ...
    def __init__(self, src = None, label = None, disable_updates: bool = True):
        ...
    @classmethod
    def from_pil_image(cls, pilimage, label: typing.Optional[str] = None, disable_updates: bool = False):
        """
        Create an `Image` from a PIL image.
        
        Parameters
        ----------
        pilimage : PIL.Image
            a PIL image object.
        label : str, optional
            Optional label for the image.
        """
        ...
    @classmethod
    def from_matplotlib(cls, plot, label: typing.Optional[str] = None, disable_updates: bool = False):
        """
        Create an `Image` from a Matplotlib plot.
        
        Parameters
        ----------
        plot :  matplotlib.figure.Figure or matplotlib.axes.Axes or matplotlib.axes._subplots.AxesSubplot
            a PIL axes (plot) object.
        label : str, optional
            Optional label for the image.
        """
        ...
    def render(self, *args, **kwargs):
        ...
    def update(self, image, label = None):
        """
        Update the image.
        
        Parameters
        ----------
        image : PIL.Image or matplotlib.figure.Figure or matplotlib.axes.Axes or matplotlib.axes._subplots.AxesSubplot or bytes or str
            The updated image object
        label : str, optional
            Optional label for the image.
        """
        ...
    ...

class Error(UserComponent, metaclass=type):
    """
    This class helps visualize Error's on the `MetaflowCard`. It can help catch and print stack traces to errors that happen in `@step` code.
    
    ### Parameters
    - `exception` (Exception) : The `Exception` to visualize. This value will be `repr`'d before passed down to `MetaflowCard`
    - `title` (str) : The title that will appear over the visualized  `Exception`.
    
    ### Usage
    ```python
    @card
    @step
    def my_step(self):
        from metaflow.cards import Error
        from metaflow import current
        try:
            ...
            ...
        except Exception as e:
            current.card.append(
                Error(e,"Something misbehaved")
            )
        ...
    ```
    """
    def __init__(self, exception, title = None):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class Markdown(UserComponent, metaclass=type):
    """
    A block of text formatted in Markdown.
    
    Example:
    ```
    current.card.append(
        Markdown("# This is a header appended from `@step` code")
    )
    ```
    
    Parameters
    ----------
    text : str
        Text formatted in Markdown.
    """
    def update(self, text = None):
        ...
    def __init__(self, text = None):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class ProgressBar(UserComponent, metaclass=type):
    """
    A Progress bar for tracking progress of any task.
    
    Example:
    ```
    progress_bar = ProgressBar(
        max=100,
        label="Progress Bar",
        value=0,
        unit="%",
        metadata="0.1 items/s"
    )
    current.card.append(
        progress_bar
    )
    for i in range(100):
        progress_bar.update(i, metadata="%s items/s" % i)
    
    ```
    
    Parameters
    ----------
    max : int, default 100
        The maximum value of the progress bar.
    label : str, optional, default None
        Optional label for the progress bar.
    value : int, default 0
        Optional initial value of the progress bar.
    unit : str, optional, default None
        Optional unit for the progress bar.
    metadata : str, optional, default None
        Optional additional information to show on the progress bar.
    """
    def __init__(self, max: int = 100, label: typing.Optional[str] = None, value: int = 0, unit: typing.Optional[str] = None, metadata: typing.Optional[str] = None):
        ...
    def update(self, new_value: int, metadata: typing.Optional[str] = None):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class VegaChart(UserComponent, metaclass=type):
    def __init__(self, spec: dict, show_controls: bool = False):
        ...
    def update(self, spec = None):
        """
        Update the chart.
        
        Parameters
        ----------
        spec : dict or altair.Chart
            The updated chart spec or an altair Chart Object.
        """
        ...
    @classmethod
    def from_altair_chart(cls, altair_chart):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

class PythonCode(UserComponent, metaclass=type):
    """
    A component to display Python code with syntax highlighting.
    
    Example:
    ```python
    @card
    @step
    def my_step(self):
        # Using code_func
        def my_function():
            x = 1
            y = 2
            return x + y
        current.card.append(
            PythonCode(my_function)
        )
    
        # Using code_string
        code = '''
        def another_function():
            return "Hello World"
        '''
        current.card.append(
            PythonCode(code_string=code)
        )
    ```
    
    Parameters
    ----------
    code_func : Callable[..., Any], optional, default None
        The function whose source code should be displayed.
    code_string : str, optional, default None
        A string containing Python code to display.
        Either code_func or code_string must be provided.
    """
    def __init__(self, code_func: typing.Optional[typing.Callable[..., typing.Any]] = None, code_string: typing.Optional[str] = None):
        ...
    def render(self, *args, **kwargs):
        ...
    ...

