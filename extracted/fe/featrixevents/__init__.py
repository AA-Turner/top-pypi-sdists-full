#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Featrix Events - Post events to the Featrix platform.

This library is write-only: it's for apps to post events onto the platform's
event streams (grouped by event_group_id). It has no read/query APIs -- it
does not list event groups, count events, or fetch history. Querying what's
been posted is a `featrixsphere` concern; if you need that and it doesn't
exist there yet, it needs to be added to featrixsphere, not here.

This directory (src/lib/featrixevents/) IS the single source of truth for
this package. The top-level featrixevents/ (repo root, published to PyPI via
`make publish-featrixclient`) is a set of symlinks into this directory --
NOT a second copy. This exists here rather than at repo root because
src/lib/ is what node-install.sh syncs (wholesale, real files, no symlinks)
to compute nodes as a self-contained tree; a symlink pointing outside
src/lib/ would dangle post-sync, so the real files have to live on this
side. See system_monitor.py's GPUMemoryTracker, which dogfoods this same
client to report training GPU memory telemetry, and job_manager.py's
notify_predictabar_progress(), for the two things every compute node
actually calls.

2026-08 history: this used to be a hand-maintained "vendored copy," kept in
sync with the root package by hand, per-commit, on the honor system. It
silently drifted -- the root package gained a `facts` parameter and a
predictabar_purge() function that this copy never got, which meant every
compute-node call to predictabar_post_event() (which always passes
facts=..., even when it's None) raised a TypeError, silently swallowed by a
broad except-Exception at the call site. See
docs/internal/plans/2026-08-featrixevents-vendored-copy-drift.md. Collapsing
to one real copy (this one) + symlinks makes that class of bug structurally
impossible instead of policed by discipline or a test.

Usage:
    from featrixevents import featrix_post_event

    featrix_post_event(
        auth_key_id="fx_...",
        event_group_id="<uuid>",
        event_payload={"action": "button_click", "page": "/dashboard"}
    )

For fields that recur across many call sites (session/job identifiers,
etc.), subclass FeatrixEventSectionObject once and pass instances instead
of hand-building the same dict everywhere:

    from featrixevents import featrix_post_event, FeatrixEventSectionObject

    class JobSection(FeatrixEventSectionObject):
        def __init__(self, session_id, job_id):
            self.session_id = session_id
            self.job_id = job_id

        def to_event_fields(self) -> dict:
            return {"session_id": self.session_id, "job_id": self.job_id}

    featrix_post_event(
        auth_key_id="fx_...",
        event_group_id="<uuid>",
        event_payload=[JobSection(session_id=sid, job_id=jid), GpuMetricsSection(...)],
    )

PredictaBar (job-progress tracking + ETA) used to live here too
(predictabar_post_event / predictabar_get_status / predictabar_purge) but
moved out to its own standalone package as of 2026-08 -- see
docs/internal/plans/2026-08-predictabar-clients-repo-migration.md. It's not
a Featrix-account concept (a PredictaBar-only customer has no reason to
`pip install` a package literally named "Featrix Events"), so it now lives
at github.com/Featrix/predictabar-clients (`pip install predictabar`):

    from predictabar import post_event, get_status

    post_event(job_id="video-render-123", status="processing",
               percent=45, job_type="video_transcode")
    status = get_status(job_id="video-render-123")

auth_key_id is optional everywhere above -- omit it and it auto-resolves via
_key_resolution.get_api_key() (env var -> ~/.featrix -> /etc/.featrix_key,
the file present on compute nodes running as root).
"""

__version__ = "2.0.13193"
__author__ = "Featrix"
__email__ = "support@featrix.com"
__license__ = "MIT"

from ._post_event import (
    INGEST_PATH, featrix_post_event, featrix_update_event, ingest_body, FeatrixEventError, FeatrixEventSectionObject,
)
from ._key_resolution import get_api_key

__all__ = [
    "featrix_post_event", "featrix_update_event", "ingest_body", "INGEST_PATH", "FeatrixEventError",
    "FeatrixEventSectionObject", "get_api_key",
]
