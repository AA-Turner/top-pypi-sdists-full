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
        """Set widget size"""
        self._size = (width, height)
        if self._tk_widget:
            self._tk_widget.configure(width=width, height=height)
        return self

    def show(self) -> 'CsslWidgetBase':
        """Show the widget"""
        self._visible = True
        if self._tk_widget:
            self._tk_widget.place(x=self._position[0], y=self._position[1])
        return self

    def hide(self) -> 'CsslWidgetBase':
        """Hide the widget"""
        self._visible = False
        if self._tk_widget:
            self._tk_widget.place_forget()
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
        for handler in self._on_close_handlers:
            try:
                handler()
            except:
                pass
        self._running = False
        self._tk_widget.destroy()

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
            self._tk_widget.mainloop()

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
        """Handle button click"""
        # Call direct callback first
        if self._click_callback:
            try:
                self._click_callback()
            except Exception as e:
                print(f"[CsslGui] Button click error: {e}")
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
]
