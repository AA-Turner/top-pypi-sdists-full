"""Numbered, resumable terminal setup using the same schema as LAN setup."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from shlex import quote

from .camera_sources import CameraSpec, discover_cameras, one_per_camera, usb_link_mbps
from .yam_can import discover_can_interfaces, locate_arms, pin_arms
from .yam_config import (
    ARM_TYPES,
    DEFAULT_CONFIG_PATH,
    GRIPPER_TYPES,
    ROLES,
    ArmConfig,
    YamConfig,
    load_config,
    save_config,
)


def config_option(config_path):
    return (
        "" if Path(config_path) == DEFAULT_CONFIG_PATH else f" --config {quote(str(config_path))}"
    )


class _Back(Exception):
    pass


class _Refresh(Exception):
    pass


class _Finish(Exception):
    pass


class _Clear(Exception):
    pass


def _choose(label, choices, *, current=None, input_fn=input, print_fn=print):
    """choices is [(value, label)]; blank reuses a saved value, otherwise skips."""
    print_fn(f"\n{label}")
    for i, (value, text) in enumerate(choices, 1):
        print_fn(f"  {i}. {text}" + (" [saved]" if value == current else ""))
    while True:
        reply = (
            input_fn(
                "Number [Enter: saved/skip; s: skip; c: clear mapping; "
                "r: refresh; b: back; q: save & exit]: "
            )
            .strip()
            .lower()
        )
        if reply == "c":
            raise _Clear
        if reply == "q":
            raise _Finish
        if reply == "b":
            raise _Back
        if reply == "r":
            raise _Refresh
        if reply == "s" or not reply and current is None:
            return None
        if not reply:
            return current
        if reply.isdecimal() and 1 <= int(reply) <= len(choices):
            return choices[int(reply) - 1][0]
        print_fn("Choose a listed number, or s to skip this mapping for now.")


def can_label(item):
    return (
        f"{item.name} · {'up' if item.up else 'down'} · {item.state} · "
        f"{str(item.bitrate) + ' bit/s' if item.bitrate else 'bitrate unknown'} · "
        f"{item.adapter or 'adapter identity unavailable'}"
    )


def run_cli_setup(
    config_path=DEFAULT_CONFIG_PATH,
    *,
    discover=discover_cameras,
    discover_can=discover_can_interfaces,
    input_fn=input,
    print_fn=print,
):
    config = load_config(config_path)
    print_fn("YAM setup — selections save as you go. No motor connection or calibration.")
    print_fn(
        "This terminal has no camera preview. Match camera roles and arm sides "
        "using labels/cabling; "
        "visually confirm all views and mappings during attended setup before motion."
    )
    step = 0
    steps = [*ROLES, "left arm", "right arm"]
    choose = lambda label, options, current=None: _choose(  # noqa: E731
        label, options, current=current, input_fn=input_fn, print_fn=print_fn
    )
    try:
        while step < len(steps):
            saved_stage = config.to_dict()
            try:
                if step < 3:
                    role = steps[step]
                    try:
                        found = discover()
                    except Exception as exc:
                        print_fn(f"Camera discovery unavailable: {exc}")
                        found = []
                    if not found and config.cameras:
                        print_fn(
                            "No additional cameras discovered. Saved choices are listed below."
                        )
                    elif not found:
                        print_fn(
                            "No cameras discovered. Check USB/power, stable /dev/v4l links "
                            "and camera drivers; "
                            "refresh or skip to keep a draft."
                        )
                    # One choice per physical camera; saved ones keep their stream settings.
                    specs = one_per_camera(config.cameras, found, link_speed=usb_link_mbps)
                    present = {s.physical_id for s in found}
                    choices = [
                        (
                            s.id,
                            f"{s.backend} · {s.physical_id} · {s.device}"
                            + (
                                " [unavailable saved camera]"
                                if s.physical_id not in present
                                else ""
                            ),
                        )
                        for s in specs
                    ]
                    choices.append(("__custom__", "Advanced: registered custom RGB reader"))
                    selected = choose(
                        f"{role.title()} camera — explicitly identify its view",
                        choices,
                        config.roles.get(role),
                    )
                    if selected is None:
                        step += 1
                        continue
                    if selected == "__custom__":
                        spec = CameraSpec(
                            id=input_fn("Local camera name: ").strip(),
                            backend="custom",
                            physical_id=input_fn("Stable physical identity: ").strip(),
                            device=input_fn("Registered custom reader name: ").strip(),
                        )
                    else:
                        spec = next(s for s in specs if s.id == selected)
                    if any(
                        other != role and camera == spec.id
                        for other, camera in config.roles.items()
                    ):
                        print_fn(
                            "That camera already has another role. "
                            "Choose a different camera or go back."
                        )
                        continue
                    if spec.backend in {"uvc", "zed"}:
                        backend = choose(
                            "Camera stream",
                            [("uvc", "UVC RGB"), ("zed", "ZED side-by-side")],
                            spec.backend,
                        )
                        if backend == "zed":
                            # USB ZED stereo modes, expressed per eye in our
                            # shared camera schema. OpenCV requests double width.
                            modes = [
                                (672, 376, 30),
                                (1280, 720, 30),
                                (1920, 1080, 30),
                                (2208, 1242, 15),
                                (672, 376, 60),
                                (1280, 720, 60),
                            ]
                            saved_mode = (
                                (spec.width, spec.height, spec.fps)
                                if spec.backend == "zed"
                                else None
                            )
                            if saved_mode is not None and saved_mode not in modes:
                                modes.append(saved_mode)
                            mode = choose(
                                "ZED capture mode — dimensions per eye",
                                [
                                    (value, f"{value[0]} × {value[1]} · {value[2]} fps")
                                    for value in modes
                                ],
                                saved_mode,
                            )
                            if mode is None:
                                print_fn("Choose a capture mode before saving a ZED stream.")
                                continue
                            eye = choose(
                                "ZED RGB eye",
                                [("left", "Left eye"), ("right", "Right eye")],
                                spec.eye,
                            )
                            if eye is None:
                                print_fn("Choose an eye before saving a ZED stream.")
                                continue
                            spec = replace(
                                spec,
                                backend=backend,
                                eye=eye,
                                width=mode[0],
                                height=mode[1],
                                fps=mode[2],
                            )
                        elif backend == "uvc":
                            spec = replace(spec, backend=backend, eye=None)
                    rotate = choose(
                        "Clockwise image rotation",
                        [(n, f"{n} degrees") for n in (0, 90, 180, 270)],
                        spec.rotate,
                    )
                    if rotate is not None:
                        spec = replace(spec, rotate=rotate)
                    config.cameras = [s for s in config.cameras if s.id != spec.id] + [spec]
                    config.roles[role] = spec.id
                else:
                    side = steps[step].split()[0]
                    inventory = discover_can()
                    # Pinned arms show under today's names; saving re-pins by name.
                    config, _ = locate_arms(config, inventory)
                    if inventory.hint:
                        print_fn(inventory.hint)
                    if not inventory.interfaces:
                        print_fn(
                            "No CAN adapters found. Check USB/power, SocketCAN driver "
                            "and iproute2; "
                            "have the operator configure the bus, then refresh. "
                            "No bus settings are changed here."
                        )
                    choices = [(i.name, can_label(i)) for i in inventory.interfaces]
                    known = {name for name, _ in choices}
                    for saved in config.arms.values():
                        if saved.can_interface not in known:
                            choices.append(
                                (
                                    saved.can_interface,
                                    f"{saved.can_interface} [unavailable saved adapter]",
                                )
                            )
                            known.add(saved.can_interface)
                    current = config.arms.get(side)
                    interface = choose(
                        f"{side.title()} arm CAN — confirm labels/cabling; "
                        "names do not establish side",
                        choices,
                        current.can_interface if current else None,
                    )
                    if interface is None:
                        step += 1
                        continue
                    if any(
                        s != side and arm.can_interface == interface
                        for s, arm in config.arms.items()
                    ):
                        print_fn(
                            "That CAN interface already belongs to the other arm. "
                            "Choose a different adapter."
                        )
                        continue
                    arm_type = choose(
                        "Actual arm variant",
                        [(s, s) for s in ARM_TYPES],
                        current.arm_type if current else None,
                    )
                    gripper = choose(
                        "Actual gripper variant",
                        [(s, s) for s in GRIPPER_TYPES],
                        current.gripper_type if current else None,
                    )
                    if arm_type is None or gripper is None:
                        print_fn("Both variants are needed to save this arm; skipped for now.")
                    else:
                        # Keeping an unplugged arm's saved choice keeps its pinned adapter.
                        kept = current.adapter_id if current and (
                            current.can_interface == interface
                        ) else None
                        config.arms[side] = ArmConfig(interface, arm_type, gripper, adapter_id=kept)
                        config = pin_arms(config, inventory)
                save_config(config, config_path)
                step += 1
            except _Clear:
                if step < 3:
                    config.roles.pop(steps[step], None)
                else:
                    config.arms.pop(steps[step].split()[0], None)
                save_config(config, config_path)
                print_fn("Mapping cleared. The device is available for another role.")
                step += 1
            except _Refresh:
                continue
            except _Back:
                step = max(0, step - 1)
            except ValueError as exc:
                config = YamConfig.from_dict(saved_stage)
                print_fn(f"Please correct this selection: {exc}")
    except (_Finish, KeyboardInterrupt, EOFError):
        print_fn("Setup paused.")
    save_config(config, config_path)
    try:
        config.validate(complete=True)
        print_fn(
            f"Saved {config_path}. Visual/physical mapping confirmation is still required."
        )
    except ValueError:
        print_fn(
            f"Draft saved to {config_path}. Resume with: "
            f"dreamscale robots yam setup --cli{config_option(config_path)}"
        )
    return config
