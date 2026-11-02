"""Present Wrapper request telemetry without introducing a second scheduler."""


def queue_snapshot(workers):
    active, missing = [], []
    for worker in workers:
        if worker.get('status') != 'online':
            continue
        name = worker.get('name') or worker.get('id')
        resources = worker.get('resources') or {}
        requests = resources.get('active_requests')
        if not isinstance(requests, list):
            missing.append(name)
            continue
        for call in requests:
            if not isinstance(call, dict) or not call.get('request_id') or call.get('inference_ended_at'):
                continue
            active.append({
                'request_id': call['request_id'], 'model_key': call.get('model_name'),
                'worker': name, 'worker_id': worker.get('id'),
                'state': 'active' if call.get('inference_started_at') else 'waiting',
                'started_at': call.get('inference_started_at'), 'created_at': call.get('received_at'),
            })
    return {'active': active, 'counts': {
        'active': sum(row['state'] == 'active' for row in active),
        'waiting': sum(row['state'] == 'waiting' for row in active),
    }, 'partial': bool(missing), 'unreported_workers': missing, 'source': 'wrapper telemetry'}
