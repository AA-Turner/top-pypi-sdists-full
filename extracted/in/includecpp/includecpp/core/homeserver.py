"""
IncludeCPP HomeServer - Local storage server for modules, projects, and files.

A lightweight background server for storing and sharing IncludeCPP content.
"""

import os
import sys
import json
import sqlite3
import hashlib
import shutil
import socket
import threading
import http.server
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple, Any
import base64

# Server configuration
DEFAULT_PORT = 2007
MAX_PORT_ATTEMPTS = 10
SERVER_NAME = "IncludeCPP-HomeServer"

def get_server_dir() -> Path:
    """Get the HomeServer installation directory."""
    if sys.platform == 'win32':
        base = Path(os.environ.get('APPDATA', os.path.expanduser('~')))
    else:
        base = Path.home() / '.config'
    return base / 'IncludeCPP' / 'homeserver'


def get_db_path() -> Path:
    """Get the SQLite database path."""
    return get_server_dir() / 'storage.db'


def get_storage_dir() -> Path:
    """Get the file storage directory."""
    return get_server_dir() / 'files'


def get_config_path() -> Path:
    """Get the server config file path."""
    return get_server_dir() / 'config.json'


def get_pid_path() -> Path:
    """Get the PID file path."""
    return get_server_dir() / 'server.pid'


