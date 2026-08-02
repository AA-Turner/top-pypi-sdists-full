import os
import json
import threading
from typing import Any

class SimpleDB:
    _locks = {}
    _global_lock = threading.Lock()

    def __init__(self, name: str, filepath: str = None):
        self.name = name
        
        if filepath:
            self.filepath = filepath
        else:
            base_dir = "."
            try:
                from org.telegram.messenger import ApplicationLoader
                context = ApplicationLoader.applicationContext
                if context:
                    base_dir = os.path.join(
                        context.getFilesDir().getAbsolutePath(), 
                        "exteraGram", "plugins_data", "alib_db"
                    )
            except Exception:
                pass
            
            if base_dir == ".":
                base_dir = os.path.expanduser("~/.alib_db")

            os.makedirs(base_dir, exist_ok=True)
            self.filepath = os.path.join(base_dir, f"{name}.json")

        with SimpleDB._global_lock:
            if self.filepath not in SimpleDB._locks:
                SimpleDB._locks[self.filepath] = threading.Lock()
            self.lock = SimpleDB._locks[self.filepath]

        self._data = {}
        self.load()

    def load(self):
        with self.lock:
            if os.path.exists(self.filepath):
                try:
                    with open(self.filepath, "r", encoding="utf-8") as f:
                        self._data = json.load(f)
                except Exception:
                    self._data = {}
            else:
                self._data = {}

    def _save(self):
        try:
            temp_path = self.filepath + ".tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.filepath)
        except Exception as e:
            try:
                from android_utils import log
                log(f"aLibary SimpleDB save error: {e}")
            except ImportError:
                print(f"aLibary SimpleDB save error: {e}")

    def set(self, key: str, value: Any):
        with self.lock:
            self._data[key] = value
            self._save()

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        with self.lock:
            if key in self._data:
                del self._data[key]
                self._save()
                return True
            return False

    def clear(self):
        with self.lock:
            self._data.clear()
            self._save()

    def increment(self, key: str, amount: int = 1) -> int:
        with self.lock:
            val = self._data.get(key, 0)
            if not isinstance(val, (int, float)):
                val = 0
            new_val = val + amount
            self._data[key] = new_val
            self._save()
            return new_val
