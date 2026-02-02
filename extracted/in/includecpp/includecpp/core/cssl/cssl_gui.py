"""
CSSL GUI Framework - Native GUI components for CSSL
Version 4.9.7

Provides a complete GUI framework with widgets, layouts, and event handling.
Uses tkinter as the backend for cross-platform compatibility.

Usage in CSSL:
    mygui = include("cssl-gui");

    class MyApp : extends mygui::Parent {
        constr initialize() {
            auto this->window = new CsslWidget(this);
            this->window::setSize(800, 600);
            this->window::setTitle("My App");
            this->window::show();
        }
    }
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import os
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum, IntEnum
import queue
import time

# Sound support - use winsound on Windows, otherwise stub
import platform
if platform.system() == 'Windows':
    import winsound
    SOUND_AVAILABLE = True
else:
    SOUND_AVAILABLE = False

# Try to import PIL for image support
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class CsslGuiPosition(IntEnum):
    """Position constants for CSSL GUI elements"""
    BigTitle = 0
    MediumTitle = 1
    SmallTitle = 2
    Title = 3
    Center = 4
    Bottom = 5
    TopLeft = 6
    TopRight = 7
    BottomLeft = 8
    BottomRight = 9
    CenterLeft = 10
    CenterRight = 11
    Middle = 12
    Top = 13
    Left = 14
    Right = 15


class CsslGui:
    """CSSL GUI namespace with position constants and utilities"""

    # Position constants
    BigTitle = CsslGuiPosition.BigTitle
    MediumTitle = CsslGuiPosition.MediumTitle
    SmallTitle = CsslGuiPosition.SmallTitle
    Title = CsslGuiPosition.Title
    Center = CsslGuiPosition.Center
    Bottom = CsslGuiPosition.Bottom
    TopLeft = CsslGuiPosition.TopLeft
    TopRight = CsslGuiPosition.TopRight
    BottomLeft = CsslGuiPosition.BottomLeft
    BottomRight = CsslGuiPosition.BottomRight
    CenterLeft = CsslGuiPosition.CenterLeft
    CenterRight = CsslGuiPosition.CenterRight
    Middle = CsslGuiPosition.Middle
    Top = CsslGuiPosition.Top
    Left = CsslGuiPosition.Left
    Right = CsslGuiPosition.Right

    @staticmethod
    def get_position_coords(position: int, parent_width: int, parent_height: int,
                           widget_width: int = 0, widget_height: int = 0) -> Tuple[int, int]:
        """Convert position constant to actual x, y coordinates"""
        padding = 10

        if position == CsslGuiPosition.BigTitle:
            return (parent_width // 2 - widget_width // 2, padding)
        elif position == CsslGuiPosition.MediumTitle:
            return (parent_width // 2 - widget_width // 2, padding + 20)
        elif position == CsslGuiPosition.SmallTitle:
            return (parent_width // 2 - widget_width // 2, padding + 40)
        elif position == CsslGuiPosition.Title:
            return (parent_width // 2 - widget_width // 2, padding + 30)
        elif position == CsslGuiPosition.Center:
            return (parent_width // 2 - widget_width // 2, parent_height // 2 - widget_height // 2)
        elif position == CsslGuiPosition.Bottom:
            return (parent_width // 2 - widget_width // 2, parent_height - widget_height - padding)
        elif position == CsslGuiPosition.TopLeft:
            return (padding, padding)
        elif position == CsslGuiPosition.TopRight:
            return (parent_width - widget_width - padding, padding)
        elif position == CsslGuiPosition.BottomLeft:
            return (padding, parent_height - widget_height - padding)
        elif position == CsslGuiPosition.BottomRight:
            return (parent_width - widget_width - padding, parent_height - widget_height - padding)
        elif position == CsslGuiPosition.CenterLeft:
            return (padding, parent_height // 2 - widget_height // 2)
        elif position == CsslGuiPosition.CenterRight:
            return (parent_width - widget_width - padding, parent_height // 2 - widget_height // 2)
        elif position == CsslGuiPosition.Middle:
            return (parent_width // 2 - widget_width // 2, parent_height // 2 - widget_height // 2)
        elif position == CsslGuiPosition.Top:
            return (parent_width // 2 - widget_width // 2, padding)
        elif position == CsslGuiPosition.Left:
            return (padding, parent_height // 2 - widget_height // 2)
        elif position == CsslGuiPosition.Right:
            return (parent_width - widget_width - padding, parent_height // 2 - widget_height // 2)
        else:
            return (0, 0)


class CsslInputFieldFilter(IntEnum):
    """Input field filter constants"""
    All = 0
    Alphabets = 1
    Numbers = 2
    Alphanumeric = 3
    Email = 4
    Phone = 5
    Custom = 6


class CSSLInputField:
    """Static class for input field filter constants"""
    All = CsslInputFieldFilter.All
    Alphabets = CsslInputFieldFilter.Alphabets
    Numbers = CsslInputFieldFilter.Numbers
    Alphanumeric = CsslInputFieldFilter.Alphanumeric
    Email = CsslInputFieldFilter.Email
    Phone = CsslInputFieldFilter.Phone
    Custom = CsslInputFieldFilter.Custom


class CsslEventHandler:
    """Event handler that supports CSSL code injection"""

    def __init__(self, widget: Any = None):
        self._handlers: List[Callable] = []
        self._widget = widget
        self._cssl_runtime = None
        self._cssl_code_blocks: List[Any] = []

    def __ilshift__(self, handler: Any) -> 'CsslEventHandler':
        """Support <<== operator for adding handlers"""
        if callable(handler):
            self._handlers.append(handler)
        else:
            # Assume it's a CSSL code block
            self._cssl_code_blocks.append(handler)
        return self

    def add(self, handler: Callable) -> None:
        """Add a handler function"""
        if callable(handler):
            self._handlers.append(handler)

    def set_runtime(self, runtime: Any) -> None:
        """Set the CSSL runtime for code block execution"""
        self._cssl_runtime = runtime

    def trigger(self, *args, **kwargs) -> None:
        """Trigger all handlers"""
        for handler in self._handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"[CsslGui] Event handler error: {e}")

        # Execute CSSL code blocks
        if self._cssl_runtime and self._cssl_code_blocks:
            for block in self._cssl_code_blocks:
                try:
                    if hasattr(block, 'children'):
                        for child in block.children:
                            self._cssl_runtime._execute_node(child)
                    elif callable(block):
                        block()
                except Exception as e:
                    print(f"[CsslGui] CSSL code block error: {e}")

    def __call__(self, *args, **kwargs) -> None:
        """Allow direct calling"""
        self.trigger(*args, **kwargs)


class CsslWidgetBase:
    """Base class for all CSSL widgets"""

    def __init__(self, parent: Any = None):
        self._parent = parent
        self._tk_widget: Optional[tk.Widget] = None
        self._position: Tuple[int, int] = (0, 0)
        self._size: Tuple[int, int] = (100, 30)
        self._visible = True
        self._enabled = True
        self._children: List['CsslWidgetBase'] = []
        self._event_handlers: Dict[str, CsslEventHandler] = {}
        self._cssl_runtime = None

        # Register with parent
        if parent and hasattr(parent, '_children'):
            parent._children.append(self)
        if parent and hasattr(parent, '_cssl_runtime'):
            self._cssl_runtime = parent._cssl_runtime

    def setPosition(self, x: Union[int, CsslGuiPosition], y: int = None) -> 'CsslWidgetBase':
        """Set widget position - can be coordinates or CsslGui position constant"""
        if isinstance(x, (CsslGuiPosition, int)) and y is None:
            # Position constant
            parent_width = 800
            parent_height = 600
            if self._parent and hasattr(self._parent, '_size'):
                parent_width, parent_height = self._parent._size
            elif self._parent and hasattr(self._parent, '_tk_widget'):
                try:
                    parent_width = self._parent._tk_widget.winfo_width()
                    parent_height = self._parent._tk_widget.winfo_height()
                except:
                    pass

            self._position = CsslGui.get_position_coords(
                int(x), parent_width, parent_height,
                self._size[0], self._size[1]
            )
        else:
            self._position = (int(x), int(y) if y is not None else 0)

        self._apply_position()
        return self

    def _apply_position(self) -> None:
        """Apply position to the underlying tk widget"""
        if self._tk_widget:
            self._tk_widget.place(x=self._position[0], y=self._position[1])

    def setSize(self, width: int, height: int) -> 'CsslWidgetBase':
        """Set widget size (in pixels)"""
        self._size = (width, height)
        if self._tk_widget:
            self._tk_widget.place_configure(width=width, height=height)
        return self

    def _run_on_main_thread(self, func):
        """Run a function on the tkinter main thread (thread-safe)."""
        import threading
        if self._tk_widget and threading.current_thread() is not threading.main_thread():
            self._tk_widget.after(0, func)
        else:
            func()

    def show(self) -> 'CsslWidgetBase':
        """Show the widget"""
        self._visible = True
        if self._tk_widget:
            self._run_on_main_thread(
                lambda: self._tk_widget.place(x=self._position[0], y=self._position[1])
            )
        return self

    def hide(self) -> 'CsslWidgetBase':
        """Hide the widget"""
        self._visible = False
        if self._tk_widget:
            self._run_on_main_thread(lambda: self._tk_widget.place_forget())
        return self

    def enable(self) -> 'CsslWidgetBase':
        """Enable the widget"""
        self._enabled = True
        if self._tk_widget:
            self._tk_widget.configure(state='normal')
        return self

    def disable(self) -> 'CsslWidgetBase':
        """Disable the widget"""
        self._enabled = False
        if self._tk_widget:
            self._tk_widget.configure(state='disabled')
        return self

    def destroy(self) -> None:
        """Destroy the widget"""
        if self._tk_widget:
            self._tk_widget.destroy()
        for child in self._children:
            child.destroy()
        self._children.clear()

    def _resolve_parent(self) -> Optional[tk.Widget]:
        """Resolve the tkinter parent widget for placing this widget.
        Walks up the parent chain to find a canvas or tk_widget to attach to."""
        parent = self._parent
        if parent is None:
            return None
        # If parent has a canvas (CsslWidget main window), use that
        if hasattr(parent, '_canvas') and parent._canvas is not None:
            return parent._canvas
        # If parent has an inner frame (ScrollPanel), use that
        if hasattr(parent, '_inner_frame') and parent._inner_frame is not None:
            return parent._inner_frame
        # If parent has a tk_widget directly, use it
        if hasattr(parent, '_tk_widget') and parent._tk_widget is not None:
            return parent._tk_widget
        # Walk up further
        if hasattr(parent, '_parent'):
            saved_parent = self._parent
            self._parent = parent._parent
            result = self._resolve_parent()
            self._parent = saved_parent
            return result
        return None

    def _get_event_handler(self, event_name: str) -> CsslEventHandler:
        """Get or create an event handler"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = CsslEventHandler(self)
            if self._cssl_runtime:
                self._event_handlers[event_name].set_runtime(self._cssl_runtime)
        return self._event_handlers[event_name]

    @property
    def on_clicked(self) -> CsslEventHandler:
        return self._get_event_handler('clicked')

    @property
    def on_hover(self) -> CsslEventHandler:
        return self._get_event_handler('hover')

    @property
    def on_focus(self) -> CsslEventHandler:
        return self._get_event_handler('focus')

    @property
    def on_blur(self) -> CsslEventHandler:
        return self._get_event_handler('blur')


