"""Pure conversion of Wrapper residents into Core allocation observations."""


def allocation(r: dict) -> dict:
    vram = r.get('vram_bytes')
    card = r.get('device_id') if r.get('device_id') is not None else r.get('device')
    if isinstance(card, bool) or not (isinstance(card, int) or isinstance(card, str) and card.isdigit()):
        card = None
    return {'kind': 'slot', 'model_key': r.get('key'), 'pid': r.get('pid'), 'slot_id': r.get('port'),
            'healthy': bool(r.get('healthy')), 'busy': bool(r.get('busy')), 'endpoint': r.get('endpoint'),
            'rss_bytes': r.get('ram_bytes'), 'rss_anon_bytes': r.get('rss_anon_bytes'),
            'rss_file_bytes': r.get('rss_file_bytes'), 'rss_shmem_bytes': r.get('rss_shmem_bytes'),
            'n_gpu_layers': r.get('n_gpu_layers'), 'ctx': r.get('ctx'), 'n_cpu_moe': r.get('n_cpu_moe'),
            'vram_bytes': vram,
            'gpu_uuid': r.get('gpu_uuid'), 'gpu_backend': r.get('gpu_backend'),
            'device': (r['gpu_backend'] + (':' + r['gpu_uuid'] if r.get('gpu_uuid') else '') if r.get('gpu_backend')
                       else f'cuda:{card}' if card is not None
                       else None if vram is None else 'cuda' if vram > 0 else 'cpu'),
            'device_id': int(card) if card is not None else None,
            'last_used': r.get('last_used'), 'loading': bool(r.get('loading')),
            'materialized': bool(r.get('healthy')) and not r.get('loading'),
            'cpu_set': r.get('cpu_set'), 'threads': r.get('threads')}
