import json
import os
import re
from enum import Enum
from typing import List, Tuple, Any, Dict, Optional

import yaml
from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.functions.bigconfig_functions import build_fq_name
from bigeye_sdk.generated.com.bigeye.models.generated import MetricConfiguration, MetricCreationState, MetricInfoList
from bigeye_sdk.model.big_config import TagDeployment, RowCreationTimes, BigConfig, ColumnSelector
from bigeye_sdk.model.protobuf_enum_facade import SimpleLookbackType, SimpleAutothresholdSensitivity, \
    SimplePredefinedMetricName, SimpleTimeIntervalType, SimpleAggregationType
from bigeye_sdk.model.protobuf_message_facade import SimpleCollection, SimpleMetricDefinition, BucketSize

log = get_logger(__name__)

_TAUTO_RE = re.compile(r"^\s*(\d+)\s*=\s*\1\s*$")

time_interval_mapping = {
    "HOURS_TIME_INTERVAL_TYPE": SimpleTimeIntervalType.HOURS,
    "DAYS_TIME_INTERVAL_TYPE": SimpleTimeIntervalType.DAYS,
    "MINUTES_TIME_INTERVAL_TYPE": SimpleTimeIntervalType.MINUTES,
    "MONTHS_TIME_INTERVAL_TYPE": SimpleTimeIntervalType.MONTHS,
}

lookback_type_mapping = {
    "DATA_TIME_LOOKBACK_TYPE": SimpleLookbackType.DATA_TIME,
    "METRIC_TIME_LOOKBACK_TYPE": SimpleLookbackType.METRIC_TIME,
}

threshold_mapping = {
    "AUTOTHRESHOLD_SENSITIVITY_NARROW": SimpleAutothresholdSensitivity.NARROW,
    "AUTOTHRESHOLD_SENSITIVITY_MEDIUM": SimpleAutothresholdSensitivity.MEDIUM,
    "AUTOTHRESHOLD_SENSITIVITY_WIDE": SimpleAutothresholdSensitivity.WIDE,
    "AUTOTHRESHOLD_SENSITIVITY_XWIDE": SimpleAutothresholdSensitivity.XWIDE
}

aggregation_type_mapping = {
    "PERCENT_AGGREGATION_TYPE": SimpleAggregationType.PERCENT,
    "COUNT_AGGREGATION_TYPE": SimpleAggregationType.COUNT,
    "MIN_AGGREGATION_TYPE": SimpleAggregationType.MIN,
    "MAX_AGGREGATION_TYPE": SimpleAggregationType.MAX,
    "AVG_AGGREGATION_TYPE": SimpleAggregationType.AVG,
    "SUM_AGGREGATION_TYPE": SimpleAggregationType.SUM
}

DEFAULT_UPPER_ONLY_METRICS = {
    SimplePredefinedMetricName.FRESHNESS,
    SimplePredefinedMetricName.FRESHNESS_DATA,
    SimplePredefinedMetricName.HOURS_SINCE_MAX_TIMESTAMP,
    SimplePredefinedMetricName.HOURS_SINCE_MAX_DATE,
}

LIST_VALUE_PREDEFINED = {SimplePredefinedMetricName.COUNT_VALUE_IN_LIST,
                         SimplePredefinedMetricName.PERCENT_VALUE_IN_LIST}


# --------------------- general helpers ---------------------
def get_all_predefined_metric_names() -> list:
    return [m.value for m in SimplePredefinedMetricName if m.value != "UNDEFINED"]


def make_predefined_smd(name: str) -> dict:
    return {
        "saved_metric_id": sanitize_id(name.lower()),
        "metric_type": {"predefined_metric": name},
    }


def make_template_smd(template_name: str, aggregation_type: str = None) -> dict:
    sid = sanitize_id(f"template_{template_name.lower()}_{aggregation_type.lower()}")
    smd = {
        "saved_metric_id": sid,
        "metric_type": {
            "type": "TEMPLATE",
            "template_name": template_name,
            "aggregation_type": aggregation_type,
        },
    }
    return smd


def sanitize_id(s: str) -> str:
    s = s.lower()
    s = re.sub(r'[^a-z0-9_]+', '_', s)
    return s.strip('_') or "id"


def get_api_metric_name(cfg: Dict[str, Any]) -> str:
    return (cfg.get("metricType") or {}).get("predefinedMetric", {}).get("metricName", "") or ""


def is_table_metric(cfg: Dict[str, Any]) -> bool:
    if cfg.get("isTableMetric") is not None:
        return bool(cfg["isTableMetric"])
    return bool((cfg.get("metricType") or {}).get("isTableMetric"))


def is_predefined_metric(cfg: dict) -> bool:
    return bool((cfg.get("metricType") or {}).get("predefinedMetric"))


def is_template_metric(cfg: dict) -> bool:
    return bool((cfg.get("metricType") or {}).get("templateMetric"))


def _norm_agg(agg: Optional[str]) -> Optional[str]:
    if not agg:
        return None
    s = str(agg).upper()
    return aggregation_type_mapping[s]