class CsslWidget(CsslWidgetBase):
    """Main window widget - the primary container for CSSL GUI applications"""

    _root_created = False
    _root: Optional[tk.Tk] = None
    _event_queue: queue.Queue = queue.Queue()

    def __init__(self, title: str = "CSSL Application", width: int = 800,
                 height: int = 600, bg_color: str = None, parent: Any = None):
        super().__init__(parent)
        self._title = title
        self._size = (width, height)
        self._bg_color = bg_color
        self._resizable = True
        self._on_close_handlers: List[Callable] = []
        self._running = False
        self._update_interval = 16  # ~60 FPS

        # Create the window
        self._create_window()

    def _create_window(self) -> None:
        """Create the tkinter window"""
        if not CsslWidget._root_created:
            CsslWidget._root = tk.Tk()
            CsslWidget._root_created = True
            self._tk_widget = CsslWidget._root
        else:
            self._tk_widget = tk.Toplevel(CsslWidget._root)

        self._tk_widget.title(self._title)
        self._tk_widget.geometry(f"{self._size[0]}x{self._size[1]}")
        self._tk_widget.protocol("WM_DELETE_WINDOW", self._on_close)

        # Apply background color
        if self._bg_color:
            self._tk_widget.configure(bg=self._bg_color)

        # Create a canvas for absolute positioning
        self._canvas = tk.Canvas(self._tk_widget, highlightthickness=0)
        if self._bg_color:
            self._canvas.configure(bg=self._bg_color)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # Bind resize event
        self._tk_widget.bind('<Configure>', self._on_resize)

    def _on_close(self) -> None:
        """Handle window close"""
        if not self._tk_widget:
            return
        for handler in self._on_close_handlers:
            try:
                handler()
            except:
                pass
        self._running = False
        try:
            is_root = (self._tk_widget == CsslWidget._root)
            self._tk_widget.destroy()
            if is_root:
                CsslWidget._root = None
                CsslWidget._root_created = False
        except tk.TclError:
            pass
        self._tk_widget = None

    def _on_resize(self, event) -> None:
        """Handle window resize"""
        if event.widget == self._tk_widget:
            self._size = (event.width, event.height)

    def setTitle(self, title: str) -> 'CsslWidget':
        """Set window title"""
        self._title = title
        if self._tk_widget:
            self._tk_widget.title(title)
        return self

    def getTitle(self) -> str:
        """Get window title"""
        return self._title

    def setSize(self, width: int, height: int) -> 'CsslWidget':
        """Set window size"""
        self._size = (width, height)
        if self._tk_widget:
            self._tk_widget.geometry(f"{width}x{height}")
        return self

    def setResizable(self, resizable: bool) -> 'CsslWidget':
        """Set whether window is resizable"""
        self._resizable = resizable
        if self._tk_widget:
            self._tk_widget.resizable(resizable, resizable)
        return self

    def center(self) -> 'CsslWidget':
        """Center the window on screen"""
        if self._tk_widget:
            self._tk_widget.update_idletasks()
            width = self._tk_widget.winfo_width()
            height = self._tk_widget.winfo_height()
            x = (self._tk_widget.winfo_screenwidth() // 2) - (width // 2)
            y = (self._tk_widget.winfo_screenheight() // 2) - (height // 2)
            self._tk_widget.geometry(f'{width}x{height}+{x}+{y}')
        return self

    def show(self) -> 'CsslWidget':
        """Show the window"""
        self._visible = True
        self._running = True
        if self._tk_widget:
            self._tk_widget.deiconify()
        return self

    def hide(self) -> 'CsslWidget':
        """Hide the window"""
        self._visible = False
        if self._tk_widget:
            self._tk_widget.withdraw()
        return self

    def close(self) -> None:
        """Close the window"""
        self._on_close()

    def update(self) -> None:
        """Process pending GUI events"""
        if self._tk_widget and self._running:
            try:
                self._tk_widget.update()
            except tk.TclError:
                self._running = False

    def mainloop(self) -> None:
        """Run the main event loop"""
        if self._tk_widget:
            try:
                self._tk_widget.mainloop()
            except tk.TclError:
                pass

    def onClose(self, handler: Callable) -> 'CsslWidget':
        """Register a close handler"""
        self._on_close_handlers.append(handler)
        return self

    @property
    def is_running(self) -> bool:
        return self._running


class CsslLabel(CsslWidgetBase):
    """Text label widget"""

    def __init__(self, parent: Any, text: str = ""):
        super().__init__(parent)
        self._text = text
        self._font_size = 12
        self._font_family = "Arial"
        self._font_weight = "normal"
        self._fg_color = "black"
        self._bg_color = None

        self._create_widget()

    def _create_widget(self) -> None:
        """Create the tkinter label"""
        parent_widget = None
        if self._parent and hasattr(self._parent, '_canvas'):
            parent_widget = self._parent._canvas
        elif self._parent and hasattr(self._parent, '_tk_widget'):
            parent_widget = self._parent._tk_widget

        if parent_widget:
            self._tk_widget = tk.Label(
                parent_widget,
                text=self._text,
                font=(self._font_family, self._font_size, self._font_weight),
                fg=self._fg_color
            )
            if self._bg_color:
                self._tk_widget.configure(bg=self._bg_color)
            self._tk_widget.place(x=self._position[0], y=self._position[1])

    def setText(self, text: str) -> 'CsslLabel':
        """Set label text"""
        self._text = text
        if self._tk_widget:
            self._tk_widget.configure(text=text)
        return self

    def getText(self) -> str:
        """Get label text"""
        return self._text

    def setFont(self, family: str = None, size: int = None, weight: str = None) -> 'CsslLabel':
        """Set font properties"""
        if family:
            self._font_family = family
        if size:
            self._font_size = size
        if weight:
            self._font_weight = weight

        if self._tk_widget:
            self._tk_widget.configure(font=(self._font_family, self._font_size, self._font_weight))
        return self

    def setColor(self, fg: str = None, bg: str = None) -> 'CsslLabel':
        """Set text and background color"""
        if fg:
            self._fg_color = fg
            if self._tk_widget:
                self._tk_widget.configure(fg=fg)
        if bg:
            self._bg_color = bg
            if self._tk_widget:
                self._tk_widget.configure(bg=bg)
        return self


class CsslButton(CsslWidgetBase):
    """Clickable button widget"""

    def __init__(self, parent: Any, text: str = "Button"):
        super().__init__(parent)
        self._text = text
        self._size = (100, 30)
        self._click_callback: Optional[Callable] = None

        self._create_widget()

    def _create_widget(self) -> None:
        """Create the tkinter button"""
        parent_widget = None
        if self._parent and hasattr(self._parent, '_canvas'):
            parent_widget = self._parent._canvas
        elif self._parent and hasattr(self._parent, '_tk_widget'):
            parent_widget = self._parent._tk_widget

        if parent_widget:
            self._tk_widget = ttk.Button(
                parent_widget,
                text=self._text,
                command=self._on_click
            )
            self._tk_widget.place(x=self._position[0], y=self._position[1])

    def _on_click(self) -> None:
        """Handle button click.

        Runs callbacks in a background thread so async::wait() and other
        blocking operations don't freeze the GUI mainloop.
        """
        import threading
        if self._click_callback:
            def _run_callback():
                try:
                    self._click_callback()
                except Exception as e:
                    print(f"[CsslGui] Button click error: {e}")
            threading.Thread(target=_run_callback, daemon=True).start()
        # Then trigger event handlers
        self.on_clicked.trigger()

    def onClick(self, callback: Callable) -> 'CsslButton':
        """Set click callback - use this from CSSL"""
        self._click_callback = callback
        return self

    def setText(self, text: str) -> 'CsslButton':
        """Set button text"""
        self._text = text
        if self._tk_widget:
            self._tk_widget.configure(text=text)
        return self

    def getText(self) -> str:
        """Get button text"""
        return self._text


class CsslPicture(CsslWidgetBase):
    """Image display widget"""

    def __init__(self, parent: Any, image_path: str = None):
        super().__init__(parent)
        self._image_path = image_path
        self._image = None
        self._photo_image = None
        self._size = (100, 100)

        self._create_widget()
        if image_path:
            self.loadImage(image_path)

    def _create_widget(self) -> None:
        """Create the tkinter label for image display"""
        parent_widget = None
        if self._parent and hasattr(self._parent, '_canvas'):
            parent_widget = self._parent._canvas
        elif self._parent and hasattr(self._parent, '_tk_widget'):
            parent_widget = self._parent._tk_widget

        if parent_widget:
            self._tk_widget = tk.Label(parent_widget)
            self._tk_widget.place(x=self._position[0], y=self._position[1])

    def loadImage(self, path: str) -> 'CsslPicture':
        """Load an image from file"""
        self._image_path = path

        if not PIL_AVAILABLE:
            print("[CsslGui] Warning: PIL not available for image loading")
            return self

        try:
            if os.path.exists(path):
                self._image = Image.open(path)
                self._image = self._image.resize(self._size, Image.Resampling.LANCZOS)
                self._photo_image = ImageTk.PhotoImage(self._image)

                if self._tk_widget:
                    self._tk_widget.configure(image=self._photo_image)
                    self._tk_widget.image = self._photo_image  # Keep reference
            else:
                print(f"[CsslGui] Image not found: {path}")
        except Exception as e:
            print(f"[CsslGui] Error loading image: {e}")

        return self

    def setSize(self, width: int, height: int) -> 'CsslPicture':
        """Set image size (will resize the image)"""
        self._size = (width, height)

        if self._image and PIL_AVAILABLE:
            self._image = self._image.resize(self._size, Image.Resampling.LANCZOS)
            self._photo_image = ImageTk.PhotoImage(self._image)

            if self._tk_widget:
                self._tk_widget.configure(image=self._photo_image)
                self._tk_widget.image = self._photo_image

        return self


class CsslSound:
    """Audio playback class - uses winsound on Windows"""

    def __init__(self, sound_path: str = None):
        self._sound_path = sound_path
        self._volume = 1.0
        self._loop = False
        self._playing = False
        self._thread: Optional[threading.Thread] = None

        if sound_path:
            self.load(sound_path)

    def load(self, path: str) -> 'CsslSound':
        """Load a sound file"""
        self._sound_path = path

        if not SOUND_AVAILABLE:
            print("[CsslGui] Warning: Sound only available on Windows")
            return self

        if not os.path.exists(path):
            print(f"[CsslGui] Sound not found: {path}")

        return self

    def play(self, loops: int = 0) -> 'CsslSound':
        """Play the sound (async on Windows)"""
        if not SOUND_AVAILABLE or not self._sound_path:
            return self

        if not os.path.exists(self._sound_path):
            return self

        self._playing = True

        def _play_sound():
            try:
                # winsound only supports .wav files natively
                if self._sound_path.lower().endswith('.wav'):
                    flags = winsound.SND_FILENAME | winsound.SND_ASYNC
                    if loops == -1:
                        flags |= winsound.SND_LOOP
                    winsound.PlaySound(self._sound_path, flags)
                else:
                    print(f"[CsslGui] winsound only supports .wav files: {self._sound_path}")
            except Exception as e:
                print(f"[CsslGui] Error playing sound: {e}")

        self._thread = threading.Thread(target=_play_sound, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> 'CsslSound':
        """Stop playing"""
        self._playing = False
        if SOUND_AVAILABLE:
            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
            except:
                pass
        return self

    def setVolume(self, volume: float) -> 'CsslSound':
        """Set volume (0.0 to 1.0) - not supported with winsound"""
        self._volume = max(0.0, min(1.0, volume))
        # winsound doesn't support volume control
        return self

    def pause(self) -> 'CsslSound':
        """Pause playback - not supported with winsound"""
        # winsound doesn't support pause
        return self

    def resume(self) -> 'CsslSound':
        """Resume playback - not supported with winsound"""
        # winsound doesn't support resume
        return self


class CsslToolbarSlot:
    """A single slot in a toolbar"""

    def __init__(self, toolbar: 'CsslToolbar', slot_id: Any, icon: str = None,
                 tooltip: str = "", on_click: Callable = None):
        self._toolbar = toolbar
        self._id = slot_id
        self._icon_path = icon
        self._tooltip = tooltip
        self._on_click_handler = on_click
        self._tk_button: Optional[ttk.Button] = None
        self._photo_image = None
        self._event_handlers: Dict[str, CsslEventHandler] = {}

        self._create_slot()

    def _create_slot(self) -> None:
        """Create the toolbar slot button"""
        if self._toolbar._tk_frame:
            self._tk_button = ttk.Button(
                self._toolbar._tk_frame,
                text="",
                command=self._on_click,
                width=3
            )
            self._tk_button.pack(side=tk.LEFT, padx=2, pady=2)

            # Load icon if provided
            if self._icon_path and PIL_AVAILABLE and os.path.exists(self._icon_path):
                try:
                    img = Image.open(self._icon_path)
                    img = img.resize((24, 24), Image.Resampling.LANCZOS)
                    self._photo_image = ImageTk.PhotoImage(img)
                    self._tk_button.configure(image=self._photo_image)
                except Exception as e:
                    print(f"[CsslGui] Error loading toolbar icon: {e}")

            # Set tooltip
            if self._tooltip:
                self._create_tooltip()

    def _create_tooltip(self) -> None:
        """Create tooltip for the button"""
        def show_tooltip(event):
            self._tooltip_window = tk.Toplevel(self._tk_button)
            self._tooltip_window.wm_overrideredirect(True)
            x = event.x_root + 10
            y = event.y_root + 10
            self._tooltip_window.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self._tooltip_window, text=self._tooltip,
                           background="lightyellow", relief="solid", borderwidth=1)
            label.pack()

        def hide_tooltip(event):
            if hasattr(self, '_tooltip_window') and self._tooltip_window:
                self._tooltip_window.destroy()
                self._tooltip_window = None

        self._tk_button.bind('<Enter>', show_tooltip)
        self._tk_button.bind('<Leave>', hide_tooltip)

    def _on_click(self) -> None:
        """Handle slot click"""
        if self._on_click_handler:
            try:
                self._on_click_handler()
            except:
                pass
        self.on_clicked.trigger()

    def setTooltip(self, tooltip: str) -> 'CsslToolbarSlot':
        """Set tooltip text"""
        self._tooltip = tooltip
        return self

    def setIcon(self, icon_path: str) -> 'CsslToolbarSlot':
        """Set slot icon"""
        self._icon_path = icon_path
        if self._tk_button and PIL_AVAILABLE and os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                img = img.resize((24, 24), Image.Resampling.LANCZOS)
                self._photo_image = ImageTk.PhotoImage(img)
                self._tk_button.configure(image=self._photo_image)
            except Exception as e:
                print(f"[CsslGui] Error updating toolbar icon: {e}")
        return self

    def _get_event_handler(self, event_name: str) -> CsslEventHandler:
        """Get or create an event handler"""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = CsslEventHandler(self)
        return self._event_handlers[event_name]

    @property
    def on_clicked(self) -> CsslEventHandler:
        return self._get_event_handler('clicked')


class CsslToolbar(CsslWidgetBase):
    """Toolbar widget with slots"""

    def __init__(self, parent: Any, position: int = CsslGuiPosition.Top):
        super().__init__(parent)
        self._position_type = position
        self._slots: Dict[Any, CsslToolbarSlot] = {}
        self._tk_frame: Optional[tk.Frame] = None

        self._create_widget()

    def _create_widget(self) -> None:
        """Create the toolbar frame"""
        parent_widget = None
        if self._parent and hasattr(self._parent, '_canvas'):
            parent_widget = self._parent._canvas
        elif self._parent and hasattr(self._parent, '_tk_widget'):
            parent_widget = self._parent._tk_widget

        if parent_widget:
            self._tk_frame = tk.Frame(parent_widget, relief=tk.RAISED, bd=1)

            # Position based on position constant
            if self._position_type == CsslGuiPosition.Top:
                self._tk_frame.pack(side=tk.TOP, fill=tk.X)
            elif self._position_type == CsslGuiPosition.Bottom:
                self._tk_frame.pack(side=tk.BOTTOM, fill=tk.X)
            elif self._position_type == CsslGuiPosition.Left:
                self._tk_frame.pack(side=tk.LEFT, fill=tk.Y)
            elif self._position_type == CsslGuiPosition.Right:
                self._tk_frame.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self._tk_frame.pack(side=tk.TOP, fill=tk.X)

    def addSlot(self, icon: str = None, tooltip: str = "",
                on_click: Callable = None, id: Any = None) -> CsslToolbarSlot:
        """Add a slot to the toolbar"""
        slot_id = id if id is not None else len(self._slots)
        slot = CsslToolbarSlot(self, slot_id, icon, tooltip, on_click)
        self._slots[slot_id] = slot
        return slot

    def Slot(self, slot_id: Any) -> Optional[CsslToolbarSlot]:
        """Get a slot by ID"""
        return self._slots.get(slot_id)

    def removeSlot(self, slot_id: Any) -> bool:
        """Remove a slot by ID"""
        if slot_id in self._slots:
            slot = self._slots.pop(slot_id)
            if slot._tk_button:
                slot._tk_button.destroy()
            return True
        return False


class CsslInputField(CsslWidgetBase):
    """Text input field widget"""

    # Filter constants available via CsslInputField::All, etc.
    All = CsslInputFieldFilter.All
    Alphabets = CsslInputFieldFilter.Alphabets
    Numbers = CsslInputFieldFilter.Numbers
    Alphanumeric = CsslInputFieldFilter.Alphanumeric
    Email = CsslInputFieldFilter.Email
    Phone = CsslInputFieldFilter.Phone
    Custom = CsslInputFieldFilter.Custom

    def __init__(self, parent: Any, text: str = ""):
        super().__init__(parent)
        self._text = text
        self._placeholder = ""
        self._max_length = -1
        self._filter_type = CsslInputFieldFilter.All
        self._custom_filter: Optional[Callable] = None
        self._size = (200, 25)
        self._text_var: Optional[tk.StringVar] = None

        self._create_widget()

    def _create_widget(self) -> None:
        """Create the tkinter entry"""
        parent_widget = None
        if self._parent and hasattr(self._parent, '_canvas'):
            parent_widget = self._parent._canvas
        elif self._parent and hasattr(self._parent, '_tk_widget'):
            parent_widget = self._parent._tk_widget

        if parent_widget:
            self._text_var = tk.StringVar(value=self._text)
            self._text_var.trace_add('write', self._on_text_changed)

            self._tk_widget = ttk.Entry(
                parent_widget,
                textvariable=self._text_var,
                width=self._size[0] // 8
            )
            self._tk_widget.place(x=self._position[0], y=self._position[1])

            # Bind validation
            vcmd = (self._tk_widget.register(self._validate_input), '%P')
            self._tk_widget.configure(validate='key', validatecommand=vcmd)

            # Bind events
            self._tk_widget.bind('<FocusIn>', lambda e: self._on_focus_in())
            self._tk_widget.bind('<FocusOut>', lambda e: self._on_focus_out())
            self._tk_widget.bind('<Return>', lambda e: self._on_submit())

    def _validate_input(self, new_value: str) -> bool:
        """Validate input based on filter type"""
        # Check max length
        if self._max_length > 0 and len(new_value) > self._max_length:
            return False

        if not new_value:
            return True

        if self._filter_type == CsslInputFieldFilter.All:
            return True
        elif self._filter_type == CsslInputFieldFilter.Alphabets:
            return new_value.replace(' ', '').isalpha()
        elif self._filter_type == CsslInputFieldFilter.Numbers:
            return new_value.replace('.', '', 1).replace('-', '', 1).isdigit()
        elif self._filter_type == CsslInputFieldFilter.Alphanumeric:
            return new_value.replace(' ', '').isalnum()
        elif self._filter_type == CsslInputFieldFilter.Email:
            # Basic email validation - allow common email characters
            allowed = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._-')
            return all(c in allowed for c in new_value)
        elif self._filter_type == CsslInputFieldFilter.Phone:
            allowed = set('0123456789+-() ')
            return all(c in allowed for c in new_value)
        elif self._filter_type == CsslInputFieldFilter.Custom and self._custom_filter:
            return self._custom_filter(new_value)

        return True

    def _on_text_changed(self, *args) -> None:
        """Handle text change"""
        self._text = self._text_var.get() if self._text_var else ""
        # Call direct callback
        if hasattr(self, '_change_callback') and self._change_callback:
            try:
                self._change_callback(self._text)
            except:
                try:
                    self._change_callback()
                except Exception as e:
                    print(f"[CsslGui] Input change error: {e}")
        self.on_text_changed.trigger(self._text)

    def onChange(self, callback: Callable) -> 'CsslInputField':
        """Set change callback - use this from CSSL"""
        self._change_callback = callback
        return self

    def onSubmit(self, callback: Callable) -> 'CsslInputField':
        """Set submit callback - use this from CSSL"""
        self._submit_callback = callback
        return self

    def _on_focus_in(self) -> None:
        """Handle focus in - clear placeholder"""
        if self._text_var and self._text_var.get() == self._placeholder:
            self._text_var.set("")
            if self._tk_widget:
                self._tk_widget.configure(foreground='black')
        self.on_focus.trigger()

    def _on_focus_out(self) -> None:
        """Handle focus out - show placeholder if empty"""
        if self._text_var and not self._text_var.get() and self._placeholder:
            self._text_var.set(self._placeholder)
            if self._tk_widget:
                self._tk_widget.configure(foreground='gray')
        self.on_blur.trigger()

    def _on_submit(self) -> None:
        """Handle submit (Enter key)"""
        # Call direct callback
        if hasattr(self, '_submit_callback') and self._submit_callback:
            try:
                self._submit_callback(self._text)
            except:
                try:
                    self._submit_callback()
                except Exception as e:
                    print(f"[CsslGui] Input submit error: {e}")
        if hasattr(self, 'on_submit'):
            self.on_submit.trigger(self._text)

    def setText(self, text: str) -> 'CsslInputField':
        """Set input text"""
        self._text = text
        if self._text_var:
            self._text_var.set(text)
        return self

    def getText(self) -> str:
        """Get input text"""
        if self._text_var:
            text = self._text_var.get()
            # Don't return placeholder text
            if text == self._placeholder:
                return ""
            return text
        return self._text

    def setPlaceholderText(self, placeholder: str) -> 'CsslInputField':
        """Set placeholder text"""
        self._placeholder = placeholder
        if self._text_var and not self._text_var.get():
            self._text_var.set(placeholder)
            if self._tk_widget:
                self._tk_widget.configure(foreground='gray')
        return self

    def setMaxLength(self, length: int) -> 'CsslInputField':
        """Set maximum input length"""
        self._max_length = length
        return self

    def onlyallow(self, filter_type: int) -> 'CsslInputField':
        """Set input filter type"""
        self._filter_type = filter_type
        return self

    def setCustomFilter(self, filter_func: Callable) -> 'CsslInputField':
        """Set a custom filter function"""
        self._filter_type = CsslInputFieldFilter.Custom
        self._custom_filter = filter_func
        return self

    def submitInput(self) -> str:
        """Submit the current input"""
        text = self.getText()
        if hasattr(self, 'on_submit'):
            self.on_submit.trigger(text)
        return text

    def clear(self) -> 'CsslInputField':
        """Clear the input"""
        self.setText("")
        return self

    def focus(self) -> 'CsslInputField':
        """Focus the input field"""
        if self._tk_widget:
            self._tk_widget.focus_set()
        return self

    @property
    def on_text_changed(self) -> CsslEventHandler:
        return self._get_event_handler('text_changed')

    @property
    def on_submit(self) -> CsslEventHandler:
        return self._get_event_handler('submit')


# =============================================================================
# v4.9.8: New Widget Classes
# =============================================================================


class CsslCheckBox(CsslWidgetBase):
    """Checkbox widget with checked/unchecked state."""

    def __init__(self, parent: Any, text: str = "", checked: bool = False):
        super().__init__(parent)
        self._text = text
        self._checked = checked
        self._size = (150, 25)
        self._check_var: Optional[tk.BooleanVar] = None
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._check_var = tk.BooleanVar(value=self._checked)
        self._tk_widget = ttk.Checkbutton(
            canvas, text=self._text, variable=self._check_var,
            command=self._on_changed
        )
        self._tk_widget.place(x=self._position[0], y=self._position[1])

    def _on_changed(self):
        self._checked = self._check_var.get() if self._check_var else False
        if self._change_handler:
            self._change_handler.trigger(self._checked)

    def setText(self, text: str) -> 'CsslCheckBox':
        self._text = text
        if self._tk_widget:
            self._tk_widget.configure(text=text)
        return self

    def getText(self) -> str:
        return self._text

    def setChecked(self, checked: bool) -> 'CsslCheckBox':
        self._checked = checked
        if self._check_var:
            self._check_var.set(checked)
        return self

    def isChecked(self) -> bool:
        if self._check_var:
            return self._check_var.get()
        return self._checked

    def toggle(self) -> 'CsslCheckBox':
        return self.setChecked(not self.isChecked())

    def onChange(self, callback) -> 'CsslCheckBox':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self

    @property
    def on_changed(self) -> CsslEventHandler:
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        return self._change_handler


class CsslRadioButton(CsslWidgetBase):
    """Radio button widget - grouped by shared group name."""

    _groups: Dict[str, tk.StringVar] = {}

    def __init__(self, parent: Any, text: str = "", group: str = "default", value: str = None):
        super().__init__(parent)
        self._text = text
        self._group = group
        self._value = value or text
        self._size = (150, 25)
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        if self._group not in CsslRadioButton._groups:
            CsslRadioButton._groups[self._group] = tk.StringVar(value="")
        self._group_var = CsslRadioButton._groups[self._group]
        self._tk_widget = ttk.Radiobutton(
            canvas, text=self._text, variable=self._group_var,
            value=self._value, command=self._on_changed
        )
        self._tk_widget.place(x=self._position[0], y=self._position[1])

    def _on_changed(self):
        if self._change_handler:
            self._change_handler.trigger(self._value)

    def setText(self, text: str) -> 'CsslRadioButton':
        self._text = text
        if self._tk_widget:
            self._tk_widget.configure(text=text)
        return self

    def getText(self) -> str:
        return self._text

    def isSelected(self) -> bool:
        if hasattr(self, '_group_var'):
            return self._group_var.get() == self._value
        return False

    def select(self) -> 'CsslRadioButton':
        if hasattr(self, '_group_var'):
            self._group_var.set(self._value)
        return self

    def getGroupValue(self) -> str:
        if hasattr(self, '_group_var'):
            return self._group_var.get()
        return ""

    def onChange(self, callback) -> 'CsslRadioButton':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self


class CsslComboBox(CsslWidgetBase):
    """Dropdown/combo box widget."""

    def __init__(self, parent: Any, items: list = None):
        super().__init__(parent)
        self._items = items or []
        self._size = (200, 25)
        self._text_var: Optional[tk.StringVar] = None
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._text_var = tk.StringVar()
        self._tk_widget = ttk.Combobox(
            canvas, textvariable=self._text_var, values=self._items, state='readonly'
        )
        self._tk_widget.bind('<<ComboboxSelected>>', self._on_selected)
        self._tk_widget.place(x=self._position[0], y=self._position[1])

    def _on_selected(self, event=None):
        if self._change_handler:
            self._change_handler.trigger(self.getSelectedItem())

    def setItems(self, items: list) -> 'CsslComboBox':
        self._items = items
        if self._tk_widget:
            self._tk_widget['values'] = items
        return self

    def getItems(self) -> list:
        return list(self._items)

    def addItem(self, item: str) -> 'CsslComboBox':
        self._items.append(item)
        if self._tk_widget:
            self._tk_widget['values'] = self._items
        return self

    def removeItem(self, index: int) -> 'CsslComboBox':
        if 0 <= index < len(self._items):
            self._items.pop(index)
            if self._tk_widget:
                self._tk_widget['values'] = self._items
        return self

    def setSelectedIndex(self, index: int) -> 'CsslComboBox':
        if self._tk_widget and 0 <= index < len(self._items):
            self._tk_widget.current(index)
        return self

    def getSelectedIndex(self) -> int:
        if self._tk_widget:
            return self._tk_widget.current()
        return -1

    def getSelectedItem(self) -> str:
        if self._text_var:
            return self._text_var.get()
        return ""

    def setSelectedItem(self, item: str) -> 'CsslComboBox':
        if self._text_var:
            self._text_var.set(item)
        return self

    def clear(self) -> 'CsslComboBox':
        if self._text_var:
            self._text_var.set("")
        return self

    def onChange(self, callback) -> 'CsslComboBox':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self


class CsslTextArea(CsslWidgetBase):
    """Multi-line text editing widget."""

    def __init__(self, parent: Any, text: str = ""):
        super().__init__(parent)
        self._text = text
        self._size = (300, 200)
        self._readonly = False
        self._wrap = 'word'
        self._change_handler: Optional[CsslEventHandler] = None
        self._scrollbar = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._frame = tk.Frame(canvas)
        self._tk_widget = tk.Text(self._frame, wrap=self._wrap, width=40, height=10)
        self._scrollbar = ttk.Scrollbar(self._frame, orient='vertical', command=self._tk_widget.yview)
        self._tk_widget.configure(yscrollcommand=self._scrollbar.set)
        self._tk_widget.pack(side='left', fill='both', expand=True)
        self._scrollbar.pack(side='right', fill='y')
        if self._text:
            self._tk_widget.insert('1.0', self._text)
        self._tk_widget.bind('<<Modified>>', self._on_modified)
        self._frame.place(x=self._position[0], y=self._position[1],
                          width=self._size[0], height=self._size[1])

    def _on_modified(self, event=None):
        if self._tk_widget and self._tk_widget.edit_modified():
            self._tk_widget.edit_modified(False)
            if self._change_handler:
                self._change_handler.trigger(self.getText())

    def setSize(self, width: int, height: int) -> 'CsslTextArea':
        self._size = (width, height)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(width=width, height=height)
        return self

    def setPosition(self, x, y=None) -> 'CsslTextArea':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def setText(self, text: str) -> 'CsslTextArea':
        self._text = text
        if self._tk_widget:
            self._tk_widget.delete('1.0', 'end')
            self._tk_widget.insert('1.0', text)
        return self

    def getText(self) -> str:
        if self._tk_widget:
            return self._tk_widget.get('1.0', 'end-1c')
        return self._text

    def appendText(self, text: str) -> 'CsslTextArea':
        if self._tk_widget:
            self._tk_widget.insert('end', text)
        return self

    def insertText(self, position: str, text: str) -> 'CsslTextArea':
        if self._tk_widget:
            self._tk_widget.insert(position, text)
        return self

    def clear(self) -> 'CsslTextArea':
        if self._tk_widget:
            self._tk_widget.delete('1.0', 'end')
        return self

    def setReadOnly(self, readonly: bool) -> 'CsslTextArea':
        self._readonly = readonly
        if self._tk_widget:
            self._tk_widget.configure(state='disabled' if readonly else 'normal')
        return self

    def isReadOnly(self) -> bool:
        return self._readonly

    def setWrap(self, mode: str) -> 'CsslTextArea':
        self._wrap = mode
        if self._tk_widget:
            self._tk_widget.configure(wrap=mode)
        return self

    def getLineCount(self) -> int:
        if self._tk_widget:
            return int(self._tk_widget.index('end-1c').split('.')[0])
        return 0

    def getSelectedText(self) -> str:
        if self._tk_widget:
            try:
                return self._tk_widget.get('sel.first', 'sel.last')
            except tk.TclError:
                return ""
        return ""

    def onChange(self, callback) -> 'CsslTextArea':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self

    def show(self) -> 'CsslTextArea':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])
        return self

    def hide(self) -> 'CsslTextArea':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self

    def destroy(self) -> None:
        if hasattr(self, '_frame') and self._frame:
            self._frame.destroy()
        super().destroy()


