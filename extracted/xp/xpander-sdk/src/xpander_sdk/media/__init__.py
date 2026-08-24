"""The media engine: classify -> plan -> prepare -> deliver, one implementation.

Promoted from modules/tasks/utils/{files,media,model_capabilities}; those paths
remain as verbatim re-export shims because the platform imports them by string
across a version skew. Finer submodule splits land as modules get touched.
"""

from xpander_sdk.media.caps import (  # noqa: F401
    DEFAULT_CAPABILITIES,
    ModelCapabilities,
    get_model_capabilities,
    media_pipeline_disabled,
    resolve_task_capabilities,
)
from xpander_sdk.media.files import (  # noqa: F401
    AttachmentDecision,
    AttachmentPlan,
    categorize_files,
    estimate_sizes,
    extract_document_text,
    extract_documents_text,
    fetch_file,
    fetch_image,
    fetch_urls,
    plan_attachments,
)
from xpander_sdk.media.prepare import (  # noqa: F401
    aprepare_image,
    aprepare_pdf,
    prepare_image,
    prepare_pdf,
)
