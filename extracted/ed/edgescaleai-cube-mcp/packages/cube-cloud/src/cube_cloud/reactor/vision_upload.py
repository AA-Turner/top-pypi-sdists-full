"""Custom vision models uploaded from the console (docs/ai-reactor-deploy-spec.md §12,
"Custom models"; design and the deferred hardening in the CV spike memo, "In-console model
upload").

A registration is one remote image build (`tools/build_image.py`, the kaniko task):

    stage 1   FROM the model-tools base image (settings.vision_tools_image), run
              `model_tools register --no-build --report-line`: prepare (Hugging Face
              export, decoder append, card prefill) and validate on ONNX Runtime and
              OpenVINO. A model that fails validation FAILS THE BUILD, so nothing is pushed,
              and the outcome is one MODEL_TOOLS_REPORT {json} line in the build log.
    stage 2   busybox + /models/<name>/{model.onnx, meta.json}: the model image.

What happens where:

    prepare_upload   presigned S3 POST for the ONNX file, capped by S3 itself
                     (content-length-range), so the bytes never cross cube-cloud's
                     request path. Hugging Face models need no upload.
    start            check the form, assemble the build context (OUR Dockerfile and the
                     card from the form, never anything caller-supplied that runs), start
                     the build.
    status           polled by the page: read the build; on success pin the digest from
                     the registry and write the `registeredBy: model_tools` entry to the
                     gateway (vision.add_registered, under the cube lock); then report the
                     gateway's own view of the model until it is ready or failed.

Job records live in the build-jobs table beside the build's own, so a poll works on any
cube-cloud task. Every record carries the cube and profile that created it, and nothing is
returned to a caller who is not both.

Deliberately NOT done yet (demo scope; listed in the spike memo before production): model
image tenancy, who may upload beyond console_ai_write_profiles, license attestation,
isolating validation from the registry token, golden images and rendered checks in the
console, quotas, and an audit trail.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import tarfile
import tempfile
import time
import uuid

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_common.apollo_client import ApolloClient
from cube_common.config import ACR_DOCKER_PREFIX, ACR_REGISTRY
from cube_cloud.config import settings
from cube_cloud.reactor import vision
from cube_cloud.tools import build_image

logger = logging.getLogger(__name__)

MAX_UPLOAD_BYTES = 1 << 30                 # model_tools.validate.MAX_MODEL_BYTES
UPLOAD_URL_SECONDS = 900
UPLOAD_PREFIX = "vision-uploads/"
RECORD_SECONDS = 7 * 24 * 3600
REPORT_PREFIX = "MODEL_TOOLS_REPORT "      # model_tools.register.REPORT_PREFIX
IMAGE_PREFIX = "esai-vision-model-"
# Model names whose image repository (IMAGE_PREFIX + name) is already ours for something else:
# `esai-vision-model-tools` holds the pinned tools image every registration builds FROM.
RESERVED_NAMES = frozenset({"tools"})
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,38}[a-z0-9])?$")
# `org/name` with an optional `@revision`; the revision is recorded as given.
HF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}/[A-Za-z0-9][A-Za-z0-9._-]{0,95}(@[A-Za-z0-9._-]{1,64})?$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TOOLS_IMAGE_RE = re.compile(r"^" + re.escape(ACR_DOCKER_PREFIX) + r"/[a-z0-9._-]+:[A-Za-z0-9._-]+@sha256:[0-9a-f]{64}$")
MANIFEST_ACCEPT = ", ".join([
    "application/vnd.oci.image.index.v1+json",
    "application/vnd.docker.distribution.manifest.list.v2+json",
    "application/vnd.oci.image.manifest.v1+json",
    "application/vnd.docker.distribution.manifest.v2+json",
])
PREPROCESS_KEYS = frozenset({"resize", "pad", "pad_align", "scale", "mean", "std", "layout", "color"})
LABELS_MAX, LABEL_MAX_CHARS, CLASSES_MAX, TEXT_MAX = 1000, 60, 200, 500

# The steps the page draws, in order.
BUILDING, ADDING, LOADING, READY, FAILED = "building", "adding", "loading", "ready", "failed"


class FormError(ValueError):
    """A field the person can fix; its text is shown to them."""


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------

def available() -> bool:
    """Uploads need the model-tools image configured and the remote build configured."""
    return bool(TOOLS_IMAGE_RE.match(settings.vision_tools_image or "")) and build_image._config_ready() is None


def upload_origin() -> str:
    """The ONE origin the browser POSTs an upload to: the build-context bucket's regional
    virtual-hosted endpoint. The console shell's `connect-src` admits exactly this, and
    only when uploads are available (routes._shell_headers)."""
    return f"https://{settings.build_ctx_bucket}.s3.{settings.aws_region}.amazonaws.com"


def _s3_for_presign():
    from botocore.config import Config
    # Regional and virtual-hosted, so the presigned POST's URL is upload_origin() exactly.
    return boto3.client("s3", region_name=settings.aws_region,
                        endpoint_url=f"https://s3.{settings.aws_region}.amazonaws.com",
                        config=Config(s3={"addressing_style": "virtual"}, signature_version="s3v4"))


# ---------------------------------------------------------------------------
# The form -> a card, an entry, and the register arguments
# ---------------------------------------------------------------------------

def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _str(v, what: str, cap: int = TEXT_MAX, required: bool = False) -> str | None:
    if v is None or v == "":
        if required:
            raise FormError(f"{what} is required.")
        return None
    if not isinstance(v, str) or len(v) > cap or not v.isprintable():
        raise FormError(f"{what} must be text of at most {cap} characters.")
    return v.strip()


def _names(v, what: str, cap: int) -> list[str] | None:
    if v is None or v == []:
        return None
    if not isinstance(v, list) or len(v) > cap:
        raise FormError(f"{what} must be a list of at most {cap} names.")
    out = []
    for x in v:
        if not isinstance(x, str) or not x.strip() or len(x) > LABEL_MAX_CHARS or not x.isprintable():
            raise FormError(f"Every entry in {what} must be a name of at most {LABEL_MAX_CHARS} characters.")
        out.append(x.strip())
    if len(set(out)) != len(out):
        raise FormError(f"{what} has a repeated name.")
    return out


def parse_form(body: dict) -> dict:
    """The registration form, checked field by field. Returns the normalized request:
    {name, source, upload_id | hf, card, input_size, classes, score_threshold, device}.
    Card VALUES are checked for shape here and for meaning by the validator in the build,
    whose words reach the person if they are wrong."""
    if not isinstance(body, dict):
        raise FormError("Expected a JSON object.")
    name = _str(body.get("name"), "The model name", 40, required=True)
    if not NAME_RE.match(name):
        raise FormError("The model name must be lowercase letters, digits and dashes, starting and ending "
                        "with a letter or digit (it is the name apps call).")
    if name in RESERVED_NAMES:
        raise FormError(f"{name!r} is reserved; choose another model name.")
    source = body.get("source")
    out: dict = {"name": name, "source": source}
    if source == "onnx":
        upload_id = body.get("upload_id")
        if not isinstance(upload_id, str) or not re.fullmatch(r"vupl-[0-9a-f]{32}", upload_id):
            raise FormError("Upload the ONNX file first.")
        out["upload_id"] = upload_id
    elif source == "hf":
        hf = _str(body.get("hf"), "The Hugging Face model", 200, required=True)
        if not HF_RE.match(hf):
            raise FormError("The Hugging Face model must look like org/name, optionally org/name@revision.")
        out["hf"] = hf
    else:
        raise FormError("Choose an ONNX upload or a Hugging Face model.")

    card: dict = {}
    if (display := _str(body.get("display_name"), "The display name", 120)) is not None:
        card["name"] = display
    if (labels := _names(body.get("labels"), "the labels", LABELS_MAX)) is not None:
        card["labels"] = labels
    pre = body.get("preprocess")
    if pre is not None:
        if not isinstance(pre, dict) or not set(pre) <= PREPROCESS_KEYS:
            raise FormError(f"Preprocessing may set only {', '.join(sorted(PREPROCESS_KEYS))}.")
        for k, v in pre.items():
            ok = (isinstance(v, str) and len(v) <= 20) or _num(v) or (
                isinstance(v, list) and len(v) == 3 and all(_num(x) for x in v))
            if not ok:
                raise FormError(f"Preprocessing {k} has a value the console cannot pass on.")
        card["preprocess"] = dict(pre)
    size = body.get("input_size")
    if size is not None:
        if not (isinstance(size, list) and len(size) == 2 and all(isinstance(x, int) and not isinstance(x, bool)
                                                                   and 1 <= x <= 4096 for x in size)):
            raise FormError("The input size must be [width, height], each 1 to 4096.")
        card["input_size"] = list(size)
    thr = body.get("score_threshold")
    if thr is not None and not (_num(thr) and 0 <= thr <= 1):
        raise FormError("The score threshold must be a number from 0 to 1.")
    if thr is not None:
        card["defaults"] = {"conf_threshold": float(thr)}
    for key, what in (("license", "The license"), ("dataset_terms", "The dataset terms")):
        if (v := _str(body.get(key), what)) is not None:
            card[key] = v
    device = body.get("device", "cpu")
    if device not in ("cpu", "gpu"):
        raise FormError("The device must be cpu or gpu.")
    out.update(card=card, input_size=card.get("input_size"),
               classes=_names(body.get("classes"), "the classes to show", CLASSES_MAX),
               score_threshold=float(thr) if thr is not None else None, device=device)
    return out


def dockerfile(form: dict, tools_image: str) -> str:
    """The registration build's Dockerfile. Generated here, from checked values only."""
    args = ["python", "-m", "model_tools", "register", "--name", form["name"], "--card", "/work/input/card.json",
            "--no-build", "--work-dir", "/work/out", "--report-line"]
    if form["source"] == "onnx":
        args += ["--onnx", "/work/input/model.onnx"]
    else:
        args += ["--hf", form["hf"]]
        if form.get("input_size"):
            args += ["--input-size", f"{form['input_size'][0]}x{form['input_size'][1]}"]
    return "\n".join([
        f"FROM {tools_image} AS prep",
        "WORKDIR /work",
        "COPY input/ /work/input/",
        "RUN " + json.dumps(args),
        "FROM busybox:1.36",
        "COPY --from=prep /work/out/context/models/ /models/",
        "USER 1000:0",
        "",
    ])


