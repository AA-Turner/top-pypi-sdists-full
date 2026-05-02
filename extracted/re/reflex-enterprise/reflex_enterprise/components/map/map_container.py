"""Map container component for leaflet."""

from __future__ import annotations

from reflex.vars.base import Var

from reflex_enterprise.components.map.base import LazyBaseLeafletComponent
from reflex_enterprise.components.map.map_consumer import MapConsumer
from reflex_enterprise.components.map.types import LatLng, LatLngBounds


class MapContainerControlOptions(LazyBaseLeafletComponent):
    """MapContainerControlOptions component for leaflet."""

    # Whether a attribution control is added to the map by default.
    attribution_control: Var[bool]

    # Whether a zoom control is added to the map by default.
    zoom_control: Var[bool]


class MapContainerInteractionOptions(LazyBaseLeafletComponent):
    """MapContainerInteractionOptions component for leaflet."""

    # Whether the map can be zoomed to a rectangular area specified by dragging the mouse while pressing the shift key.
    box_zoom: Var[bool]

    # Whether the map can be zoomed in by double clicking on it and zoomed out by double clicking while holding shift. If passed 'center', double-click zoom will zoom to the center of the view regardless of where the mouse was.
    double_click_zoom: Var[bool | str]

    # Whether the map is draggable with mouse/touch or not.
    dragging: Var[bool]

    # Forces the map's zoom level to always be a multiple of this, particularly right after a fitBounds() or a pinch-zoom. By default, the zoom level snaps to the nearest integer; lower values (e.g. 0.5 or 0.1) allow for greater granularity. A value of 0 means the zoom level will not be snapped after fitBounds or a pinch-zoom.
    zoom_snap: Var[float]

    # Controls how much the map's zoom level will change after a zoomIn(), zoomOut(), pressing + or - on the keyboard, or using the zoom controls. Values smaller than 1 (e.g. 0.5) allow for greater granularity.
    zoom_delta: Var[float]

    # Whether the map automatically handles browser window resize to update itself.
    track_resize: Var[bool]


class MapContainerPanningInertiaOptions(LazyBaseLeafletComponent):
    """MapContainerPanningInertiaOptions component for leaflet."""

    # If enabled, panning of the map will have an inertia effect where the map builds momentum while dragging and continues moving in the same direction for some time. Feels especially nice on touch devices. Enabled by default.
    inertia: Var[bool]

    # The rate with which the inertial movement slows down, in pixels/second².
    inertia_deceleration: Var[int]

    # Max speed of the inertial movement, in pixels/second.
    inertia_max_speed: Var[int]

    #
    ease_linearity: Var[float]

    # Whether the map pans when the mouse is dragged outside its bounds.
    world_copy_jump: Var[bool]

    # If maxBounds is set, this option will control how solid the bounds are when dragging the map around. The default value of 0.0 allows the user to drag outside the bounds at normal speed, higher values will slow down map dragging outside bounds, and 1.0 makes the bounds fully solid, preventing the user from dragging outside the bounds.
    max_bounds_viscosity: Var[float]


class MapContainerKeyboardNavigationOptions(LazyBaseLeafletComponent):
    """MapContainerKeyboardNavigationOptions component for leaflet."""

    # Makes the map focusable and allows users to navigate the map with keyboard arrows and +/- keys.
    keyboard: Var[bool]

    # Amount of pixels to pan when pressing an arrow key.
    keyboard_pan_delta: Var[int]


class MapContainerMouseWheelOptions(LazyBaseLeafletComponent):
    """MapContainerMouseWheelOptions component for leaflet."""

    # Whether the map can be zoomed by using the mouse wheel. If passed 'center', it will zoom to the center of the view regardless of where the mouse was.
    scroll_wheel_zoom: Var[bool | str]

    # Limits the rate at which a wheel can fire (in milliseconds). By default user can't zoom via wheel more often than once per 40 ms.
    wheel_debounce_time: Var[int]

    # How many scroll pixels (as reported by L.DomEvent.getWheelDelta) mean a change of one full zoom level. Smaller values will make wheel-zooming faster (and vice versa).
    wheel_px_per_zoom_level: Var[int]

    # Whether the map can be scrolled with a mouse wheel.
    wheel_delta: Var[int]


