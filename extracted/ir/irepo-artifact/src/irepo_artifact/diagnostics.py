"""Opt-in diagnostics with redacted URLs; no API credentials."""
import json
import sys
import threading
from urllib.parse import urlsplit, urlunsplit

_WRITE_LOCK = threading.Lock()


def safe_url(url):
    parsed = urlsplit(url)
    # Drop userinfo defensively, even though validated download URLs forbid it.
    return urlunsplit((parsed.scheme, parsed.netloc.rsplit('@', 1)[-1], parsed.path,
                       '<redacted>' if parsed.query else '', ''))


def _field(value):
    text = str(value)
    if any(c.isspace() or ord(c) < 32 or ord(c) == 127 or c in '\\"' for c in text):
        return json.dumps(text, ensure_ascii=True)
    return text


class Diagnostics:
    def __init__(self, enabled=False):
        self.enabled = enabled

    def emit(self, message, **fields):
        if not self.enabled:
            return
        try:
            line = '[irepo-artifact] ' + ' '.join(f'{k}={_field(v)}' for k, v in fields.items())
            line += ' ' + message + '\n'
            with _WRITE_LOCK:
                sys.stderr.write(line)
                sys.stderr.flush()
        except Exception:
            # Diagnostics must never replace a download result or exception.
            pass

    def request(self, path, url, body=None, **error):
        if not self.enabled:
            return
        try:
            parts = urlsplit(path).path.strip('/').split('/')
            context = {}
            if body and 'job_ids' in body:
                context['job'] = ','.join(body['job_ids'])
            elif len(parts) > 1 and parts[0] in ('jobs', 'groups'):
                context['job' if parts[0] == 'jobs' else 'group'] = parts[1]
            message = ('request_failed' if error else 'POST' if body is not None else 'GET')
            self.emit(message + ' ' + _field(safe_url(url)), **context, **error)
        except Exception:
            pass

    def links(self, job_id, targets, normalize, *, file=None):
        if not self.enabled:
            return
        try:
            for kind, target in targets.items():
                fields = {'job': job_id, 'channel': 'unknown' if kind == 'legacy' else kind}
                if file is not None:
                    fields['file'] = file
                fields['url'] = safe_url(target.url)
                internal = normalize(target.url)
                if internal != target.url:
                    fields['internal_url'] = safe_url(internal)
                self.emit('links_received', **fields)
        except Exception:
            pass
