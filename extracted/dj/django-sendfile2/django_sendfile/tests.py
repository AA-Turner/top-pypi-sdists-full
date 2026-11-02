# coding=utf-8

from tempfile import mkdtemp
from urllib.parse import unquote
import os
import shutil

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.encoding import smart_str

from .utils import _get_sendfile
from .utils import sendfile as real_sendfile


def sendfile(request, filename, **kwargs):
    # just a simple response with the filename
    # as content - so we can test without a backend active
    return HttpResponse(filename)


class TempFileTestCase(TestCase):

    def setUp(self):
        super(TempFileTestCase, self).setUp()
        self.TEMP_FILE = mkdtemp()
        self.TEMP_FILE_ROOT = os.path.join(self.TEMP_FILE, "root")
        os.mkdir(self.TEMP_FILE_ROOT)
        settings.SENDFILE_ROOT = self.TEMP_FILE_ROOT
        _get_sendfile.cache_clear()

    def tearDown(self):
        super(TempFileTestCase, self).tearDown()
        if os.path.exists(self.TEMP_FILE_ROOT):
            shutil.rmtree(self.TEMP_FILE_ROOT)

    def ensure_file(self, filename):
        path = os.path.join(self.TEMP_FILE_ROOT, filename)
        if not os.path.exists(path):
            open(path, 'w').close()
        return path