def model_entry(form: dict, ref: str) -> dict:
    entry = {"name": form["name"], "task": "detection", "backend": "onnx", "image": ref, "path": form["name"],
             "device": form["device"]}
    if form.get("classes"):
        entry["classes"] = list(form["classes"])
    if form.get("score_threshold") is not None:
        entry["scoreThreshold"] = form["score_threshold"]
    entry[vision.REGISTERED_KEY] = vision.REGISTERED_VALUE
    entry[vision.UPLOADED_KEY] = vision.UPLOADED_VALUE      # the console's own mark: removable
    return entry


def parse_report(logs: str) -> dict | None:
    """The MODEL_TOOLS_REPORT line from a build log, or None."""
    for line in reversed((logs or "").splitlines()):
        i = line.find(REPORT_PREFIX)
        if i >= 0:
            try:
                rep = json.loads(line[i + len(REPORT_PREFIX):])
            except ValueError:
                return None
            if isinstance(rep, dict):
                return {k: rep.get(k) for k in ("passed", "errors", "warnings", "notes")}
    return None


# ---------------------------------------------------------------------------
# Records (the build-jobs table)
# ---------------------------------------------------------------------------

def _table():
    return build_image._jobs_table()


def _get(record_id: str) -> dict | None:
    try:
        return _table().get_item(Key={"job_id": record_id}).get("Item")
    except ClientError as e:
        logger.error("vision upload record read failed (%s)", type(e).__name__)
        return None