def is_not_freshness_volume(cfg: dict) -> bool:
    """
    Freshness and Volume (non-data variants) cannot accept rct_overrides or lookbacks.
    Freshness (data) / Volume (data) can.
    Applies only to predefined metrics; templates are allowed.
    """
    # Disallow ONLY the non-data variants
    return get_api_metric_name(cfg) not in {SimplePredefinedMetricName.FRESHNESS,
                                            SimplePredefinedMetricName.VOLUME}


def is_value_in_list(cfg: dict) -> bool:
    return get_api_metric_name(cfg) in LIST_VALUE_PREDEFINED


def is_default_metric_lookback(lb_block: Optional[dict], data_time_window_default: bool) -> bool:
    """
    Suppress metric-level lookback if it matches the workspace default:
      - If data_time_window_default == True:
          default = METRIC_TIME + lookback_window: { interval_type: DAYS, interval_value: -1 }
      - If data_time_window_default == False:
          default = DATA_TIME   + lookback_window: { interval_type: DAYS, interval_value:  2 }

    Expects the normalized shape from lookback_from_config():
      {'lookback': {'lookback_window': {'interval_type': 'DAYS', 'interval_value': N},
                    'lookback_type': 'METRIC_TIME'|'DATA_TIME'}}
    """
    if not lb_block:
        return True  # nothing provided -> default applies

    if "bucket_size" in lb_block:
        return False

    w = lb_block.get("lookback_window", {})
    lt = lb_block.get("lookback_type", "").upper()
    it = w.get("interval_type", "").upper()
    iv = w.get("interval_value")

    if data_time_window_default:
        return lt == SimpleLookbackType.METRIC_TIME and it == SimpleTimeIntervalType.DAYS and iv == 2
    else:
        return lt == SimpleLookbackType.DATA_TIME and it == SimpleTimeIntervalType.DAYS and iv == 2


def is_default_metric_schedule(ms: Optional[dict]) -> bool:
    """
    Default is 24 hours. Return True if the built block equals that default.
    Any named_schedule is NOT default.
    """
    if not ms:
        return True  # nothing provided -> default
    named = ms.get("metric_schedule", {}).get("named_schedule")
    if named:
        return False  # explicit named schedule is never default
    sf = ms.get("metric_schedule", {}).get("schedule_frequency") or {}
    return sf.get("interval_type") == "HOURS" and sf.get("interval_value") == 24


def is_default_threshold(th_block: Optional[dict], cfg: dict) -> bool:
    """
    Default thresholds to suppress from YAML:
      - Most metrics: AUTO + MEDIUM sensitivity, both sides (no *_only flags)
      - Freshness-like metrics (listed in DEFAULT_UPPER_ONLY_METRICS):
          AUTO + MEDIUM sensitivity + upper_bound_only
    """
    if not th_block:
        return True  # no threshold emitted -> default applies

    t = th_block.get("threshold") or {}
    if (t.get("type") or "").upper() != "AUTO":
        return False

    # Sensitivity: treat missing as MEDIUM (SDK default)
    sensitivity = (t.get("sensitivity") or "MEDIUM").upper()
    if sensitivity != "MEDIUM":
        return False

    name = get_api_metric_name(cfg)

    if name in DEFAULT_UPPER_ONLY_METRICS:
        # Default = upper_bound_only; must NOT have lower_only or extra fields
        if t.get("lower_bound_only"):
            return False
        # explicit upper_bound_only True is default; also accept missing (if caller
        # didn't set flags) only if you want to consider that non-default—most setups
        # will set the flag, but we’ll require it True here:
        if not t.get("upper_bound_only"):
            return False
        extra = set(t.keys()) - {"type", "sensitivity", "upper_bound_only"}
        return not extra

    # Generic default: both sides (no *_only flags)
    if t.get("upper_bound_only") or t.get("lower_bound_only"):
        return False
    extra = set(t.keys()) - {"type", "sensitivity"}
    return not extra


def metric_identity(cfg: dict) -> tuple[Optional[str], Optional[str], Optional[str], Optional[dict]]:
    """
    Returns (kind, key, saved_metric_id, metric_type_block) or (None, None, None, None)
    kind: 'predefined' | 'template'
    key:  API name for predefined OR templateId string for template
    saved_metric_id: stable id to reference in deployments
    metric_type_block: what goes under saved_metric_definitions.metrics[].metric_type
    """
    mt = cfg.get("metricType") or {}
    if mt.get("predefinedMetric"):
        api = mt["predefinedMetric"].get("metricName")
        if not api:
            return None, None, None, None
        saved_id = sanitize_id(api.lower())
        return "predefined", api, saved_id, {"predefined_metric": api}

    if mt.get("templateMetric"):
        tm = mt["templateMetric"]
        tid = tm.get("templateId")
        if tid is None:
            return None, None, None, None
        agg = _norm_agg(tm.get("aggregationType"))
        templates_name = tm.get("templateName")
        saved_id = sanitize_id(f"template_{templates_name}_{agg.lower()}")
        metric_type = {"type": "TEMPLATE", "template_name": templates_name, "aggregation_type": agg}
        return "template", str(tid), saved_id, metric_type

    return None, None, None, None