class CsslSlider(CsslWidgetBase):
    """Horizontal or vertical slider/scale widget."""

    def __init__(self, parent: Any, min_val: float = 0, max_val: float = 100,
                 value: float = 0, orientation: str = "horizontal"):
        super().__init__(parent)
        self._min = min_val
        self._max = max_val
        self._value = value
        self._orientation = orientation
        self._size = (200, 40) if orientation == "horizontal" else (40, 200)
        self._scale_var: Optional[tk.DoubleVar] = None
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._scale_var = tk.DoubleVar(value=self._value)
        orient = tk.HORIZONTAL if self._orientation == "horizontal" else tk.VERTICAL
        self._tk_widget = ttk.Scale(
            canvas, from_=self._min, to=self._max, variable=self._scale_var,
            orient=orient, command=self._on_changed
        )
        self._tk_widget.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])

    def _on_changed(self, value=None):
        if self._change_handler:
            self._change_handler.trigger(self.getValue())

    def setValue(self, value: float) -> 'CsslSlider':
        self._value = value
        if self._scale_var:
            self._scale_var.set(value)
        return self

    def getValue(self) -> float:
        if self._scale_var:
            return self._scale_var.get()
        return self._value

    def setRange(self, min_val: float, max_val: float) -> 'CsslSlider':
        self._min = min_val
        self._max = max_val
        if self._tk_widget:
            self._tk_widget.configure(from_=min_val, to=max_val)
        return self

    def getMin(self) -> float:
        return self._min

    def getMax(self) -> float:
        return self._max

    def onChange(self, callback) -> 'CsslSlider':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self


