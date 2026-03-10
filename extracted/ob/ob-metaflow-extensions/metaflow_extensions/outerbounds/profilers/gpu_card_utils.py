"""
utils.py — helpers that read live Metaflow task context.

Must be called from inside a running Metaflow task (current.* available).
All functions that touch current.* must be called on the main thread before
the GpuCardProcess subprocess is spawned.
"""

import os


def capture_card_state(card_id="gpu_profile"):
    """
    After the initial card.refresh(force=True), extract everything the
    subprocess needs to write data.json updates:
      - card_uuid
      - comp_ids  (the IDs we assigned when calling card.append(..., id=X))
      - reload_token  (must match the token baked into the initial HTML)

    Returns a dict ready to merge into the subprocess config.
    """
    from metaflow import current

    collector = current.card
    if card_id not in collector._card_id_map:
        raise RuntimeError(
            "Card id '%s' not found in current.card. "
            "Make sure @card(id='%s') is on this step and refresh(force=True) "
            "has been called before capture_card_state()." % (card_id, card_id)
        )
    card_uuid = collector._card_id_map[card_id]
    mgr = collector._card_component_store[card_uuid]

    # This is the token baked into the HTML by the initial render_runtime call.
    # BlankCard.reload_content_token returns "runtime-<component_update_ts>".
    # We keep this constant for all subsequent data.json writes so the browser
    # always does in-place DOM patches rather than full iframe reloads.
    component_update_ts = mgr.components.layout_last_changed_on
    reload_token = "runtime-%s" % str(component_update_ts)

    return {
        "card_uuid": card_uuid,
        "reload_token": reload_token,
    }


def get_datastore_type():
    """Return the active datastore type string (e.g. 's3', 'local')."""
    from metaflow.metaflow_config import DEFAULT_DATASTORE

    return os.environ.get("METAFLOW_DEFAULT_DATASTORE", DEFAULT_DATASTORE)


def make_card_datastore(config):
    """
    Construct a CardDatastore from a config dict (as passed to GpuCardProcess).
    Safe to call from a background thread after construction on main thread.

    config must contain: datastore_type, card_sysroot, pathspec
    """
    from metaflow.plugins.cards.card_datastore import CardDatastore
    from metaflow.datastore import FlowDataStore
    from metaflow.plugins import DATASTORES

    ds_type = config["datastore_type"]
    storage_impl_class = next(d for d in DATASTORES if d.TYPE == ds_type)

    flow_name = config["pathspec"].split("/")[0]
    flow_ds = FlowDataStore(
        flow_name=flow_name,
        environment=None,
        storage_impl=storage_impl_class,
        ds_root=config["card_sysroot"],
    )
    return CardDatastore(flow_ds, pathspec=config["pathspec"])


def build_subprocess_config(
    card_id,
    comp_ids,
    interval,
    card_interval,
    devices=None,
    readings_path=None,
    max_samples_per_gpu=None,
):
    """
    Build the complete config dict to pass to GpuCardProcess.
    Call this on the main thread after the initial card.refresh(force=True).

    Parameters
    ----------
    card_id : str         e.g. "gpu_profile"
    comp_ids : dict       per-device component ID map (see wrapper._build_comp_ids)
    interval : int        nvidia-smi sampling rate in seconds
    card_interval : int   card data.json write rate in seconds
    devices : list        device metadata (passed through to subprocess)
    max_samples_per_gpu : int  memory-bounded ring buffer size per GPU (None = unbounded)
    """
    from metaflow import current

    card_state = capture_card_state(card_id)

    from metaflow.plugins.cards.card_datastore import CardDatastore

    ds_type = get_datastore_type()

    return {
        "sample_interval": interval,
        "card_interval": card_interval,
        "card_id": card_id,
        "card_type": "blank",
        "comp_ids": comp_ids,
        "devices": devices or [],
        "datastore_type": ds_type,
        "card_sysroot": CardDatastore.get_storage_root(ds_type),
        "pathspec": current.pathspec,
        "readings_path": readings_path,
        "max_samples_per_gpu": max_samples_per_gpu,
        **card_state,  # card_uuid, reload_token
    }
