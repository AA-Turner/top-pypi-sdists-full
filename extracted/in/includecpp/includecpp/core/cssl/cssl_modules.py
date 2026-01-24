"""
CSSL Standard Modules
Provides standard library modules accessible via service-include

Available Modules:
  @Time    - Date, time, and duration operations
  @Secrets - Secure credential and secret management
  @Math    - Mathematical operations and constants
  @Crypto  - Cryptographic functions (hashing, encoding)
  @Net     - Network operations (HTTP, sockets)
  @IO      - File and stream I/O operations
  @JSON    - JSON parsing and serialization
  @Regex   - Regular expression operations
  @System  - System information and process control
  @Log     - Logging and diagnostics
  @Cache   - In-memory caching with TTL support
  @Queue   - Message queue and task scheduling
  @Format  - String formatting and templating
  @Desktop - Desktop widget creation (registered separately)
"""

import os
import time
import math
import json
import re
import hashlib
import base64
import secrets
import threading
import queue
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable, Union


class CSSLModuleBase:
    """Base class for CSSL standard modules"""

    def __init__(self, runtime=None):
        self.runtime = runtime
        self._methods: Dict[str, Callable] = {}
        self._register_methods()

    def _register_methods(self):
        """Override to register module methods"""
        pass

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        if name in self._methods:
            return self._methods[name]
        raise AttributeError(f"Module has no method '{name}'")

    def get_method(self, name: str) -> Optional[Callable]:
        return self._methods.get(name)

    def list_methods(self) -> List[str]:
        return sorted(self._methods.keys())


# =============================================================================
# @Time Module - Date, time, and duration operations
# =============================================================================

