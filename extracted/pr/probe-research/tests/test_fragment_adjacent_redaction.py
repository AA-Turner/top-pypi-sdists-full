"""A credential split across consecutive ATIF fragments (session upload protocol 3).

A fragment is one event's share of its session's trajectory (prbe-knowledge
`engine/ingest/atif/fragment.py`). The scrubber already catches a credential
split across adjacent events; these pin the same for fragments: their prose
(`message`, text and thinking `parts`) is joined, the halves also leave each
fragment's `line.text` (the index text, which repeats the prose behind a
speaker label), and tool-call metadata never joins anything. Events read the
same prose as the fragments built from them, so a canary batch carrying both
never ships halves in one that the other redacted.
"""
import hashlib
import itertools
import json

import pytest

from probe.tap_core import codex_sanitize, kimi_sanitize, pi_sanitize, sanitize
from probe.tap_core.secrets import redact_event
from probe.tap_core.session_journal import UnsafePending, _require_safe_pending, _scrub_content

GITHUB = 'ghp_' + hashlib.sha256(b'synthetic-fragment-regression').hexdigest()[:36]
INGEST = 'ros_ing_' + hashlib.sha256(b'synthetic-fragment-ingest').hexdigest()[:32]


def _line(n, text, *, user_turn=False):
    return {'line_no': n, 'text': text, 'user_turn': user_turn,
            'compact_boundary': False, 'compact_summary': False}


def user(n, message):
    return {'v': 1, 'line': _line(n, 'USER: ' + message, user_turn=True), 'kind': 'user', 'message': message}


def system(n, message):
    return {'v': 1, 'line': _line(n, 'SYSTEM (informational): ' + message), 'kind': 'system',
            'message': message, 'subtype': 'informational'}


def assistant(n, *parts):
    """Parts as (type, value): text/thinking take a str, tool_call a dict of id, name, summary."""
    pieces, rendered = [], []
    for seq, (kind, value) in enumerate(parts):
        if kind == 'tool_call':
            pieces.append({'type': kind, 'seq': seq, **value})
            rendered.append(f"TOOL_USE: {value['name']} — {value['summary']}")
        else:
            pieces.append({'type': kind, 'seq': seq, 'text': value})
            rendered.append(('ASSISTANT (thinking): ' if kind == 'thinking' else 'ASSISTANT: ') + value)
    return {'v': 1, 'line': _line(n, '\n'.join(rendered)), 'kind': 'assistant', 'parts': pieces}


def texts_of(fragments):
    """Every prose string and line text, in order."""
    out = []
    for fragment in fragments:
        out.append(fragment['line']['text'])
        if 'message' in fragment:
            out.append(fragment['message'])
        out.extend(part['text'] for part in fragment.get('parts', []) if 'text' in part)
    return out


def assert_scrubbed(payload, halves):
    clean, fired = redact_event(payload)
    assert fired
    for text in texts_of(clean['fragments']):
        assert all(half not in text for half in halves), text
    # The journal stages a fixed point and refuses anything else.
    assert redact_event(clean) == (clean, [])
    return clean


@pytest.mark.parametrize('key', [GITHUB, INGEST], ids=['github', 'ingest'])
def test_split_across_consecutive_fragment_messages(key):
    payload = {'fragments': [user(0, 'here it is ' + key[:20]), user(1, key[20:] + ' thanks')]}
    clean = assert_scrubbed(payload, [key[:20], key[20:]])
    first, second = clean['fragments']
    assert first['message'].startswith('here it is <redacted:')
    assert first['line']['text'].startswith('USER: here it is <redacted:')
    assert second['message'].endswith('> thanks')
    assert second['line']['text'].startswith('USER: <redacted:') and second['line']['text'].endswith('> thanks')


