# encryption.py

try:
    from .key import *
except ImportError:
    from key import *
from datetime import datetime
import os
import platform


class Encryptor:
    def __init__(self, key=None, silent: bool = False):
        if type(key) is Key or key is None:
            self.key = key
        elif type(key) is str:
            self.key = Key(key)

        self.silent_mode = silent

        if self.key:
            self.key_size = len(self.key)

        self.cfg = Config()
        self.chars = [_ for _ in self.cfg["chars"] + "\n"] * 2

    def __repr__(self):
        return f"Class Encryptor from {__name__}\nKey: '{self.key}'"

    def encrypt(self, content: str, key=None):
        if not key and not self.key:
            key = Key()
        elif not key:
            key = self.key
        if not self.silent_mode:
            log("Encryption", f"Info: Started encrypting with key '{key}'")

        errors = 0
        encrypted = ""
        key_iter, content_iter = -1, -1
        for char in content:
            key_iter, content_iter = (_ + 1 for _ in (key_iter, content_iter))
            if key_iter >= len(key):
                key_iter -= len(key)

            key_idx = self.chars.index(key[key_iter])
            try:
                char_idx = self.chars.index(char, 0, len(self.chars) // 2)
            except ValueError:
                log("Encryption", f"Warning: Couldn't encrypt {char.encode('utf-8')}")
                key_iter -= 1
                errors += 1
                continue

            encrypted_idx = int(str(key_idx + char_idx).replace("-", ""))
            encrypted_char = self.chars[encrypted_idx]
            encrypted += encrypted_char if encrypted_char != "\n" else "€"
        if not self.silent_mode:
            log("Encryption", f"Info: Encryption finished with {errors} errors")
        return key, encrypted

    def encrypt_file(self, path: str, key=None):
        key = self.key if not key else key
        with open(path, "r") as f:
            plain_text = f.read()
            f.close()
        plain_text = plain_text.replace("\t", "    ")
        key, value = self.encrypt(plain_text, key)
        with open(path, "wb") as f:
            f.write(value.encode("utf-8"))
            f.close()
        log("Encryption", f"Info: Encrypted file '{path}' with key '{key if key is not None else self.key}'")
        return key

    def add_to_register(self, path: str, file_path: str, key=None):
        if path == "def":
            if platform.system() == "Windows":
                path = "".join([_ + "\\" for _ in __file__.split("\\")[:-1]]) + "data\\.register"
            else:
                path = "".join([_ + "/" for _ in __file__.split("/")[:-1]]) + "data/.register"
        new_lines = ""
        try:
            with open(path, "r") as f:
                for line in f.read().split("\n"):
                    lin = line
                    if line.__contains__(": "):
                        line = line.split(": ")
                        if line[0].replace("\\", "/") != os.path.realpath(file_path).replace("\\", "/"):
                            new_lines += lin + "\n"
                f.close()
        except FileNotFoundError:
            pass
        with open(path, "w") as f:
            f.write(f"{new_lines}{os.path.realpath(file_path)}: {key if key else self.key}\n")
            f.close()
        log("Encryption", f"Info: Wrote key to register at '{path}'")

    # key_idx = index from the current char in the key in self.chars
    # char_idx = index from current char of the content in self.chars
    # encrypted_idx = key_idx + char_idx in the list


class Decrypter:
    def __init__(self, key=None, silent: bool = False):
        if type(key) is Key or key is None:
            self.key = key
        elif type(key) is str:
            self.key = Key(key)

        self.silent_mode = silent

        if self.key:
            self.key_size = len(self.key)

        self.cfg = Config()
        self.chars = [_ for _ in self.cfg["chars"] + "\n"] * 2

    def decrypt(self, content: str = None, key=None, key_value: tuple = None):
        if not key and not self.key:
            key = Key()
        elif not key:
            key = self.key

        if key_value is not None:
            key = key_value[0]
            content = key_value[1]
        if not self.silent_mode:
            log("Decryption", f"Info: Started decrypting with key '{key}'")
        errors = 0
        decrypted = ""
        key_iter, c = -1, -1
        for char in content:
            key_iter, c = (_ + 1 for _ in (key_iter, c))
            if key_iter >= len(key):
                key_iter -= len(key)

            if char == "€":
                char = "\n"
            key_idx = self.chars.index(key[key_iter])
            try:
                content_idx = self.chars.index(char)
            except ValueError:
                log("Decryption", f"Warning: Can't decrypt char '{char}' at index {c}, it is not registered")
                errors += 1
                continue
            if content_idx - key_idx < 0:
                content_idx = self.chars.index(char, len(self.cfg["chars"]))
            decrypted_idx = content_idx - key_idx
            decrypted += self.chars[decrypted_idx]
        if not self.silent_mode:
            log("Decryption", f"Info: Decryption finished with {errors} errors")
        return decrypted

    def decrypt_file(self, path: str, key: Key = None):
        key = self.key if not key else key
        with open(path, "r") as f:
            encrypted = f.read()
            f.close()
        encrypted = encrypted.replace("â‚¬", "€")
        decrypted = self.decrypt(encrypted, key)
        with open(path, "w") as f:
            f.write(decrypted)
            f.close()
        log("Decryption", f"Info: Decrypted file '{path}' with key '{key if key is not None else self.key}'")

    def decrypt_with_register(self, path: str):
        if path == "def":
            if platform.system() == "Windows":
                path = "".join([_ + "\\" for _ in __file__.split("\\")[:-1]]) + "data\\.register"
            else:
                path = "".join([_ + "/" for _ in __file__.split("/")[:-1]]) + "data/.register"
        files = []
        try:
            with open(path, "r") as f:
                for line in f.read().split("\n"):
                    if line.__contains__(": "):
                        files.append(line.split(": "))
                f.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"Register wasn't found at {path}")

        c = 0
        for file, key in files:
            c += 1
            self.decrypt_file(file, key)
        with open(path, "w") as f:
            f.write("")
            f.close()
        log("Decryption", f"Info: Decrypted {c} files with register at '{path}'")


def log(*args):
    print(f"[{datetime.now().strftime('%H:%M:%S')} - {args[0]}]", end=" ")
    for arg in args[1:]:
        print(arg, end=" ")
    print()