def extract_location(meta: Dict[str, Any]) -> Tuple[str, str, str]:
    # Expecting: warehouseName, schemaName (can be db.schema for Snowflake), datasetName (table)
    wh = (meta.get("warehouseName") or "").strip()
    schema = (meta.get("schemaName") or "").strip()
    table = (meta.get("datasetName") or "").strip()
    return wh, schema, table


def infer_column_for_column_metric(meta: Dict[str, Any], cfg: Dict[str, Any]) -> str:
    col = meta.get("fieldName")
    if col:
        return str(col)
    for p in cfg.get("parameters", []) or []:
        if p.get("columnName"):
            return str(p["columnName"])
    return ""  # fallback to "*"


def metric_schedule_from_config(cfg: dict) -> dict:
    """
    Build YAML:
      metric_schedule:
        named_schedule: { name: ... }
      OR
      metric_schedule:
        schedule_frequency: { interval_type, interval_value }
    Only reads cfg['metricSchedule'].
    """
    ms = cfg.get("metricSchedule") or {}

    # Named schedule wins if present
    named = (ms.get("namedSchedule") or {}).get("name")
    if named:
        return {"metric_schedule": {"named_schedule": {"name": str(named)}}}

    sf = ms.get("scheduleFrequency") or {}
    itype = sf.get("intervalType")
    ival = sf.get("intervalValue")
    if itype and ival is not None:
        return {
            "metric_schedule": {
                "schedule_frequency": {
                    "interval_type": time_interval_mapping.get(itype, itype),
                    "interval_value": ival
                }
            }
        }

    return {}


def lookback_from_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    lb = cfg.get("lookback") or {}
    if not lb:
        return {}
    window = {
        "interval_type": time_interval_mapping.get(lb.get("intervalType"), lb.get("intervalType")),
        "interval_value": lb.get("intervalValue"),
    }

    raw_lt = cfg.get("lookbackType")
    lt = lookback_type_mapping.get(raw_lt)

    out = {"lookback_window": window, "lookback_type": lt}
    grain = cfg.get("grainSeconds")
    if lt == SimpleLookbackType.METRIC_TIME and grain == BucketSize.HOUR.to_seconds():
        out["bucket_size"] = BucketSize.HOUR

    return out


def parameters_from_config(cfg: dict) -> list[dict]:
    """
    For template metrics ONLY, emit:
      parameters:
        - key: <k>
          string_value|numeric_value|boolean_value|column_name: <v>
    For predefined metrics: return [].
    """
    if not is_template_metric(cfg):
        return []

    out: list[dict] = []
    for p in (cfg.get("parameters") or []):
        k = p.get("key")
        if not k:
            continue

        # Pick the typed value (in priority order), mapping to snake_case keys
        if "columnName" in p and p["columnName"]:
            out.append({"key": k, "column_name": p["columnName"]})
            continue
        if "stringValue" in p and p["stringValue"] is not None:
            out.append({"key": k, "string_value": p["stringValue"]})
            continue
        if "numericValue" in p and p["numericValue"] is not None:
            out.append({"key": k, "numeric_value": p["numericValue"]})
            continue
        if "booleanValue" in p and p["booleanValue"] is not None:
            out.append({"key": k, "boolean_value": bool(p["booleanValue"])})
            continue

        # Fallback (rare API shapes)
        if "value" in p and p["value"] is not None:
            # best-effort typing for 'value'
            v = p["value"]
            typed_key = (
                "numeric_value" if isinstance(v, (int, float)) else
                "boolean_value" if isinstance(v, bool) else
                "string_value"
            )
            out.append({"key": k, typed_key: v})

    return out


def predefined_parameters_for_value_in_list(cfg: dict) -> list[dict]:
    """
    For COUNT_VALUE_IN_LIST / PERCENT_VALUE_IN_LIST, emit only:
      parameters:
        - key: list
          string_value: "A,B,C"
    Ignore arg1/columnName (handled by column_selector).
    For all other predefined metrics: return [].
    """
    out: list[dict] = []
    for p in (cfg.get("parameters") or []):
        if p.get("key") != "list":
            continue
        # Only stringValue is expected for 'list'
        sv = p.get("stringValue")
        if sv is not None:
            out.append({"key": "list", "string_value": sv})
        # If other types ever appear, you could add fallbacks here.
    return out


def filters_from_config(cfg: Dict[str, Any]) -> List[str]:
    raw = cfg.get("filters") or []
    return [f for f in raw if str(f).strip() != "1=1"]


def group_by_from_config(cfg: dict) -> dict:
    """
    Convert metricConfiguration.groupBys into bigConfig's:
      group_by:
        - <column>
        - <column>
    Accepts either a list of strings or a list of objects with column-like keys.
    """
    raw = cfg.get("groupBys") or []
    cols: list[str] = []
    for item in raw:
        if isinstance(item, str):
            name = item.strip()
        else:
            name = ""

        if name:
            cols.append(name)

    return {"group_by": cols} if cols else {}


