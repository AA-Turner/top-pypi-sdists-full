"""config route registration (abstract_flask ``register_categories`` convention).

Consolidates the three config route surfaces into ONE blueprint:

  * ``settings.py``     — the console Settings page (boxes, secrets, audit,
                          artifacts, policies) + the box relay (enroll/bundle).
  * ``prompt.py``       — the one-call /prompt dispatch surface.
  * ``envprofiles.py``  — the Environments panel (per-model python envs).

The handlers LIVE in those sibling modules as plain functions (kwargs in, fed by
get_request_datas + prune_inputs; JSON-able out); this module only states the URL
tree and registers it. The registrar wraps the returned data as ``{"result":
...}``. Original custom HTTP statuses (400/403/502/503) collapse to 200
(accepted), and PUT/PATCH/DELETE verbs collapse to GET+POST (accepted).
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.config.envprofiles import (
    env_profiles_approve,
    env_profiles_list,
    env_profiles_save,
    env_profiles_test,
)
from hugpy_core.config.prompt import prompt_execute, prompt_tasks
from hugpy_core.config.settings import (
    boxes_bundle,
    boxes_bundle_version,
    boxes_enroll,
    settings_artifacts,
    settings_audit,
    settings_boxes,
    settings_boxes_enroll_token,
    settings_boxes_revoke,
    settings_policies_get,
    settings_policies_post,
    settings_secrets,
    settings_secrets_delete,
    settings_secrets_grant,
    settings_secrets_revoke,
    settings_secrets_rotate,
    settings_secrets_set,
)

config_bp, logger = get_bp("config_bp", __name__)


ALL_CATEGORIES = {
    "settings": {
        "boxes": {
            "": settings_boxes,                          # /settings/boxes (was GET)
            "enroll-token": settings_boxes_enroll_token, # /settings/boxes/enroll-token
            "revoke": settings_boxes_revoke,             # /settings/boxes/revoke
        },
        "secrets": {
            "": settings_secrets,                # /settings/secrets (was GET)
            "set": settings_secrets_set,         # /settings/secrets/set
            "rotate": settings_secrets_rotate,   # /settings/secrets/rotate
            "grant": settings_secrets_grant,     # /settings/secrets/grant
            "revoke": settings_secrets_revoke,   # /settings/secrets/revoke
            "delete": settings_secrets_delete,   # /settings/secrets/delete
        },
        "audit": settings_audit,                 # /settings/audit            (was GET)
        "artifacts": settings_artifacts,         # /settings/artifacts        (was GET)
        "policies": {
            "": settings_policies_get,           # /settings/policies (was GET)
            "save": settings_policies_post,      # /settings/policies/save (was POST /settings/policies)
        },
    },
    "boxes": {
        "enroll": boxes_enroll,                  # /boxes/enroll
        "bundle": boxes_bundle,                  # /boxes/bundle
        "bundle_version": boxes_bundle_version,  # /boxes/bundle_version
    },
    "prompt": {
        "": spec(prompt_execute, "POST"),        # /prompt: existing Media browser contract
        "execute": prompt_execute,               # /prompt/execute (was POST /prompt)
        "tasks": prompt_tasks,                   # /prompt/tasks
    },
    "llm": {
        "env-profiles": {
            "": env_profiles_list,               # /llm/env-profiles (was GET)
            "save": env_profiles_save,           # /llm/env-profiles/save (was POST /llm/env-profiles)
            "approve": env_profiles_approve,     # /llm/env-profiles/approve (was POST /<name>/approve)
            "test": env_profiles_test,           # /llm/env-profiles/test (was POST /<name>/test)
        },
    },
}
register_categories(config_bp, ALL_CATEGORIES)