def _put(item: dict) -> None:
    _table().put_item(Item=item)


ADDING_STALE_SECONDS = 180


def _claim(reg_id: str, frm: str, to: str) -> bool:
    """Move a record from state `frm` to `to` only if it is still in `frm`: the one poll
    that wins writes the gateway entry; a concurrent one does not write it twice."""
    try:
        _table().update_item(Key={"job_id": reg_id}, UpdateExpression="SET #s = :to, claimed_at = :t",
                             ConditionExpression="#s = :frm", ExpressionAttributeNames={"#s": "state"},
                             ExpressionAttributeValues={":to": to, ":frm": frm, ":t": int(time.time())})
        return True
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            return False
        raise


def _mine(rec: dict | None, kind: str, env: dict, profile: str) -> bool:
    return bool(rec) and rec.get("kind") == kind and rec.get("env_id") == env.get("id") and rec.get("profile") == profile


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------

async def prepare_upload(env: dict, profile: str, size) -> dict:
    """A presigned POST for one ONNX file, at most MAX_UPLOAD_BYTES (enforced by S3)."""
    if not _num(size) or not 0 < size <= MAX_UPLOAD_BYTES:
        raise FormError(f"The ONNX file must be at most {MAX_UPLOAD_BYTES // (1 << 20)} MB.")
    upload_id = "vupl-" + uuid.uuid4().hex
    key = f"{UPLOAD_PREFIX}{upload_id}/model.onnx"
    post = await asyncio.to_thread(
        _s3_for_presign().generate_presigned_post,
        settings.build_ctx_bucket, key, Fields=None,
        Conditions=[["content-length-range", 1, MAX_UPLOAD_BYTES]], ExpiresIn=UPLOAD_URL_SECONDS)
    now = int(time.time())
    await asyncio.to_thread(_put, {"job_id": upload_id, "kind": "vision-upload", "env_id": env["id"],
                                    "profile": profile, "s3_key": key, "created_at": now,
                                    "expiry": now + RECORD_SECONDS})
    if not post["url"].rstrip("/") == upload_origin():
        raise RuntimeError("presigned upload URL is not the bucket origin the console admits")
    return {"upload_id": upload_id, "url": post["url"], "fields": post["fields"], "max_bytes": MAX_UPLOAD_BYTES}