def notification_channels_from_config(cfg: dict) -> list[dict]:
    """
    API: metricConfiguration.notificationChannels -> YAML: notification_channels
      - {"email": "test@bigeye.com"} ->
          {"email": "test@bigeye.com"}
      - {"slackChannelInfo": {"channelName": "#chan"}} ->
          {"slack": "#chan"}    # prefer channelName; fallback to channelId
      - {"webhook": {"webhookUrl": "https://...", "webhookHeaders":[{"key":"a","value":"b"}, ...]}}
          -> if headers present: one entry per header pair:
               {"webhook": "https://...", "webhook_header_key": "a", "webhook_header_value": "b"}
             else:
               {"webhook": "https://..."}
    """
    out: list[dict] = []
    for nc in (cfg.get("notificationChannels") or []):
        if not isinstance(nc, dict):
            continue

        # email
        if "email" in nc and nc["email"]:
            out.append({"email": str(nc["email"])})
            continue

        # slack
        sci = nc.get("slackChannelInfo")
        if isinstance(sci, dict):
            name = sci.get("channelName")
            chan = name or sci.get("channelId")
            if chan:
                out.append({"slack": str(chan)})
            continue

        # webhook
        wh = nc.get("webhook")
        if isinstance(wh, dict):
            url = wh.get("webhookUrl")
            headers = wh.get("webhookHeaders") or []
            if url:
                if headers:
                    # emit one YAML entry per header pair
                    for h in headers:
                        k = h.get("key")
                        v = h.get("value")
                        if k is None or v is None:
                            continue
                        out.append({
                            "webhook": str(url),
                            "webhook_header_key": str(k),
                            "webhook_header_value": str(v),
                        })
                else:
                    out.append({"webhook": str(url)})
            continue

    return out


def threshold_from_config(cfg: dict) -> dict:
    """
    Convert metricConfiguration.thresholds (API list) → ONE bigConfig 'threshold' object.

    Rules:
    - If no thresholds → return {} (omit from YAML).
    - If only empty dicts → returns {'threshold': {'type': 'NONE'}}.
    - If multiple entries of the SAME kind (e.g., two CONSTANT bounds) → combine (upper+lower, etc.).
    - If MORE THAN ONE kind is present (AUTO + CONSTANT, etc.) → raise ThresholdConflict.

    Supported kinds (exclusive): AUTO, CONSTANT, STDDEV, RELATIVE, FRESHNESS, NONE
    """
    items = cfg.get("thresholds", [])
    if not items:
        return {"threshold": {"type": "NONE"}}

    kinds_found = set()
    # Accumulators per kind
    auto = {"type": "AUTO", "sensitivity": None, "want_upper": False, "want_lower": False}
    constant = {"type": "CONSTANT", "upper_bound": None, "lower_bound": None}
    stddev = {"type": "STDDEV", "upper_bound": None, "lower_bound": None, "lookback": None}
    relative = {"type": "RELATIVE", "upper_bound": None, "lower_bound": None, "lookback": None}
    freshness = {"type": "FRESHNESS", "schedule": None, "delay_at_update": None}

    def _add_kind(k):
        if k:
            kinds_found.add(k)

    def _apply_bound(store: dict, bound: dict):
        if not isinstance(bound, dict):
            return
        btype = str(bound.get("boundType", "")).upper()
        val = bound.get("value")
        if val is None:
            return
        if btype.startswith("LOWER_"):
            store["lower_bound"] = val
        else:
            store["upper_bound"] = val

    def _simple_lb(lb_obj):
        if not isinstance(lb_obj, dict):
            return None
        it, iv = lb_obj.get("intervalType"), lb_obj.get("intervalValue")
        if it is None and iv is None:
            return None
        return {"interval_type": time_interval_mapping.get(it, it) if it else None,
                "interval_value": iv}

    # -------- scan (accumulate; no returns here) --------
    for t in items:
        if not isinstance(t, dict):
            continue

        if "autoThreshold" in t and isinstance(t["autoThreshold"], dict):
            at = t["autoThreshold"]
            _add_kind("AUTO")
            # sensitivity: AUTOTHRESHOLD_SENSITIVITY_WIDE -> WIDE
            sens = at.get("sensitivity")
            if sens:
                s = str(sens).upper()
                if "AUTOTHRESHOLD_SENSITIVITY_" in s:
                    s = s.split("AUTOTHRESHOLD_SENSITIVITY_")[-1]
                auto["sensitivity"] = s
            # side flags from boundType
            btype = str((at.get("bound") or {}).get("boundType", "")).upper()
            if btype.startswith("UPPER_"):
                auto["want_upper"] = True
            if btype.startswith("LOWER_"):
                auto["want_lower"] = True
            continue

        if "constantThreshold" in t and isinstance(t["constantThreshold"], dict):
            ct = t["constantThreshold"]
            _add_kind("CONSTANT")
            _apply_bound(constant, ct.get("bound"))
            continue

        if "standardDeviationThreshold" in t and isinstance(t["standardDeviationThreshold"], dict):
            sd = t["standardDeviationThreshold"]
            _add_kind("STDDEV")
            stddev["lookback"] = _simple_lb(sd.get("lookback")) or stddev["lookback"]
            _apply_bound(stddev, sd.get("bound"))
            continue

        if "relativeThreshold" in t and isinstance(t["relativeThreshold"], dict):
            rt = t["relativeThreshold"]
            _add_kind("RELATIVE")
            relative["lookback"] = _simple_lb(rt.get("lookback")) or relative["lookback"]
            _apply_bound(relative, rt.get("bound"))
            continue

        if "freshnessScheduleThreshold" in t and isinstance(t["freshnessScheduleThreshold"], dict):
            fr = t["freshnessScheduleThreshold"]
            _add_kind("FRESHNESS")
            cron, tz = fr.get("cron"), fr.get("timezone")
            freshness.update({k: v for k, v in (("cron", cron), ("timezone", tz)) if v})
            freshness["delay_at_update"] = _simple_lb(fr.get("delayAtUpdate")) or freshness["delay_at_update"]
            continue

    kind = next(iter(kinds_found), None)

    # -------- build single threshold object for that kind --------
    if kind == "AUTO":
        out = {"type": "AUTO"}
        if auto["sensitivity"]:
            out["sensitivity"] = auto["sensitivity"]
        # set *_only flags if exactly one side requested
        if auto["want_upper"] and not auto["want_lower"]:
            out["upper_bound_only"] = True
        if auto["want_lower"] and not auto["want_upper"]:
            out["lower_bound_only"] = True
        return {"threshold": out}

    if kind == "CONSTANT":
        out = {"type": "CONSTANT"}
        if constant["upper_bound"] is not None:
            out["upper_bound"] = constant["upper_bound"]
        if constant["lower_bound"] is not None:
            out["lower_bound"] = constant["lower_bound"]
        return {"threshold": out}

    if kind == "STDDEV":
        out = {"type": "STDDEV"}
        if stddev["lookback"]:
            out["lookback"] = stddev["lookback"]
        if stddev["upper_bound"] is not None:
            out["upper_bound"] = stddev["upper_bound"]
        if stddev["lower_bound"] is not None:
            out["lower_bound"] = stddev["lower_bound"]
        return {"threshold": out}

    if kind == "RELATIVE":
        out = {"type": "RELATIVE"}
        if relative["lookback"]:
            out["lookback"] = relative["lookback"]
        if relative["upper_bound"] is not None:
            out["upper_bound"] = relative["upper_bound"]
        if relative["lower_bound"] is not None:
            out["lower_bound"] = relative["lower_bound"]
        return {"threshold": out}

    if kind == "FRESHNESS":
        out = {"type": "FRESHNESS", "cron": freshness["cron"], "timezone": freshness["timezone"]}
        if freshness["delay_at_update"]:
            out["delay_at_update"] = freshness["delay_at_update"]
        return {"threshold": out}

    # Fallback (shouldn't happen)
    return {}


