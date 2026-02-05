"""
CSSL Service Manager - IPC (Inter-Process Communication) layer.
Server embeds in target runtime; Client connects from Service Manager.
JSON-over-TCP protocol for runtime control.
"""
import json
import socket
import threading
import time
from typing import Any, Callable, Dict, List, Optional


class CSSLIPCServer(threading.Thread):
    """IPC server that embeds in a CSSL runtime to accept remote commands.

    Runs as a daemon thread, listening on 127.0.0.1:auto_port.
    Handles JSON commands: execute, scan_api, get_var, set_var, introspect, ping, etc.
    """

    def __init__(self, runtime=None, port: int = 0, host: str = "127.0.0.1"):
        super().__init__(daemon=True)
        self.runtime = runtime
        self.host = host
        self.port = port  # 0 = auto-assign
        self._server_socket: Optional[socket.socket] = None
        self._running = False
        self._start_time = time.time()
        self._clients: List[socket.socket] = []

    @property
    def actual_port(self) -> int:
        if self._server_socket:
            return self._server_socket.getsockname()[1]
        return self.port

    def run(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)
        self.port = self._server_socket.getsockname()[1]
        self._running = True

        while self._running:
            try:
                client, addr = self._server_socket.accept()
                self._clients.append(client)
                handler = threading.Thread(target=self._handle_client,
                                           args=(client,), daemon=True)
                handler.start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, client: socket.socket):
        client.settimeout(30.0)
        try:
            while self._running:
                data = self._recv_message(client)
                if data is None:
                    break
                response = self._process_command(data)
                self._send_message(client, response)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            if client in self._clients:
                self._clients.remove(client)
            try:
                client.close()
            except Exception:
                pass

    def _recv_message(self, sock: socket.socket) -> Optional[dict]:
        """Receive a length-prefixed JSON message."""
        try:
            header = b""
            while len(header) < 8:
                chunk = sock.recv(8 - len(header))
                if not chunk:
                    return None
                header += chunk
            length = int(header.decode('utf-8').strip())
            data = b""
            while len(data) < length:
                chunk = sock.recv(min(4096, length - len(data)))
                if not chunk:
                    return None
                data += chunk
            return json.loads(data.decode('utf-8'))
        except (ValueError, json.JSONDecodeError):
            return None

    def _send_message(self, sock: socket.socket, data: dict):
        """Send a length-prefixed JSON message."""
        payload = json.dumps(data).encode('utf-8')
        header = f"{len(payload):8d}".encode('utf-8')
        sock.sendall(header + payload)

    def _process_command(self, cmd: dict) -> dict:
        """Process a command from the client."""
        action = cmd.get('cmd', '')

        if action == 'ping':
            return {"ok": True, "uptime": time.time() - self._start_time}

        if action == 'execute':
            return self._cmd_execute(cmd.get('code', ''))

        if action == 'scan_api':
            return self._cmd_scan_api()

        if action == 'get_var':
            return self._cmd_get_var(cmd.get('name', ''))

        if action == 'set_var':
            return self._cmd_set_var(cmd.get('name', ''), cmd.get('value'))

        if action == 'introspect':
            return self._cmd_introspect()

        if action == 'list_scopes':
            return self._cmd_list_scopes()

        if action == 'memory_stats':
            return self._cmd_memory_stats()

        return {"ok": False, "error": f"Unknown command: {action}"}

    def _cmd_execute(self, code: str) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            try:
                result = self.runtime.execute(code)
            finally:
                sys.stdout = old_stdout
            output = buffer.getvalue()
            return {"ok": True, "output": output, "result": repr(result) if result is not None else None}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cmd_scan_api(self) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            api = {"functions": {}, "classes": {}, "variables": {}, "modules": {}}
            scope = getattr(self.runtime, 'scope', None)
            if scope:
                for name, val in scope.variables.items():
                    if callable(val) or (isinstance(val, dict) and 'params' in val):
                        api["functions"][name] = {
                            "type": "function",
                            "signature": self._get_signature(name, val),
                        }
                    elif isinstance(val, type):
                        api["classes"][name] = {"type": "class", "name": name}
                    else:
                        api["variables"][name] = {
                            "type": type(val).__name__,
                            "value": repr(val)[:200],
                        }

            # Built-in functions
            builtins = getattr(self.runtime, '_builtins', {})
            for name, func in builtins.items():
                api["functions"][name] = {
                    "type": "builtin",
                    "signature": f"{name}(...)",
                }

            # Modules
            modules = getattr(self.runtime, '_modules', {})
            for name, mod in modules.items():
                api["modules"][name] = {
                    "type": "module",
                    "members": list(mod.keys()) if isinstance(mod, dict) else [],
                }

            return {"ok": True, **api}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _get_signature(self, name: str, val) -> str:
        if isinstance(val, dict):
            params = val.get('params', [])
            param_names = []
            for p in params:
                if isinstance(p, dict):
                    param_names.append(p.get('name', '?'))
                elif isinstance(p, str):
                    param_names.append(p)
            return f"{name}({', '.join(param_names)})"
        return f"{name}()"

    def _cmd_get_var(self, name: str) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            scope = getattr(self.runtime, 'scope', None)
            if scope and name in scope.variables:
                val = scope.variables[name]
                return {"ok": True, "value": repr(val)[:500], "type": type(val).__name__}
            return {"ok": False, "error": f"Variable '{name}' not found"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cmd_set_var(self, name: str, value) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            scope = getattr(self.runtime, 'scope', None)
            if scope:
                scope.variables[name] = value
                return {"ok": True}
            return {"ok": False, "error": "No scope available"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cmd_introspect(self) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            data = {
                "uptime": time.time() - self._start_time,
                "variables": {},
                "functions": [],
                "modules": [],
            }
            scope = getattr(self.runtime, 'scope', None)
            if scope:
                for name, val in scope.variables.items():
                    data["variables"][name] = {
                        "value": repr(val)[:200],
                        "type": type(val).__name__,
                    }
            return {"ok": True, **data}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cmd_list_scopes(self) -> dict:
        if not self.runtime:
            return {"ok": False, "error": "No runtime attached"}
        try:
            scopes = []
            scope = getattr(self.runtime, 'scope', None)
            while scope:
                scopes.append({
                    "name": getattr(scope, 'name', 'anonymous'),
                    "variables": list(scope.variables.keys()) if hasattr(scope, 'variables') else [],
                })
                scope = getattr(scope, 'parent', None)
            return {"ok": True, "scopes": scopes}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cmd_memory_stats(self) -> dict:
        try:
            import gc
            stats = {
                "gc_counts": gc.get_count(),
                "gc_threshold": gc.get_threshold(),
                "objects_tracked": len(gc.get_objects()),
            }
            # CSSL-specific
            try:
                from includecpp.core.cssl.cssl_types import Address
                stats["addresses"] = len(Address._registry)
            except Exception:
                stats["addresses"] = 0
            return {"ok": True, **stats}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop(self):
        self._running = False
        for client in self._clients:
            try:
                client.close()
            except Exception:
                pass
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass


class CSSLIPCClient:
    """IPC client that connects to a CSSL runtime's IPC server."""

    def __init__(self):
        self._socket: Optional[socket.socket] = None
        self._connected = False
        self._lock = threading.Lock()

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self, host: str = "127.0.0.1", port: int = 0) -> bool:
        """Connect to a CSSL IPC server."""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(5.0)
            self._socket.connect((host, port))
            self._connected = True
            return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            self._connected = False
            return False

    def disconnect(self):
        self._connected = False
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None

    def _send_command(self, cmd: dict) -> dict:
        """Send a command and wait for response."""
        if not self._connected or not self._socket:
            return {"ok": False, "error": "Not connected"}
        with self._lock:
            try:
                payload = json.dumps(cmd).encode('utf-8')
                header = f"{len(payload):8d}".encode('utf-8')
                self._socket.sendall(header + payload)

                # Receive response
                resp_header = b""
                while len(resp_header) < 8:
                    chunk = self._socket.recv(8 - len(resp_header))
                    if not chunk:
                        self._connected = False
                        return {"ok": False, "error": "Connection closed"}
                    resp_header += chunk
                length = int(resp_header.decode('utf-8').strip())
                data = b""
                while len(data) < length:
                    chunk = self._socket.recv(min(4096, length - len(data)))
                    if not chunk:
                        self._connected = False
                        return {"ok": False, "error": "Connection closed"}
                    data += chunk
                return json.loads(data.decode('utf-8'))
            except Exception as e:
                self._connected = False
                return {"ok": False, "error": str(e)}

    def ping(self) -> dict:
        return self._send_command({"cmd": "ping"})

    def execute(self, code: str) -> dict:
        return self._send_command({"cmd": "execute", "code": code})

    def scan_api(self) -> dict:
        return self._send_command({"cmd": "scan_api"})

    def get_variable(self, name: str) -> dict:
        return self._send_command({"cmd": "get_var", "name": name})

    def set_variable(self, name: str, value) -> dict:
        return self._send_command({"cmd": "set_var", "name": name, "value": value})

    def introspect(self) -> dict:
        return self._send_command({"cmd": "introspect"})

    def list_scopes(self) -> dict:
        return self._send_command({"cmd": "list_scopes"})

    def memory_stats(self) -> dict:
        return self._send_command({"cmd": "memory_stats"})
