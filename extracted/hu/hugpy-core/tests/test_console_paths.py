"""What Core serves at the root: its prefixes, the console, and nothing that only looks like an answer."""
import json

from hugpy_core.web import ui


def test_only_the_console_s_own_pages_get_the_console_page(tmp_path):
    (tmp_path / 'index.html').write_text('<html>console</html>')
    (tmp_path / 'assets').mkdir()
    (tmp_path / 'assets' / 'app.js').write_text('console.log(1)')
    reached = []

    def api(environ, start_response):
        reached.append((environ['SCRIPT_NAME'], environ['PATH_INFO']))
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [b'[]']

    app = ui.ConsoleApp(api, str(tmp_path))

    def get(path, method='GET'):
        seen = {}

        def start(line, headers):
            seen.update(status=int(line.split()[0]), type=dict(headers).get('Content-Type', ''))
        body = b''.join(app({'PATH_INFO': path, 'REQUEST_METHOD': method, 'SCRIPT_NAME': ''}, start))
        return seen['status'], seen['type'].split(';')[0], body

    for page in ('/', '/console', '/console/workers', '/docs', '/login', '/guest', '/media/chat'):
        assert get(page)[:2] == (200, 'text/html'), page
    assert get('/assets/app.js')[0] == 200

    # a control route called without its prefix is the caller's mistake, said plainly
    for wrong in ('/llm/workers', '/models', '/fleet/workers', '/keys', '/assets/missing.js'):
        status, kind, body = get(wrong)
        assert (status, kind) == (404, 'application/json'), wrong
    assert '/api/llm/workers' in json.loads(get('/llm/workers')[2])['error']['message']
    assert get('/keys', 'POST')[:2] == (404, 'application/json')
    assert reached == []                                   # none of that reached the API

    assert get('/api/llm/workers')[0] == 200 and reached[-1] == ('/api', '/llm/workers')
    assert get('/v1/models')[0] == 200 and reached[-1] == ('', '/v1/models')
    status, kind, body = get('/health')
    assert (status, kind) == (200, 'application/json') and json.loads(body)['ok'] is True


def test_a_page_below_its_entry_point_goes_to_browsers_only():
    def pages(environ, start_response):          # a single-page app: its page for every path under it
        if environ['PATH_INFO'].endswith('.js'):
            start_response('200 OK', [('Content-Type', 'text/javascript')])
            return [b'js']
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [b'<html>video</html>']

    app = ui.PagesForBrowsers(pages)

    def get(path, accept=None):
        seen = {}
        environ = {'PATH_INFO': path, 'REQUEST_METHOD': 'GET', **({'HTTP_ACCEPT': accept} if accept else {})}
        body = b''.join(app(environ, lambda line, headers: seen.update(
            status=int(line.split()[0]), type=dict(headers).get('Content-Type', '').split(';')[0])))
        return seen['status'], seen['type'], body

    browser = 'text/html,application/xhtml+xml,*/*;q=0.8'
    assert get('/video/jobs/7', browser) == (200, 'text/html', b'<html>video</html>')     # a deep link, reloaded
    for program in (None, '*/*', 'application/json'):
        status, kind, body = get('/video/jobs/7', program)                              # the same path, no /api
        assert (status, kind) == (404, 'application/json') and b'/api/video/jobs/7' in body
    assert get('/video/', '*/*')[:2] == (200, 'text/html')                              # the page itself: anyone
    assert get('/console', None)[:2] == (200, 'text/html')
    assert get('/video/assets/app.js', None) == (200, 'text/javascript', b'js')          # files: anyone
