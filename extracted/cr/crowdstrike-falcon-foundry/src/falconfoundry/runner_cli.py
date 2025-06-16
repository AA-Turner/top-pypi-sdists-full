import argparse
import json
from logging import Formatter, Logger, StreamHandler, getLogger
from sys import stdout
from typing import Dict, List, Union
from falconfoundry.context import ctx_request
from falconfoundry.mapping import canonize_header, dict_to_request, response_to_dict
from falconfoundry.model import FoundryAPIError, FoundryFDKException, FoundryRequest, FoundryResponse
from falconfoundry.runner import RunnerBase


INTERNAL_SERVER_ERROR = 500


def _new_cli_logger() -> Logger:
    f = Formatter('%(asctime)s [%(levelname)s]  %(filename)s %(funcName)s:%(lineno)d  ->  %(message)s')

    h = StreamHandler(stdout)
    h.setFormatter(f)

    logger = getLogger("cs-logger")
    logger.setLevel('DEBUG')
    logger.addHandler(h)
    return logger


class CLIRunner(RunnerBase):
    """Runs the user's request without starting an HTTP server."""
    def __init__(self):
        RunnerBase.__init__(self)
        self.logger = None
        self.headers = None
        self.data = None
        self.args = None

        self._setup_arguments()

    def _setup_arguments(self):
        self.parser = argparse.ArgumentParser(
            description=(
                "Invoke the function handler with the provided input without starting an HTTP server. "
                "When FOUNDRY_FUNCTION_RUN_MODE environment variable is set to 'cli', "
                "no HTTP server is started and the function handler is invoked directly. "
                "To run in HTTP server mode, unset FOUNDRY_FUNCTION_RUN_MODE environment variable or "
                "set it to 'http'."
            )
        )

        self.parser.add_argument(
            '-d', '--data', type=str,
            help='Path to a JSON file containing the "method", "url", and optionally the "body" fields.'
        )
        self.parser.add_argument(
            '-H', '--header', type=str, action='append', nargs='*',
            help="Optional HTTP request headers to provide to the function handler"
        )
        # This is used to simulate request file input when content-type is multipart/form-data, value must be a file
        self.parser.add_argument(
            '-f', '--file', type=str, action='append', nargs='*',
            help='Optional file input to the function handler.'
            'The "Content-Type: multipart/form-data" header must also be specified for file input.'
        )

    def _verify_arguments(self):
        self.headers = {}
        if self.args.header:
            for header in self.args.header:
                name_value = header[0].split(":")
                if len(name_value) != 2:
                    self.parser.error('Invalid header. Must be in "name: value" format.')
                self.headers[name_value[0].strip().lower()] = name_value[1].strip().lower()

        if self.args.file:
            content_type = self.headers.get('content-type', 'application/json')
            if not content_type.startswith('multipart/form-data'):
                self.parser.print_help()
                self.parser.error('Also provide "-H "Content-Type: multipart/form-data" to use the --file argument')

    def run(self, *args, **kwargs):
        self.logger = kwargs.get('logger', None)
        if self.logger is None:
            self.logger = _new_cli_logger()


        self.args = self.parser.parse_args()
        self._verify_arguments()


        self.logger.info('Running without HTTP server')
        self._exec_request()

    def _exec_request(self):
        req = self._read_request()
        ctx_request.set(req)
        try:
            resp = self.router.route(req, logger=self.logger)
        except FoundryFDKException as fe:
            resp = FoundryResponse(errors=[FoundryAPIError(code=fe.code, message=fe.message)])
        self._write_response(req, resp)

    def _read_request(self) -> FoundryRequest:
        payload = self._read_json_request()
        content_type = self.headers.get('content-type', 'application/json')
        if content_type.startswith('multipart/form-data'):
            payload['files'] = self._read_multipart_request()
        return dict_to_request(payload)

    def _read_json_request(self) -> dict:
        payload = {}
        with open(self.args.data, 'r') as fd:
            payload = json.load(fd)
        return payload

    def _read_multipart_request(self) -> dict:
        files = {}
        for file in self.args.file:
            with open(file[0], 'r') as fd:
                files[file[0]] = fd.read().encode('utf-8')
        return files

    def _write_response(self, req: FoundryRequest, resp: Union[FoundryResponse, None]):
        if resp is None or not isinstance(resp, FoundryResponse):
            msg = f'Object is not of type {FoundryResponse.__base__.__name__}. Got {type(resp)} instead.'
            resp = FoundryResponse(errors=[FoundryAPIError(code=INTERNAL_SERVER_ERROR, message=msg)])

        if resp.code == 0 and resp.errors is not None and len(resp.errors) > 0:
            for e in resp.errors:
                e_code = e.code
                if type(e_code) is not int and e_code is not None:
                    e_code = int(e_code)
                if type(e_code) is int and 100 <= e.code and resp.code < e.code < 600:
                    resp.code = e_code

        resp.header = self._resp_headers(req, resp)
        payload_dict = response_to_dict(resp)
        payload = json.dumps(payload_dict)

        print('')
        print(f'Status code: {resp.code}')
        print(f'Response Header: Content-Length: {str(len(payload))}')
        print('Response Header: Content-Type: application/json')
        for k, v in resp.header.items():
            print(f'Response Header: {k}: {v}')
        print('Response Payload: ')
        print(payload)

    def _resp_headers(self, req: FoundryRequest, resp: FoundryResponse):
        headers = {}
        if resp.header is not None and len(resp.header) > 0:
            for k, v in resp.header.items():
                if v is None or len(v) == 0:
                    continue
                headers[canonize_header(k)] = v

        if req.params is None or req.params.header is None or len(req.params.header) == 0:
            return headers

        req_header = req.params.header
        self._take_header('X-Cs-Executionid', req_header, headers)
        self._take_header('X-Cs-Origin', req_header, headers)
        self._take_header('X-Cs-Traceid', req_header, headers)

        headers = {k: ';'.join(v) for k, v in headers}
        return headers

    def _take_header(self, key: str, src_header: Dict[str, List[str]], dst_header: Dict[str, List[str]]):
        value = src_header.get(key, [])
        if len(value) == 0:
            return
        dst_header[key] = value
