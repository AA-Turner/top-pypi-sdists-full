"""
`weights=` shorthand — the model-weights URI, validated at authoring time and expanded to a provisioned
volume mount at deploy time.

WHY validate here (authoring), not at the gateway: the robot engineer has only the SDK and a test key and
cannot see any platform internals (S2 persona). A malformed `hf://` URI or template name must fail while they are
writing the policy — with an error that names the problem — not as an opaque build failure later
.

Weights live on a VOLUME, never baked into the image: this module produces a `VolumeMount`
(the deploy body's `weights` field) whose default mount path is the contract value `/data`.
It never emits an image build step — that separation is what keeps a >10 GB checkpoint out of the image
layers.
"""
from __future__ import annotations

from sequence_base.contract import VolumeMount
from sequence_base.contract.templates import TEMPLATE_SCHEME, parse_template

from seq.errors import PolicyDefinitionError



DEFAULT_WEIGHTS_MOUNT = "/data"


_SUPPORTED_SCHEMES = ("hf://",)


class Weights:
    """Where a policy's weights come from when they are an official template's checkpoint:

        weights=seq.Weights.template("pi05-droid")              # the template's latest published version
        weights=seq.Weights.template("pi05-droid", version=1)   # one version, pinned

    The platform resolves the name (and the version, when none is pinned) at deploy. While the policy's code is that
    template's, unchanged, its machines read the platform's read-only copy of that version - nothing copied, nothing
    billed as storage; with any line of its code changed, the deployment keeps a copy of its own, billed as storage.
    Your own weights are an hf:// repo or a volume you uploaded with `seq volume put`
    (weights=seq.Volume.from_name("my-ckpt")).


"""

    @staticmethod
    def template(name: str, version: int | str | None = None) -> str:
        if version is None:
            uri = f"{TEMPLATE_SCHEME}{name}"
        else:
            n = str(version)
            uri = f"{TEMPLATE_SCHEME}{name}@{n if n.startswith('v') else 'v' + n}"
        return validate_weights_uri(uri)


def validate_weights_uri(uri) -> str:
    """Strictly validate a `weights=` URI, returning it verbatim. Rejects, each with a naming error:
    empty bucket/repo, a single-slash scheme (`gs:/x`), `..` traversal, an `hf://` missing a repo, and any
    unsupported scheme.

    An uploaded volume is accepted as `seq.Volume.from_name("my-ckpt")` or `"vol://my-ckpt[@v<n>]"` — what
    `seq volume put` made; the platform resolves the name under the deploying account."""
    from seq.volume import Volume

    if isinstance(uri, Volume):
        uri = f"vol://{uri.name}"
    if isinstance(uri, str) and uri.startswith(TEMPLATE_SCHEME):
        try:
            parse_template(uri)
        except ValueError as exc:
            raise PolicyDefinitionError(f"weights {exc}") from None
        return uri
    if isinstance(uri, str) and uri.startswith("vol://"):
        from sequence_base.contract.volumes import parse_vol

        try:
            parse_vol(uri)
        except ValueError as exc:
            raise PolicyDefinitionError(f"weights {exc}") from None
        return uri
    if not isinstance(uri, str) or not uri:
        raise PolicyDefinitionError("weights must be seq.Weights.template(...), an hf:// repo or an uploaded "
                                    "seq.Volume (vol://)")
    scheme: str | None = None
    for s in _SUPPORTED_SCHEMES:
        if uri.startswith(s):
            scheme = s
            break

    if scheme is None:

        if uri.startswith("hf:/"):
            raise PolicyDefinitionError(f"weights {uri!r} uses a single-slash scheme; the form is hf://org/repo")
        head = uri.split("://", 1)[0] if "://" in uri else uri.split(":", 1)[0]
        raise PolicyDefinitionError(
            f"weights {uri!r} has unsupported scheme {head!r}; use seq.Weights.template(...), an hf:// repo or an "
            "uploaded seq.Volume (vol://)"
        )


    if ".." in uri:
        raise PolicyDefinitionError(f"weights {uri!r} contains '..' (path traversal)")

    rest = uri[len(scheme):]

    if not rest or rest.startswith("/"):
        raise PolicyDefinitionError(f"weights {uri!r} names an empty repo")

    if scheme == "hf://":

        if not rest.strip("/"):
            raise PolicyDefinitionError(f"weights {uri!r} is missing a repo (expected hf://org/model)")

    return uri


def weights_volume_mount(uri: str, mount: str = DEFAULT_WEIGHTS_MOUNT) -> VolumeMount:
    """Expand a validated `weights=` URI to the deploy body's `weights` `VolumeMount{uri, mount}` — a
    provisioned pull from the URI onto the mount (default `/data`). Distinct from an explicit `volumes=`
    mount, which carries no URI and triggers no pull."""
    return VolumeMount(uri=uri, mount=mount)