class MapContainerTouchInteractionOptions(LazyBaseLeafletComponent):
    """MapContainerTouchInteractionOptions component for leaflet."""

    # Enables simulation of contextmenu event, default is true for mobile Safari.
    tap_hold: Var[bool]

    # The max number of pixels a user can shift his finger during touch for it to be considered a valid tap.
    tap_tolerance: Var[int]

    # Whether the map can be zoomed by touch-dragging with two fingers. If passed 'center', it will zoom to the center of the view regardless of where the touch events (fingers) were. Enabled for touch-capable web browsers.
    touch_zoom: Var[bool | str]

    # Set it to false if you don't want the map to zoom beyond min/max zoom and then bounce back when pinch-zooming.
    bounce_at_zoom_limits: Var[bool]


class MapContainerMapStateOptions(LazyBaseLeafletComponent):
    """MapContainerMapStateOtions component for leaflet."""

    # The Coordinate Reference System to use. Don't change this if you're not sure what it means.
    crs: Var[str]

    # Initial geographic center of the map view.
    center: Var[LatLng]

    # Initial zoom level of the map view.
    zoom: Var[float]

    # Minimum zoom level of the map. If not specified and at least one GridLayer or TileLayer is in the map, the lowest of their minZoom options will be used instead.
    min_zoom: Var[int]

    # Maximum zoom level of the map. If not specified and at least one GridLayer or TileLayer is in the map, the highest of their maxZoom options will be used instead.
    max_zoom: Var[int]

    # The bounds of the map view. If not specified, the map will be initialized to show the whole world.
    max_bounds: Var[LatLngBounds]


class MapContainerAnimationOptions(LazyBaseLeafletComponent):
    """MapContainerAnimationOptions component for leaflet."""

    # Whether the map zoom animation is enabled. By default it's enabled in all browsers that support CSS3 Transitions except Android.
    zoom_animation: Var[bool]

    # Won't animate zoom if the zoom difference exceeds this value.
    zoom_animation_threshold: Var[int]

    # Whether the tile fade animation is enabled. By default it's enabled in all browsers that support CSS3 Transitions except Android.
    fade_animation: Var[int]

    # Whether markers animate their zoom with the zoom animation, if disabled they will disappear for the length of the animation. By default it's enabled in all browsers that support CSS3 Transitions except Android.
    marker_zoom_animation: Var[bool]

    # Defines the maximum size of a CSS translation transform. The default value should not be changed unless a web browser positions layers in the wrong place after doing a large panBy.
    transform_3d_limit: Var[int]


class MapContainer(
    MapContainerControlOptions,
    MapContainerInteractionOptions,
    MapContainerPanningInertiaOptions,
    MapContainerKeyboardNavigationOptions,
    MapContainerMouseWheelOptions,
    MapContainerTouchInteractionOptions,
    MapContainerMapStateOptions,
    MapContainerAnimationOptions,
    LazyBaseLeafletComponent,
):
    """MapContainer component for leaflet."""

    tag = "MapContainer"

    # Whether Paths should be rendered on a Canvas renderer. By default, all Paths are rendered in a SVG renderer.
    prefer_canvas: Var[bool]

    @classmethod
    def create(cls, *children, id: str, **props):
        """Create a MapContainer."""
        # Extract event props for the MapConsumer, but exclude on_mount and on_unmount
        events_props = {
            key: value
            for key, value in props.items()
            if key.startswith("on_") and key not in ("on_mount", "on_unmount")
        }

        # Remove extracted event props from the main props
        for key in events_props:
            if key in props:
                props.pop(key)

        # Add the MapConsumer if we have events
        children = (*children, MapConsumer.create(map_ref=id, **events_props))

        return super().create(*children, **props)

    def add_custom_code(self) -> list[str]:
        """Add custom code for leaflet components."""
        return []