class CsslProgressBar(CsslWidgetBase):
    """Progress bar widget."""

    def __init__(self, parent: Any, value: float = 0, max_val: float = 100,
                 mode: str = "determinate"):
        super().__init__(parent)
        self._value = value
        self._max = max_val
        self._mode = mode
        self._size = (200, 25)
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._tk_widget = ttk.Progressbar(
            canvas, maximum=self._max, value=self._value, mode=self._mode
        )
        self._tk_widget.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])

    def setValue(self, value: float) -> 'CsslProgressBar':
        self._value = value
        if self._tk_widget:
            self._tk_widget['value'] = value
        return self

    def getValue(self) -> float:
        if self._tk_widget:
            return self._tk_widget['value']
        return self._value

    def setMax(self, max_val: float) -> 'CsslProgressBar':
        self._max = max_val
        if self._tk_widget:
            self._tk_widget['maximum'] = max_val
        return self

    def setMode(self, mode: str) -> 'CsslProgressBar':
        self._mode = mode
        if self._tk_widget:
            self._tk_widget['mode'] = mode
        return self

    def start(self, interval: int = 50) -> 'CsslProgressBar':
        if self._tk_widget:
            self._tk_widget.start(interval)
        return self

    def stop(self) -> 'CsslProgressBar':
        if self._tk_widget:
            self._tk_widget.stop()
        return self

    def step(self, amount: float = 1) -> 'CsslProgressBar':
        if self._tk_widget:
            self._tk_widget.step(amount)
        return self