class TimeModule(CSSLModuleBase):
    """
    @Time - Date, time, and duration operations

    Methods:
      now()                    - Current timestamp (float)
      timestamp()              - Current timestamp (int)
      date(fmt)                - Current date string
      time(fmt)                - Current time string
      datetime(fmt)            - Current datetime string
      parse(str, fmt)          - Parse string to timestamp
      format(ts, fmt)          - Format timestamp to string
      add(ts, days, hours, minutes, seconds) - Add duration
      diff(ts1, ts2)           - Difference in seconds
      sleep(seconds)           - Sleep for duration
      year(), month(), day()   - Current date components
      hour(), minute(), second() - Current time components
      weekday()                - Day of week (0=Monday)
      iso()                    - ISO 8601 formatted string
      utc()                    - Current UTC timestamp
    """

    def _register_methods(self):
        self._methods['now'] = self.now
        self._methods['timestamp'] = self.timestamp
        self._methods['date'] = self.date
        self._methods['time'] = self.time_str
        self._methods['datetime'] = self.datetime_str
        self._methods['parse'] = self.parse
        self._methods['format'] = self.format
        self._methods['add'] = self.add
        self._methods['diff'] = self.diff
        self._methods['sleep'] = self.sleep
        self._methods['year'] = self.year
        self._methods['month'] = self.month
        self._methods['day'] = self.day
        self._methods['hour'] = self.hour
        self._methods['minute'] = self.minute
        self._methods['second'] = self.second
        self._methods['weekday'] = self.weekday
        self._methods['iso'] = self.iso
        self._methods['utc'] = self.utc

    def now(self) -> float:
        return time.time()

    def timestamp(self) -> int:
        return int(time.time())

    def date(self, fmt: str = '%Y-%m-%d') -> str:
        return datetime.now().strftime(fmt)

    def time_str(self, fmt: str = '%H:%M:%S') -> str:
        return datetime.now().strftime(fmt)

    def datetime_str(self, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        return datetime.now().strftime(fmt)

    def parse(self, date_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> float:
        return datetime.strptime(date_str, fmt).timestamp()

    def format(self, ts: float, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
        return datetime.fromtimestamp(ts).strftime(fmt)

    def add(self, ts: float = None, days: int = 0, hours: int = 0,
            minutes: int = 0, seconds: int = 0) -> float:
        if ts is None:
            ts = time.time()
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return ts + delta.total_seconds()

    def diff(self, ts1: float, ts2: float) -> float:
        return abs(ts1 - ts2)

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)

    def year(self) -> int:
        return datetime.now().year

    def month(self) -> int:
        return datetime.now().month

    def day(self) -> int:
        return datetime.now().day

    def hour(self) -> int:
        return datetime.now().hour

    def minute(self) -> int:
        return datetime.now().minute

    def second(self) -> int:
        return datetime.now().second

    def weekday(self) -> int:
        return datetime.now().weekday()

    def iso(self) -> str:
        return datetime.now().isoformat()

    def utc(self) -> float:
        return datetime.utcnow().timestamp()


# =============================================================================
# @Secrets Module - Secure credential and secret management
# =============================================================================

class SecretsModule(CSSLModuleBase):
    """
    @Secrets - Secure credential and secret management

    Methods:
      generate(length)         - Generate secure random string
      token(nbytes)            - Generate secure token (hex)
      token_bytes(nbytes)      - Generate secure random bytes
      token_urlsafe(nbytes)    - Generate URL-safe token
      choice(seq)              - Secure random choice
      randint(a, b)            - Secure random integer
      compare(a, b)            - Constant-time string comparison
      store(key, value)        - Store secret (memory only)
      retrieve(key)            - Retrieve stored secret
      delete(key)              - Delete stored secret
      env(name, default)       - Get environment variable
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._store: Dict[str, str] = {}

    def _register_methods(self):
        self._methods['generate'] = self.generate
        self._methods['token'] = self.token
        self._methods['token_bytes'] = self.token_bytes
        self._methods['token_urlsafe'] = self.token_urlsafe
        self._methods['choice'] = self.choice
        self._methods['randint'] = self.randint
        self._methods['compare'] = self.compare
        self._methods['store'] = self.store
        self._methods['retrieve'] = self.retrieve
        self._methods['delete'] = self.delete
        self._methods['env'] = self.env

    def generate(self, length: int = 32) -> str:
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def token(self, nbytes: int = 32) -> str:
        return secrets.token_hex(nbytes)

    def token_bytes(self, nbytes: int = 32) -> bytes:
        return secrets.token_bytes(nbytes)

    def token_urlsafe(self, nbytes: int = 32) -> str:
        return secrets.token_urlsafe(nbytes)

    def choice(self, seq: list) -> Any:
        return secrets.choice(seq)

    def randint(self, a: int, b: int) -> int:
        return secrets.randbelow(b - a + 1) + a

    def compare(self, a: str, b: str) -> bool:
        return secrets.compare_digest(a, b)

    def store(self, key: str, value: str) -> bool:
        self._store[key] = value
        return True

    def retrieve(self, key: str) -> Optional[str]:
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def env(self, name: str, default: str = None) -> Optional[str]:
        return os.environ.get(name, default)


# =============================================================================
# @Math Module - Mathematical operations and constants
# =============================================================================

class MathModule(CSSLModuleBase):
    """
    @Math - Mathematical operations and constants

    Constants:
      PI, E, TAU, INF, NAN

    Methods:
      abs(x)                   - Absolute value
      ceil(x)                  - Ceiling
      floor(x)                 - Floor
      round(x, digits)         - Round to digits
      trunc(x)                 - Truncate
      sqrt(x)                  - Square root
      pow(x, y)                - Power
      exp(x)                   - Exponential
      log(x, base)             - Logarithm
      log10(x)                 - Log base 10
      log2(x)                  - Log base 2
      sin(x), cos(x), tan(x)   - Trigonometric
      asin(x), acos(x), atan(x) - Inverse trig
      sinh(x), cosh(x), tanh(x) - Hyperbolic
      degrees(x)               - Radians to degrees
      radians(x)               - Degrees to radians
      min(args), max(args)     - Min/max values
      sum(list), avg(list)     - Aggregations
      factorial(n)             - Factorial
      gcd(a, b)                - Greatest common divisor
      lcm(a, b)                - Least common multiple
      clamp(x, lo, hi)         - Clamp value to range
      lerp(a, b, t)            - Linear interpolation
      random()                 - Random float [0, 1)
      randint(a, b)            - Random integer [a, b]
    """

    def _register_methods(self):
        # Constants
        self._methods['PI'] = lambda: math.pi
        self._methods['E'] = lambda: math.e
        self._methods['TAU'] = lambda: math.tau
        self._methods['INF'] = lambda: math.inf
        self._methods['NAN'] = lambda: math.nan

        # Basic operations
        self._methods['abs'] = abs
        self._methods['ceil'] = math.ceil
        self._methods['floor'] = math.floor
        self._methods['round'] = round
        self._methods['trunc'] = math.trunc
        self._methods['sqrt'] = math.sqrt
        self._methods['pow'] = pow
        self._methods['exp'] = math.exp
        self._methods['log'] = self.log
        self._methods['log10'] = math.log10
        self._methods['log2'] = math.log2

        # Trigonometry
        self._methods['sin'] = math.sin
        self._methods['cos'] = math.cos
        self._methods['tan'] = math.tan
        self._methods['asin'] = math.asin
        self._methods['acos'] = math.acos
        self._methods['atan'] = math.atan
        self._methods['atan2'] = math.atan2
        self._methods['sinh'] = math.sinh
        self._methods['cosh'] = math.cosh
        self._methods['tanh'] = math.tanh
        self._methods['degrees'] = math.degrees
        self._methods['radians'] = math.radians

        # Aggregations
        self._methods['min'] = min
        self._methods['max'] = max
        self._methods['sum'] = sum
        self._methods['avg'] = self.avg

        # Number theory
        self._methods['factorial'] = math.factorial
        self._methods['gcd'] = math.gcd
        self._methods['lcm'] = self.lcm
        self._methods['isfinite'] = math.isfinite
        self._methods['isinf'] = math.isinf
        self._methods['isnan'] = math.isnan

        # Utility
        self._methods['clamp'] = self.clamp
        self._methods['lerp'] = self.lerp
        self._methods['random'] = self.random
        self._methods['randint'] = self.randint

    def log(self, x: float, base: float = math.e) -> float:
        return math.log(x, base)

    def avg(self, items: list) -> float:
        if not items:
            return 0.0
        return sum(items) / len(items)

    def lcm(self, a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b)

    def clamp(self, x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    def lerp(self, a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def random(self) -> float:
        import random
        return random.random()

    def randint(self, a: int, b: int) -> int:
        import random
        return random.randint(a, b)


# =============================================================================
# @Crypto Module - Cryptographic functions
# =============================================================================

class CryptoModule(CSSLModuleBase):
    """
    @Crypto - Cryptographic functions

    Methods:
      md5(data)                - MD5 hash
      sha1(data)               - SHA-1 hash
      sha256(data)             - SHA-256 hash
      sha384(data)             - SHA-384 hash
      sha512(data)             - SHA-512 hash
      hmac(key, data, algo)    - HMAC signature
      base64_encode(data)      - Base64 encode
      base64_decode(data)      - Base64 decode
      hex_encode(data)         - Hex encode
      hex_decode(data)         - Hex decode
      uuid()                   - Generate UUID4
      uuid1()                  - Generate UUID1
    """

    def _register_methods(self):
        self._methods['md5'] = self.md5
        self._methods['sha1'] = self.sha1
        self._methods['sha256'] = self.sha256
        self._methods['sha384'] = self.sha384
        self._methods['sha512'] = self.sha512
        self._methods['hmac'] = self.hmac
        self._methods['base64_encode'] = self.base64_encode
        self._methods['base64_decode'] = self.base64_decode
        self._methods['hex_encode'] = self.hex_encode
        self._methods['hex_decode'] = self.hex_decode
        self._methods['uuid'] = self.uuid
        self._methods['uuid1'] = self.uuid1

    def _to_bytes(self, data: Union[str, bytes]) -> bytes:
        if isinstance(data, str):
            return data.encode('utf-8')
        return data

    def md5(self, data: Union[str, bytes]) -> str:
        return hashlib.md5(self._to_bytes(data)).hexdigest()

    def sha1(self, data: Union[str, bytes]) -> str:
        return hashlib.sha1(self._to_bytes(data)).hexdigest()

    def sha256(self, data: Union[str, bytes]) -> str:
        return hashlib.sha256(self._to_bytes(data)).hexdigest()

    def sha384(self, data: Union[str, bytes]) -> str:
        return hashlib.sha384(self._to_bytes(data)).hexdigest()

    def sha512(self, data: Union[str, bytes]) -> str:
        return hashlib.sha512(self._to_bytes(data)).hexdigest()

    def hmac(self, key: Union[str, bytes], data: Union[str, bytes],
             algo: str = 'sha256') -> str:
        import hmac as hmac_lib
        hash_func = getattr(hashlib, algo, hashlib.sha256)
        return hmac_lib.new(
            self._to_bytes(key),
            self._to_bytes(data),
            hash_func
        ).hexdigest()

    def base64_encode(self, data: Union[str, bytes]) -> str:
        return base64.b64encode(self._to_bytes(data)).decode('utf-8')

    def base64_decode(self, data: str) -> str:
        return base64.b64decode(data).decode('utf-8')

    def hex_encode(self, data: Union[str, bytes]) -> str:
        return self._to_bytes(data).hex()

    def hex_decode(self, data: str) -> str:
        return bytes.fromhex(data).decode('utf-8')

    def uuid(self) -> str:
        import uuid
        return str(uuid.uuid4())

    def uuid1(self) -> str:
        import uuid
        return str(uuid.uuid1())


# =============================================================================
# @Net Module - Network operations
# =============================================================================

class NetModule(CSSLModuleBase):
    """
    @Net - Network operations

    Methods:
      get(url, headers)        - HTTP GET request
      post(url, data, headers) - HTTP POST request
      put(url, data, headers)  - HTTP PUT request
      delete(url, headers)     - HTTP DELETE request
      download(url, path)      - Download file
      hostname()               - Get local hostname
      ip()                     - Get local IP address
      ping(host)               - Check if host is reachable
      url_encode(data)         - URL encode string/dict
      url_decode(data)         - URL decode string
      parse_url(url)           - Parse URL into components
    """

    def _register_methods(self):
        self._methods['get'] = self.http_get
        self._methods['post'] = self.http_post
        self._methods['put'] = self.http_put
        self._methods['delete'] = self.http_delete
        self._methods['download'] = self.download
        self._methods['hostname'] = self.hostname
        self._methods['ip'] = self.ip
        self._methods['ping'] = self.ping
        self._methods['url_encode'] = self.url_encode
        self._methods['url_decode'] = self.url_decode
        self._methods['parse_url'] = self.parse_url

    def http_get(self, url: str, headers: Dict = None) -> Dict:
        try:
            import urllib.request
            import urllib.error
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'body': resp.read().decode('utf-8')
                }
        except urllib.error.HTTPError as e:
            return {'status': e.code, 'error': str(e), 'body': ''}
        except Exception as e:
            return {'status': 0, 'error': str(e), 'body': ''}

    def http_post(self, url: str, data: Union[str, Dict] = None,
                  headers: Dict = None) -> Dict:
        try:
            import urllib.request
            import urllib.error
            if isinstance(data, dict):
                data = json.dumps(data).encode('utf-8')
                headers = headers or {}
                headers['Content-Type'] = 'application/json'
            elif isinstance(data, str):
                data = data.encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers or {})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'body': resp.read().decode('utf-8')
                }
        except urllib.error.HTTPError as e:
            return {'status': e.code, 'error': str(e), 'body': ''}
        except Exception as e:
            return {'status': 0, 'error': str(e), 'body': ''}

    def http_put(self, url: str, data: Union[str, Dict] = None,
                 headers: Dict = None) -> Dict:
        try:
            import urllib.request
            if isinstance(data, dict):
                data = json.dumps(data).encode('utf-8')
                headers = headers or {}
                headers['Content-Type'] = 'application/json'
            elif isinstance(data, str):
                data = data.encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers or {},
                                         method='PUT')
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'body': resp.read().decode('utf-8')
                }
        except Exception as e:
            return {'status': 0, 'error': str(e), 'body': ''}

    def http_delete(self, url: str, headers: Dict = None) -> Dict:
        try:
            import urllib.request
            req = urllib.request.Request(url, headers=headers or {},
                                         method='DELETE')
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {
                    'status': resp.status,
                    'headers': dict(resp.headers),
                    'body': resp.read().decode('utf-8')
                }
        except Exception as e:
            return {'status': 0, 'error': str(e), 'body': ''}

    def download(self, url: str, path: str) -> bool:
        try:
            import urllib.request
            urllib.request.urlretrieve(url, path)
            return True
        except Exception:
            return False

    def hostname(self) -> str:
        import socket
        return socket.gethostname()

    def ip(self) -> str:
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return '127.0.0.1'

    def ping(self, host: str) -> bool:
        import subprocess
        import platform
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        try:
            result = subprocess.run(
                ['ping', param, '1', host],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def url_encode(self, data: Union[str, Dict]) -> str:
        import urllib.parse
        if isinstance(data, dict):
            return urllib.parse.urlencode(data)
        return urllib.parse.quote(str(data))

    def url_decode(self, data: str) -> str:
        import urllib.parse
        return urllib.parse.unquote(data)

    def parse_url(self, url: str) -> Dict:
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'hostname': parsed.hostname,
            'port': parsed.port
        }


# =============================================================================
# @IO Module - File and stream I/O operations
# =============================================================================

class IOModule(CSSLModuleBase):
    """
    @IO - File and stream I/O operations

    Methods:
      read(path)               - Read entire file
      read_lines(path)         - Read file as lines
      read_bytes(path)         - Read file as bytes
      write(path, content)     - Write content to file
      write_lines(path, lines) - Write lines to file
      write_bytes(path, data)  - Write bytes to file
      append(path, content)    - Append to file
      exists(path)             - Check if path exists
      isfile(path)             - Check if path is file
      isdir(path)              - Check if path is directory
      mkdir(path)              - Create directory
      mkdirs(path)             - Create directory tree
      remove(path)             - Remove file
      rmdir(path)              - Remove directory
      rename(old, new)         - Rename file/directory
      copy(src, dst)           - Copy file
      move(src, dst)           - Move file
      listdir(path)            - List directory contents
      glob(pattern)            - Find files by pattern
      size(path)               - Get file size
      mtime(path)              - Get modification time
    """

    def _register_methods(self):
        self._methods['read'] = self.read
        self._methods['read_lines'] = self.read_lines
        self._methods['read_bytes'] = self.read_bytes
        self._methods['write'] = self.write
        self._methods['write_lines'] = self.write_lines
        self._methods['write_bytes'] = self.write_bytes
        self._methods['append'] = self.append
        self._methods['exists'] = os.path.exists
        self._methods['isfile'] = os.path.isfile
        self._methods['isdir'] = os.path.isdir
        self._methods['mkdir'] = self.mkdir
        self._methods['mkdirs'] = self.mkdirs
        self._methods['remove'] = self.remove
        self._methods['rmdir'] = self.rmdir
        self._methods['rename'] = os.rename
        self._methods['copy'] = self.copy
        self._methods['move'] = self.move
        self._methods['listdir'] = os.listdir
        self._methods['glob'] = self.glob
        self._methods['size'] = self.size
        self._methods['mtime'] = self.mtime

    def read(self, path: str, encoding: str = 'utf-8') -> str:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()

    def read_lines(self, path: str, encoding: str = 'utf-8') -> List[str]:
        with open(path, 'r', encoding=encoding) as f:
            return f.readlines()

    def read_bytes(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

    def write(self, path: str, content: str, encoding: str = 'utf-8') -> bool:
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        return True

    def write_lines(self, path: str, lines: List[str],
                    encoding: str = 'utf-8') -> bool:
        with open(path, 'w', encoding=encoding) as f:
            f.writelines(lines)
        return True

    def write_bytes(self, path: str, data: bytes) -> bool:
        with open(path, 'wb') as f:
            f.write(data)
        return True

    def append(self, path: str, content: str, encoding: str = 'utf-8') -> bool:
        with open(path, 'a', encoding=encoding) as f:
            f.write(content)
        return True

    def mkdir(self, path: str) -> bool:
        os.makedirs(path, exist_ok=True)
        return True

    def mkdirs(self, path: str) -> bool:
        os.makedirs(path, exist_ok=True)
        return True

    def remove(self, path: str) -> bool:
        if os.path.isfile(path):
            os.remove(path)
            return True
        return False

    def rmdir(self, path: str) -> bool:
        import shutil
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        return False

    def copy(self, src: str, dst: str) -> bool:
        import shutil
        shutil.copy2(src, dst)
        return True

    def move(self, src: str, dst: str) -> bool:
        import shutil
        shutil.move(src, dst)
        return True

    def glob(self, pattern: str) -> List[str]:
        import glob as glob_module
        return glob_module.glob(pattern, recursive=True)

    def size(self, path: str) -> int:
        return os.path.getsize(path)

    def mtime(self, path: str) -> float:
        return os.path.getmtime(path)


# =============================================================================
# @JSON Module - JSON parsing and serialization
# =============================================================================

class JSONModule(CSSLModuleBase):
    """
    @JSON - JSON parsing and serialization

    Methods:
      parse(string)            - Parse JSON string to object
      stringify(obj, indent)   - Convert object to JSON string
      read(path)               - Read JSON file
      write(path, obj, indent) - Write JSON file
      valid(string)            - Check if string is valid JSON
      get(obj, path, default)  - Get nested value by path
      set(obj, path, value)    - Set nested value by path
      merge(obj1, obj2)        - Deep merge two objects
    """

    def _register_methods(self):
        self._methods['parse'] = self.parse
        self._methods['stringify'] = self.stringify
        self._methods['read'] = self.read_file
        self._methods['write'] = self.write_file
        self._methods['valid'] = self.valid
        self._methods['get'] = self.get_path
        self._methods['set'] = self.set_path
        self._methods['merge'] = self.merge

    def parse(self, string: str) -> Any:
        return json.loads(string)

    def stringify(self, obj: Any, indent: int = None) -> str:
        return json.dumps(obj, indent=indent, ensure_ascii=False)

    def read_file(self, path: str) -> Any:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_file(self, path: str, obj: Any, indent: int = 2) -> bool:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=indent, ensure_ascii=False)
        return True

    def valid(self, string: str) -> bool:
        try:
            json.loads(string)
            return True
        except Exception:
            return False

    def get_path(self, obj: Any, path: str, default: Any = None) -> Any:
        keys = path.split('.')
        current = obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        return current

    def set_path(self, obj: Dict, path: str, value: Any) -> Dict:
        keys = path.split('.')
        current = obj
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
        return obj

    def merge(self, obj1: Dict, obj2: Dict) -> Dict:
        result = obj1.copy()
        for key, value in obj2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge(result[key], value)
            else:
                result[key] = value
        return result


# =============================================================================
# @Regex Module - Regular expression operations
# =============================================================================

class RegexModule(CSSLModuleBase):
    """
    @Regex - Regular expression operations

    Methods:
      match(pattern, string)   - Match pattern at start
      search(pattern, string)  - Search for pattern anywhere
      findall(pattern, string) - Find all matches
      finditer(pattern, string)- Iterate over matches
      sub(pattern, repl, string, count) - Substitute matches
      split(pattern, string)   - Split by pattern
      escape(string)           - Escape special characters
      compile(pattern, flags)  - Compile pattern
      test(pattern, string)    - Test if pattern matches
    """

    def _register_methods(self):
        self._methods['match'] = self.match
        self._methods['search'] = self.search
        self._methods['findall'] = re.findall
        self._methods['finditer'] = self.finditer
        self._methods['sub'] = re.sub
        self._methods['split'] = re.split
        self._methods['escape'] = re.escape
        self._methods['compile'] = re.compile
        self._methods['test'] = self.test

    def match(self, pattern: str, string: str) -> Optional[Dict]:
        m = re.match(pattern, string)
        if m:
            return {
                'match': m.group(),
                'groups': m.groups(),
                'start': m.start(),
                'end': m.end(),
                'span': m.span()
            }
        return None

    def search(self, pattern: str, string: str) -> Optional[Dict]:
        m = re.search(pattern, string)
        if m:
            return {
                'match': m.group(),
                'groups': m.groups(),
                'start': m.start(),
                'end': m.end(),
                'span': m.span()
            }
        return None

    def finditer(self, pattern: str, string: str) -> List[Dict]:
        return [{
            'match': m.group(),
            'groups': m.groups(),
            'start': m.start(),
            'end': m.end()
        } for m in re.finditer(pattern, string)]

    def test(self, pattern: str, string: str) -> bool:
        return re.search(pattern, string) is not None


# =============================================================================
# @System Module - System information and process control
# =============================================================================

class SystemModule(CSSLModuleBase):
    """
    @System - System information and process control

    Methods:
      platform()               - Operating system name
      version()                - OS version
      arch()                   - CPU architecture
      hostname()               - Computer hostname
      user()                   - Current username
      home()                   - User home directory
      cwd()                    - Current working directory
      chdir(path)              - Change directory
      env(name, default)       - Get environment variable
      setenv(name, value)      - Set environment variable
      exec(cmd)                - Execute shell command
      spawn(cmd)               - Spawn background process
      pid()                    - Current process ID
      cpus()                   - Number of CPUs
      memory()                 - Memory info
      uptime()                 - System uptime
      exit(code)               - Exit with code
    """

    def _register_methods(self):
        self._methods['platform'] = self.platform
        self._methods['version'] = self.version
        self._methods['arch'] = self.arch
        self._methods['hostname'] = self.hostname
        self._methods['user'] = self.user
        self._methods['home'] = self.home
        self._methods['cwd'] = os.getcwd
        self._methods['chdir'] = os.chdir
        self._methods['env'] = self.env
        self._methods['setenv'] = self.setenv
        self._methods['exec'] = self.exec_cmd
        self._methods['spawn'] = self.spawn
        self._methods['pid'] = os.getpid
        self._methods['cpus'] = self.cpus
        self._methods['memory'] = self.memory
        self._methods['uptime'] = self.uptime
        self._methods['exit'] = self.exit_sys

    def platform(self) -> str:
        import platform
        return platform.system()

    def version(self) -> str:
        import platform
        return platform.version()

    def arch(self) -> str:
        import platform
        return platform.machine()

    def hostname(self) -> str:
        import socket
        return socket.gethostname()

    def user(self) -> str:
        return os.environ.get('USER') or os.environ.get('USERNAME', '')

    def home(self) -> str:
        return os.path.expanduser('~')

    def env(self, name: str, default: str = None) -> Optional[str]:
        return os.environ.get(name, default)

    def setenv(self, name: str, value: str) -> bool:
        os.environ[name] = value
        return True

    def exec_cmd(self, cmd: str) -> Dict:
        import subprocess
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=300
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'returncode': -1, 'stdout': '', 'stderr': 'Command timed out'}
        except Exception as e:
            return {'returncode': -1, 'stdout': '', 'stderr': str(e)}

    def spawn(self, cmd: str) -> int:
        import subprocess
        proc = subprocess.Popen(cmd, shell=True)
        return proc.pid

    def cpus(self) -> int:
        return os.cpu_count() or 1

    def memory(self) -> Dict:
        try:
            import psutil
            mem = psutil.virtual_memory()
            return {
                'total': mem.total,
                'available': mem.available,
                'used': mem.used,
                'percent': mem.percent
            }
        except ImportError:
            return {'total': 0, 'available': 0, 'used': 0, 'percent': 0}

    def uptime(self) -> float:
        try:
            import psutil
            return time.time() - psutil.boot_time()
        except ImportError:
            return 0.0

    def exit_sys(self, code: int = 0) -> None:
        raise SystemExit(code)


# =============================================================================
# @Log Module - Logging and diagnostics
# =============================================================================

class LogModule(CSSLModuleBase):
    """
    @Log - Logging and diagnostics

    Methods:
      debug(msg)               - Debug level message
      info(msg)                - Info level message
      warn(msg)                - Warning level message
      error(msg)               - Error level message
      fatal(msg)               - Fatal level message
      log(level, msg)          - Log with custom level
      setLevel(level)          - Set minimum log level
      setOutput(path)          - Set log file output
      setFormat(fmt)           - Set log format
      clear()                  - Clear log buffer
      history(count)           - Get recent log entries
    """

    LEVELS = {'DEBUG': 0, 'INFO': 1, 'WARN': 2, 'ERROR': 3, 'FATAL': 4}

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._level = 'DEBUG'
        self._output = None
        self._format = '[{timestamp}] [{level}] {message}'
        self._history: List[Dict] = []
        self._max_history = 1000

    def _register_methods(self):
        self._methods['debug'] = self.debug
        self._methods['info'] = self.info
        self._methods['warn'] = self.warn
        self._methods['error'] = self.error
        self._methods['fatal'] = self.fatal
        self._methods['log'] = self.log
        self._methods['setLevel'] = self.setLevel
        self._methods['setOutput'] = self.setOutput
        self._methods['setFormat'] = self.setFormat
        self._methods['clear'] = self.clear
        self._methods['history'] = self.history

    def _write(self, level: str, msg: str):
        if self.LEVELS.get(level, 0) < self.LEVELS.get(self._level, 0):
            return

        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': msg
        }

        formatted = self._format.format(**entry)
        print(formatted)

        self._history.append(entry)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        if self._output:
            try:
                with open(self._output, 'a', encoding='utf-8') as f:
                    f.write(formatted + '\n')
            except Exception:
                pass

    def debug(self, msg: str):
        self._write('DEBUG', msg)

    def info(self, msg: str):
        self._write('INFO', msg)

    def warn(self, msg: str):
        self._write('WARN', msg)

    def error(self, msg: str):
        self._write('ERROR', msg)

    def fatal(self, msg: str):
        self._write('FATAL', msg)

    def log(self, level: str, msg: str):
        self._write(level.upper(), msg)

    def setLevel(self, level: str) -> bool:
        if level.upper() in self.LEVELS:
            self._level = level.upper()
            return True
        return False

    def setOutput(self, path: str) -> bool:
        self._output = path
        return True

    def setFormat(self, fmt: str) -> bool:
        self._format = fmt
        return True

    def clear(self):
        self._history.clear()

    def history(self, count: int = 100) -> List[Dict]:
        return self._history[-count:]


# =============================================================================
# @Cache Module - In-memory caching with TTL support
# =============================================================================

class CacheModule(CSSLModuleBase):
    """
    @Cache - In-memory caching with TTL support

    Methods:
      get(key, default)        - Get cached value
      set(key, value, ttl)     - Set value with optional TTL (seconds)
      has(key)                 - Check if key exists and not expired
      delete(key)              - Delete cached value
      clear()                  - Clear all cached values
      keys()                   - Get all cache keys
      size()                   - Get number of cached items
      stats()                  - Get cache statistics
      cleanup()                - Remove expired entries
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._cache: Dict[str, Dict] = {}
        self._hits = 0
        self._misses = 0

    def _register_methods(self):
        self._methods['get'] = self.get
        self._methods['set'] = self.set
        self._methods['has'] = self.has
        self._methods['delete'] = self.delete
        self._methods['clear'] = self.clear
        self._methods['keys'] = self.keys
        self._methods['size'] = self.size
        self._methods['stats'] = self.stats
        self._methods['cleanup'] = self.cleanup

    def _is_expired(self, entry: Dict) -> bool:
        if entry.get('ttl') is None:
            return False
        return time.time() > entry['expires']

    def get(self, key: str, default: Any = None) -> Any:
        entry = self._cache.get(key)
        if entry is None or self._is_expired(entry):
            self._misses += 1
            if entry:
                del self._cache[key]
            return default
        self._hits += 1
        return entry['value']

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        entry = {'value': value, 'ttl': ttl}
        if ttl is not None:
            entry['expires'] = time.time() + ttl
        self._cache[key] = entry
        return True

    def has(self, key: str) -> bool:
        entry = self._cache.get(key)
        if entry is None:
            return False
        if self._is_expired(entry):
            del self._cache[key]
            return False
        return True

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self):
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def keys(self) -> List[str]:
        self.cleanup()
        return list(self._cache.keys())

    def size(self) -> int:
        self.cleanup()
        return len(self._cache)

    def stats(self) -> Dict:
        return {
            'size': len(self._cache),
            'hits': self._hits,
            'misses': self._misses,
            'hit_rate': self._hits / (self._hits + self._misses) if (self._hits + self._misses) > 0 else 0
        }

    def cleanup(self):
        expired = [k for k, v in self._cache.items() if self._is_expired(v)]
        for k in expired:
            del self._cache[k]


# =============================================================================
# @Queue Module - Message queue and task scheduling
# =============================================================================

class QueueModule(CSSLModuleBase):
    """
    @Queue - Message queue and task scheduling

    Methods:
      create(name)             - Create a named queue
      push(name, item)         - Push item to queue
      pop(name, timeout)       - Pop item from queue (blocking)
      peek(name)               - Peek at front item without removing
      size(name)               - Get queue size
      empty(name)              - Check if queue is empty
      clear(name)              - Clear queue
      list()                   - List all queue names
      delete(name)             - Delete a queue
      schedule(func, delay)    - Schedule function execution
      interval(func, interval) - Repeat function at interval
      cancel(task_id)          - Cancel scheduled task
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._queues: Dict[str, queue.Queue] = {}
        self._tasks: Dict[str, threading.Timer] = {}
        self._task_counter = 0

    def _register_methods(self):
        self._methods['create'] = self.create
        self._methods['push'] = self.push
        self._methods['pop'] = self.pop
        self._methods['peek'] = self.peek
        self._methods['size'] = self.size
        self._methods['empty'] = self.empty
        self._methods['clear'] = self.clear
        self._methods['list'] = self.list_queues
        self._methods['delete'] = self.delete
        self._methods['schedule'] = self.schedule
        self._methods['interval'] = self.interval
        self._methods['cancel'] = self.cancel

    def create(self, name: str) -> bool:
        if name not in self._queues:
            self._queues[name] = queue.Queue()
        return True

    def push(self, name: str, item: Any) -> bool:
        self.create(name)
        self._queues[name].put(item)
        return True

    def pop(self, name: str, timeout: float = None) -> Any:
        if name not in self._queues:
            return None
        try:
            return self._queues[name].get(timeout=timeout)
        except queue.Empty:
            return None

    def peek(self, name: str) -> Any:
        if name not in self._queues:
            return None
        q = self._queues[name]
        if q.empty():
            return None
        # Peek without removing
        with q.mutex:
            if q.queue:
                return q.queue[0]
        return None

    def size(self, name: str) -> int:
        if name not in self._queues:
            return 0
        return self._queues[name].qsize()

    def empty(self, name: str) -> bool:
        if name not in self._queues:
            return True
        return self._queues[name].empty()

    def clear(self, name: str) -> bool:
        if name in self._queues:
            with self._queues[name].mutex:
                self._queues[name].queue.clear()
        return True

    def list_queues(self) -> List[str]:
        return list(self._queues.keys())

    def delete(self, name: str) -> bool:
        if name in self._queues:
            del self._queues[name]
            return True
        return False

    def schedule(self, func: Callable, delay: float) -> str:
        self._task_counter += 1
        task_id = f"task_{self._task_counter}"
        timer = threading.Timer(delay, func)
        self._tasks[task_id] = timer
        timer.start()
        return task_id

    def interval(self, func: Callable, interval_secs: float) -> str:
        self._task_counter += 1
        task_id = f"interval_{self._task_counter}"

        def repeat():
            if task_id in self._tasks:
                func()
                timer = threading.Timer(interval_secs, repeat)
                self._tasks[task_id] = timer
                timer.start()

        timer = threading.Timer(interval_secs, repeat)
        self._tasks[task_id] = timer
        timer.start()
        return task_id

    def cancel(self, task_id: str) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id].cancel()
            del self._tasks[task_id]
            return True
        return False


# =============================================================================
# @Format Module - String formatting and templating
# =============================================================================

class FormatModule(CSSLModuleBase):
    """
    @Format - String formatting and templating

    Methods:
      sprintf(fmt, args)       - C-style sprintf formatting
      format(template, kwargs) - Python format string
      template(tmpl, vars)     - Simple ${var} template substitution
      pad(str, width, char, align) - Pad string to width
      truncate(str, maxlen, ellipsis) - Truncate with ellipsis
      wrap(str, width)         - Word wrap text
      indent(str, spaces)      - Indent each line
      dedent(str)              - Remove common leading whitespace
      upper(str)               - Convert to uppercase
      lower(str)               - Convert to lowercase
      title(str)               - Convert to title case
      camel(str)               - Convert to camelCase
      snake(str)               - Convert to snake_case
      kebab(str)               - Convert to kebab-case
      bytes(n, decimals)       - Format bytes as human readable
      number(n, decimals, sep) - Format number with separators
      currency(n, symbol)      - Format as currency
      percent(n, decimals)     - Format as percentage
    """

    def _register_methods(self):
        self._methods['sprintf'] = self.sprintf
        self._methods['format'] = self.format_str
        self._methods['template'] = self.template
        self._methods['pad'] = self.pad
        self._methods['truncate'] = self.truncate
        self._methods['wrap'] = self.wrap
        self._methods['indent'] = self.indent
        self._methods['dedent'] = self.dedent
        self._methods['upper'] = str.upper
        self._methods['lower'] = str.lower
        self._methods['title'] = str.title
        self._methods['camel'] = self.camel
        self._methods['snake'] = self.snake
        self._methods['kebab'] = self.kebab
        self._methods['bytes'] = self.format_bytes
        self._methods['number'] = self.format_number
        self._methods['currency'] = self.currency
        self._methods['percent'] = self.percent

    def sprintf(self, fmt: str, *args) -> str:
        return fmt % args

    def format_str(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def template(self, tmpl: str, vars: Dict) -> str:
        result = tmpl
        for key, value in vars.items():
            result = result.replace('${' + key + '}', str(value))
        return result

    def pad(self, s: str, width: int, char: str = ' ', align: str = 'right') -> str:
        if align == 'left':
            return s.ljust(width, char)
        elif align == 'center':
            return s.center(width, char)
        return s.rjust(width, char)

    def truncate(self, s: str, maxlen: int, ellipsis: str = '...') -> str:
        if len(s) <= maxlen:
            return s
        return s[:maxlen - len(ellipsis)] + ellipsis

    def wrap(self, s: str, width: int = 80) -> str:
        import textwrap
        return '\n'.join(textwrap.wrap(s, width))

    def indent(self, s: str, spaces: int = 4) -> str:
        prefix = ' ' * spaces
        return '\n'.join(prefix + line for line in s.split('\n'))

    def dedent(self, s: str) -> str:
        import textwrap
        return textwrap.dedent(s)

    def camel(self, s: str) -> str:
        words = re.split(r'[-_\s]+', s)
        return words[0].lower() + ''.join(w.capitalize() for w in words[1:])

    def snake(self, s: str) -> str:
        s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
        s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
        return re.sub(r'[-\s]+', '_', s).lower()

    def kebab(self, s: str) -> str:
        return self.snake(s).replace('_', '-')

    def format_bytes(self, n: int, decimals: int = 2) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if abs(n) < 1024:
                return f"{n:.{decimals}f} {unit}"
            n /= 1024
        return f"{n:.{decimals}f} EB"

    def format_number(self, n: float, decimals: int = 2, sep: str = ',') -> str:
        parts = f"{n:.{decimals}f}".split('.')
        parts[0] = re.sub(r'(\d)(?=(\d{3})+$)', r'\1' + sep, parts[0])
        return '.'.join(parts)

    def currency(self, n: float, symbol: str = '$') -> str:
        return f"{symbol}{self.format_number(abs(n), 2)}"

    def percent(self, n: float, decimals: int = 1) -> str:
        return f"{n * 100:.{decimals}f}%"


# =============================================================================
# @Console Module - Terminal/Console operations
# =============================================================================

class ConsoleModule(CSSLModuleBase):
    """
    @Console - Terminal/Console operations

    Methods:
      clear()                  - Clear console screen
      print(text, color)       - Print with optional color
      println(text, color)     - Print line with optional color
      table(data, headers)     - Print formatted table
      progress(current, total, width) - Show progress bar
      spinner(message)         - Show loading spinner
      prompt(message, default) - Prompt for input
      confirm(message)         - Yes/No confirmation
      select(message, options) - Select from options menu
      color(text, color)       - Colorize text
      bold(text)               - Bold text
      dim(text)                - Dim text
      underline(text)          - Underlined text
      cursor_hide()            - Hide cursor
      cursor_show()            - Show cursor
      cursor_move(x, y)        - Move cursor to position
      beep()                   - Terminal beep
    """

    COLORS = {
        'black': '30', 'red': '31', 'green': '32', 'yellow': '33',
        'blue': '34', 'magenta': '35', 'cyan': '36', 'white': '37',
        'bright_black': '90', 'bright_red': '91', 'bright_green': '92',
        'bright_yellow': '93', 'bright_blue': '94', 'bright_magenta': '95',
        'bright_cyan': '96', 'bright_white': '97',
        'reset': '0', 'bold': '1', 'dim': '2', 'italic': '3',
        'underline': '4', 'blink': '5', 'reverse': '7'
    }

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._spinner_running = False
        self._spinner_thread = None

    def _register_methods(self):
        self._methods['clear'] = self.clear
        self._methods['print'] = self.print_styled
        self._methods['println'] = self.println_styled
        self._methods['table'] = self.print_table
        self._methods['progress'] = self.show_progress
        self._methods['spinner'] = self.show_spinner
        self._methods['spinner_stop'] = self.stop_spinner
        self._methods['prompt'] = self.prompt
        self._methods['confirm'] = self.confirm
        self._methods['select'] = self.select_menu
        self._methods['color'] = self.colorize
        self._methods['bold'] = self.bold
        self._methods['dim'] = self.dim
        self._methods['underline'] = self.underline_text
        self._methods['cursor_hide'] = self.cursor_hide
        self._methods['cursor_show'] = self.cursor_show
        self._methods['cursor_move'] = self.cursor_move
        self._methods['beep'] = self.beep

    def clear(self):
        """Clear the console screen using ANSI escape codes (works on all modern terminals)."""
        print('\033[2J\033[H', end='', flush=True)

    def print_styled(self, text: str, color: str = None) -> None:
        """Print text with optional color."""
        if color:
            text = self.colorize(text, color)
        print(text, end='')

    def println_styled(self, text: str, color: str = None) -> None:
        """Print line with optional color."""
        if color:
            text = self.colorize(text, color)
        print(text)

    def print_table(self, data: List[Dict], headers: List[str] = None) -> None:
        """Print a formatted table."""
        if not data:
            print("(no data)")
            return

        # Auto-detect headers from first row if not provided
        if headers is None:
            if isinstance(data[0], dict):
                headers = list(data[0].keys())
            else:
                headers = [f"Col {i+1}" for i in range(len(data[0]))]

        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in data:
            if isinstance(row, dict):
                values = [str(row.get(h, '')) for h in headers]
            else:
                values = [str(v) for v in row]
            for i, v in enumerate(values):
                if i < len(widths):
                    widths[i] = max(widths[i], len(v))

        # Print header
        sep = '+-' + '-+-'.join('-' * w for w in widths) + '-+'
        print(sep)
        header_line = '| ' + ' | '.join(h.ljust(widths[i]) for i, h in enumerate(headers)) + ' |'
        print(header_line)
        print(sep)

        # Print rows
        for row in data:
            if isinstance(row, dict):
                values = [str(row.get(h, '')) for h in headers]
            else:
                values = [str(v) for v in row]
            row_line = '| ' + ' | '.join(v.ljust(widths[i]) for i, v in enumerate(values) if i < len(widths)) + ' |'
            print(row_line)

        print(sep)

    def show_progress(self, current: int, total: int, width: int = 40, show_text: bool = True) -> None:
        """Show a progress bar."""
        if total <= 0:
            return
        percent = min(100, current * 100 // total)
        filled = int(width * current // total)
        bar = '█' * filled + '░' * (width - filled)
        if show_text:
            print(f'\r[{bar}] {percent}% ({current}/{total})', end='', flush=True)
        else:
            print(f'\r[{bar}]', end='', flush=True)
        if current >= total:
            print()

    def show_spinner(self, message: str = "Loading") -> None:
        """Show a loading spinner."""
        self._spinner_running = True
        spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

        def spin():
            i = 0
            while self._spinner_running:
                print(f'\r{spinners[i % len(spinners)]} {message}...', end='', flush=True)
                time.sleep(0.1)
                i += 1
            print('\r' + ' ' * (len(message) + 10) + '\r', end='')

        self._spinner_thread = threading.Thread(target=spin, daemon=True)
        self._spinner_thread.start()

    def stop_spinner(self) -> None:
        """Stop the loading spinner."""
        self._spinner_running = False
        if self._spinner_thread:
            self._spinner_thread.join(timeout=1)
            self._spinner_thread = None

    def prompt(self, message: str, default: str = '') -> str:
        """Prompt for user input."""
        if default:
            result = input(f"{message} [{default}]: ")
            return result if result else default
        return input(f"{message}: ")

    def confirm(self, message: str) -> bool:
        """Yes/No confirmation prompt."""
        result = input(f"{message} (y/n): ").lower().strip()
        return result in ('y', 'yes', 'ja', 'j', '1', 'true')

    def select_menu(self, message: str, options: List[str]) -> int:
        """Select from options menu. Returns index of selected option."""
        print(f"\n{message}")
        for i, opt in enumerate(options):
            print(f"  {i + 1}. {opt}")
        while True:
            try:
                choice = int(input("\nWahl: "))
                if 1 <= choice <= len(options):
                    return choice - 1
            except ValueError:
                pass
            print("Ungültige Auswahl, bitte erneut versuchen.")

    def colorize(self, text: str, color: str) -> str:
        """Apply ANSI color to text."""
        code = self.COLORS.get(color.lower(), color)
        return f'\033[{code}m{text}\033[0m'

    def bold(self, text: str) -> str:
        """Make text bold."""
        return f'\033[1m{text}\033[0m'

    def dim(self, text: str) -> str:
        """Make text dim."""
        return f'\033[2m{text}\033[0m'

    def underline_text(self, text: str) -> str:
        """Underline text."""
        return f'\033[4m{text}\033[0m'

    def cursor_hide(self) -> None:
        """Hide cursor."""
        print('\033[?25l', end='')

    def cursor_show(self) -> None:
        """Show cursor."""
        print('\033[?25h', end='')

    def cursor_move(self, x: int, y: int) -> None:
        """Move cursor to position."""
        print(f'\033[{y};{x}H', end='')

    def beep(self) -> None:
        """Terminal beep."""
        print('\a', end='')


# =============================================================================
# @Process Module - Process and subprocess management
# =============================================================================

class ProcessModule(CSSLModuleBase):
    """
    @Process - Process and subprocess management

    Methods:
      run(cmd, timeout, cwd)   - Run command and wait for result
      spawn(cmd, cwd)          - Spawn background process
      kill(pid)                - Kill process by PID
      list()                   - List running processes
      pid()                    - Get current process ID
      ppid()                   - Get parent process ID
      exists(pid)              - Check if process exists
      wait(pid, timeout)       - Wait for process to finish
      shell(cmd)               - Run in system shell
      popen(cmd, cwd)          - Open process for streaming
      read_stdout(handle)      - Read from process stdout
      write_stdin(handle, data) - Write to process stdin
      close(handle)            - Close process handle
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._handles: Dict[int, Any] = {}
        self._handle_counter = 0

    def _register_methods(self):
        self._methods['run'] = self.run_command
        self._methods['spawn'] = self.spawn_process
        self._methods['kill'] = self.kill_process
        self._methods['list'] = self.list_processes
        self._methods['pid'] = lambda: os.getpid()
        self._methods['ppid'] = lambda: os.getppid()
        self._methods['exists'] = self.process_exists
        self._methods['wait'] = self.wait_for_process
        self._methods['shell'] = self.shell_command
        self._methods['popen'] = self.popen_process
        self._methods['read_stdout'] = self.read_stdout
        self._methods['write_stdin'] = self.write_stdin
        self._methods['close'] = self.close_handle

    def run_command(self, cmd: Union[str, List[str]], timeout: float = 300, cwd: str = None) -> Dict:
        """Run command and wait for result."""
        import subprocess
        try:
            result = subprocess.run(
                cmd,
                shell=isinstance(cmd, str),
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {'returncode': -1, 'stdout': '', 'stderr': 'Command timed out', 'success': False}
        except Exception as e:
            return {'returncode': -1, 'stdout': '', 'stderr': str(e), 'success': False}

    def spawn_process(self, cmd: Union[str, List[str]], cwd: str = None) -> int:
        """Spawn background process, returns PID."""
        import subprocess
        proc = subprocess.Popen(
            cmd,
            shell=isinstance(cmd, str),
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return proc.pid

    def kill_process(self, pid: int) -> bool:
        """Kill process by PID."""
        try:
            os.kill(pid, 9)  # SIGKILL
            return True
        except OSError:
            return False

    def list_processes(self) -> List[Dict]:
        """List running processes."""
        try:
            import psutil
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    processes.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'cpu': info['cpu_percent'],
                        'memory': info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return processes
        except ImportError:
            # Fallback without psutil
            import subprocess
            if os.name == 'nt':
                result = subprocess.run(['tasklist', '/fo', 'csv'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')[1:]
                processes = []
                for line in lines:
                    parts = line.strip('"').split('","')
                    if len(parts) >= 2:
                        processes.append({'name': parts[0], 'pid': int(parts[1])})
                return processes
            else:
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                lines = result.stdout.strip().split('\n')[1:]
                processes = []
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 11:
                        processes.append({
                            'user': parts[0],
                            'pid': int(parts[1]),
                            'cpu': float(parts[2]),
                            'memory': float(parts[3]),
                            'name': parts[10]
                        })
                return processes

    def process_exists(self, pid: int) -> bool:
        """Check if process exists."""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def wait_for_process(self, pid: int, timeout: float = None) -> int:
        """Wait for process to finish, returns exit code."""
        import subprocess
        try:
            if os.name == 'nt':
                # Windows
                import subprocess
                result = subprocess.run(['tasklist', '/fi', f'pid eq {pid}'], capture_output=True, text=True)
                start = time.time()
                while str(pid) in result.stdout:
                    if timeout and (time.time() - start) > timeout:
                        return -1
                    time.sleep(0.5)
                    result = subprocess.run(['tasklist', '/fi', f'pid eq {pid}'], capture_output=True, text=True)
                return 0
            else:
                # Unix
                os.waitpid(pid, 0)
                return 0
        except Exception:
            return -1

    def shell_command(self, cmd: str) -> int:
        """Run command in system shell, returns exit code."""
        import subprocess
        result = subprocess.run(cmd, shell=True)
        return result.returncode

    def popen_process(self, cmd: Union[str, List[str]], cwd: str = None) -> int:
        """Open process for streaming, returns handle ID."""
        import subprocess
        proc = subprocess.Popen(
            cmd,
            shell=isinstance(cmd, str),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )
        self._handle_counter += 1
        self._handles[self._handle_counter] = proc
        return self._handle_counter

    def read_stdout(self, handle: int, timeout: float = None) -> Optional[str]:
        """Read from process stdout."""
        proc = self._handles.get(handle)
        if not proc:
            return None
        try:
            import select
            if hasattr(select, 'select'):
                # Unix
                ready, _, _ = select.select([proc.stdout], [], [], timeout or 0)
                if ready:
                    return proc.stdout.readline()
            return proc.stdout.readline()
        except Exception:
            return None

    def write_stdin(self, handle: int, data: str) -> bool:
        """Write to process stdin."""
        proc = self._handles.get(handle)
        if not proc:
            return False
        try:
            proc.stdin.write(data)
            proc.stdin.flush()
            return True
        except Exception:
            return False

    def close_handle(self, handle: int) -> bool:
        """Close process handle."""
        proc = self._handles.get(handle)
        if not proc:
            return False
        try:
            proc.terminate()
            del self._handles[handle]
            return True
        except Exception:
            return False


# =============================================================================
# @Config Module - Configuration file management
# =============================================================================

class ConfigModule(CSSLModuleBase):
    """
    @Config - Configuration file management (JSON, INI, ENV)

    Methods:
      load(path)               - Load config file (auto-detect format)
      save(path, data)         - Save config file
      loadJSON(path)           - Load JSON config
      saveJSON(path, data)     - Save JSON config
      loadINI(path)            - Load INI config
      saveINI(path, data)      - Save INI config
      loadENV(path)            - Load .env file
      saveENV(path, data)      - Save .env file
      get(key, default)        - Get config value by key path
      set(key, value)          - Set config value by key path
      has(key)                 - Check if key exists
      delete(key)              - Delete config key
      merge(config)            - Merge config into current
      reload()                 - Reload from file
      env(name, default)       - Get environment variable
      setenv(name, value)      - Set environment variable
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._config: Dict[str, Any] = {}
        self._file_path: Optional[str] = None

    def _register_methods(self):
        self._methods['load'] = self.load
        self._methods['save'] = self.save
        self._methods['loadJSON'] = self.load_json
        self._methods['saveJSON'] = self.save_json
        self._methods['loadINI'] = self.load_ini
        self._methods['saveINI'] = self.save_ini
        self._methods['loadENV'] = self.load_env
        self._methods['saveENV'] = self.save_env
        self._methods['get'] = self.get_value
        self._methods['set'] = self.set_value
        self._methods['has'] = self.has_key
        self._methods['delete'] = self.delete_key
        self._methods['merge'] = self.merge_config
        self._methods['reload'] = self.reload
        self._methods['env'] = self.get_env
        self._methods['setenv'] = self.set_env
        self._methods['all'] = lambda: dict(self._config)

    def load(self, path: str) -> Dict:
        """Load config file, auto-detecting format."""
        self._file_path = path
        ext = os.path.splitext(path)[1].lower()

        if ext == '.json':
            return self.load_json(path)
        elif ext in ('.ini', '.cfg', '.conf'):
            return self.load_ini(path)
        elif ext == '.env' or os.path.basename(path).startswith('.env'):
            return self.load_env(path)
        else:
            # Try JSON first, then INI
            try:
                return self.load_json(path)
            except:
                try:
                    return self.load_ini(path)
                except:
                    return {}

    def save(self, path: str = None, data: Dict = None) -> bool:
        """Save config file."""
        path = path or self._file_path
        if not path:
            return False

        data = data if data is not None else self._config
        ext = os.path.splitext(path)[1].lower()

        if ext == '.json':
            return self.save_json(path, data)
        elif ext in ('.ini', '.cfg', '.conf'):
            return self.save_ini(path, data)
        elif ext == '.env' or os.path.basename(path).startswith('.env'):
            return self.save_env(path, data)
        else:
            return self.save_json(path, data)

    def load_json(self, path: str) -> Dict:
        """Load JSON config."""
        with open(path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)
        self._file_path = path
        return self._config

    def save_json(self, path: str, data: Dict = None) -> bool:
        """Save JSON config."""
        data = data if data is not None else self._config
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    def load_ini(self, path: str) -> Dict:
        """Load INI config."""
        import configparser
        parser = configparser.ConfigParser()
        parser.read(path, encoding='utf-8')

        config = {}
        for section in parser.sections():
            config[section] = dict(parser.items(section))

        # Handle DEFAULT section
        if parser.defaults():
            config['DEFAULT'] = dict(parser.defaults())

        self._config = config
        self._file_path = path
        return config

    def save_ini(self, path: str, data: Dict = None) -> bool:
        """Save INI config."""
        import configparser
        data = data if data is not None else self._config
        parser = configparser.ConfigParser()

        for section, values in data.items():
            if section.upper() == 'DEFAULT':
                for key, value in values.items():
                    parser['DEFAULT'][key] = str(value)
            else:
                parser[section] = {k: str(v) for k, v in values.items()}

        with open(path, 'w', encoding='utf-8') as f:
            parser.write(f)
        return True

    def load_env(self, path: str) -> Dict:
        """Load .env file."""
        config = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    config[key] = value
                    # Also set in environment
                    os.environ[key] = value

        self._config = config
        self._file_path = path
        return config

    def save_env(self, path: str, data: Dict = None) -> bool:
        """Save .env file."""
        data = data if data is not None else self._config
        with open(path, 'w', encoding='utf-8') as f:
            for key, value in data.items():
                # Quote values with spaces
                if ' ' in str(value):
                    value = f'"{value}"'
                f.write(f"{key}={value}\n")
        return True

    def get_value(self, key: str, default: Any = None) -> Any:
        """Get config value by key path (e.g., 'section.key')."""
        keys = key.split('.')
        current = self._config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def set_value(self, key: str, value: Any) -> bool:
        """Set config value by key path."""
        keys = key.split('.')
        current = self._config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        return True

    def has_key(self, key: str) -> bool:
        """Check if key exists."""
        return self.get_value(key, _MISSING) is not _MISSING

    def delete_key(self, key: str) -> bool:
        """Delete config key."""
        keys = key.split('.')
        current = self._config
        for k in keys[:-1]:
            if k not in current:
                return False
            current = current[k]
        if keys[-1] in current:
            del current[keys[-1]]
            return True
        return False

    def merge_config(self, config: Dict) -> Dict:
        """Merge config into current."""
        def deep_merge(base, overlay):
            for key, value in overlay.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
        deep_merge(self._config, config)
        return self._config

    def reload(self) -> Dict:
        """Reload from file."""
        if self._file_path and os.path.exists(self._file_path):
            return self.load(self._file_path)
        return self._config

    def get_env(self, name: str, default: str = None) -> Optional[str]:
        """Get environment variable."""
        return os.environ.get(name, default)

    def set_env(self, name: str, value: str) -> bool:
        """Set environment variable."""
        os.environ[name] = value
        return True


# Sentinel for missing values
class _MissingSentinel:
    pass
_MISSING = _MissingSentinel()


# =============================================================================
# @Server Module - HTTP Server for APIs and static files
# =============================================================================

class ServerModule(CSSLModuleBase):
    """
    @Server - HTTP Server for web APIs and static files

    Methods:
      run(port, host)          - Start HTTP server
      stop()                   - Stop the server
      api(path, method)        - Register API endpoint
      static(path, dir)        - Serve static files
      showServer()             - Display server information
      getConnections()         - Get active connections count
      getRoutes()              - List registered routes
      status()                 - Get server status
      setErrorHandler(func)    - Set custom error handler
      setCORS(origins)         - Configure CORS

    Example:
      @Server <== get('Server');
      @Server.run(port=3030);

      @Server.api('/status') <== {
          define handler {
              return { "status": "ok" };
          }
      };
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._server = None
        self._server_thread = None
        self._port = 8080
        self._host = '0.0.0.0'
        self._running = False
        self._routes: Dict[str, Dict] = {}
        self._static_dirs: Dict[str, str] = {}
        self._connections = 0
        self._cors_origins = ['*']
        self._error_handler = None

    def _register_methods(self):
        self._methods['run'] = self.run
        self._methods['stop'] = self.stop
        self._methods['api'] = self.api
        self._methods['static'] = self.static
        self._methods['showServer'] = self.show_server
        self._methods['getConnections'] = self.get_connections
        self._methods['getRoutes'] = self.get_routes
        self._methods['status'] = self.status
        self._methods['setErrorHandler'] = self.set_error_handler
        self._methods['setCORS'] = self.set_cors

    def run(self, port: int = 8080, host: str = '0.0.0.0') -> bool:
        """Start the HTTP server."""
        if self._running:
            print(f"[Server] Already running on {self._host}:{self._port}")
            return False

        self._port = port
        self._host = host

        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import socket

            module_ref = self

            class CSSLRequestHandler(BaseHTTPRequestHandler):
                def log_message(self, format, *args):
                    # Custom logging
                    print(f"[Server] {self.address_string()} - {format % args}")

                def _send_response(self, status: int, body: Any, content_type: str = 'application/json'):
                    self.send_response(status)
                    self.send_header('Content-Type', content_type)
                    # CORS headers
                    origin = self.headers.get('Origin', '*')
                    if '*' in module_ref._cors_origins or origin in module_ref._cors_origins:
                        self.send_header('Access-Control-Allow-Origin', origin)
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()

                    if isinstance(body, dict) or isinstance(body, list):
                        body = json.dumps(body, ensure_ascii=False)
                    if isinstance(body, str):
                        body = body.encode('utf-8')
                    self.wfile.write(body)

                def _handle_request(self, method: str):
                    module_ref._connections += 1
                    try:
                        path = self.path.split('?')[0]

                        # Check API routes
                        route_key = f"{method}:{path}"
                        if route_key in module_ref._routes:
                            route = module_ref._routes[route_key]
                            handler = route.get('handler')

                            # Parse request body
                            content_length = int(self.headers.get('Content-Length', 0))
                            body = None
                            if content_length > 0:
                                raw_body = self.rfile.read(content_length)
                                try:
                                    body = json.loads(raw_body.decode('utf-8'))
                                except:
                                    body = raw_body.decode('utf-8')

                            # Build request object
                            request = {
                                'method': method,
                                'path': path,
                                'headers': dict(self.headers),
                                'query': self._parse_query(),
                                'body': body
                            }

                            # Call handler
                            if callable(handler):
                                try:
                                    result = handler(request)
                                    self._send_response(200, result)
                                except Exception as e:
                                    if module_ref._error_handler:
                                        result = module_ref._error_handler(e)
                                        self._send_response(500, result)
                                    else:
                                        self._send_response(500, {'error': str(e)})
                            else:
                                self._send_response(200, handler)
                            return

                        # Check static directories
                        for url_path, dir_path in module_ref._static_dirs.items():
                            if path.startswith(url_path):
                                file_path = path[len(url_path):].lstrip('/')
                                full_path = os.path.join(dir_path, file_path)
                                if os.path.isfile(full_path):
                                    self._serve_file(full_path)
                                    return

                        # 404 Not Found
                        self._send_response(404, {'error': 'Not Found', 'path': path})

                    finally:
                        module_ref._connections -= 1

                def _parse_query(self) -> Dict:
                    from urllib.parse import urlparse, parse_qs
                    query = urlparse(self.path).query
                    return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()}

                def _serve_file(self, path: str):
                    import mimetypes
                    mime_type = mimetypes.guess_type(path)[0] or 'application/octet-stream'
                    try:
                        with open(path, 'rb') as f:
                            content = f.read()
                        self._send_response(200, content, mime_type)
                    except Exception as e:
                        self._send_response(500, {'error': str(e)})

                def do_GET(self):
                    self._handle_request('GET')

                def do_POST(self):
                    self._handle_request('POST')

                def do_PUT(self):
                    self._handle_request('PUT')

                def do_DELETE(self):
                    self._handle_request('DELETE')

                def do_OPTIONS(self):
                    # CORS preflight
                    self.send_response(200)
                    origin = self.headers.get('Origin', '*')
                    if '*' in module_ref._cors_origins or origin in module_ref._cors_origins:
                        self.send_header('Access-Control-Allow-Origin', origin)
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.send_header('Access-Control-Max-Age', '86400')
                    self.end_headers()

            # Create server with SO_REUSEADDR
            class ReusableTCPServer(HTTPServer):
                allow_reuse_address = True

            self._server = ReusableTCPServer((host, port), CSSLRequestHandler)
            self._running = True

            # Start server in thread
            def serve():
                print(f"[Server] Started on http://{host}:{port}")
                self._server.serve_forever()

            self._server_thread = threading.Thread(target=serve, daemon=True)
            self._server_thread.start()

            return True

        except Exception as e:
            print(f"[Server] Failed to start: {e}")
            return False

    def stop(self) -> bool:
        """Stop the HTTP server."""
        if not self._running or not self._server:
            print("[Server] Not running")
            return False

        try:
            self._server.shutdown()
            self._running = False
            print("[Server] Stopped")
            return True
        except Exception as e:
            print(f"[Server] Error stopping: {e}")
            return False

    def api(self, path: str, method: str = 'GET', handler: Callable = None) -> 'ApiRouteBuilder':
        """
        Register an API endpoint.

        Can be used as:
          @Server.api('/status', handler=myFunc)
        or:
          @Server.api('/status') <== { define handler { return {...}; } };
        """
        method = method.upper()
        route_key = f"{method}:{path}"

        if handler:
            self._routes[route_key] = {
                'path': path,
                'method': method,
                'handler': handler
            }
            print(f"[Server] Registered {method} {path}")
            return True

        # Return builder for <== assignment
        return ApiRouteBuilder(self, path, method)

    def static(self, url_path: str, directory: str) -> bool:
        """Serve static files from a directory."""
        if not os.path.isdir(directory):
            print(f"[Server] Directory not found: {directory}")
            return False

        # Ensure url_path starts with /
        if not url_path.startswith('/'):
            url_path = '/' + url_path

        self._static_dirs[url_path] = directory
        print(f"[Server] Static files: {url_path} -> {directory}")
        return True

    def show_server(self) -> Dict:
        """Display server information."""
        info = {
            'running': self._running,
            'host': self._host,
            'port': self._port,
            'url': f"http://{self._host}:{self._port}" if self._running else None,
            'routes': len(self._routes),
            'static_dirs': len(self._static_dirs),
            'connections': self._connections
        }

        print(f"\n{'='*50}")
        print(f"  CSSL Server Status")
        print(f"{'='*50}")
        print(f"  Status:      {'Running' if self._running else 'Stopped'}")
        if self._running:
            print(f"  URL:         http://{self._host}:{self._port}")
        print(f"  Routes:      {len(self._routes)}")
        print(f"  Static Dirs: {len(self._static_dirs)}")
        print(f"  Connections: {self._connections}")
        print(f"{'='*50}\n")

        return info

    def get_connections(self) -> int:
        """Get number of active connections."""
        return self._connections

    def get_routes(self) -> List[Dict]:
        """Get list of registered routes."""
        return [
            {'method': r['method'], 'path': r['path']}
            for r in self._routes.values()
        ]

    def status(self) -> Dict:
        """Get server status."""
        return {
            'running': self._running,
            'host': self._host,
            'port': self._port,
            'routes': len(self._routes),
            'connections': self._connections
        }

    def set_error_handler(self, handler: Callable) -> bool:
        """Set custom error handler."""
        self._error_handler = handler
        return True

    def set_cors(self, origins: Union[str, List[str]]) -> bool:
        """Configure CORS allowed origins."""
        if isinstance(origins, str):
            origins = [origins]
        self._cors_origins = origins
        return True


class ApiRouteBuilder:
    """Builder class for API route registration with <== syntax."""

    def __init__(self, server: ServerModule, path: str, method: str):
        self._server = server
        self._path = path
        self._method = method

    def __call__(self, handler: Callable) -> bool:
        """Called when used as @Server.api('/path')(handler)"""
        return self._server.api(self._path, self._method, handler)

    def set_handler(self, handler: Any) -> bool:
        """Called by runtime for <== assignment"""
        route_key = f"{self._method}:{self._path}"
        self._server._routes[route_key] = {
            'path': self._path,
            'method': self._method,
            'handler': handler
        }
        print(f"[Server] Registered {self._method} {self._path}")
        return True


# =============================================================================
# @APK Module - App Registration and Management
# =============================================================================

class APKModule(CSSLModuleBase):
    """
    @APK - App package management and registration

    Methods:
      createAppService(config)    - Register an app from CSSL
      registerApp(app_info)       - Register app directly
      getAppInfo(app_id)          - Get app metadata
      listApps()                  - List all registered apps
      launchApp(app_id)           - Launch an app
      isInstalled(app_id)         - Check if app is installed

    Usage in CSSL:
      @APK.createAppService() <== {
          script = "app.py";
          service = "myapp.cll";
          execute_on_boot = false;
      }
    """

    def __init__(self, runtime=None):
        super().__init__(runtime)
        self._registry = None
        self._root_dir = None

    def _register_methods(self):
        self._methods['createAppService'] = self.createAppService
        self._methods['registerApp'] = self.registerApp
        self._methods['getAppInfo'] = self.getAppInfo
        self._methods['listApps'] = self.listApps
        self._methods['launchApp'] = self.launchApp
        self._methods['isInstalled'] = self.isInstalled

    def _get_registry(self):
        """Lazy load AppRegistry"""
        if self._registry is None:
            try:
                import sys
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                from common.clients.apk import AppRegistry
                self._registry = AppRegistry()
                self._registry.scan()
            except ImportError:
                pass
        return self._registry

    def _get_root_dir(self) -> str:
        """Get root32 directory"""
        if self._root_dir is None:
            if self.runtime and hasattr(self.runtime, 'kernel') and hasattr(self.runtime.kernel, 'RootDirectory'):
                self._root_dir = self.runtime.kernel.RootDirectory
            else:
                self._root_dir = os.path.expanduser("~/.cso/root32")
        return self._root_dir

    def createAppService(self, config: Dict = None) -> 'AppServiceBuilder':
        """
        Create an app service registration.

        Returns a builder that can be used with <== assignment.

        Usage:
            @APK.createAppService() <== { script="app.py", service="myapp.cll" }
        """
        return AppServiceBuilder(self, config or {})

    def registerApp(self, app_info: Dict) -> bool:
        """
        Register an app directly.

        Args:
            app_info: Dict with name, version, category, icon, module_path
        """
        registry = self._get_registry()
        if not registry:
            return False

        try:
            from common.clients.apk import AppInfo
            info = AppInfo(
                app_id=app_info.get('id', app_info.get('name', '').lower()),
                name=app_info.get('name', ''),
                version=app_info.get('version', '1.0.0'),
                category=app_info.get('category', 'Apps'),
                description=app_info.get('description', ''),
                icon=app_info.get('icon'),
                module_path=app_info.get('module_path')
            )
            return registry.register_app(info)
        except Exception as e:
            print(f"[APK] Error registering app: {e}")
            return False

    def getAppInfo(self, app_id: str) -> Optional[Dict]:
        """Get app info by ID"""
        registry = self._get_registry()
        if not registry:
            return None

        info = registry.get_app(app_id)
        if info:
            return {
                'id': info.app_id,
                'name': info.name,
                'version': info.version,
                'category': info.category,
                'description': info.description,
                'icon': info.icon
            }
        return None

    def listApps(self) -> List[Dict]:
        """List all registered apps"""
        registry = self._get_registry()
        if not registry:
            return []

        return [
            {
                'id': info.app_id,
                'name': info.name,
                'category': info.category
            }
            for info in registry.get_all_apps()
        ]

    def launchApp(self, app_id: str) -> bool:
        """Launch an app by ID (placeholder - needs desktop integration)"""
        print(f"[APK] TODO: Launch app {app_id}")
        return False

    def isInstalled(self, app_id: str) -> bool:
        """Check if app is installed"""
        registry = self._get_registry()
        if not registry:
            return False
        return app_id in registry


class AppServiceBuilder:
    """Builder class for app service registration with <== syntax."""

    def __init__(self, module: APKModule, config: Dict):
        self._module = module
        self._config = config

    def set_handler(self, config: Dict) -> bool:
        """Called by runtime for <== assignment"""
        # Merge configs
        full_config = {**self._config, **config}

        script = full_config.get('script', '')
        service = full_config.get('service', '')
        execute_on_boot = full_config.get('execute_on_boot', False)

        # Derive service name from .cll filename
        service_name = service.replace('.cll', '') if service else ''

        if not service_name:
            print("[APK] Error: service name is required")
            return False

        # Look for .cll-meta file
        root_dir = self._module._get_root_dir()
        meta_path = os.path.join(root_dir, "sys", "intern", f"{service_name}.cll-meta")

        if os.path.exists(meta_path):
            # Parse metadata and register
            app_info = self._parse_meta_file(meta_path)
            if app_info:
                app_info['script'] = script
                success = self._module.registerApp(app_info)

                if success:
                    print(f"[APK] Registered app: {app_info.get('name', service_name)}")

                    if execute_on_boot:
                        print(f"[APK] TODO: Schedule {service_name} for boot execution")

                return success

        print(f"[APK] Meta file not found: {meta_path}")
        return False

    def _parse_meta_file(self, path: str) -> Optional[Dict]:
        """Parse .cll-meta file"""
        try:
            data = {}
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        data[key.strip()] = value.strip()

            return {
                'id': data.get('Name', '').lower().replace(' ', '_'),
                'name': data.get('Name', ''),
                'version': data.get('Version', '1.0.0'),
                'category': data.get('Category', 'Apps'),
                'description': data.get('Description', ''),
                'icon': data.get('Icon'),
                'module_path': data.get('Module')
            }
        except Exception as e:
            print(f"[APK] Error parsing {path}: {e}")
            return None


# =============================================================================
# Module Registry
# =============================================================================

class CSSLModuleRegistry:
    """Registry of all CSSL standard modules"""

    _instance = None
    _modules: Dict[str, CSSLModuleBase] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_modules()
        return cls._instance

    def _init_modules(self):
        """Initialize all standard modules"""
        self._modules = {
            'Time': TimeModule(),
            'Secrets': SecretsModule(),
            'Math': MathModule(),
            'Crypto': CryptoModule(),
            'Net': NetModule(),
            'IO': IOModule(),
            'JSON': JSONModule(),
            'Regex': RegexModule(),
            'System': SystemModule(),
            'Log': LogModule(),
            'Cache': CacheModule(),
            'Queue': QueueModule(),
            'Format': FormatModule(),
            'Console': ConsoleModule(),
            'Process': ProcessModule(),
            'Config': ConfigModule(),
            'Server': ServerModule(),
        }

        # Register Desktop module (lazy loaded)
        try:
            from .cssl_desktop import get_desktop_module
            self._modules['Desktop'] = get_desktop_module()
        except ImportError:
            pass

        # Register APK module for app registration
        self._modules['APK'] = APKModule()

    def get_module(self, name: str) -> Optional[CSSLModuleBase]:
        """Get a module by name"""
        return self._modules.get(name)

    def list_modules(self) -> List[str]:
        """List all available module names"""
        return sorted(self._modules.keys())

    def register_module(self, name: str, module: CSSLModuleBase):
        """Register a custom module"""
        self._modules[name] = module


def get_module_registry() -> CSSLModuleRegistry:
    """Get the global module registry"""
    return CSSLModuleRegistry()


def get_standard_module(name: str) -> Optional[CSSLModuleBase]:
    """Get a standard module by name"""
    return get_module_registry().get_module(name)