# --------------------- tag build functions ---------------------


def _norm_for_signature(metric_entry: dict) -> dict:
    """
        Remove 'saved_metric_id' and return only the override-relevant fields
        (what you already emit after default suppression).
    """
    keep = ("metric_schedule", "lookback", "parameters", "filters", "group_by", "threshold")
    return {k: metric_entry[k] for k in keep if k in metric_entry}


def _entry_is_for(saved_id: str, entry: dict) -> bool:
    return entry.get("saved_metric_id") == saved_id


def _json_sig(d: dict) -> str:
    # Stable signature to compare equality across tables
    return json.dumps(d, sort_keys=True, separators=(",", ":"))


def _uniqueness_signature(entry: dict) -> str:
    """
    Bigeye considers metrics 'same' unless any of these differ:
      - conditions  (our YAML override for API 'filters')
      - group_by
      - rct_overrides
      - lookback
    Thresholds/names/schedule/etc are ignored for uniqueness.
    Return a stable JSON string for easy comparison.
    """
    sig = {
        "conditions": entry.get("conditions", []),
        "group_by": entry.get("group_by", []),
        "rct_overrides": entry.get("rct_override", []),
        "lookback": entry.get("lookback", []),
    }
    return json.dumps(sig, sort_keys=True, separators=(",", ":"))


def _next_tautology(exclude: set[str]) -> str:
    """
    Return a simple always-true SQL predicate not in 'exclude'.
    Generates '1=1', '2=2', '3=3', ...
    """
    i = 1
    while True:
        cand = f"{i}={i}"
        if cand not in exclude:
            return cand
        i += 1


def _strip_tautologies(conds: list[str]) -> list[str]:
    return [c for c in conds if not _TAUTO_RE.match(str(c))]