class CsslTable(CsslWidgetBase):
    """Table/DataGrid widget for tabular data display."""

    def __init__(self, parent: Any, columns: list = None):
        super().__init__(parent)
        self._columns = columns or []
        self._rows = []
        self._row_counter = 0
        self._size = (400, 300)
        self._select_handler: Optional[CsslEventHandler] = None
        self._dblclick_handler: Optional[CsslEventHandler] = None
        self._tree = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._frame = tk.Frame(canvas)
        col_ids = [f'col{i}' for i in range(len(self._columns))]
        self._tree = ttk.Treeview(self._frame, columns=col_ids, show='headings', selectmode='browse')
        for i, col_name in enumerate(self._columns):
            cid = f'col{i}'
            self._tree.heading(cid, text=str(col_name), command=lambda c=i: self._sort_column(c))
            self._tree.column(cid, width=100, minwidth=50)
        vsb = ttk.Scrollbar(self._frame, orient='vertical', command=self._tree.yview)
        hsb = ttk.Scrollbar(self._frame, orient='horizontal', command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self._tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        self._tree.bind('<<TreeviewSelect>>', self._on_select)
        self._tree.bind('<Double-1>', self._on_dblclick)
        self._frame.place(x=self._position[0], y=self._position[1],
                          width=self._size[0], height=self._size[1])
        self._tk_widget = self._tree

    def _sort_column(self, col_index: int, reverse: bool = False):
        items = [(self._tree.set(k, f'col{col_index}'), k) for k in self._tree.get_children('')]
        try:
            items.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        for index, (val, k) in enumerate(items):
            self._tree.move(k, '', index)
        self._tree.heading(f'col{col_index}',
                           command=lambda: self._sort_column(col_index, not reverse))

    def _on_select(self, event=None):
        if self._select_handler:
            sel = self.getSelectedRow()
            if sel:
                self._select_handler.trigger(sel)

    def _on_dblclick(self, event=None):
        if self._dblclick_handler:
            sel = self.getSelectedRow()
            if sel:
                self._dblclick_handler.trigger(sel)

    def setColumns(self, columns: list) -> 'CsslTable':
        self._columns = columns
        if self._tree:
            self._tree.destroy()
            self._tree = None
        self._create_widget()
        return self

    def getColumns(self) -> list:
        return list(self._columns)

    def addRow(self, values: list) -> str:
        row_id = f'row_{self._row_counter}'
        self._row_counter += 1
        if self._tree:
            self._tree.insert('', 'end', iid=row_id, values=values)
        self._rows.append({'id': row_id, 'values': values})
        return row_id

    def insertRow(self, index: int, values: list) -> str:
        row_id = f'row_{self._row_counter}'
        self._row_counter += 1
        if self._tree:
            self._tree.insert('', index, iid=row_id, values=values)
        self._rows.insert(index, {'id': row_id, 'values': values})
        return row_id

    def removeRow(self, row_id: str) -> 'CsslTable':
        if self._tree:
            try:
                self._tree.delete(row_id)
            except tk.TclError:
                pass
        self._rows = [r for r in self._rows if r['id'] != row_id]
        return self

    def updateRow(self, row_id: str, values: list) -> 'CsslTable':
        if self._tree:
            try:
                self._tree.item(row_id, values=values)
            except tk.TclError:
                pass
        for r in self._rows:
            if r['id'] == row_id:
                r['values'] = values
                break
        return self

    def getRow(self, row_id: str) -> list:
        if self._tree:
            try:
                return list(self._tree.item(row_id, 'values'))
            except tk.TclError:
                pass
        return []

    def getSelectedRow(self) -> Optional[str]:
        if self._tree:
            sel = self._tree.selection()
            return sel[0] if sel else None
        return None

    def getSelectedRows(self) -> list:
        if self._tree:
            return list(self._tree.selection())
        return []

    def setRowData(self, data: list) -> 'CsslTable':
        self.clear()
        for row in data:
            self.addRow(row)
        return self

    def getData(self) -> list:
        if self._tree:
            return [list(self._tree.item(child, 'values')) for child in self._tree.get_children('')]
        return []

    def getRowCount(self) -> int:
        if self._tree:
            return len(self._tree.get_children(''))
        return 0

    def clear(self) -> 'CsslTable':
        if self._tree:
            self._tree.delete(*self._tree.get_children(''))
        self._rows = []
        return self

    def setColumnWidth(self, column: int, width: int) -> 'CsslTable':
        if self._tree and 0 <= column < len(self._columns):
            self._tree.column(f'col{column}', width=width)
        return self

    def sortByColumn(self, column: int, reverse: bool = False) -> 'CsslTable':
        self._sort_column(column, reverse)
        return self

    def onSelect(self, callback) -> 'CsslTable':
        if self._select_handler is None:
            self._select_handler = CsslEventHandler()
        self._select_handler.add(callback)
        return self

    def onDoubleClick(self, callback) -> 'CsslTable':
        if self._dblclick_handler is None:
            self._dblclick_handler = CsslEventHandler()
        self._dblclick_handler.add(callback)
        return self

    def setSize(self, width: int, height: int) -> 'CsslTable':
        self._size = (width, height)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(width=width, height=height)
        return self

    def setPosition(self, x, y=None) -> 'CsslTable':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def show(self) -> 'CsslTable':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])
        return self

    def hide(self) -> 'CsslTable':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self

    def destroy(self) -> None:
        if hasattr(self, '_frame') and self._frame:
            self._frame.destroy()
        super().destroy()


