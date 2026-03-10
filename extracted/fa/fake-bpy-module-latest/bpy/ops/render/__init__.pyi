import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def color_management_white_balance_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a white balance preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def cycles_integrator_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an Integrator Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def cycles_performance_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an Performance Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def cycles_sampling_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a Sampling Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def cycles_viewport_sampling_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a Viewport Sampling Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def eevee_raytracing_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove an EEVEE ray-tracing preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def opengl(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    animation: bool | None = False,
    render_keyed_only: bool | None = False,
    sequencer: bool | None = False,
    write_still: bool | None = False,
    view_context: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Take a snapshot of the active viewport

    :param animation: Animation, Render files from the animation range of this scene (optional)
    :param render_keyed_only: Render Keyframes Only, Render only those frames where selected objects have a key in their animation data. Only used when rendering animation (optional)
    :param sequencer: Sequencer, Render using the sequencers OpenGL display (optional)
    :param write_still: Write Image, Save the rendered image to the output path (used only when animation is disabled) (optional)
    :param view_context: View Context, Use the current 3D view for rendering, else use scene settings (optional)
    :return: Result of the operator call.
    """

def play_rendered_anim(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Play back rendered frames/movies using an external player

    :return: Result of the operator call.
    """

def preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a Render Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def render(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    animation: bool | None = False,
    write_still: bool | None = False,
    use_viewport: bool | None = False,
    use_sequencer_scene: bool | None = False,
    layer: str | None = "",
    scene: str | None = "",
    frame_start: int | None = 0,
    frame_end: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param animation: Animation, Render files from the animation range of this scene (optional)
    :param write_still: Write Image, Save the rendered image to the output path (used only when animation is disabled) (optional)
    :param use_viewport: Use 3D Viewport, When inside a 3D viewport, use layers and camera of the viewport (optional)
    :param use_sequencer_scene: Use Sequencer Scene, Render the sequencer scene instead of the active scene (optional)
    :param layer: Render Layer, Single render layer to re-render (used only when animation is disabled) (optional, never None)
    :param scene: Scene, Scene to render, current scene if not specified (optional, never None)
    :param frame_start: Start Frame, Frame to start rendering animation at. If not specified, the scene start frame will be assumed. This should only be specified if doing an animation render (in [-inf, inf], optional)
    :param frame_end: End Frame, Frame to end rendering animation at. If not specified, the scene end frame will be assumed. This should only be specified if doing an animation render (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def shutter_curve_preset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    shape: typing.Literal["SHARP", "SMOOTH", "MAX", "LINE", "ROUND", "ROOT"]
    | None = "SMOOTH",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set shutter curve

    :param shape: Mode, (optional)
    :return: Result of the operator call.
    """

def swap_dimensions(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flip X and Y resolutions

    :return: Result of the operator call.
    """

def view_cancel(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cancel showing the render view

    :return: Result of the operator call.
    """

def view_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle show render view

    :return: Result of the operator call.
    """