@override_settings(SENDFILE_BACKEND='django_sendfile.tests')
class TestSendfile(TempFileTestCase):

    def _get_readme(self):
        return self.ensure_file('testfile.txt')

    @override_settings(SENDFILE_BACKEND=None)
    def test_backend_is_none(self):
        with self.assertRaises(ImproperlyConfigured):
            real_sendfile(HttpRequest(), "notafile.txt")

    @override_settings(SENDFILE_ROOT=None)
    def test_root_is_none(self):
        with self.assertRaises(ImproperlyConfigured):
            real_sendfile(HttpRequest(), "notafile.txt")

    def test_404(self):
        with self.assertRaises(Http404):
            real_sendfile(HttpRequest(), 'fhdsjfhjk.txt')

    def test_sendfile(self):
        response = real_sendfile(HttpRequest(), self._get_readme())
        self.assertEqual(response.status_code, 200)
        self.assertEqual('text/plain', response['Content-Type'])
        self.assertEqual('inline; filename="testfile.txt"', response['Content-Disposition'])
        self.assertEqual(self._get_readme(), smart_str(response.content))
        # file is actually empty, so 0 is correct
        self.assertEqual('0', response['Content-Length'])

    def test_set_mimetype(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), mimetype='text/plain')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('text/plain', response['Content-Type'])

    def test_set_encoding(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), encoding='utf8')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('utf8', response['Content-Encoding'])

    def test_inline_filename(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment_filename='tests.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('inline; filename="tests.txt"', response['Content-Disposition'])

    def test_attachment(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('attachment; filename="testfile.txt"', response['Content-Disposition'])

    def test_attachment_filename_false(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('attachment', response['Content-Disposition'])

    def test_attachment_filename(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename='tests.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('attachment; filename="tests.txt"', response['Content-Disposition'])

    def test_attachment_filename_unicode(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename='test’s.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('attachment; filename="tests.txt"; filename*=UTF-8\'\'test%E2%80%99s.txt',
                         response['Content-Disposition'])

    def test_attachment_filename_with_space(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename='space test’s.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            'attachment; filename="space tests.txt"; filename*=UTF-8\'\'space%20test%E2%80%99s.txt',
            response['Content-Disposition']
        )

    def test_cve_2022_36359(self):
        # test that we're not vulnerable to cve-2022-36359.  data from
        # https://github.com/django/django/commit/bd062445cffd3f6cc6dcd20d13e2abed818fa173
        tests = [
            (
                'multi-part-one";\" dummy".txt',
                r"multi-part-one\";\" dummy\".txt"
            ),
            (
                'multi-part-one\\";\" dummy".txt',
                r"multi-part-one\\\";\" dummy\".txt"
            ),
            (
                'multi-part-one\\";\\\" dummy".txt',
                r"multi-part-one\\\";\\\" dummy\".txt"
            ),
        ]
        for filename, escaped in tests:
            with self.subTest(filename=filename, escaped=escaped):
                response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                         attachment_filename=filename)
                self.assertIsNotNone(response)
                self.assertEqual(
                    f'attachment; filename="{escaped}"',
                    response['Content-Disposition']
                )

    def test_guess_mimetype_none(self):
        response = real_sendfile(HttpRequest(), self.ensure_file('bluh.bluh'))
        self.assertEqual('application/octet-stream', response['Content-Type'])

    @override_settings(SENDFILE_CHECK_FILE_EXISTS=False)
    def test_dont_check_file_exists(self):
        response = real_sendfile(HttpRequest(), 'bluh.bluh')
        self.assertEqual('application/octet-stream', response['Content-Type'])

    def test_manually_set_content_length(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), content_length=123)
        self.assertEqual(str(123), response['Content-Length'])


@override_settings(SENDFILE_BACKEND='django_sendfile.backends.development')
class TestDevelopmentSendfileBackend(TempFileTestCase):

    def test_correct_file(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        response.close()  # prevent resource warning from occurring

    @override_settings(SENDFILE_CHECK_FILE_EXISTS=False)
    def test_check_file_exists_still_raises_error(self):
        filepath = "file/does/not/exist"
        with self.assertRaises(Http404):
            real_sendfile(HttpRequest(), filepath)


@override_settings(SENDFILE_BACKEND='django_sendfile.backends.simple')
class TestSimpleSendfileBackend(TempFileTestCase):

    def test_correct_file(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)

    def test_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)

    def test_sensible_file_access_in_simplesendfile(self):
        filepath = self.ensure_file('../passwd')
        with self.assertRaises(Http404):
            real_sendfile(HttpRequest(), filepath)

    @override_settings(SENDFILE_CHECK_FILE_EXISTS=False)
    def test_check_file_exists_still_raises_error(self):
        filepath = "file/does/not/exist"
        with self.assertRaises(Http404):
            real_sendfile(HttpRequest(), filepath)

    def test_last_modified(self):
        request = HttpRequest()
        request.method = 'GET'
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(request, filepath)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Last-Modified", response)

        request.META['HTTP_IF_MODIFIED_SINCE'] = response['Last-Modified']
        response = real_sendfile(request, filepath)
        self.assertEqual(response.status_code, 304)

    def test_etag(self):
        request = HttpRequest()
        request.method = 'GET'
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(request, filepath)
        self.assertEqual(response.status_code, 200)
        self.assertIn("ETag", response)

        request.META['HTTP_IF_NONE_MATCH'] = response['ETag']
        response = real_sendfile(request, filepath)
        self.assertEqual(response.status_code, 304)


@override_settings(SENDFILE_BACKEND='django_sendfile.backends.xsendfile')
class TestXSendfileBackend(TempFileTestCase):

    def test_correct_file_in_xsendfile_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(filepath, response['X-Sendfile'])

    def test_xsendfile_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(smart_str(filepath), response['X-Sendfile'])


@override_settings(
    SENDFILE_BACKEND='django_sendfile.backends.nginx',
    SENDFILE_URL='/private',
)
class TestNginxBackend(TempFileTestCase):

    @override_settings(SENDFILE_URL=None)
    def test_sendfile_url_not_set(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual(os.path.join(self.TEMP_FILE_ROOT, 'readme.txt'),
                         response['X-Accel-Redirect'])

    def test_correct_url_in_xaccelredirect_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/readme.txt', response['X-Accel-Redirect'])

    def test_xaccelredirect_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/péter_là_gueule.txt', unquote(response['X-Accel-Redirect']))


@override_settings(
    SENDFILE_BACKEND='django_sendfile.backends.mod_wsgi',
    SENDFILE_URL='/private',
)
class TestModWsgiBackend(TempFileTestCase):

    @override_settings(SENDFILE_URL=None)
    def test_sendfile_url_not_set(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual(os.path.join(self.TEMP_FILE_ROOT, 'readme.txt'),
                         response['Location'])

    def test_correct_url_in_location_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/readme.txt', response['Location'])

    def test_location_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/péter_là_gueule.txt', unquote(response['Location']))
