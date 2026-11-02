from hugpy_core.web.queue_view import queue_snapshot


def test_request_telemetry_distinguishes_waiting_active_finished_and_offline():
    calls = [
        {'request_id': 'load', 'model_name': 'm', 'received_at': 10},
        {'request_id': 'answer', 'model_name': 'n', 'inference_started_at': 20},
        {'request_id': 'finished', 'inference_ended_at': 30},
    ]
    result = queue_snapshot([
        {'id': 'online', 'status': 'online', 'resources': {'active_requests': calls}},
        {'id': 'offline', 'status': 'offline', 'resources': {'active_requests': calls}},
    ])
    assert result['counts'] == {'active': 1, 'waiting': 1}
    assert [row['request_id'] for row in result['active']] == ['load', 'answer']
    assert result['partial'] is False


def test_missing_telemetry_is_not_an_empty_queue():
    result = queue_snapshot([{'id': 'old', 'status': 'online'},
                             {'id': 'idle', 'status': 'online', 'resources': {'active_requests': []}}])
    assert result['partial'] is True
    assert result['unreported_workers'] == ['old']
