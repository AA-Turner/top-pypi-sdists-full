######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-12T21:59:19.386524                                                            #
######################################################################################################

from __future__ import annotations



def capture_card_state(card_id = 'gpu_profile'):
    """
    After the initial card.refresh(force=True), extract everything the
    subprocess needs to write data.json updates:
      - card_uuid
      - comp_ids  (the IDs we assigned when calling card.append(..., id=X))
      - reload_token  (must match the token baked into the initial HTML)
    
    Returns a dict ready to merge into the subprocess config.
    """
    ...

def get_datastore_type():
    """
    Return the active datastore type string (e.g. 's3', 'local').
    """
    ...

def make_card_datastore(config):
    """
    Construct a CardDatastore from a config dict (as passed to GpuCardProcess).
    Safe to call from a background thread after construction on main thread.
    
    config must contain: datastore_type, card_sysroot, pathspec
    """
    ...

def build_subprocess_config(card_id, comp_ids, interval, card_interval, devices = None, readings_path = None, max_samples_per_gpu = None):
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
    ...

