"""Build ``incident_res`` payloads matching the new-flow ``IncidentMessage`` wire format.

Legacy post-processing (``weapon_detection``, ``fire_smoke_detection``, etc.)
reuses the same envelope as ``AnalyticsEngineSession`` → ``IncidentMessage.from_event()``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ...analytics.engine_session import resolve_camera_fields_from_stream_info
from ...analytics.schemas import IncidentEvent, IncidentMessage, StreamInfo


def map_severity_for_wire(level: str) -> str:
    """Map internal ``significant`` to backend ``high``."""
    normalized = (level or "").lower().strip()
    if normalized == "significant":
        return "high"
    return normalized


def utc_now_iso_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Every shape a legacy use case's own start_time/end_time formatting has been
# observed to produce, tried in order. Includes "%Y:%m:%d %H:%M:%S" -- the
# EXIF-style colon-in-date format several use cases build by hand (see
# fire_detection.py's `_format_timestamp`) -- which the backend's RFC3339
# parser rejects outright. Rather than fix each of the ~30 producers, every
# legacy incident timestamp is normalized here, at the one place they all
# funnel through before reaching the wire.
_INCIDENT_TIMESTAMP_INPUT_FORMATS = (
    "%Y-%m-%dT%H:%M:%SZ",  # already RFC3339 (IncidentManager / IncidentLifecycle)
    "%Y-%m-%d-%H:%M:%S.%f UTC",  # stream_time style, with microseconds
    "%Y-%m-%d-%H:%M:%S UTC",  # stream_time style, no microseconds
    "%Y:%m:%d %H:%M:%S",  # legacy use-case bug: EXIF-style colon date
)


def normalize_incident_timestamp(value: Any) -> str:
    """Coerce a legacy use case's start_time/end_time into RFC3339 (``%Y-%m-%dT%H:%M:%SZ``).

    Unparseable or empty input is returned unchanged (as ``_pick_str`` would leave it) --
    passing through rather than dropping data on a shape not seen before.
    """
    text = _pick_str(value)
    if not text:
        return text
    for fmt in _INCIDENT_TIMESTAMP_INPUT_FORMATS:
        try:
            dt = datetime.strptime(text, fmt)
        except ValueError:
            continue
        return dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return text


def _pick_str(*candidates: Any) -> str:
    for value in candidates:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


_INCIDENT_END_TIME_PLACEHOLDERS = frozenset(
    {
        "",
        "n/a",
        "incident still active",
        "incident active",
    }
)


def is_valid_incident_end_time(value: Any) -> bool:
    """True when ``value`` is a real closing timestamp (not a lifecycle placeholder)."""
    text = _pick_str(value).lower()
    if not text:
        return False
    return text not in _INCIDENT_END_TIME_PLACEHOLDERS


def format_incident_human_text(
    incident_type: str,
    severity_level: str,
    *,
    is_end: bool = False,
) -> str:
    if is_end or (severity_level or "").lower().strip() == "info":
        return "Incident ended"
    incident_type = (incident_type or "incident").strip()
    severity = map_severity_for_wire(severity_level)
    return f"INCIDENT DETECTED: {incident_type} severity={severity}"


def stream_info_dict_to_stream_info(
    stream_info: Optional[Dict[str, Any]],
    *,
    application_name: Optional[str] = None,
    factory_app_deployment_id: str = "",
    factory_application_id: str = "",
) -> StreamInfo:
    """Map legacy pipeline ``stream_info`` dict → :class:`StreamInfo`."""
    si = stream_info or {}
    inp = si.get("input_settings") if isinstance(si.get("input_settings"), dict) else {}
    camera_info = si.get("camera_info") if isinstance(si.get("camera_info"), dict) else {}
    cam_fields = resolve_camera_fields_from_stream_info(si)

    camera_id = _pick_str(
        cam_fields.get("camera_id"),
        si.get("camera_id"),
        inp.get("camera_id"),
        camera_info.get("camera_id"),
        si.get("stream_key"),
    )
    camera_name = _pick_str(cam_fields.get("camera_name"))
    app_deployment_id = _pick_str(
        si.get("app_deployment_id"),
        inp.get("app_deployment_id"),
        camera_info.get("app_deployment_id"),
        factory_app_deployment_id,
    )
    app_id = _pick_str(
        si.get("application_id"),
        si.get("app_id"),
        inp.get("application_id"),
        camera_info.get("application_id"),
        factory_application_id,
    )
    resolved_app_name = _pick_str(
        application_name,
        si.get("application_name"),
        inp.get("application_name"),
        si.get("app_name"),
    )
    rtp_number = _pick_str(si.get("rtp_number"), inp.get("rtp_number"))
    stream_time = _pick_str(si.get("stream_time"), inp.get("stream_time"))
    location = _pick_str(
        cam_fields.get("location"),
        si.get("location"),
        inp.get("location"),
        camera_info.get("location"),
    )
    location_id = _pick_str(
        cam_fields.get("location_id"),
        si.get("locationId"),
        si.get("location_id"),
        inp.get("location_id"),
        camera_info.get("location_id"),
    )

    return StreamInfo(
        camera_id=camera_id,
        camera_name=camera_name,
        app_deployment_id=app_deployment_id,
        app_id=app_id,
        application_name=resolved_app_name,
        rtp_number=rtp_number,
        stream_time=stream_time,
        location=location,
        location_id=location_id,
    )


def _frame_id_from_stream_info(stream_info: Optional[Dict[str, Any]]) -> str:
    si = stream_info or {}
    inp = si.get("input_settings") if isinstance(si.get("input_settings"), dict) else {}
    return _pick_str(si.get("frame_id"), inp.get("frame_id"))


def build_incident_res_message(
    incident_data: Dict[str, Any],
    stream_info: Optional[Dict[str, Any]],
    *,
    camera_id: str = "",
    camera_name: Optional[str] = None,
    application_name: Optional[str] = None,
    location_name: Optional[str] = None,
    factory_app_deployment_id: str = "",
    factory_application_id: str = "",
    frame_id: str = "",
    stream_time: str = "",
) -> Dict[str, Any]:
    """Serialize a legacy incident dict to the canonical ``incident_res`` envelope."""
    ctx = stream_info_dict_to_stream_info(
        stream_info,
        application_name=application_name,
        factory_app_deployment_id=factory_app_deployment_id,
        factory_application_id=factory_application_id,
    )
    cid = _pick_str(camera_id, ctx.camera_id, "default_camera")

    incident_type = _pick_str(incident_data.get("incident_type"), "incident")
    raw_severity = _pick_str(incident_data.get("severity_level"), "none")
    raw_end_time = incident_data.get("end_time")
    is_end = raw_severity.lower() == "info" or is_valid_incident_end_time(raw_end_time)
    wire_severity = "info" if is_end else map_severity_for_wire(raw_severity)

    start_time = normalize_incident_timestamp(incident_data.get("start_time"))
    if is_end:
        end_time = (
            normalize_incident_timestamp(raw_end_time)
            if is_valid_incident_end_time(raw_end_time)
            else utc_now_iso_z()
        )
    else:
        end_time = ""

    human_text = _pick_str(incident_data.get("human_text"))
    if is_end:
        human_text = "Incident ended"
    elif not human_text.startswith("INCIDENT DETECTED:"):
        human_text = format_incident_human_text(incident_type, raw_severity)

    event = IncidentEvent(
        incident_id=_pick_str(incident_data.get("incident_id")),
        incident_type=incident_type,
        severity_level=wire_severity,
        human_text=human_text,
        start_time=start_time,
        end_time=end_time if is_end else "",
        camera_id=cid,
        frame_id=_pick_str(frame_id, _frame_id_from_stream_info(stream_info)),
    )

    resolved_location = _pick_str(location_name, ctx.location)
    message = IncidentMessage.from_event(
        event,
        stream_info=ctx,
        frame_id=event.frame_id,
        stream_time=_pick_str(stream_time, ctx.stream_time),
        location_name=resolved_location,
    )
    payload = message.model_dump()
    payload["camera_id"] = cid
    resolved_camera_name = _pick_str(camera_name, ctx.camera_name)
    if resolved_camera_name and resolved_camera_name != cid:
        payload["camera_name"] = resolved_camera_name
    elif payload.get("camera_name") == cid:
        payload["camera_name"] = ""
    return payload