def test_split_across_assistant_text_parts_of_consecutive_fragments():
    call = {'id': 'toolu_01', 'name': 'Bash', 'summary': 'git status'}
    payload = {'fragments': [
        assistant(0, ('thinking', 'the user wants the key'), ('text', 'use ' + GITHUB[:15])),
        assistant(1, ('text', GITHUB[15:] + ' for the push'), ('tool_call', call)),
    ]}
    clean = assert_scrubbed(payload, [GITHUB[:15], GITHUB[15:]])
    first, second = clean['fragments']
    assert first['parts'][0] == payload['fragments'][0]['parts'][0]
    assert first['parts'][1]['text'].startswith('use <redacted:')
    assert second['parts'][1] == payload['fragments'][1]['parts'][1]
    assert second['line']['text'].endswith('\nTOOL_USE: Bash — git status')


def test_line_text_of_consecutive_fragments_keeps_no_half():
    # The index text reads `line.text`; a label sits where the halves meet, so
    # it is the prose join that must clear every line, across three kinds.
    payload = {'fragments': [
        user(0, 'push with ' + GITHUB[:10]),
        assistant(1, ('text', GITHUB[10:25])),
        system(2, GITHUB[25:] + ' (end)'),
    ]}
    clean = assert_scrubbed(payload, [GITHUB[:10], GITHUB[10:25], GITHUB[25:]])
    lines = [fragment['line']['text'] for fragment in clean['fragments']]
    assert lines[0].startswith('USER: push with <redacted:')
    assert lines[1].startswith('ASSISTANT: <redacted:')
    assert lines[2].startswith('SYSTEM (informational): <redacted:') and lines[2].endswith(' (end)')


@pytest.mark.parametrize('field', ['id', 'name', 'summary'])
def test_tool_call_metadata_never_joins_the_next_fragment(field):
    # Control: the same half in a text part is joined and redacted.
    control = {'fragments': [assistant(0, ('text', GITHUB[:20])), user(1, GITHUB[20:] + ' ok')]}
    assert_scrubbed(control, [GITHUB[:20], GITHUB[20:]])
    call = {'id': 'toolu_01', 'name': 'Bash', 'summary': 'ls'} | {field: GITHUB[:20]}
    payload = {'fragments': [assistant(0, ('tool_call', call)), user(1, GITHUB[20:] + ' ok')]}
    assert redact_event(payload) == (payload, [])


def test_empty_prose_inside_a_split_leaves_its_line_alone():
    # fragment() never emits an empty text part, but a scrubbed piece that was
    # empty must not be "found" everywhere in its line.
    middle = {'v': 1, 'line': _line(1, 'ASSISTANT (thinking): unrelated'), 'kind': 'assistant',
              'parts': [{'type': 'text', 'seq': 0, 'text': ''}]}
    payload = {'fragments': [user(0, 'key ' + GITHUB[:20]), middle, user(2, GITHUB[20:])]}
    clean = assert_scrubbed(payload, [GITHUB[:20], GITHUB[20:]])
    assert clean['fragments'][1]['line']['text'] == 'ASSISTANT (thinking): unrelated'


def test_journal_refuses_a_pending_body_with_a_split_in_its_fragments():
    payload = {'batch_seq': 3, 'events': [], 'cwd': '/work',
               'fragments': [user(0, 'here it is ' + INGEST[:20]), user(1, INGEST[20:])]}
    with pytest.raises(UnsafePending):
        _require_safe_pending(json.dumps(payload).encode())
    clean = _scrub_content(payload)
    assert INGEST[:20] not in json.dumps(clean) and INGEST[20:] not in json.dumps(clean)
    assert clean['batch_seq'] == 3
    _require_safe_pending(json.dumps(clean).encode())


# --- line.text is edited by position ------------------------------------------


def test_a_one_character_piece_never_rewrites_the_label():
    key = 'ghp_' + 'aB3' * 11 + 'aBA'  # ends in "A", which the label "ASSISTANT" holds twice
    clean = assert_scrubbed({'fragments': [assistant(0, ('text', 'key ' + key[:-1])), assistant(1, ('text', 'A'))]},
                            [key[:-1]])
    assert clean['fragments'][1]['line']['text'] == 'ASSISTANT: <redacted:github-token>'