class CsslListBox(CsslWidgetBase):
    """Scrollable list widget."""

    def __init__(self, parent: Any, items: list = None):
        super().__init__(parent)
        self._items = items or []
        self._size = (200, 150)
        self._select_mode = 'browse'
        self._select_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._frame = tk.Frame(canvas)
        self._listbox = tk.Listbox(self._frame, selectmode=self._select_mode)
        scrollbar = ttk.Scrollbar(self._frame, orient='vertical', command=self._listbox.yview)
        self._listbox.configure(yscrollcommand=scrollbar.set)
        self._listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        for item in self._items:
            self._listbox.insert('end', item)
        self._listbox.bind('<<ListboxSelect>>', self._on_select)
        self._frame.place(x=self._position[0], y=self._position[1],
                          width=self._size[0], height=self._size[1])
        self._tk_widget = self._listbox

    def _on_select(self, event=None):
        if self._select_handler:
            self._select_handler.trigger(self.getSelectedItem())

    def setItems(self, items: list) -> 'CsslListBox':
        self._items = items
        if self._listbox:
            self._listbox.delete(0, 'end')
            for item in items:
                self._listbox.insert('end', item)
        return self

    def getItems(self) -> list:
        return list(self._items)

    def addItem(self, item: str) -> 'CsslListBox':
        self._items.append(item)
        if self._listbox:
            self._listbox.insert('end', item)
        return self

    def removeItem(self, index: int) -> 'CsslListBox':
        if 0 <= index < len(self._items):
            self._items.pop(index)
            if self._listbox:
                self._listbox.delete(index)
        return self

    def getSelectedIndex(self) -> int:
        if self._listbox:
            sel = self._listbox.curselection()
            return sel[0] if sel else -1
        return -1

    def getSelectedItem(self) -> Optional[str]:
        idx = self.getSelectedIndex()
        if idx >= 0 and idx < len(self._items):
            return self._items[idx]
        return None

    def setSelectedIndex(self, index: int) -> 'CsslListBox':
        if self._listbox and 0 <= index < len(self._items):
            self._listbox.selection_clear(0, 'end')
            self._listbox.selection_set(index)
        return self

    def getItemCount(self) -> int:
        return len(self._items)

    def clear(self) -> 'CsslListBox':
        self._items = []
        if self._listbox:
            self._listbox.delete(0, 'end')
        return self

    def setMultiSelect(self, enabled: bool) -> 'CsslListBox':
        self._select_mode = 'extended' if enabled else 'browse'
        if self._listbox:
            self._listbox.configure(selectmode=self._select_mode)
        return self

    def getSelectedIndices(self) -> list:
        if self._listbox:
            return list(self._listbox.curselection())
        return []

    def onSelect(self, callback) -> 'CsslListBox':
        if self._select_handler is None:
            self._select_handler = CsslEventHandler()
        self._select_handler.add(callback)
        return self

    def setSize(self, width: int, height: int) -> 'CsslListBox':
        self._size = (width, height)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(width=width, height=height)
        return self

    def setPosition(self, x, y=None) -> 'CsslListBox':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def show(self) -> 'CsslListBox':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])
        return self

    def hide(self) -> 'CsslListBox':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self


class CsslTimePicker(CsslWidgetBase):
    """Time picker widget with hour:minute:second spinners."""

    def __init__(self, parent: Any, hour: int = 0, minute: int = 0, second: int = 0,
                 show_seconds: bool = True):
        super().__init__(parent)
        self._hour = hour
        self._minute = minute
        self._second = second
        self._show_seconds = show_seconds
        self._size = (180, 30) if show_seconds else (120, 30)
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._frame = tk.Frame(canvas)
        self._h_var = tk.StringVar(value=f'{self._hour:02d}')
        self._m_var = tk.StringVar(value=f'{self._minute:02d}')
        self._s_var = tk.StringVar(value=f'{self._second:02d}')

        self._h_spin = ttk.Spinbox(self._frame, from_=0, to=23, width=3,
                                    textvariable=self._h_var, wrap=True,
                                    command=self._on_changed, format='%02.0f')
        tk.Label(self._frame, text=':').pack(side='left')
        self._h_spin.pack(side='left')
        tk.Label(self._frame, text=':').pack(side='left')
        self._m_spin = ttk.Spinbox(self._frame, from_=0, to=59, width=3,
                                    textvariable=self._m_var, wrap=True,
                                    command=self._on_changed, format='%02.0f')
        self._m_spin.pack(side='left')
        if self._show_seconds:
            tk.Label(self._frame, text=':').pack(side='left')
            self._s_spin = ttk.Spinbox(self._frame, from_=0, to=59, width=3,
                                        textvariable=self._s_var, wrap=True,
                                        command=self._on_changed, format='%02.0f')
            self._s_spin.pack(side='left')
        self._frame.place(x=self._position[0], y=self._position[1])
        self._tk_widget = self._frame

    def _on_changed(self):
        try:
            self._hour = int(self._h_var.get())
            self._minute = int(self._m_var.get())
            self._second = int(self._s_var.get()) if self._show_seconds else 0
        except ValueError:
            pass
        if self._change_handler:
            self._change_handler.trigger(self.getTime())

    def setTime(self, hour: int, minute: int, second: int = 0) -> 'CsslTimePicker':
        self._hour, self._minute, self._second = hour, minute, second
        if hasattr(self, '_h_var'):
            self._h_var.set(f'{hour:02d}')
            self._m_var.set(f'{minute:02d}')
            self._s_var.set(f'{second:02d}')
        return self

    def getTime(self) -> dict:
        return {'hour': self._hour, 'minute': self._minute, 'second': self._second}

    def getHour(self) -> int:
        return self._hour

    def getMinute(self) -> int:
        return self._minute

    def getSecond(self) -> int:
        return self._second

    def setHour(self, h: int) -> 'CsslTimePicker':
        self._hour = h
        if hasattr(self, '_h_var'):
            self._h_var.set(f'{h:02d}')
        return self

    def setMinute(self, m: int) -> 'CsslTimePicker':
        self._minute = m
        if hasattr(self, '_m_var'):
            self._m_var.set(f'{m:02d}')
        return self

    def setSecond(self, s: int) -> 'CsslTimePicker':
        self._second = s
        if hasattr(self, '_s_var'):
            self._s_var.set(f'{s:02d}')
        return self

    def getTimeString(self, fmt: str = '%H:%M:%S') -> str:
        return fmt.replace('%H', f'{self._hour:02d}').replace('%M', f'{self._minute:02d}').replace('%S', f'{self._second:02d}')

    def onChange(self, callback) -> 'CsslTimePicker':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self

    def setPosition(self, x, y=None) -> 'CsslTimePicker':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def show(self) -> 'CsslTimePicker':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1])
        return self

    def hide(self) -> 'CsslTimePicker':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self


