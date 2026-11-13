"""The model name Core sends a worker is one that worker resolves."""
from hugpy_core.relay.pick import served_name
from hugpy_core.relay.relay import worker_payload

WORKER = {'id': 'w1', 'name': 'ae', 'engine': {'name': 'fitevict'},
          'models': ['Qwen/Qwen2.5-7B-Instruct-GGUF::qwen2.5-7b-instruct-q4_k_m-*.gguf',
                     'Qwen/Qwen2.5-7B-Instruct-GGUF::qwen2.5-7b-instruct-q8_0-*.gguf',
                     'bartowski/Tiny-GGUF::tiny-q4.gguf', 'other/Tiny-GGUF::tiny-q4.gguf', 'acme/dir-model::*'],
          'loaded_models': ['other/Tiny-GGUF::tiny-q4.gguf']}


def test_a_short_or_default_name_goes_out_as_the_name_the_worker_serves():
    unit = 'Qwen/Qwen2.5-7B-Instruct-GGUF::qwen2.5-7b-instruct-q4_k_m-*.gguf'
    assert served_name(unit, WORKER) == unit                                      # a unit: as it is
    assert served_name('Qwen/Qwen2.5-7B-Instruct-GGUF', WORKER) == 'Qwen/Qwen2.5-7B-Instruct-GGUF'   # its repo: the worker picks the unit
    # the engine's default and other legacy short names: the repo they stand for
    assert served_name('Qwen2.5-7B-Instruct-GGUF', WORKER) == 'Qwen/Qwen2.5-7B-Instruct-GGUF'
    assert served_name('qwen2.5-7b-instruct-gguf', WORKER) == 'Qwen/Qwen2.5-7B-Instruct-GGUF'
    assert served_name('Tiny-GGUF', WORKER) == 'other/Tiny-GGUF'                  # two repos share the tail: the loaded one
    assert served_name('Unknown-Model', WORKER) == 'Unknown-Model'                # nothing to map to: the worker says so


def test_the_request_built_for_a_worker_carries_that_name(monkeypatch):
    from hugpy_core.calllog import call_record
    monkeypatch.setattr(call_record, 'dispatch', lambda payload, worker: payload)
    from hugpy_core.models import modeldb
    monkeypatch.setattr(modeldb, 'get_knobs', lambda *args: {})
    sent = worker_payload({'model_key': 'Qwen2.5-7B-Instruct-GGUF', 'messages': [{'role': 'user', 'content': 'hi'}]}, WORKER)
    assert sent['model_key'] == 'Qwen/Qwen2.5-7B-Instruct-GGUF'