def test_a_piece_repeated_inside_a_later_piece_leaves_no_half_of_either():
    # "853" ends GITHUB and recurs in the next piece, which starts a second
    # credential; replacing every "853" used to hide that piece from its own edit.
    other = 'ghp_' + hashlib.sha256(b'second synthetic credential').hexdigest()[:36]
    tail = GITHUB[-3:]
    payload = {'fragments': [
        assistant(0, ('text', 'k ' + GITHUB[:-3])),
        assistant(1, ('text', tail), ('text', ' see ' + tail + ' then ' + other[:20])),
        assistant(2, ('text', other[20:] + ' end')),
    ]}
    clean = assert_scrubbed(payload, [GITHUB[:-3], other[:20], other[20:]])
    assert clean['fragments'][1]['line']['text'] == (
        'ASSISTANT: <redacted:github-token>\nASSISTANT:  see ' + tail + ' then <redacted:github-token>')


def test_a_line_that_does_not_hold_its_piece_is_replaced_whole():
    first = user(0, 'here it is ' + GITHUB[:20])
    first['line']['text'] = 'USER: rendered differently ' + GITHUB[:20]
    clean = assert_scrubbed({'fragments': [first, user(1, GITHUB[20:] + ' thanks')]}, [GITHUB[:20], GITHUB[20:]])
    assert clean['fragments'][0]['line']['text'] == '<redacted:github-token>'
    assert clean['fragments'][1]['line']['text'] == 'USER: <redacted:github-token> thanks'


def test_a_piece_is_looked_for_behind_prose_labels_only():
    # A tool line (`TOOL_USE: <name>`) can hold the same text as the prose after
    # it; the half must leave the ASSISTANT segment, not the tool line.
    head = GITHUB[:20]
    first = assistant(0, ('tool_call', {'id': 'toolu_01', 'name': head, 'summary': ''}), ('text', head))
    first['line']['text'] = 'TOOL_USE: ' + head + '\nASSISTANT: ' + head
    clean = assert_scrubbed({'fragments': [first, user(1, GITHUB[20:])]}, [GITHUB[20:]])
    assert clean['fragments'][0]['line']['text'] == 'TOOL_USE: ' + head + '\nASSISTANT: <redacted:github-token>'


def test_a_piece_must_be_its_whole_segment():
    first = user(0, 'here it is ' + GITHUB[:20])
    first['line']['text'] += ' (edited)'
    clean = assert_scrubbed({'fragments': [first, user(1, GITHUB[20:])]}, [GITHUB[:20], GITHUB[20:]])
    assert clean['fragments'][0]['line']['text'] == '<redacted:github-token>'


def test_a_split_inside_one_fragment_leaves_its_line_too():
    payload = {'fragments': [assistant(0, ('text', 'use ' + GITHUB[:20]), ('text', GITHUB[20:] + ' now'))]}
    clean = assert_scrubbed(payload, [GITHUB[:20], GITHUB[20:]])
    assert clean['fragments'][0]['line']['text'] == (
        'ASSISTANT: use <redacted:github-token>\nASSISTANT: <redacted:github-token> now')


# --- events read what their fragments read --------------------------------------

STAMP = '2026-10-06T12:00:00.000Z'


def _cc_user(text):
    return {'type': 'user', 'uuid': 'u1', 'timestamp': STAMP, 'message': {'role': 'user', 'content': text}}


def _cc_assistant(block):
    return {'type': 'assistant', 'uuid': 'a1', 'timestamp': STAMP,
            'message': {'role': 'assistant', 'model': 'm', 'content': [block]}}


def _pi_message(role, content):
    return {'type': 'message', 'id': 'a1b2c3d4', 'parentId': 'p', 'timestamp': STAMP,
            'message': {'role': role, 'content': content, 'provider': 'anthropic', 'model': 'm'}}


def _kimi_part(part):
    return {'type': 'context.append_loop_event', 'agentId': 'main', 'time': 1791170640485,
            'event': {'type': 'content.part', 'turnId': 't1', 'step': 1, 'part': part}}