# ---------------------------------------------------------------------------
# Start
# ---------------------------------------------------------------------------

def _build_context(form: dict, model_path: str | None, out_path: str) -> None:
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "input"))
        with open(os.path.join(d, "Dockerfile"), "w") as fh:
            fh.write(dockerfile(form, settings.vision_tools_image))
        with open(os.path.join(d, "input", "card.json"), "w") as fh:
            json.dump(form["card"], fh)
        if model_path:
            os.replace(model_path, os.path.join(d, "input", "model.onnx"))
        with tarfile.open(out_path, "w:gz") as tar:
            tar.add(d, arcname=".")


async def start(client: ApolloClient, env: dict, profile: str, body: dict) -> dict:
    """Check the form, assemble the build context, start the build. Returns the status."""
    form = parse_form(body)
    state = await vision.read_state(client, env, True, profile=profile)
    if (refusal := vision._refusal(state)) is not None:
        raise FormError(refusal)
    if vision.load_vision_catalog().model(form["name"]) is not None or any(o.name == form["name"] for o in state.others):
        raise FormError(f"This cube's vision gateway already has a model named {form['name']}; choose another name.")
    s3 = boto3.client("s3", region_name=settings.aws_region)
    reg_id = "vreg-" + uuid.uuid4().hex
    tag = f"0.1.0-{reg_id[5:17]}"
    with tempfile.TemporaryDirectory() as work:
        model_path = None
        if form["source"] == "onnx":
            up = await asyncio.to_thread(_get, form["upload_id"])
            if not _mine(up, "vision-upload", env, profile):
                raise FormError("That upload was not found; upload the ONNX file again.")
            try:
                head = await asyncio.to_thread(s3.head_object, Bucket=settings.build_ctx_bucket, Key=up["s3_key"])
            except ClientError:
                raise FormError("The ONNX file has not finished uploading.") from None
            if not 0 < head.get("ContentLength", 0) <= MAX_UPLOAD_BYTES:
                raise FormError("The ONNX file is empty or too large.")
            model_path = os.path.join(work, "model.onnx")
            await asyncio.to_thread(s3.download_file, settings.build_ctx_bucket, up["s3_key"], model_path)
        ctx = os.path.join(work, "context.tar.gz")
        await asyncio.to_thread(_build_context, form, model_path, ctx)
        prep = json.loads(await build_image.build_image_prepare(IMAGE_PREFIX + form["name"], tag))
        if "error" in prep:
            raise RuntimeError("build prepare failed")
        await asyncio.to_thread(s3.upload_file, ctx, settings.build_ctx_bucket, prep["s3_key"])
    started = json.loads(await build_image.build_image_start(client, prep["job_id"], dockerfile="Dockerfile"))
    if "error" in started:
        raise RuntimeError("build start failed")
    now = int(time.time())
    rec = {"job_id": reg_id, "kind": "vision-registration", "env_id": env["id"], "env_name": env.get("name", ""),
           "profile": profile, "build_job_id": prep["job_id"], "form": json.dumps(form), "tag": tag,
           "state": BUILDING, "created_at": now, "expiry": now + RECORD_SECONDS}
    await asyncio.to_thread(_put, rec)
    logger.info("vision registration %s of %s on %s by profile=%s started", reg_id, form["name"], env.get("name"), profile)
    return _view(rec)


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

def _lines(raw: str | None) -> list[str]:
    """A stored list of validator messages, as strings only: the page renders each as text,
    and the build log's report line is the validator's output, not ours to trust the shape of."""
    try:
        items = json.loads(raw or "[]")
    except ValueError:
        return []
    return [x if isinstance(x, str) else json.dumps(x) for x in items] if isinstance(items, list) else []


