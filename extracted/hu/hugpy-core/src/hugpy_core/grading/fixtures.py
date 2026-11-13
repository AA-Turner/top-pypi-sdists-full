"""Gated fixture grading owned by Core; no judge model or extra engine calls."""
import os
import json
import math
import re
from hugpy_core.lifted.fixtures import load_fixture

LEVELS = ('compatibility', 'validity', 'quality')


def _text(payload):
    choices = payload.get('choices') or []
    if choices and isinstance(choices[0], dict):
        message = choices[0].get('message') or {}
        return message.get('content') if isinstance(message.get('content'), str) else ''
    return payload.get('text') if isinstance(payload.get('text'), str) else ''


def _tools(payload):
    choices = payload.get('choices') or []
    return ((choices[0].get('message') or {}).get('tool_calls') or []) if choices else []


def _evaluate(fixture, check, payload, probe):
    family, name, truth = fixture['family'], check['name'], fixture['ground_truth']
    text = _text(payload)
    media = probe.get('media') or {}
    artifacts = payload.get('artifacts') or []
    if name in ('artifact-returned', 'image-returned', 'mesh-returned'):
        return bool(artifacts)
    if name == 'decodes':
        return {'passed': True, 'failed': False}.get(media.get('status'))
    if family == 'generation-prompts':
        expected = truth.get('expected') or {}
        outputs = media.get('artifacts') or []
        if media.get('status') != 'passed':
            return None
        if name == 'dims':
            return bool(outputs) and all(a.get('width') == expected.get('width') and a.get('height') == expected.get('height') for a in outputs)
        if name == 'duration':
            return bool(outputs) and all(a.get('duration_s', 0) >= expected['min_seconds'] for a in outputs)
    if family in ('image-simple', 'real-vision', 'long-document'):
        if name in ('answer-returned', 'answers-returned', 'non-empty'):
            return bool(text.strip())
        if name == 'no-truncation-error':
            choices = payload.get('choices') or []
            return bool(choices) and all(c.get('finish_reason') not in (None, 'length') for c in choices)
        if family == 'long-document' and name.startswith('retrieve-'):
            question = truth['questions'][name.removeprefix('retrieve-')]
            expected = question.split('->', 1)[1].strip()
            return re.search(r'(?<!\w)' + re.escape(expected) + r'(?!\w)', text, re.I) is not None
    if family == 'speech':
        if name == 'transcript-returned':
            return bool(text.strip())
    if family in ('person-face', 'real-face') and name == 'runs':
        return isinstance(payload.get('faces'), list)
    if family == 'video-short' and name == 'accepted':
        return bool(artifacts) or isinstance(payload.get('dets'), list)
    if family == 'text-short':
        if name == 'returns-choices':
            return bool(text.strip())
        if name == 'usage-present':
            usage = payload.get('usage') or {}
            return all(type(usage.get(k)) is int and usage[k] >= 0 for k in ('prompt_tokens', 'completion_tokens'))
        if name == 'single-line':
            return bool(text.strip()) and len(text.strip().splitlines()) == 1
        if name == 'answer-match':
            normalize = lambda t: t.strip().casefold().rstrip('.!?;:')
            return normalize(text) == normalize(truth['expected_answer'])
    if family == 'tool-request':
        tools = _tools(payload)
        if name == 'tool-call-emitted':
            return bool(tools)
        if not tools:
            return False
        function = tools[0].get('function') or {}
        try:
            args = json.loads(function.get('arguments', ''))
        except (ValueError, TypeError):
            args = None
        if name == 'args-parse':
            return isinstance(args, dict)
        if name == 'correct-tool':
            return function.get('name') == truth['name']
        if name == 'correct-args':
            return args == truth['arguments']
    if family == 'text-pairs':
        vectors = [row.get('embedding') for row in payload.get('data', [])]
        valid = len(vectors) == 3 and all(isinstance(v, list) and v and all(type(x) in (int, float) and math.isfinite(x) for x in v) for v in vectors)
        if name == 'vectors-returned':
            return valid
        if name == 'dims-consistent':
            return valid and len({len(v) for v in vectors}) == 1
        if name == 'similarity-ordering':
            if not valid or len({len(v) for v in vectors}) != 1:
                return False
            def cosine(a, b):
                denom = math.sqrt(sum(x*x for x in a) * sum(x*x for x in b))
                return sum(x*y for x,y in zip(a,b)) / denom if denom else None
            positive, negative = cosine(vectors[0], vectors[1]), cosine(vectors[0], vectors[2])
            return positive is not None and negative is not None and positive > negative
    # Other domains retain their manifest criteria as unresolved until a scoped
    # decoder/evaluator exists. Caption keywords are not a substitute for vision
    # ground truth; subtitle text is not an exact speech transcript.
    return None


def grade(probe, payload, *, library=None):
    ref = ((probe.get('method') or {}).get('library_fixture'))
    if not ref:
        return None
    report = {'fixture_id': ref.get('id'), 'difficulty_tier': ref.get('difficulty_tier'),
              'levels': {}, 'level_reached': 0, 'status': 'unresolved'}
    root = library or os.environ.get('HUGPY_FIXTURE_LIBRARY')
    if not root:
        return {**report, 'reason': 'worker HUGPY_FIXTURE_LIBRARY is not configured'}
    try:
        fixture, _, digest = load_fixture(root, ref['id'])
        if digest != ref.get('manifest_sha256') or fixture['revision'] != ref.get('revision'):
            return {**report, 'reason': 'worker fixture manifest differs from the selected fixture'}
    except (OSError, ValueError, KeyError) as exc:
        return {**report, 'reason': 'fixture unavailable or invalid: ' + str(exc)}
    if probe.get('method_status') != 'passed':
        return {**report, 'reason': 'runtime/method compatibility gate did not pass'}
    open_gate = True
    for index, level in enumerate(LEVELS, 1):
        checks = [c for c in fixture['checks'] if c['level'] == level]
        results = []
        for check in checks:
            value, reason = None, 'gated by earlier level' if not open_gate else 'no evaluator'
            if open_gate:
                try:
                    value = _evaluate(fixture, check, payload, probe)
                    if value is not None:
                        reason = 'deterministic fixture check'
                except (ValueError, TypeError, KeyError, IndexError, AttributeError, OverflowError):
                    reason = 'malformed response or unsupported evaluation scope'
            results.append({'name': check['name'], 'status': 'unresolved' if value is None else 'passed' if value else 'failed', 'reason': reason})
        states = {r['status'] for r in results}
        state = 'failed' if 'failed' in states else 'passed' if results and states == {'passed'} else 'unresolved'
        report['levels'][level] = {'status': state, 'checks': results}
        open_gate = open_gate and state == 'passed'
        if open_gate:
            report['level_reached'] = index
    report['status'] = 'passed' if report['level_reached'] == 3 else 'failed' if any(v['status'] == 'failed' for v in report['levels'].values()) else 'unresolved'
    return report