def _enforce_saved_id_uniqueness(deployments: list[dict]) -> None:
    """
    For entries with the same saved_metric_id and identical compare-fields
    (conditions, group_by, rct_overrides.column, lookback):
      - Keep the first (original) as-is (strip any existing tautologies, keep real conditions)
      - For each subsequent duplicate #k (k starts at 1), ensure conditions end with exactly one tautology: "{k}={k}"
    """
    for dep in deployments:
        metrics = dep.get("metrics") or []
        # Group by saved_metric_id
        by_saved = {}
        for idx, m in enumerate(metrics):
            sid = m.get("saved_metric_id")
            if sid:
                by_saved.setdefault(sid, []).append((idx, m))

        for sid, items in by_saved.items():
            if len(items) < 2:
                continue

            # Group by Bigeye "sameness" signature
            sig_groups = {}
            for idx, m in items:
                sig = _uniqueness_signature(m)
                sig_groups.setdefault(sig, []).append((idx, m))

            for _, dup_list in sig_groups.items():
                if len(dup_list) < 2:
                    continue
                # Stable order of appearance
                dup_list.sort(key=lambda t: t[0])

                # ----- Original (first) -----
                orig_idx, orig = dup_list[0]
                orig_real = _strip_tautologies(
                    [str(x).strip() for x in (orig.get("conditions") or []) if str(x).strip()])
                if orig_real:
                    orig["conditions"] = orig_real
                else:
                    # remove empty list entirely
                    if "conditions" in orig:
                        del orig["conditions"]

                # Duplicates: assign exactly one tautology by duplicate count (1...N-1)
                for k, (_i, m) in enumerate(dup_list[1:], start=1):
                    real = _strip_tautologies([str(x).strip() for x in (m.get("conditions") or []) if str(x).strip()])
                    m["conditions"] = real + [f"{k}={k}"]


def selector_name_for(mi: Dict[str, Any]) -> str:
    cfg = mi.get("metricConfiguration", {}) or {}
    meta = mi.get("metricMetadata", {}) or {}
    wh, schema, table = extract_location(meta)
    if not (wh and schema and table):
        return ""  # invalid; will be skipped
    col = "*" if is_table_metric(cfg) else (infer_column_for_column_metric(meta, cfg) or "*")
    return f"{wh}.{schema}.{table}.{('*' if col == '*' else col)}"