class CsslDatePicker(CsslWidgetBase):
    """Date picker widget with year/month/day spinners."""

    def __init__(self, parent: Any, year: int = None, month: int = None, day: int = None):
        super().__init__(parent)
        from datetime import date
        today = date.today()
        self._year = year or today.year
        self._month = month or today.month
        self._day = day or today.day
        self._size = (220, 30)
        self._change_handler: Optional[CsslEventHandler] = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._frame = tk.Frame(canvas)
        self._y_var = tk.StringVar(value=str(self._year))
        self._m_var = tk.StringVar(value=f'{self._month:02d}')
        self._d_var = tk.StringVar(value=f'{self._day:02d}')

        self._y_spin = ttk.Spinbox(self._frame, from_=1900, to=2100, width=5,
                                    textvariable=self._y_var, command=self._on_changed)
        self._y_spin.pack(side='left')
        tk.Label(self._frame, text='-').pack(side='left')
        self._m_spin = ttk.Spinbox(self._frame, from_=1, to=12, width=3,
                                    textvariable=self._m_var, wrap=True,
                                    command=self._on_changed, format='%02.0f')
        self._m_spin.pack(side='left')
        tk.Label(self._frame, text='-').pack(side='left')
        self._d_spin = ttk.Spinbox(self._frame, from_=1, to=31, width=3,
                                    textvariable=self._d_var, wrap=True,
                                    command=self._on_changed, format='%02.0f')
        self._d_spin.pack(side='left')
        self._frame.place(x=self._position[0], y=self._position[1])
        self._tk_widget = self._frame

    def _on_changed(self):
        try:
            self._year = int(self._y_var.get())
            self._month = int(self._m_var.get())
            self._day = int(self._d_var.get())
        except ValueError:
            pass
        if self._change_handler:
            self._change_handler.trigger(self.getDate())

    def setDate(self, year: int, month: int, day: int) -> 'CsslDatePicker':
        self._year, self._month, self._day = year, month, day
        if hasattr(self, '_y_var'):
            self._y_var.set(str(year))
            self._m_var.set(f'{month:02d}')
            self._d_var.set(f'{day:02d}')
        return self

    def getDate(self) -> dict:
        return {'year': self._year, 'month': self._month, 'day': self._day}

    def getYear(self) -> int:
        return self._year

    def getMonth(self) -> int:
        return self._month

    def getDay(self) -> int:
        return self._day

    def getDateString(self, fmt: str = '%Y-%m-%d') -> str:
        return fmt.replace('%Y', str(self._year)).replace('%m', f'{self._month:02d}').replace('%d', f'{self._day:02d}')

    def onChange(self, callback) -> 'CsslDatePicker':
        if self._change_handler is None:
            self._change_handler = CsslEventHandler()
        self._change_handler.add(callback)
        return self

    def setPosition(self, x, y=None) -> 'CsslDatePicker':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def show(self) -> 'CsslDatePicker':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1])
        return self

    def hide(self) -> 'CsslDatePicker':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self


class CsslTabPanel:
    """Panel within a TabControl — acts as parent for child widgets."""

    def __init__(self, frame):
        self._tk_widget = frame
        self._canvas = frame
        self._children: List[Any] = []
        self._cssl_runtime = None


class CsslTabControl(CsslWidgetBase):
    """Tabbed container widget."""

    def __init__(self, parent: Any):
        super().__init__(parent)
        self._tabs: Dict[str, CsslTabPanel] = {}
        self._size = (400, 300)
        self._tab_handler: Optional[CsslEventHandler] = None
        self._notebook = None
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        self._notebook = ttk.Notebook(canvas)
        self._notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)
        self._notebook.place(x=self._position[0], y=self._position[1],
                             width=self._size[0], height=self._size[1])
        self._tk_widget = self._notebook

    def _on_tab_changed(self, event=None):
        if self._tab_handler:
            self._tab_handler.trigger(self.getActiveTab())

    def addTab(self, name: str) -> CsslTabPanel:
        if self._notebook:
            frame = tk.Frame(self._notebook)
            self._notebook.add(frame, text=name)
            panel = CsslTabPanel(frame)
            self._tabs[name] = panel
            return panel
        return None

    def removeTab(self, name: str) -> 'CsslTabControl':
        if name in self._tabs and self._notebook:
            panel = self._tabs[name]
            tab_id = self._notebook.index(panel._tk_widget)
            self._notebook.forget(tab_id)
            del self._tabs[name]
        return self

    def setActiveTab(self, name: str) -> 'CsslTabControl':
        if name in self._tabs and self._notebook:
            self._notebook.select(self._tabs[name]._tk_widget)
        return self

    def getActiveTab(self) -> str:
        if self._notebook:
            try:
                current = self._notebook.select()
                tab_text = self._notebook.tab(current, 'text')
                return tab_text
            except Exception:
                pass
        return ""

    def getTabCount(self) -> int:
        return len(self._tabs)

    def getTabNames(self) -> list:
        return list(self._tabs.keys())

    def onTabChanged(self, callback) -> 'CsslTabControl':
        if self._tab_handler is None:
            self._tab_handler = CsslEventHandler()
        self._tab_handler.add(callback)
        return self


class CsslSeparator(CsslWidgetBase):
    """Visual separator/divider line."""

    def __init__(self, parent: Any, orientation: str = "horizontal"):
        super().__init__(parent)
        self._orientation = orientation
        self._size = (200, 2) if orientation == "horizontal" else (2, 200)
        self._create_widget()

    def _create_widget(self):
        canvas = self._resolve_parent()
        if canvas is None:
            return
        orient = tk.HORIZONTAL if self._orientation == "horizontal" else tk.VERTICAL
        self._tk_widget = ttk.Separator(canvas, orient=orient)
        self._tk_widget.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])

    def setOrientation(self, orientation: str) -> 'CsslSeparator':
        self._orientation = orientation
        if self._tk_widget:
            orient = tk.HORIZONTAL if orientation == "horizontal" else tk.VERTICAL
            self._tk_widget.configure(orient=orient)
        return self


class CsslMenu:
    """A menu within a menu bar."""

    def __init__(self, parent_menu, label: str):
        self._menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=label, menu=self._menu)
        self._label = label

    def addItem(self, label: str, callback=None) -> 'CsslMenu':
        self._menu.add_command(label=label, command=callback)
        return self

    def addSeparator(self) -> 'CsslMenu':
        self._menu.add_separator()
        return self

    def addCheckItem(self, label: str, callback=None) -> 'CsslMenu':
        var = tk.BooleanVar()
        self._menu.add_checkbutton(label=label, variable=var, command=callback)
        return self

    def addSubMenu(self, label: str) -> 'CsslMenu':
        submenu = CsslMenu(self._menu, label)
        return submenu

    def setEnabled(self, label: str, enabled: bool) -> 'CsslMenu':
        state = 'normal' if enabled else 'disabled'
        try:
            idx = self._menu.index(label)
            self._menu.entryconfigure(idx, state=state)
        except Exception:
            pass
        return self


class CsslMenuBar(CsslWidgetBase):
    """Menu bar for windows."""

    def __init__(self, parent: Any):
        super().__init__(parent)
        self._menus: Dict[str, CsslMenu] = {}
        self._menu_bar = None
        self._create_widget()

    def _create_widget(self):
        # MenuBar attaches to the root Tk window
        parent = self._parent
        root = None
        if isinstance(parent, CsslWidget):
            root = parent._tk_widget if hasattr(parent, '_tk_widget') else None
        if root is None:
            canvas = self._resolve_parent()
            if canvas and hasattr(canvas, 'winfo_toplevel'):
                root = canvas.winfo_toplevel()
        if root:
            self._menu_bar = tk.Menu(root)
            root.configure(menu=self._menu_bar)
            self._tk_widget = self._menu_bar

    def addMenu(self, label: str) -> CsslMenu:
        if self._menu_bar:
            menu = CsslMenu(self._menu_bar, label)
            self._menus[label] = menu
            return menu
        return None

    def getMenu(self, label: str) -> Optional[CsslMenu]:
        return self._menus.get(label)

    def removeMenu(self, label: str) -> 'CsslMenuBar':
        if label in self._menus and self._menu_bar:
            try:
                idx = self._menu_bar.index(label)
                self._menu_bar.delete(idx)
                del self._menus[label]
            except Exception:
                pass
        return self