class HomeServerDB:
    """SQLite database manager for HomeServer storage."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or get_db_path()
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    item_type TEXT NOT NULL,  -- 'file' or 'project'
                    original_path TEXT,
                    storage_path TEXT NOT NULL,
                    size_bytes INTEGER,
                    file_count INTEGER DEFAULT 1,
                    checksum TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT  -- JSON for extra data
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS project_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    relative_path TEXT NOT NULL,
                    file_hash TEXT,
                    size_bytes INTEGER,
                    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_items_name ON items(name)
            ''')
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_project_files_item ON project_files(item_id)
            ''')
            # Add category column if not exists (for upgrades)
            try:
                conn.execute('ALTER TABLE items ADD COLUMN category TEXT DEFAULT NULL')
            except sqlite3.OperationalError:
                pass  # Column already exists
            conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_items_category ON items(category)
            ''')
            conn.commit()

    def add_item(self, name: str, item_type: str, storage_path: str,
                 original_path: str = None, size_bytes: int = 0,
                 file_count: int = 1, checksum: str = None,
                 metadata: dict = None, category: str = None) -> int:
        """Add a new item to the database."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO items (name, item_type, original_path, storage_path,
                                   size_bytes, file_count, checksum, created_at,
                                   updated_at, metadata, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, item_type, original_path, storage_path, size_bytes,
                  file_count, checksum, now, now,
                  json.dumps(metadata) if metadata else None, category))
            conn.commit()
            return cursor.lastrowid

    def add_project_file(self, item_id: int, relative_path: str,
                         file_hash: str, size_bytes: int):
        """Add a file entry for a project."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO project_files (item_id, relative_path, file_hash, size_bytes)
                VALUES (?, ?, ?, ?)
            ''', (item_id, relative_path, file_hash, size_bytes))
            conn.commit()

    def get_item(self, name: str) -> Optional[Dict]:
        """Get an item by name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM items WHERE name = ?', (name,))
            row = cursor.fetchone()
            if row:
                return dict(row)
        return None

    def get_all_items(self) -> List[Dict]:
        """Get all items."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM items ORDER BY updated_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def delete_item(self, name: str) -> bool:
        """Delete an item by name."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('DELETE FROM items WHERE name = ?', (name,))
            conn.commit()
            return cursor.rowcount > 0

    def item_exists(self, name: str) -> bool:
        """Check if an item exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT 1 FROM items WHERE name = ?', (name,))
            return cursor.fetchone() is not None

    def get_project_files(self, item_id: int) -> List[Dict]:
        """Get all files for a project."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                'SELECT * FROM project_files WHERE item_id = ?', (item_id,))
            return [dict(row) for row in cursor.fetchall()]

    # Category management methods
    def add_category(self, name: str) -> bool:
        """Add a new category."""
        now = datetime.now().isoformat()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    'INSERT INTO categories (name, created_at) VALUES (?, ?)',
                    (name, now))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Category already exists

    def delete_category(self, name: str) -> bool:
        """Delete a category (items in it become uncategorized)."""
        with sqlite3.connect(self.db_path) as conn:
            # Unset category for all items in this category
            conn.execute('UPDATE items SET category = NULL WHERE category = ?', (name,))
            cursor = conn.execute('DELETE FROM categories WHERE name = ?', (name,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_categories(self) -> List[str]:
        """Get all category names."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT name FROM categories ORDER BY name')
            return [row[0] for row in cursor.fetchall()]

    def category_exists(self, name: str) -> bool:
        """Check if a category exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT 1 FROM categories WHERE name = ?', (name,))
            return cursor.fetchone() is not None

    def set_item_category(self, item_name: str, category: str) -> bool:
        """Move an item to a category (or None to uncategorize)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'UPDATE items SET category = ?, updated_at = ? WHERE name = ?',
                (category, datetime.now().isoformat(), item_name))
            conn.commit()
            return cursor.rowcount > 0

    def get_items_by_category(self, category: str) -> List[Dict]:
        """Get all items in a category."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            if category:
                cursor = conn.execute(
                    'SELECT * FROM items WHERE category = ? ORDER BY updated_at DESC',
                    (category,))
            else:
                cursor = conn.execute(
                    'SELECT * FROM items WHERE category IS NULL ORDER BY updated_at DESC')
            return [dict(row) for row in cursor.fetchall()]


class HomeServerConfig:
    """Configuration manager for HomeServer."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or get_config_path()
        self._config = self._load()

    def _load(self) -> Dict:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            'port': DEFAULT_PORT,
            'auto_start': True,
            'version': '1.0.0',
            'installed_at': None,
            'last_started': None
        }

    def save(self):
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)

    @property
    def port(self) -> int:
        return self._config.get('port', DEFAULT_PORT)

    @port.setter
    def port(self, value: int):
        self._config['port'] = value
        self.save()

    @property
    def auto_start(self) -> bool:
        return self._config.get('auto_start', True)

    @auto_start.setter
    def auto_start(self, value: bool):
        self._config['auto_start'] = value
        self.save()

    def set_installed(self):
        self._config['installed_at'] = datetime.now().isoformat()
        self.save()

    def set_last_started(self):
        self._config['last_started'] = datetime.now().isoformat()
        self.save()

    def is_installed(self) -> bool:
        return self._config.get('installed_at') is not None


def find_available_port(start_port: int = DEFAULT_PORT) -> int:
    """Find an available port starting from the given port."""
    for offset in range(MAX_PORT_ATTEMPTS):
        port = start_port + offset
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available port found in range {start_port}-{start_port + MAX_PORT_ATTEMPTS}")


def compute_file_hash(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_dir_size(path: Path) -> Tuple[int, int]:
    """Get total size and file count of a directory."""
    total_size = 0
    file_count = 0
    for item in path.rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
            file_count += 1
    return total_size, file_count


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


class HomeServerHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for HomeServer."""

    def __init__(self, *args, db: HomeServerDB = None, storage_dir: Path = None, **kwargs):
        self.db = db
        self.storage_dir = storage_dir
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def send_json(self, data: Any, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == '/status':
            self.send_json({'status': 'running', 'server': SERVER_NAME})

        elif path == '/list':
            items = self.db.get_all_items()
            self.send_json({'items': items})

        elif path == '/get':
            name = query.get('name', [None])[0]
            if not name:
                self.send_json({'error': 'Missing name parameter'}, 400)
                return
            item = self.db.get_item(name)
            if item:
                self.send_json({'item': item})
            else:
                self.send_json({'error': 'Item not found'}, 404)

        elif path == '/categories':
            categories = self.db.get_all_categories()
            self.send_json({'categories': categories})

        elif path == '/category/items':
            category = query.get('category', [None])[0]
            items = self.db.get_items_by_category(category)
            self.send_json({'items': items, 'category': category})

        elif path.startswith('/download/'):
            name = urllib.parse.unquote(path[10:])
            item = self.db.get_item(name)
            if not item:
                self.send_json({'error': 'Item not found'}, 404)
                return

            storage_path = Path(item['storage_path'])
            if not storage_path.exists():
                self.send_json({'error': 'File not found on disk'}, 404)
                return

            # For projects, create a zip
            if item['item_type'] == 'project':
                import zipfile
                import io
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file in storage_path.rglob('*'):
                        if file.is_file():
                            zf.write(file, file.relative_to(storage_path))
                buffer.seek(0)
                content = buffer.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', f'attachment; filename="{name}.zip"')
                self.end_headers()
                self.wfile.write(content)
            else:
                # Single file
                with open(storage_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{name}"')
                self.end_headers()
                self.wfile.write(content)

        else:
            self.send_json({'error': 'Unknown endpoint'}, 404)

    def do_POST(self):
        """Handle POST requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        if path == '/upload':
            try:
                data = json.loads(body)
                name = data.get('name')
                item_type = data.get('type', 'file')
                content_b64 = data.get('content')
                original_filename = data.get('filename', name)  # Preserve original filename
                category = data.get('category')  # Optional category

                if not name or not content_b64:
                    self.send_json({'error': 'Missing name or content'}, 400)
                    return

                if self.db.item_exists(name):
                    self.send_json({'error': f'Item "{name}" already exists'}, 409)
                    return

                # Auto-create category if specified and doesn't exist
                if category and not self.db.category_exists(category):
                    self.db.add_category(category)

                content = base64.b64decode(content_b64)

                if item_type == 'project':
                    # Extract zip to storage
                    import zipfile
                    import io
                    storage_path = self.storage_dir / 'projects' / name
                    storage_path.mkdir(parents=True, exist_ok=True)

                    with zipfile.ZipFile(io.BytesIO(content), 'r') as zf:
                        zf.extractall(storage_path)

                    size, count = get_dir_size(storage_path)
                    item_id = self.db.add_item(
                        name=name,
                        item_type='project',
                        storage_path=str(storage_path),
                        size_bytes=size,
                        file_count=count,
                        category=category
                    )

                    # Add file entries
                    for file in storage_path.rglob('*'):
                        if file.is_file():
                            self.db.add_project_file(
                                item_id=item_id,
                                relative_path=str(file.relative_to(storage_path)),
                                file_hash=compute_file_hash(file),
                                size_bytes=file.stat().st_size
                            )
                else:
                    # Single file - store with original filename
                    storage_path = self.storage_dir / 'files' / original_filename
                    storage_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(storage_path, 'wb') as f:
                        f.write(content)

                    # Use metadata from client if provided, else build default
                    file_metadata = data.get('metadata', {'filename': original_filename})
                    if 'filename' not in file_metadata:
                        file_metadata['filename'] = original_filename

                    self.db.add_item(
                        name=name,
                        item_type='file',
                        storage_path=str(storage_path),
                        size_bytes=len(content),
                        checksum=hashlib.sha256(content).hexdigest(),
                        metadata=file_metadata,
                        category=category
                    )

                self.send_json({'success': True, 'name': name, 'filename': original_filename, 'category': category})

            except Exception as e:
                self.send_json({'error': str(e)}, 500)

        elif path == '/delete':
            try:
                data = json.loads(body)
                name = data.get('name')

                if not name:
                    self.send_json({'error': 'Missing name'}, 400)
                    return

                item = self.db.get_item(name)
                if not item:
                    self.send_json({'error': 'Item not found'}, 404)
                    return

                # Delete from disk
                storage_path = Path(item['storage_path'])
                if storage_path.exists():
                    if storage_path.is_dir():
                        shutil.rmtree(storage_path)
                    else:
                        storage_path.unlink()

                # Delete from database
                self.db.delete_item(name)
                self.send_json({'success': True})

            except Exception as e:
                self.send_json({'error': str(e)}, 500)

        elif path == '/category/add':
            try:
                data = json.loads(body)
                name = data.get('name')
                if not name:
                    self.send_json({'error': 'Missing category name'}, 400)
                    return
                if self.db.add_category(name):
                    self.send_json({'success': True, 'category': name})
                else:
                    self.send_json({'error': f'Category "{name}" already exists'}, 409)
            except Exception as e:
                self.send_json({'error': str(e)}, 500)

        elif path == '/category/delete':
            try:
                data = json.loads(body)
                name = data.get('name')
                if not name:
                    self.send_json({'error': 'Missing category name'}, 400)
                    return
                if self.db.delete_category(name):
                    self.send_json({'success': True})
                else:
                    self.send_json({'error': 'Category not found'}, 404)
            except Exception as e:
                self.send_json({'error': str(e)}, 500)

        elif path == '/category/move':
            try:
                data = json.loads(body)
                item_name = data.get('item')
                category = data.get('category')  # Can be None to uncategorize
                if not item_name:
                    self.send_json({'error': 'Missing item name'}, 400)
                    return
                # Auto-create category if specified
                if category and not self.db.category_exists(category):
                    self.db.add_category(category)
                if self.db.set_item_category(item_name, category):
                    self.send_json({'success': True, 'item': item_name, 'category': category})
                else:
                    self.send_json({'error': 'Item not found'}, 404)
            except Exception as e:
                self.send_json({'error': str(e)}, 500)

        else:
            self.send_json({'error': 'Unknown endpoint'}, 404)


def create_handler(db: HomeServerDB, storage_dir: Path):
    """Create a handler class with bound database and storage."""
    class BoundHandler(HomeServerHandler):
        def __init__(self, *args, **kwargs):
            self.db = db
            self.storage_dir = storage_dir
            # Skip parent __init__ that causes issues
            http.server.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    return BoundHandler


def is_server_running(port: int = None) -> bool:
    """Check if the HomeServer is running."""
    config = HomeServerConfig()
    port = port or config.port

    try:
        import urllib.request
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/status', timeout=2) as response:
            data = json.loads(response.read())
            return data.get('server') == SERVER_NAME
    except:
        return False


def _run_server_foreground(port: int):
    """Internal: Run server in foreground mode (called by subprocess)."""
    config = HomeServerConfig()
    db = HomeServerDB()
    storage_dir = get_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)

    handler = create_handler(db, storage_dir)
    server = http.server.HTTPServer(('127.0.0.1', port), handler)

    config.set_last_started()

    # Write PID file
    pid_path = get_pid_path()
    with open(pid_path, 'w') as f:
        f.write(str(os.getpid()))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        pid_path.unlink(missing_ok=True)


def start_server(port: int = None, foreground: bool = False) -> Tuple[bool, int, str]:
    """
    Start the HomeServer.

    Returns:
        Tuple of (success, port, message)
    """
    # Check if already running
    config = HomeServerConfig()
    port = port or config.port

    if is_server_running(port):
        return (True, port, f"HomeServer already running on port {port}")

    server_dir = get_server_dir()
    server_dir.mkdir(parents=True, exist_ok=True)

    # Find available port
    try:
        actual_port = find_available_port(port)
    except RuntimeError as e:
        return (False, port, str(e))

    if actual_port != port:
        config.port = actual_port

    if foreground:
        # Run directly in current process
        _run_server_foreground(actual_port)
        return (True, actual_port, "Server stopped")
    else:
        # Spawn as independent background process
        import subprocess

        # Use pythonw on Windows for no console window
        python_exe = sys.executable
        if sys.platform == 'win32':
            pythonw = python_exe.replace('python.exe', 'pythonw.exe')
            if os.path.exists(pythonw):
                python_exe = pythonw

        # Start server as subprocess
        cmd = [
            python_exe, '-c',
            f'from includecpp.core.homeserver import _run_server_foreground; _run_server_foreground({actual_port})'
        ]

        if sys.platform == 'win32':
            # Windows: CREATE_NO_WINDOW flag
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(cmd, creationflags=CREATE_NO_WINDOW,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # Unix: double fork via nohup
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           start_new_session=True)

        # Wait briefly and verify server started
        import time
        for _ in range(10):
            time.sleep(0.2)
            if is_server_running(actual_port):
                return (True, actual_port, f"HomeServer started on port {actual_port}")

        return (False, actual_port, "Server failed to start")


def stop_server() -> Tuple[bool, str]:
    """
    Stop the HomeServer.

    Returns:
        Tuple of (success, message)
    """
    config = HomeServerConfig()

    # Check if running first
    if not is_server_running(config.port):
        return (False, "HomeServer is not running")

    pid_path = get_pid_path()
    if pid_path.exists():
        try:
            pid = int(pid_path.read_text().strip())
            if sys.platform == 'win32':
                import subprocess
                subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                os.kill(pid, 9)
            pid_path.unlink(missing_ok=True)

            # Verify stopped
            import time
            time.sleep(0.5)
            if not is_server_running(config.port):
                return (True, "HomeServer stopped successfully")
            else:
                return (False, "Failed to stop server")
        except Exception as e:
            return (False, f"Error stopping server: {e}")

    return (False, "Server PID file not found")


# Windows auto-start helpers
def setup_windows_autostart():
    """Set up Windows auto-start via registry."""
    if sys.platform != 'win32':
        return False

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )

        # Path to the server starter script
        server_exe = get_server_dir() / 'start_server.bat'

        # Create starter batch file (use \r\n for Windows batch files)
        with open(server_exe, 'w', newline='\r\n') as f:
            f.write('@echo off\n')
            f.write('pythonw -c "from includecpp.core.homeserver import start_server; start_server(foreground=True)" >nul 2>&1\n')

        winreg.SetValueEx(key, SERVER_NAME, 0, winreg.REG_SZ, str(server_exe))
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Warning: Could not set up auto-start: {e}")
        return False


def remove_windows_autostart():
    """Remove Windows auto-start."""
    if sys.platform != 'win32':
        return False

    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, SERVER_NAME)
        winreg.CloseKey(key)
        return True
    except:
        return False


# Client functions for CLI commands
class HomeServerClient:
    """Client for communicating with HomeServer."""

    def __init__(self, host: str = '127.0.0.1', port: int = None):
        self.host = host
        config = HomeServerConfig()
        self.port = port or config.port
        self.base_url = f'http://{self.host}:{self.port}'

    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make HTTP request to server."""
        import urllib.request
        import urllib.error

        url = f'{self.base_url}{endpoint}'

        if method == 'GET':
            if data:
                url += '?' + urllib.parse.urlencode(data)
            req = urllib.request.Request(url)
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode() if data else None,
                headers={'Content-Type': 'application/json'},
                method=method
            )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            return json.loads(e.read())
        except urllib.error.URLError as e:
            raise ConnectionError(f"Cannot connect to HomeServer: {e}")

    def status(self) -> dict:
        """Check server status."""
        return self._request('GET', '/status')

    def list_items(self) -> List[dict]:
        """List all items."""
        result = self._request('GET', '/list')
        return result.get('items', [])

    def get_item(self, name: str) -> Optional[dict]:
        """Get item info."""
        result = self._request('GET', '/get', {'name': name})
        return result.get('item')

    def upload_file(self, name: str, filepath: Path, category: str = None) -> dict:
        """Upload a single file.

        For .py files, auto-detects includecpp usage and saves the project path.
        """
        with open(filepath, 'rb') as f:
            content = f.read()

        # Build metadata with original filename
        metadata = {'filename': filepath.name}

        # Auto-detect project path for Python files using includecpp
        if filepath.suffix.lower() == '.py':
            try:
                script_content = content.decode('utf-8', errors='ignore')
                # Check if includecpp is imported
                if 'includecpp' in script_content and ('import includecpp' in script_content or 'from includecpp' in script_content):
                    # Search for cpp.proj in parent directories
                    search_dir = filepath.parent.resolve()
                    for _ in range(5):  # Search up to 5 levels
                        cpp_proj = search_dir / 'cpp.proj'
                        if cpp_proj.exists():
                            metadata['project_path'] = str(search_dir)
                            break
                        if search_dir.parent == search_dir:
                            break
                        search_dir = search_dir.parent
            except:
                pass

        data = {
            'name': name,
            'type': 'file',
            'filename': filepath.name,
            'metadata': metadata,
            'content': base64.b64encode(content).decode()
        }
        if category:
            data['category'] = category
        return self._request('POST', '/upload', data)

    def upload_project(self, name: str, project_path: Path, category: str = None) -> dict:
        """Upload a project folder."""
        import zipfile
        import io

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in project_path.rglob('*'):
                if file.is_file():
                    # Skip common non-essential files
                    if any(p in str(file) for p in ['__pycache__', '.git', 'node_modules', '.pyc']):
                        continue
                    zf.write(file, file.relative_to(project_path))

        buffer.seek(0)
        content = buffer.read()

        data = {
            'name': name,
            'type': 'project',
            'content': base64.b64encode(content).decode()
        }
        if category:
            data['category'] = category
        return self._request('POST', '/upload', data)

    def delete_item(self, name: str) -> dict:
        """Delete an item."""
        return self._request('POST', '/delete', {'name': name})

    def get_filename(self, name: str) -> str:
        """Get the original filename for an item."""
        item = self.get_item(name)
        if item and item.get('metadata'):
            try:
                meta = json.loads(item['metadata']) if isinstance(item['metadata'], str) else item['metadata']
                return meta.get('filename', name)
            except:
                pass
        return name

    def get_project_path(self, name: str) -> Optional[str]:
        """Get the saved includecpp project path for an item (if any)."""
        item = self.get_item(name)
        if item and item.get('metadata'):
            try:
                meta = json.loads(item['metadata']) if isinstance(item['metadata'], str) else item['metadata']
                return meta.get('project_path')
            except:
                pass
        return None

    def download_file(self, name: str, output_path: Path, is_dir: bool = False) -> Path:
        """Download a file or project.

        Args:
            name: Item name to download
            output_path: Output path (file or directory)
            is_dir: If True, treat output_path as directory and write file into it

        Returns:
            Path to the downloaded file/directory
        """
        import urllib.request

        # Get original filename from metadata
        original_filename = self.get_filename(name)

        url = f'{self.base_url}/download/{urllib.parse.quote(name)}'

        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                content = response.read()

                # Check if it's a zip (project)
                content_type = response.headers.get('Content-Type', '')

                if 'zip' in content_type:
                    # Extract project - always to a directory
                    import zipfile
                    import io
                    if is_dir:
                        # Extract into specified directory with item name as subfolder
                        final_path = output_path / name
                    else:
                        final_path = output_path
                    final_path.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(io.BytesIO(content), 'r') as zf:
                        zf.extractall(final_path)
                    return final_path
                else:
                    # Single file - use original filename
                    if is_dir or output_path.is_dir():
                        # Write into directory with original filename
                        output_path.mkdir(parents=True, exist_ok=True)
                        final_path = output_path / original_filename
                    else:
                        final_path = output_path
                        final_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(final_path, 'wb') as f:
                        f.write(content)
                    return final_path

        except Exception as e:
            raise RuntimeError(f"Download failed: {e}")

    # Category management methods
    def list_categories(self) -> List[str]:
        """List all categories."""
        result = self._request('GET', '/categories')
        return result.get('categories', [])

    def get_items_by_category(self, category: str = None) -> List[dict]:
        """Get items in a category (None for uncategorized)."""
        result = self._request('GET', '/category/items', {'category': category or ''})
        return result.get('items', [])

    def add_category(self, name: str) -> dict:
        """Create a new category."""
        return self._request('POST', '/category/add', {'name': name})

    def delete_category(self, name: str) -> dict:
        """Delete a category (items become uncategorized)."""
        return self._request('POST', '/category/delete', {'name': name})

    def move_to_category(self, item_name: str, category: str = None) -> dict:
        """Move an item to a category (None to uncategorize)."""
        return self._request('POST', '/category/move', {'item': item_name, 'category': category})

    def download_category(self, category: str, output_dir: Path) -> List[Path]:
        """Download all items in a category."""
        items = self.get_items_by_category(category)
        downloaded = []
        for item in items:
            try:
                path = self.download_file(item['name'], output_dir, is_dir=True)
                downloaded.append(path)
            except Exception:
                pass  # Skip failed downloads
        return downloaded
