"""Native workers own saved controls, finite output defaults and execution IDs."""
import json
from unittest.mock import patch
from hugpy_core.intake.presence import allocation
from hugpy_core.intake.service import presence
from hugpy_core.relay import relay

NATIVE={'id':'op','name':'op','url':'http://127.0.0.1:15302',
        'engine':{'name':'hugpy-wrapper'},
        'data_service':{'implementation':'hugpy-wrapper-native'}}


def test_native_relay_does_not_replay_cached_operator_controls():
    with patch('hugpy_core.models.modeldb.get_knobs',side_effect=AssertionError('Core cache must not own controls')), \
         patch('hugpy_core.calllog.call_record.dispatch',side_effect=lambda out,worker:out):
        out=relay.worker_payload({'model_key':'model','knobs':{'ctx_pct':25}},NATIVE)
    assert out['knobs']=={'ctx_pct':25}
    assert relay.is_front_door(NATIVE)


def test_native_default_output_does_not_start_legacy_unbounded_rounds():
    calls=[]
    def events(worker,payload,timeout):
        calls.append(payload)
        yield {'type':'token','text':'answer'}
        yield {'type':'done','finish_reason':'max_tokens','usage':{'completion_tokens':1}}
    with patch.object(relay,'_front_door_round',side_effect=events):
        out=list(relay.front_door_stream(NATIVE,{'model_key':'model'}))
    assert len(calls)==1 and 'max_new_tokens' not in calls[0]
    assert out[-1]['finish_reason']=='max_tokens'


def test_amd_resident_identity_is_not_changed_to_cuda():
    out=allocation({'key':'model::q.gguf','gpu_uuid':'AMD-0000:01:00.0','gpu_backend':'vulkan','vram_bytes':100})
    assert out['device']=='vulkan:AMD-0000:01:00.0'
    assert out['gpu_uuid']=='AMD-0000:01:00.0'
    assert allocation({'key':'legacy','device':0,'vram_bytes':100})['device']=='cuda:0'


def test_presence_uses_native_engine_and_keeps_catalog_separate_from_copies():
    state={'store_id':'s','engine':{'name':'hugpy-wrapper'},'data_service':{
        'protocol':'hugpy-wrapper-data','version':1,'store_id':'s',
        'implementation':'hugpy-wrapper-native','capabilities':{'physical_inventory':False}}}
    out=presence(NATIVE,state,[{'id':'model::q.gguf','selectable':True}])
    assert out['engine']['name']=='hugpy-wrapper'
    assert out['models']==['model::q.gguf'] and out['models_local']==[]
    assert out['models_discovered'] is None


def test_native_cancellation_uses_execution_receipt_endpoint():
    class Response:
        status=200
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def read(self):return b'{"state":"cancelled"}'
    def open_(req,**kwargs):
        assert req.full_url.endswith('/v1/requests/native-123/cancel')
        return Response()
    with patch('urllib.request.urlopen',side_effect=open_),patch('hugpy_core.registry.transport.headers',return_value={}):
        assert relay.worker_cancel(NATIVE,'native-123')[0]==200