class MetricController:
    infos_to_convert: List[dict] = []
    existing_saved_metric_defs: List[dict] = []
    predefined_metrics: List[dict] = []
    saved_metric_def_path: str

    def __init__(self, client: DatawatchClient, saved_metric_definitions_path: str = "saved_metric_definitions.yaml"):
        self.client = client
        self.predefined_metrics = [make_predefined_smd(name) for name in get_all_predefined_metric_names()]
        self.saved_metric_def_path = os.path.abspath(saved_metric_definitions_path)

    @staticmethod
    def delete_metrics(metrics: List[MetricConfiguration]):
        deleatable = [m for m in metrics if m.metric_creation_state != MetricCreationState.METRIC_CREATION_STATE_SUITE]

    def metric_info_to_bigconfig(self,
                                 metric_info: MetricInfoList,
                                 collection: SimpleCollection = None) -> BigConfig:
        # Loop through metrics and create list of tag deployments / row creation times
        tag_deployments: List[TagDeployment] = []
        rct_columns: List[ColumnSelector] = []
        for m in metric_info.metrics:
            meta = m.metric_metadata

            # Get the fully qualified column selector for each metric
            if m.metric_configuration.is_table_metric:
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, "*")
            elif m.metric_configuration.metric_type.template_metric.template_id != 0:
                column_name = next((p.column_name for p in m.metric_configuration.parameters if p.column_name), None)
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, column_name)
            else:
                fq_selector = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name, meta.field_name)
            tag_deployments.append(TagDeployment(
                column_selectors=[ColumnSelector(name=fq_selector)],
                metrics=[SimpleMetricDefinition.from_datawatch_object(m.metric_configuration)])
            )

            # Get the row creation time column
            if meta.dataset_time_column_name and meta.dataset_time_column_name not in ['Collected time', '']:
                rct_column = build_fq_name(meta.warehouse_name, meta.schema_name, meta.dataset_name,
                                           meta.dataset_time_column_name)
                rct_columns.append(ColumnSelector(name=rct_column))

        row_creation_times = RowCreationTimes(column_selectors=list(set(rct_columns)))

        dtw_is_default: bool = [ac.boolean_value for ac in self.client.get_advanced_configs()
                                if ac.key == "metric.data_time_window.default"][0]

        return BigConfig.tag_deployments_to_bigconfig(tag_deployments=tag_deployments,
                                                      row_creation_times=row_creation_times,
                                                      collection=collection,
                                                      dtw_is_default=dtw_is_default)

    # --------------------- Saved Metric Definition helpers ---------------------

    def collect_template_smds_from_inputs(self) -> list[dict]:
        seen = set()
        out = []
        for mi in self.infos_to_convert:
            cfg = mi.get("metricConfiguration", {}) or {}
            mt = (cfg.get("metricType") or {}).get("templateMetric")
            if not mt:
                continue
            tid = mt.get("templateId")
            if tid is None:
                continue
            agg = _norm_agg(mt.get("aggregationType"))  # you already added _norm_agg earlier
            template_name = mt.get("templateName")
            smd = make_template_smd(template_name, agg)
            sid = smd["saved_metric_id"]
            if sid in seen:
                continue
            seen.add(sid)
            out.append(smd)
        return out

    def _load_existing_smd_lib(self) -> Optional[List[dict]]:
        """
        Return existing saved_metric_definitions.metrics list or [] if file missing/empty.
        """
        if not self.saved_metric_def_path or not os.path.exists(self.saved_metric_def_path):
            return []
        with open(self.saved_metric_def_path, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f) or {}
            except Exception:
                return []
        smd = (((data or {}).get("saved_metric_definitions") or {}).get("metrics")) or []
        return [x for x in smd if isinstance(x, dict)]

    def _merge_smds(self, new_items: list[dict]) -> list[dict]:
        """
        Union by saved_metric_id, prefer existing on key conflicts (no destructive updates).
        """
        new_and_existing_metrics = new_items + self.predefined_metrics
        by_id = {e.get("saved_metric_id"): e for e in self.existing_saved_metric_defs if e.get("saved_metric_id")}
        for n in new_and_existing_metrics:
            sid = n.get("saved_metric_id")
            if not sid:
                continue
            if sid not in by_id:
                by_id[sid] = n

        # stable order: predefined first alphabetically, then templates by id
        def _sort_key(item):
            mt = item.get("metric_type", {})
            if "predefined_metric" in mt:
                return 0, item["saved_metric_id"]
            return 1, item["saved_metric_id"]

        return sorted(by_id.values(), key=_sort_key)

    def write_or_update_smd_library(self, template_smds_from_inputs: list[dict], auto_apply: bool) -> None:
        """
        Update (or create) an SMD library bigConfig file:
          type: BIGCONFIG_FILE
          saved_metric_definitions:
            metrics: [ all predefined + templates from inputs (+ existing) ]
        Never deletes existing entries.
        """
        self.existing_saved_metric_defs = self._load_existing_smd_lib()

        # Merge existing + predefined + new templates
        merged = self._merge_smds(template_smds_from_inputs)

        doc = {
            "type": "BIGCONFIG_FILE",
            **({"auto_apply_on_indexing": True} if auto_apply else {}),
            "saved_metric_definitions": {"metrics": merged},
        }
        with open(self.saved_metric_def_path, "w", encoding="utf-8") as f:
            yaml.SafeDumper.add_multi_representer(Enum, yaml.representer.SafeRepresenter.represent_str)
            yaml.safe_dump(doc, f, sort_keys=False)

    # --------------------- core build functions ---------------------

    def build_saved_metric_definitions(self) -> List[Dict[str, Any]]:
        seen_ids: set[str] = set()
        out: list[dict] = []
        for mi in self.infos_to_convert:
            cfg = mi.get("metricConfiguration", {}) or {}
            kind, key, saved_id, metric_type = metric_identity(cfg)
            if not saved_id or not metric_type:
                continue
            if saved_id in seen_ids:
                continue
            seen_ids.add(saved_id)
            out.append({
                "saved_metric_id": saved_id,
                "metric_type": metric_type,
            })
        return out

    def build_tag_deployments(self, data_time_window_default: bool):

        # Group metrics by selector_name
        groups: Dict[str, List[Dict[str, Any]]] = {}

        for mi in self.infos_to_convert:
            cfg = mi.get("metricConfiguration", {}) or {}
            meta = mi.get("metricMetadata", {}) or {}

            selector = selector_name_for(mi)
            if not selector:
                continue

            # saved metric id (predefined OR template)
            kind, key, saved_id, _ = metric_identity(cfg)
            if not saved_id:
                continue

            # Build metric entry
            entry: Dict[str, Any] = {"saved_metric_id": saved_id}

            # ----- metric_name / description overrides -----
            cfg_name = (cfg.get("name") or "").strip()
            meta_full = (meta.get("statisticFullName") or "").strip()

            # Emit metric_name ONLY if it differs from the statisticFullName
            if cfg_name and cfg_name != meta_full:
                entry["metric_name"] = cfg_name

            # Emit description ONLY if non-empty
            cfg_desc = (cfg.get("description") or "").strip()
            if cfg_desc:
                entry["description"] = cfg_desc

            rct = cfg.get("rctOverride")  # or meta.get("datasetTimeColumnName")
            if rct and is_not_freshness_volume(cfg):
                entry["rct_overrides"] = [rct]

            ms = metric_schedule_from_config(cfg)
            if ms and not is_default_metric_schedule(ms):
                entry.update(ms)

            thr = threshold_from_config(cfg)
            if thr and not is_default_threshold(thr, cfg):
                entry.update(thr)

            lb = lookback_from_config(cfg)
            if lb and is_not_freshness_volume(cfg) and not is_default_metric_lookback(lb, data_time_window_default):
                entry["lookback"] = lb

            if is_template_metric(cfg):
                params = parameters_from_config(cfg)
                if params:
                    entry["parameters"] = params

            if is_value_in_list(cfg):
                list_params = predefined_parameters_for_value_in_list(cfg)
                if list_params:
                    entry["parameters"] = list_params

            flt = filters_from_config(cfg)
            if flt:
                entry["conditions"] = flt

            # group_by
            gb = group_by_from_config(cfg)
            if gb:
                entry.update(gb)

            ncs = notification_channels_from_config(cfg)
            if ncs:
                entry["notification_channels"] = ncs

            groups.setdefault(selector, []).append(entry)

        if not groups:
            return []

        # Emit one section with deployments; each deployment has column_selectors + metrics
        deployments = [{"column_selectors": [{"name": selector}], "metrics": metrics}
                       for selector, metrics in groups.items()]

        # 1) Collect selectors that have BOTH non-data Freshness and Volume
        fresh_saved_id = SimplePredefinedMetricName.FRESHNESS.lower()  # from your saved_metric_definitions convention
        vol_saved_id = SimplePredefinedMetricName.VOLUME.lower()

        selector_to_fv_overrides: dict[str, tuple[dict, dict]] = {}  # selector -> (fresh_norm, vol_norm)
        selector_deployments_idx: dict[str, int] = {}  # selector -> index in deployments list

        for di, dep in enumerate(deployments):
            # each dep has exactly one selector per your builder
            selectors = dep.get("column_selectors") or []
            if not selectors:
                continue
            selector_name = selectors[0].get("name")
            if not selector_name:
                continue

            ms = dep.get("metrics") or []
            f_entry = next((m for m in ms if _entry_is_for(fresh_saved_id, m)), None)
            v_entry = next((m for m in ms if _entry_is_for(vol_saved_id, m)), None)

            # Only consider non-data predefined variants: your pipeline already uses saved_metric_id keys
            if f_entry and v_entry:
                # Normalize to override-only dicts
                f_norm = _norm_for_signature(f_entry)
                v_norm = _norm_for_signature(v_entry)
                selector_to_fv_overrides[selector_name] = (f_norm, v_norm)
                selector_deployments_idx[selector_name] = di

        # 2) If fewer than 2 selectors match, skip grouping (nothing to do)
        if len(selector_to_fv_overrides) >= 2:
            # 3) Check that ALL Freshness overrides are identical across selectors,
            #    and ALL Volume overrides are identical across selectors
            f_sigs = {_json_sig(pair[0]) for pair in selector_to_fv_overrides.values()}
            v_sigs = {_json_sig(pair[1]) for pair in selector_to_fv_overrides.values()}

            if len(f_sigs) == 1 and len(v_sigs) == 1:
                # 4) They match across tables → build a single tag deployment
                common_f = next(iter(selector_to_fv_overrides.values()))[0]
                common_v = next(iter(selector_to_fv_overrides.values()))[1]

                # (a) Remove the per-selector FRESHNESS and VOLUME entries
                for selector_name, di in selector_deployments_idx.items():
                    ms = deployments[di]["metrics"]
                    deployments[di]["metrics"] = [
                        m for m in ms
                        if not (_entry_is_for(fresh_saved_id, m) or _entry_is_for(vol_saved_id, m))
                    ]
                deployments = [
                    d for d in deployments
                    if not (d.get("column_selectors") and len(d.get("metrics", [])) == 0)
                ]

                # (b) Build a tag_definition with all selectors
                fv_tag_def = {
                    "tag_id": "freshness_and_volume",
                    "column_selectors": [{"name": s} for s in selector_to_fv_overrides.keys()],
                }

                # (c) Build one tag-based deployment carrying the two metrics with the common overrides
                fv_metrics = []
                f_entry = {"saved_metric_id": fresh_saved_id}
                f_entry.update(common_f)
                fv_metrics.append(f_entry)

                v_entry = {"saved_metric_id": vol_saved_id}
                v_entry.update(common_v)
                fv_metrics.append(v_entry)

                fv_deployment = {"tag_id": "freshness_and_volume", "metrics": fv_metrics}

                # (d) Append a new section (or merge into existing) with the tag deployment
                #     Keep your existing structure: tag_deployments is a list of sections
                #     with "deployments": [...]
                deployments.insert(0, fv_deployment)  # temporary holder; we’ll wrap below

                # Export both: deployments section(s) + extra tag_defs
                grouped_tag_definitions = [fv_tag_def]
            else:
                grouped_tag_definitions = []
        else:
            grouped_tag_definitions = []

        _enforce_saved_id_uniqueness(deployments)
        final_section = [{"deployments": deployments}]
        return final_section, grouped_tag_definitions

    def to_bigconfig_yaml(self,
                          collection: SimpleCollection,
                          data_time_window_default: Optional[bool] = None,
                          namespace: Optional[str] = None,
                          auto_apply_on_indexing: bool = False
                          ) -> Dict[str, Any]:

        dtw_default = data_time_window_default
        if dtw_default is None:
            dtw_default = [ac.boolean_value for ac in self.client.get_advanced_configs()
                           if ac.key == "metric.data_time_window.default"][0]

        # saved_defs = self.build_saved_metric_definitions()
        # tag_defs = build_tag_definitions(metric_infos)
        tag_deployments, extra_tag_defs = self.build_tag_deployments(dtw_default)

        for deployment in tag_deployments:
            if deployment:
                deployment = {
                    "collection": {"name": collection.name, "description": collection.description}, **deployment
                }
                tag_deployments = [deployment]
        # Returning namespace but if using that feature there are likely multiple, and it's best to use the CLI param
        # It wouldn't make sense to add a namespace to the SMD library file.
        return {
            "type": "BIGCONFIG_FILE",
            **({"auto_apply_on_indexing": True} if auto_apply_on_indexing else {}),
            **({"namespace": namespace} if namespace else {}),
            **({"tag_definitions": extra_tag_defs} if extra_tag_defs else {}),
            # "saved_metric_definitions": {"metrics": saved_defs},
            "tag_deployments": tag_deployments,
        }