def _view(rec: dict, **extra) -> dict:
    form = json.loads(rec.get("form") or "{}")
    out = {"id": rec["job_id"], "name": form.get("name", ""), "state": rec.get("state", BUILDING),
           "message": rec.get("message", ""), "errors": _lines(rec.get("errors")),
           "warnings": _lines(rec.get("warnings")), "notes": _lines(rec.get("notes")),
           "image": rec.get("image", "")}
    out.update(extra)
    return out


async def _digest(client: ApolloClient, name: str, tag: str) -> str | None:
    token = await client.get_token()
    repo = f"{ACR_DOCKER_PREFIX[len(ACR_REGISTRY) + 1:]}/{IMAGE_PREFIX}{name}"
    async with httpx.AsyncClient(timeout=30) as http:
        r = await http.head(f"https://{ACR_REGISTRY}/v2/{repo}/manifests/{tag}",
                            headers={"Authorization": f"Bearer {token}", "Accept": MANIFEST_ACCEPT})
    digest = r.headers.get("Docker-Content-Digest", "")
    return digest if r.status_code == 200 and DIGEST_RE.match(digest) else None


async def _add(client: ApolloClient, env: dict, profile: str, rec: dict, form: dict) -> dict:
    """Write the entry (the claimed step), then move to LOADING or FAILED."""
    state = await vision.safe_read_state(client, env, True, profile=profile)
    if vision.is_registered_here(state, form["name"]):
        result_ok, message = True, f"{form['name']} is on the gateway."      # an earlier write landed
    else:
        result = await vision.add_registered(client, env, model_entry(form, rec["image"]), profile=profile)
        result_ok, message = result.ok, result.message
    rec["state"] = LOADING if result_ok else FAILED
    rec["message"] = message
    if not result_ok:
        rec["errors"] = json.dumps([message])
    await asyncio.to_thread(_put, rec)
    return _view(rec)


async def status(client: ApolloClient, env: dict, profile: str, reg_id: str) -> dict | None:
    """Where a registration has got to, advancing it when its build has finished. None
    for an id that is not this caller's on this cube."""
    if not re.fullmatch(r"vreg-[0-9a-f]{32}", reg_id or ""):
        return None
    rec = await asyncio.to_thread(_get, reg_id)
    if not _mine(rec, "vision-registration", env, profile):
        return None
    form = json.loads(rec["form"])
    if rec["state"] == BUILDING:
        build = json.loads(await build_image.build_image_status(rec["build_job_id"]))
        st_ = build.get("state")
        if st_ not in ("SUCCEEDED", "FAILED"):
            return _view(rec, building=st_ or "PENDING")
        report = parse_report(build.get("logs_tail", "")) or {}
        rec["warnings"] = json.dumps(report.get("warnings") or [])
        rec["notes"] = json.dumps(report.get("notes") or [])
        if st_ == "FAILED":
            rec["state"] = FAILED
            rec["errors"] = json.dumps(report.get("errors") or ["The model could not be prepared or validated."])
            rec["message"] = "The model did not pass validation, so nothing was added." if report else \
                "The build failed before the model could be validated."
            await asyncio.to_thread(_put, rec)
            return _view(rec)
        digest = await _digest(client, form["name"], rec["tag"])
        if digest is None:
            return _view(rec, building="PINNING")
        rec["image"] = f"{ACR_DOCKER_PREFIX}/{IMAGE_PREFIX}{form['name']}:{rec['tag']}@{digest}"
        await asyncio.to_thread(_put, rec)
        if not await asyncio.to_thread(_claim, reg_id, BUILDING, ADDING):
            return _view({**rec, "state": ADDING})
        rec["state"] = ADDING
        return await _add(client, env, profile, rec, form)
    if rec["state"] == ADDING:
        # A poll that claimed the write and then died leaves the record here: finish it.
        if int(time.time()) - int(rec.get("claimed_at") or 0) < ADDING_STALE_SECONDS:
            return _view(rec)
        if not await asyncio.to_thread(_claim, reg_id, ADDING, ADDING):
            return _view(rec)
        return await _add(client, env, profile, rec, form)
    if rec["state"] == LOADING:
        state = await vision.safe_read_state(client, env, True, profile=profile)
        other = next((o for o in (state.others if state else []) if o.name == form["name"]), None)
        if other is not None and other.status == vision.READY:
            rec["state"], rec["message"] = READY, f"{form['name']} is serving."
            await asyncio.to_thread(_put, rec)
        elif other is not None and other.status == vision.FAILED:
            err = other.live.error if other.live else ""
            rec["state"], rec["message"] = FAILED, "The gateway could not load it."
            rec["errors"] = json.dumps([err or "The gateway gave no reason."])
            await asyncio.to_thread(_put, rec)
    return _view(rec)