#: Native lines of each harness, (sanitizer, {slot: line(text)}). A tool call
#: ends a run in both readings, so it is part of every harness's alphabet.
HARNESSES = {
    'claude_code': (sanitize.sanitize_event, {
        'user': _cc_user,
        'text': lambda t: _cc_assistant({'type': 'text', 'text': t}),
        'think': lambda t: _cc_assistant({'type': 'thinking', 'thinking': t, 'signature': 's'}),
        'tool': lambda t: _cc_assistant({'type': 'tool_use', 'id': 'toolu_1', 'name': 'Bash',
                                         'input': {'command': 'echo ' + t}}),
        'system': lambda t: {'type': 'system', 'subtype': 'informational', 'content': t,
                             'timestamp': STAMP, 'uuid': 's1'},
    }),
    'codex': (codex_sanitize.sanitize_event, {
        'user': lambda t: {'type': 'response_item', 'timestamp': STAMP, 'payload': {
            'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': t}]}},
        'text': lambda t: {'type': 'response_item', 'timestamp': STAMP, 'payload': {
            'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': t}]}},
        'think': lambda t: {'type': 'response_item', 'timestamp': STAMP, 'payload': {
            'type': 'reasoning', 'content': [{'type': 'reasoning_text', 'text': t}], 'summary': []}},
        'tool': lambda t: {'type': 'response_item', 'timestamp': STAMP, 'payload': {
            'type': 'function_call', 'name': 'shell', 'call_id': 'c1',
            'arguments': json.dumps({'command': ['echo', t]})}},
    }),
    'pi': (pi_sanitize.sanitize_event, {
        'user': lambda t: _pi_message('user', t),
        'text': lambda t: _pi_message('assistant', [{'type': 'text', 'text': t}]),
        'think': lambda t: _pi_message('assistant', [{'type': 'thinking', 'thinking': t}]),
        'tool': lambda t: _pi_message('assistant', [{'type': 'toolCall', 'id': 'c1', 'name': 'bash',
                                                     'arguments': {'command': 'echo ' + t}}]),
    }),
    'kimi': (kimi_sanitize.sanitize_event, {
        'user': lambda t: {'type': 'context.append_message', 'agentId': 'main', 'time': 1791170640485,
                           'message': {'role': 'user', 'content': [{'type': 'text', 'text': t}],
                                       'origin': {'kind': 'user'}}},
        'text': lambda t: _kimi_part({'type': 'text', 'text': t}),
        'think': lambda t: _kimi_part({'type': 'think', 'think': t}),
        'tool': lambda t: {'type': 'context.append_loop_event', 'agentId': 'main', 'time': 1791170640485,
                           'event': {'type': 'tool.call', 'turnId': 't1', 'step': 1, 'id': 'c1',
                                     'name': 'Bash', 'args': {'command': 'echo ' + t}}},
    }),
}


def _fragment_of(event):
    """The prose and Line of prbe-knowledge `fragment()` (FRAGMENT_VERSION 1)
    for the shapes above; T4 vendors the real one into tap_core."""
    raw, n = event['raw'], event['line_no']
    out = {'v': 1, 'line': _line(n, '')}
    message = raw.get('message') if isinstance(raw.get('message'), dict) else None
    if raw.get('type') not in ('user', 'assistant'):
        out['kind'] = 'system' if raw.get('type') == 'system' else 'other'
        if isinstance(raw.get('content'), str) and raw['content']:
            out['message'] = raw['content']
            label = f"SYSTEM ({raw['subtype']})" if raw.get('type') == 'system' else str(raw.get('type')).upper()
            out['line']['text'] = f"{label}: {raw['content']}"
        return out
    if message is None:
        out['kind'] = 'none'
        return out
    out['kind'] = raw['type']
    content, label = message['content'], 'USER: ' if raw['type'] == 'user' else 'ASSISTANT: '
    if isinstance(content, str):
        if raw['type'] == 'user':
            out['message'] = content.strip()
        else:
            out['parts'] = [{'type': 'text', 'seq': 0, 'text': content}]
        out['line']['text'] = label + content.strip()
        return out
    parts, rendered = [], []
    for seq, block in enumerate(content):
        if block.get('type') == 'text':
            text = block['text'].strip() if raw['type'] == 'user' else block['text']
            parts.append({'type': 'text', 'seq': seq, 'text': text})
            rendered.append(label + text)
        elif block.get('type') == 'thinking' and raw['type'] == 'assistant':
            parts.append({'type': 'thinking', 'seq': seq, 'text': block['thinking']})
            rendered.append('ASSISTANT (thinking): ' + block['thinking'])
        elif block.get('type') == 'tool_use':
            parts.append({'type': 'tool_call', 'seq': seq, 'id': block.get('id'), 'name': block.get('name')})
            rendered.append('TOOL_USE: ' + block.get('name', 'tool'))
    out['parts'] = parts
    out['line']['text'] = '\n'.join(rendered)
    return out