class CsslFileDialog:
    """File open/save dialog — static methods only."""

    @staticmethod
    def openFile(title: str = "Open File", filetypes: list = None,
                 initialdir: str = None) -> str:
        ft = filetypes or [("All files", "*.*")]
        result = filedialog.askopenfilename(title=title, filetypes=ft, initialdir=initialdir)
        return result or ""

    @staticmethod
    def openFiles(title: str = "Open Files", filetypes: list = None,
                  initialdir: str = None) -> list:
        ft = filetypes or [("All files", "*.*")]
        result = filedialog.askopenfilenames(title=title, filetypes=ft, initialdir=initialdir)
        return list(result) if result else []

    @staticmethod
    def saveFile(title: str = "Save File", filetypes: list = None,
                 initialdir: str = None, defaultext: str = None) -> str:
        ft = filetypes or [("All files", "*.*")]
        result = filedialog.asksaveasfilename(
            title=title, filetypes=ft, initialdir=initialdir, defaultextension=defaultext
        )
        return result or ""

    @staticmethod
    def openDirectory(title: str = "Select Folder", initialdir: str = None) -> str:
        result = filedialog.askdirectory(title=title, initialdir=initialdir)
        return result or ""


class CsslScrollPanel(CsslWidgetBase):
    """Scrollable container widget."""

    def __init__(self, parent: Any, scroll_x: bool = False, scroll_y: bool = True):
        super().__init__(parent)
        self._scroll_x = scroll_x
        self._scroll_y = scroll_y
        self._size = (300, 200)
        self._inner_frame = None
        self._create_widget()

    def _create_widget(self):
        canvas_parent = self._resolve_parent()
        if canvas_parent is None:
            return
        self._frame = tk.Frame(canvas_parent)
        self._scroll_canvas = tk.Canvas(self._frame)
        self._inner_frame = tk.Frame(self._scroll_canvas)

        if self._scroll_y:
            vsb = ttk.Scrollbar(self._frame, orient='vertical', command=self._scroll_canvas.yview)
            self._scroll_canvas.configure(yscrollcommand=vsb.set)
            vsb.pack(side='right', fill='y')
        if self._scroll_x:
            hsb = ttk.Scrollbar(self._frame, orient='horizontal', command=self._scroll_canvas.xview)
            self._scroll_canvas.configure(xscrollcommand=hsb.set)
            hsb.pack(side='bottom', fill='x')

        self._scroll_canvas.pack(side='left', fill='both', expand=True)
        self._window_id = self._scroll_canvas.create_window((0, 0), window=self._inner_frame, anchor='nw')
        self._inner_frame.bind('<Configure>', self._on_frame_configure)

        self._frame.place(x=self._position[0], y=self._position[1],
                          width=self._size[0], height=self._size[1])
        # Expose inner frame as canvas so children can parent to it
        self._canvas = self._inner_frame
        self._tk_widget = self._inner_frame

    def _on_frame_configure(self, event=None):
        self._scroll_canvas.configure(scrollregion=self._scroll_canvas.bbox('all'))

    def setScrollRegion(self, width: int, height: int) -> 'CsslScrollPanel':
        if self._scroll_canvas:
            self._scroll_canvas.configure(scrollregion=(0, 0, width, height))
        return self

    def scrollTo(self, x: float, y: float) -> 'CsslScrollPanel':
        if self._scroll_canvas:
            self._scroll_canvas.xview_moveto(x)
            self._scroll_canvas.yview_moveto(y)
        return self

    def scrollToTop(self) -> 'CsslScrollPanel':
        if self._scroll_canvas:
            self._scroll_canvas.yview_moveto(0)
        return self

    def scrollToBottom(self) -> 'CsslScrollPanel':
        if self._scroll_canvas:
            self._scroll_canvas.yview_moveto(1)
        return self

    def setSize(self, width: int, height: int) -> 'CsslScrollPanel':
        self._size = (width, height)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(width=width, height=height)
        return self

    def setPosition(self, x, y=None) -> 'CsslScrollPanel':
        if y is None and isinstance(x, (list, tuple)):
            x, y = x[0], x[1]
        self._position = (x, y)
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_configure(x=x, y=y)
        return self

    def show(self) -> 'CsslScrollPanel':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place(x=self._position[0], y=self._position[1],
                              width=self._size[0], height=self._size[1])
        return self

    def hide(self) -> 'CsslScrollPanel':
        if hasattr(self, '_frame') and self._frame:
            self._frame.place_forget()
        return self


class CsslParent:
    """Base parent class for CSSL GUI applications - provides mygui::Parent"""

    def __init__(self):
        self._children: List[CsslWidgetBase] = []
        self._cssl_runtime = None
        self._main_widget: Optional[CsslWidget] = None

    def setRuntime(self, runtime: Any) -> None:
        """Set the CSSL runtime"""
        self._cssl_runtime = runtime
        for child in self._children:
            if hasattr(child, '_cssl_runtime'):
                child._cssl_runtime = runtime


class CsslGuiModule:
    """The CSSL GUI module - returned by include("cssl-gui")"""

    # Classes available in the module
    Parent = CsslParent
    Widget = CsslWidget
    Label = CsslLabel
    Button = CsslButton
    Picture = CsslPicture
    Sound = CsslSound
    Toolbar = CsslToolbar
    ToolbarSlot = CsslToolbarSlot
    InputField = CsslInputField
    CheckBox = CsslCheckBox
    RadioButton = CsslRadioButton
    ComboBox = CsslComboBox
    TextArea = CsslTextArea
    Slider = CsslSlider
    ProgressBar = CsslProgressBar
    Table = CsslTable
    ListBox = CsslListBox
    TimePicker = CsslTimePicker
    DatePicker = CsslDatePicker
    TabControl = CsslTabControl
    ScrollPanel = CsslScrollPanel
    MenuBar = CsslMenuBar
    Menu = CsslMenu
    Separator = CsslSeparator
    FileDialog = CsslFileDialog

    # Position constants
    Gui = CsslGui

    # Input filter constants
    InputFieldFilter = CSSLInputField

    def __init__(self):
        self._runtime = None

    def __getattr__(self, name: str) -> Any:
        """Allow accessing classes via module.ClassName"""
        class_map = {
            'Parent': CsslParent,
            'Widget': CsslWidget,
            'CsslWidget': CsslWidget,
            'Label': CsslLabel,
            'CsslLabel': CsslLabel,
            'Button': CsslButton,
            'CsslButton': CsslButton,
            'Picture': CsslPicture,
            'CsslPicture': CsslPicture,
            'Sound': CsslSound,
            'CsslSound': CsslSound,
            'Toolbar': CsslToolbar,
            'CsslToolbar': CsslToolbar,
            'InputField': CsslInputField,
            'CsslInputField': CsslInputField,
            'Gui': CsslGui,
            'CsslGui': CsslGui,
            'CheckBox': CsslCheckBox,
            'CsslCheckBox': CsslCheckBox,
            'RadioButton': CsslRadioButton,
            'CsslRadioButton': CsslRadioButton,
            'ComboBox': CsslComboBox,
            'CsslComboBox': CsslComboBox,
            'TextArea': CsslTextArea,
            'CsslTextArea': CsslTextArea,
            'Slider': CsslSlider,
            'CsslSlider': CsslSlider,
            'ProgressBar': CsslProgressBar,
            'CsslProgressBar': CsslProgressBar,
            'Table': CsslTable,
            'CsslTable': CsslTable,
            'ListBox': CsslListBox,
            'CsslListBox': CsslListBox,
            'TimePicker': CsslTimePicker,
            'CsslTimePicker': CsslTimePicker,
            'DatePicker': CsslDatePicker,
            'CsslDatePicker': CsslDatePicker,
            'TabControl': CsslTabControl,
            'CsslTabControl': CsslTabControl,
            'ScrollPanel': CsslScrollPanel,
            'CsslScrollPanel': CsslScrollPanel,
            'MenuBar': CsslMenuBar,
            'CsslMenuBar': CsslMenuBar,
            'Menu': CsslMenu,
            'CsslMenu': CsslMenu,
            'Separator': CsslSeparator,
            'CsslSeparator': CsslSeparator,
            'FileDialog': CsslFileDialog,
            'CsslFileDialog': CsslFileDialog,
        }

        if name in class_map:
            return class_map[name]

        raise AttributeError(f"'CsslGuiModule' has no attribute '{name}'")


# Global module instance
_gui_module = CsslGuiModule()


def get_gui_module() -> CsslGuiModule:
    """Get the GUI module instance"""
    return _gui_module


# Export classes for direct import
__all__ = [
    'CsslGui',
    'CsslGuiPosition',
    'CsslWidget',
    'CsslWidgetBase',
    'CsslLabel',
    'CsslButton',
    'CsslPicture',
    'CsslSound',
    'CsslToolbar',
    'CsslToolbarSlot',
    'CsslInputField',
    'CsslInputFieldFilter',
    'CSSLInputField',
    'CsslParent',
    'CsslEventHandler',
    'CsslGuiModule',
    'get_gui_module',
    'CsslCheckBox',
    'CsslRadioButton',
    'CsslComboBox',
    'CsslTextArea',
    'CsslSlider',
    'CsslProgressBar',
    'CsslTable',
    'CsslListBox',
    'CsslTimePicker',
    'CsslDatePicker',
    'CsslTabPanel',
    'CsslTabControl',
    'CsslScrollPanel',
    'CsslMenuBar',
    'CsslMenu',
    'CsslSeparator',
    'CsslFileDialog',
]
