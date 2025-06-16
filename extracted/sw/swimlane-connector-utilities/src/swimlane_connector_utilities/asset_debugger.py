import inspect
import socket
from inspect import getmembers, ismethod

from requests import request, head

from urllib.parse import urlparse


def check_params(f):
    '''
        This decorator is to be used on test functions for the `AssetDebugger` class that have named params.

        Decorating with this func will ensure that each of the named parameters with default `None` have
        a value in them in order to run the test.  If a value is not present for those parameters, the test
        will be ignored.

        Example:
            @check_params
            def test_func(my_param=None, **kwargs):
                ... do some tests

            test_func() => Test is passed over
            test_func(my_param="test parameter") => test runs
    '''

    def wrapper(*args, **kwargs):
        sig = inspect.getargspec(f)
        default_map = dict(zip(sig.args[1:], sig.defaults))
        if not any(kwargs.get(k) for k in default_map.keys() if not default_map.get(k)):
            return None
        else:
            return f(*args, **kwargs)
    return wrapper


class AssetDebugger(object):

    def __init__(self, asset, test_conn_exception, custom_tests):
        self.all_results = {}
        self.asset = asset
        self._add_tests(*custom_tests)
        self._results = None
        self._run_tests()
        self._add_test_connection_exception(test_conn_exception)
        self._set_results()

    def _run_tests(self):
        # Grab all no private methods on this class
        target_methods = dict(
            (
                (method_name, method_func)
                for method_name, method_func in getmembers(self, predicate=ismethod)
                if not method_name.startswith("_")
            )
        )
        for check_name, check_method in target_methods.items():
            self.all_results[check_name] = check_method(**self.asset)

    def _add_tests(self, *funcs):
        for func in funcs:
            setattr(self, func.func_name, func.__get__(self))

    def _add_test_connection_exception(self, e):
        self.all_results["connection"] = str(e)

    def _set_results(self):
        self.results = "Failed Test {}: \n\n{}\n\n\n".format('Connection',
                                                             self.all_results['connection'])
        self.all_results.pop('connection')
        self.results += "\n".join(["Failed Test {}: \n\n{}\n\n".format(" ".join(
                                    str(k).split("_")).title(),
                                    str(v))
                                    for k, v in self.all_results.items()
                                    if v not in [None, True]]
                                  )

    def _get_socket_target(self, **kwargs):
        target_keys = ["ip_address", "url", "domain", "host"]
        addr = [kwargs.get(key) for key in target_keys if kwargs.get(key)][0]
        parsed_target = urlparse(addr)
        port = kwargs.get("port") or parsed_target.port
        if not port:
            port = 443 if "https://" in addr else 80
        return parsed_target, port

    @check_params
    def curl_host(self, host=None, verify_ssl=True, http_proxy=None, **kwargs):
        # Mock a curl head request to the host
        try:
            r = head(host, verify=verify_ssl, proxies={
                "http": http_proxy,
                "https": http_proxy} if http_proxy else None)
            r.raise_for_status()
            return True
        except Exception as e:
            return e

    @check_params
    def is_verify_correct(self, host="", verify_ssl=True, http_proxy="", **kwargs):
        # Check if verify value makes sense
        if ("http://" in host or "http://" in http_proxy) and verify_ssl:
            return Exception("Found http:// in host/proxy and verify set to {}, is this correct?".format(verify_ssl))
        return True

    def no_whitespace(self, **kwargs):
        # Check for whitespace in asset values
        whitespace_found = []
        for k, v in kwargs.items():
            if isinstance(v, str):
                if " " in v or "\n" in v:
                    whitespace_found.append(k)
        if whitespace_found:
            return Exception("Whitespace found in {}".format(str(whitespace_found)))
        return True

    def socket_check(self, **kwargs):
        # Check if socket connection is possible
        if kwargs.get('http_proxy'):
            return None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        parsed_target = None
        try:
            parsed_target, port = self._get_socket_target(**kwargs)
            s.connect((socket.gethostbyname(parsed_target.hostname or parsed_target.path), port))
            s.close()
            return True
        except Exception as e:
            return Exception("Exception for socket connection: {}".format(str(e)))

    @check_params
    def proxy(self, http_proxy=None, verify_ssl=True, **kwargs):
        # Check proxy connection
        try:
            r = request(method="get", url="https://google.com", verify=verify_ssl, proxies={
                "http": http_proxy,
                "https": http_proxy
            } if http_proxy else None)
            r.raise_for_status()
            return True
        except Exception as e:
            return e

    @check_params
    def valid_email_address(self, email="", **kwargs):
        # Check if email address is valid
        import re
        res = bool(re.search(r"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,})+)$", email))
        if res:
            return True
        return Exception("Email {} is invalid".format(email))