SHAPES = [('user', 'text'), ('text', 'user'), ('text', 'text'), ('think', 'think'), ('user', 'user'),
          ('text', 'think'), ('user', 'text', 'text'), ('think', 'text', 'user'), ('text', 'tool', 'text')]
#: Shapes only some harnesses write: Claude Code keeps a system event's text.
EXTRA_SHAPES = {'claude_code': [('user', 'system'), ('system', 'text'), ('text', 'system', 'user')]}


def _splits(key, slots):
    """Every way to cut `key` into `slots` pieces of at least five characters
    at these offsets (shorter pieces cannot be told apart from other text)."""
    for cuts in itertools.combinations((5, 12, 20, 28, len(key) - 5), slots - 1):
        bounds = (0, *cuts, len(key))
        yield [key[a:b] for a, b in zip(bounds, bounds[1:])]


def _event_prose(events):
    out = []
    for event in events:
        content = event['raw'].get('message', {}).get('content', event['raw'].get('content'))
        if isinstance(content, str):
            out.append(content)
        for block in content if isinstance(content, list) else ():
            out.extend(block[key] for key in ('text', 'thinking') if isinstance(block.get(key), str))
    return out


@pytest.mark.parametrize('harness', sorted(HARNESSES))
def test_events_redact_every_split_their_fragments_redact(harness):
    sanitize_event, lines = HARNESSES[harness]
    joined = around_a_tool = 0
    for shape, key in itertools.product(SHAPES + EXTRA_SHAPES.get(harness, []), (GITHUB, INGEST)):
        for chunks in _splits(key, len(shape)):
            texts = list(chunks)
            texts[0], texts[-1] = 'use ' + texts[0], texts[-1] + ' now'
            events = [{'line_no': i, 'raw': sanitize_event(lines[slot](text))}
                      for i, (slot, text) in enumerate(zip(shape, texts))]
            assert all(event['raw'] for event in events), (harness, shape)
            clean = _scrub_content({'events': events, 'fragments': [_fragment_of(e) for e in events]})
            in_fragments = [c for c in chunks if any(c in t for t in texts_of(clean['fragments']))]
            in_events = [c for c in chunks if any(c in t for t in _event_prose(clean['events']))]
            if 'tool' in shape:
                # A tool call between two halves is metadata: neither side joins across it.
                around_a_tool += 1
                assert in_fragments == chunks[:1] + chunks[2:] and in_events == in_fragments, (shape, chunks)
            else:
                joined += 1
                # Every line.text included; and what the fragments lost, the events lost.
                assert in_fragments == [] and in_events == [], (harness, shape, chunks, in_fragments, in_events)
            assert redact_event(clean)[0] == clean
    assert joined == (140 if harness == 'claude_code' else 100) and around_a_tool == 20


def test_an_empty_line_stays_empty_when_its_prose_is_redacted():
    """A fragment whose renderer failed carries `line.text == ""` (and
    `line_error`); there is no half to remove there, so no marker is added."""
    first, second = user(0, 'token ' + GITHUB[:20]), user(1, GITHUB[20:])
    second['line']['text'] = ''
    second['line_error'] = 'ValueError'
    clean, _ = redact_event({'fragments': [first, second]})
    assert clean['fragments'][1]['line']['text'] == ''
    assert GITHUB[20:] not in clean['fragments'][1]['message']
