from .agent_call import agent_call
from .code import (
    code_execute_python,
    code_fetch_code,
    code_fetch_tree,
    code_store_html,
)
from .code_ingest import git_ingest, llms_txt_fetch, package_info
from .ctx import context, ctx_batch, ctx_get
from .ctx_write import context_patch, ctx_create
from .database import db_insert, db_query, db_schema, db_update
from .datasets_tools import (
    usertable_add_rows,
    usertable_create,
    usertable_create_advanced,
    usertable_delete_row,
    usertable_get_all,
    usertable_get_data,
    usertable_get_fields,
    usertable_get_metadata,
    usertable_search_data,
    usertable_update_row,
)
from .filesystem import fs_list, fs_mkdir, fs_patch, fs_read, fs_search, fs_write
from .kind_authoring import (
    kind_add_example,
    kind_create,
    kind_create_content_block,
    kind_create_skill,
    kind_get,
    kind_update_schema,
)
from .kind_component import (
    kindcomp_create_component,
    kindcomp_get_code,
    kindcomp_get_context,
    kindcomp_patch_code,
    kindcomp_resolve_incident,
    kindcomp_update_code,
    kindcomp_update_settings,
)
from .kind_instance import (
    instance_create,
    instance_delete,
    instance_get,
    instance_list,
    instance_update,
)
from .math import math_calculate
from .memory import memory_forget, memory_recall, memory_search, memory_store, memory_update
from .news import news_get_headlines
from .notes import note_create, note_delete, note_get, note_list, note_patch, note_update
from .picklists_tools import (
    userlist_batch_update,
    userlist_create,
    userlist_create_simple,
    userlist_get_all,
    userlist_get_details,
    userlist_update_item,
)
from .questionnaire import interaction_ask
from .seo import (
    seo_check_meta_descriptions,
    seo_check_meta_tags_batch,
    seo_check_meta_titles,
    seo_get_keyword_data,
)
from .shell import shell_execute, shell_python
from .skill import skill
from .tasks import task_create, task_delete, task_get, task_list, task_update
from .text import text_analyze, text_regex_extract
from .tool_component import (
    toolcomp_create_component,
    toolcomp_get_code,
    toolcomp_get_context,
    toolcomp_get_incident_detail,
    toolcomp_get_sample_detail,
    toolcomp_list_tools,
    toolcomp_patch_code,
    toolcomp_resolve_incident,
    toolcomp_update_code,
    toolcomp_update_settings,
)
from .travel import (
    travel_create_summary,
    travel_get_activities,
    travel_get_events,
    travel_get_location,
    travel_get_restaurants,
    travel_get_weather,
)
from .user_secrets_tool import user_secret_set
from .vsc import vsc_get_state
from .web import research_web, web_read, web_search

__all__ = [
    # Agent-as-tool
    "agent_call",
    # Math
    "math_calculate",
    # Text
    "text_analyze",
    "text_regex_extract",
    # Web
    "web_search",
    "web_read",
    # Research
    "research_web",
    # Database
    "db_query",
    "db_insert",
    "db_update",
    "db_schema",
    # Memory
    "memory_store",
    "memory_recall",
    "memory_search",
    "memory_update",
    "memory_forget",
    # Filesystem
    "fs_read",
    "fs_write",
    "fs_list",
    "fs_search",
    "fs_mkdir",
    "fs_patch",
    # Shell
    "shell_execute",
    "shell_python",
    # Browser
    # Picklists (user-owned structured lists)
    "userlist_create",
    "userlist_create_simple",
    "userlist_get_all",
    "userlist_get_details",
    "userlist_update_item",
    "userlist_batch_update",
    # SEO
    "seo_check_meta_titles",
    "seo_check_meta_descriptions",
    "seo_check_meta_tags_batch",
    "seo_get_keyword_data",
    # Code
    "code_store_html",
    "code_fetch_code",
    "code_fetch_tree",
    "code_execute_python",
    # News
    "news_get_headlines",
    # Datasets (user-owned tabular data) — simple variant
    "usertable_create",
    # Datasets — advanced variant
    "usertable_create_advanced",
    "usertable_get_all",
    "usertable_get_metadata",
    "usertable_get_fields",
    "usertable_get_data",
    "usertable_search_data",
    "usertable_add_rows",
    "usertable_update_row",
    "usertable_delete_row",
    # Interaction
    "interaction_ask",
    # Tool Component Agent
    # Kind registry authoring (creator agent) — kinds + examples + skills
    "kind_create",
    "kind_get",
    "kind_update_schema",
    "kind_add_example",
    "kind_create_skill",
    "kind_create_content_block",
    # Kind instances (creator agent + any agent) — saved user data shaped by a kind
    "instance_create",
    "instance_list",
    "instance_get",
    "instance_update",
    "instance_delete",
    # Kind component authoring (creator agent) — the kind-registry sibling of toolcomp_*
    "kindcomp_get_context",
    "kindcomp_create_component",
    "kindcomp_get_code",
    "kindcomp_update_code",
    "kindcomp_patch_code",
    "kindcomp_update_settings",
    "kindcomp_resolve_incident",
    "toolcomp_get_context",
    "toolcomp_get_code",
    "toolcomp_update_code",
    "toolcomp_patch_code",
    "toolcomp_update_settings",
    "toolcomp_get_sample_detail",
    "toolcomp_get_incident_detail",
    "toolcomp_resolve_incident",
    "toolcomp_list_tools",
    "toolcomp_create_component",
    # Travel
    "travel_get_location",
    "travel_get_weather",
    "travel_get_restaurants",
    "travel_get_activities",
    "travel_get_events",
    "travel_create_summary",
    # VSCode IDE state
    "vsc_get_state",
    # Deferred context — unified reader (get|batch|create) + patch
    "context",
    "context_patch",
    "ctx_get",
    "ctx_batch",
    "ctx_create",
    # Skill library — unified (list|get|search)
    "skill",
    # Notes
    "note_get",
    "note_list",
    "note_create",
    "note_update",
    "note_patch",
    "note_delete",
    # Tasks
    "task_get",
    "task_list",
    "task_create",
    "task_update",
    "task_delete",
    # Code & docs ingestion (code_ingest bundle)
    "git_ingest",
    "llms_txt_fetch",
    "package_info",
]
