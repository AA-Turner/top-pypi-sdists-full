"""MODEL PRIORITY GROUPS — the EXPLICIT, operator-ordered fallback list.

    GET    /llm/model-groups           list every group          (member-read)
    GET    /llm/model-groups/resolve?key=<model>
                                       the ordered walk + the WHY (member-read)
    POST   /llm/model-groups           create or replace         (OPERATOR)
    PUT    /llm/model-groups/<id>      replace                   (OPERATOR)
    PATCH  /llm/model-groups/<id>      partial update            (OPERATOR)
    DELETE /llm/model-groups/<id>      remove                    (OPERATOR)

Sibling of ``group_routes.py``, which reads the DERIVED grouping (suffix
stripping + a ranking pipeline, off by default). This file owns the EXPLICIT
one: an ordered list the operator wrote by hand, which outranks the derivation
for any key it names.

WHY THIS FILE HAS WRITE ROUTES AND ``group_routes.py`` MUST NOT
--------------------------------------------------------------
That module's state is a TICK on a DERIVED group — three booleans that already
had a home in the F4 settings namespace, so a second write path there would have
been a parallel store. A priority group is a first-class RECORD with structural
invariants (ordering, at-most-one-enabled-group-per-key) that must be validated
on every write. Validation lives in ``comms.priority_groups.put_group`` and this
blueprint is its only caller, so there is still exactly ONE validated write path
— the thing the parallel-store rule is actually protecting.

The mutations are listed in ``operator_auth._SENSITIVE``, so a member gets 403
and an anonymous caller 401 automatically. The two GETs are deliberately absent
from that inventory: reads are member-visible like every other console read.
"""
from flask import jsonify, request

from .imports import *  # get_bp + the functions star

model_group_bp, logger = get_bp("model_group_bp", __name__)


def _who() -> str:
    """Best-effort authorship for the audit fields; never raises."""
    try:
        from ..operator_auth import current_principal
        p = current_principal() or {}
        return str(p.get("name") or p.get("id") or "operator")
    except Exception:  # noqa: BLE001
        return "operator"


def _payload() -> dict:
    return request.get_json(silent=True) or {}


@model_group_bp.route("/llm/model-groups", methods=["GET"])
def model_groups_list():
    """Every priority group, in display order. Member-readable.

    Never 500s: a store read that fails reports an empty list with the error
    attached, because a broken groups PAGE must not look like a broken groups
    FEATURE (same posture as GET /llm/groups)."""
    try:
        from ....comms.priority_groups import all_groups
        return jsonify({"groups": all_groups()})
    except Exception as exc:  # noqa: BLE001
        logger.warning("GET /llm/model-groups failed: %s", exc, exc_info=True)
        return jsonify({"groups": [], "error": str(exc)}), 200


@model_group_bp.route("/llm/model-groups/resolve", methods=["GET"])
def model_groups_resolve():
    """THE PREVIEW: what would happen if this key were requested right now.

    ``?key=<model>`` (required), optional ``?pool=`` / ``?task=`` so the preview
    is scoped exactly the way the serve path would be. Returns the ordered
    candidate list with, for EVERY member, the reason it was chosen or skipped
    (blocked / missing / no-worker / lower-priority) — the say-why discipline
    the rest of this console runs on.

    ``route: null`` means "change nothing": either no group claims the key, or
    no member is usable and the request will fail exactly as it does today."""
    key = (request.args.get("key") or "").strip()
    if not key:
        return jsonify({"error": "key is required"}), 400
    pool = (request.args.get("pool") or "").strip() or None
    task = (request.args.get("task") or "").strip() or None
    try:
        from ..functions.imports.utils.priority_groups import resolve
        return jsonify(resolve(key, pool, task, full=True))
    except Exception as exc:  # noqa: BLE001 — a preview must not 500
        logger.warning("GET /llm/model-groups/resolve failed for %s: %s",
                       key, exc, exc_info=True)
        return jsonify({"requested": key, "group": None, "candidates": [],
                        "chosen": None, "route": None,
                        "why": f"preview failed: {exc}"}), 200


@model_group_bp.route("/llm/model-groups", methods=["POST"])
def model_groups_create():
    """Create or REPLACE a group. Body: {id?, name, members: [...], enabled?}.

    ``members`` is an ORDER, so a write always carries the whole list — see
    ``put_group``. 409 on the one structural conflict (a key already claimed by
    another ENABLED group), with the offending key and the group that holds it
    named in the message; nothing is silently dropped."""
    body = _payload()
    try:
        from ....comms.priority_groups import put_group
        rec, errors = put_group(
            body.get("id") or body.get("name"),
            name=body.get("name"),
            members=body.get("members"),
            enabled=body.get("enabled", True),
            by=_who())
    except Exception as exc:  # noqa: BLE001
        logger.warning("POST /llm/model-groups failed: %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500
    if errors:
        conflict = any("at most one enabled group" in e for e in errors)
        return jsonify({"error": "; ".join(errors), "errors": errors}), \
            (409 if conflict else 400)
    return jsonify({"group": rec}), 200


@model_group_bp.route("/llm/model-groups/<group_id>", methods=["PUT", "PATCH"])
def model_groups_update(group_id):
    """Replace (PUT) or patch (PATCH) a group.

    PATCH reads the current record, applies only the supplied fields, and goes
    through the SAME validated write — a partial update never bypasses the
    conflict check."""
    body = _payload()
    try:
        from ....comms.priority_groups import get_group, put_group
        cur = get_group(group_id)
        if cur is None and request.method == "PATCH":
            return jsonify({"error": f"no such priority group: {group_id}"}), 404
        base = cur or {"name": group_id, "members": [], "enabled": True}
        rec, errors = put_group(
            group_id,
            name=body.get("name", base.get("name")),
            members=body.get("members", base.get("members")),
            enabled=body.get("enabled", base.get("enabled", True)),
            by=_who())
    except Exception as exc:  # noqa: BLE001
        logger.warning("%s /llm/model-groups/%s failed: %s",
                       request.method, group_id, exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500
    if errors:
        conflict = any("at most one enabled group" in e for e in errors)
        return jsonify({"error": "; ".join(errors), "errors": errors}), \
            (409 if conflict else 400)
    return jsonify({"group": rec}), 200


@model_group_bp.route("/llm/model-groups/<group_id>", methods=["DELETE"])
def model_groups_delete(group_id):
    """Remove a group. Idempotent-ish: 404 when it was never there, so a
    console that thinks it deleted something twice learns the truth."""
    try:
        from ....comms.priority_groups import delete_group
        if not delete_group(group_id):
            return jsonify({"error": f"no such priority group: {group_id}"}), 404
    except Exception as exc:  # noqa: BLE001
        logger.warning("DELETE /llm/model-groups/%s failed: %s",
                       group_id, exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500
    return jsonify({"deleted": group_id}), 200
