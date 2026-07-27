import os
import tempfile
from pathlib import Path
from sage.core.asset_generator import (
    make_png, make_jpg, make_webp, make_bmp, make_tiff, make_gif,
    make_animated_gif, make_svg, make_pdf, make_ico, make_mp4, make_webm,
    make_wav, make_mp3, make_ogg, make_flac, make_m4a, make_opus
)

MEDIA_GENERATORS = {
    "png": make_png,
    "jpg": make_jpg,
    "jpeg": make_jpg,
    "webp": make_webp,
    "bmp": make_bmp,
    "tiff": make_tiff,
    "tif": make_tiff,
    "gif": make_gif,
    "animated_gif": make_animated_gif,
    "svg": make_svg,
    "ico": make_ico,
    "pdf": make_pdf,
    "mp4": make_mp4,
    "webm": make_webm,
    "mkv": make_mp4,
    "avi": make_mp4,
    "mov": make_mp4,
    "wmv": make_mp4,
    "flv": make_mp4,
    "m4v": make_mp4,
    "3gp": make_mp4,
    "wav": make_wav,
    "mp3": make_mp3,
    "ogg": make_ogg,
    "flac": make_flac,
    "m4a": make_m4a,
    "opus": make_opus,
    "aac": make_wav,
    "wma": make_wav,
    "mid": make_wav,
    "midi": make_wav,
    "amr": make_wav,
    "aiff": make_wav,
}

def make_dummy_file(path: Path, ext: str) -> Path:
    if ext in ("zip", "docx", "xlsx", "pptx", "apk", "ipa", "jar", "odt", "ods", "odp"):
        import zipfile
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr("mimetype" if ext.startswith("od") else "test.txt", "content")
    elif ext in ("gz", "tgz"):
        import gzip
        with gzip.open(path, 'wb') as f:
            f.write(b"dummy compressed content")
    elif ext == "tar":
        import tarfile
        with tarfile.open(path, 'w') as tar:
            pass
    elif ext in ("db", "sqlite", "sqlite3", "sqlitedb"):
        import sqlite3
        conn = sqlite3.connect(path)
        try:
            conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, val TEXT)")
            conn.commit()
        finally:
            conn.close()
    elif ext in ("pem", "crt", "key", "pub", "asc", "gpg"):
        path.write_text(f"-----BEGIN {ext.upper()}-----\nDummy Key Content\n-----END {ext.upper()}-----\n", encoding="utf-8")
    elif ext in ("bin", "exe", "dll", "so", "dylib", "class", "o", "a", "app", "dmg", "pkg", "iso", "img", "cab"):
        headers = {
            "so": b"\x7fELF\x00\x00\x00\x00",
            "exe": b"MZ\x00\x00",
            "dll": b"MZ\x00\x00",
            "class": b"\xca\xfe\xba\xbe",
            "dmg": b"koly\x00\x00\x00\x00",
            "iso": b"\x00" * 32768 + b"CD001",
        }
        path.write_bytes(headers.get(ext, b"\x00\x01\x02\x03\x04\x05"))
    elif ext in ("ttf", "otf", "woff", "woff2", "eot"):
        headers = {
            "ttf": b"\x00\x01\x00\x00",
            "otf": b"OTTO",
            "woff": b"wOFF",
            "woff2": b"wOF2",
        }
        path.write_bytes(headers.get(ext, b"\x00\x01\x02\x03"))
    elif ext in ("fbx", "obj", "gltf", "glb", "blend", "unity", "tscn", "dae", "stl", "ply"):
        if ext in ("obj", "gltf", "tscn", "dae"):
            path.write_text("# Blender OBJ\nv 0 0 0\nv 1 0 0\n", encoding="utf-8")
        else:
            path.write_bytes(b"FTM\x00" if ext == "fbx" else b"glTF\x02\x00\x00\x00" if ext == "glb" else b"BLENDER_v280" if ext == "blend" else b"\x00\x01\x02\x03")
    else:
        content_map = {
            "js": "const message = 'hello';\nconsole.log(message);",
            "ts": "const answer: number = 42;\nconsole.log(answer);",
            "tsx": "import React from 'react';\nexport const MyComponent = () => {\n  return <div>Hello</div>;\n};",
            "jsx": "import React from 'react';\nexport const MyComponent = () => {\n  return <div>Hello</div>;\n};",
            "py": "import sys\nprint('hello from python')",
            "pyw": "import sys\nprint('hello from pythonw')",
            "html": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body>Hello</body>\n</html>",
            "css": "body {\n  color: #333333;\n  background-color: #f5f5f5;\n}",
            "json": '{\n  "status": "ok",\n  "message": "success"\n}',
            "csv": "id,name\n1,test_item",
            "xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<root>\n  <status>ok</status>\n</root>",
            "md": "# Title\nHello world description",
            "yaml": "status: ok\nmessage: success",
            "yml": "status: ok\nmessage: success",
            "ini": "[settings]\nstatus = ok\nenabled = true",
            "conf": "status = ok\nenabled = true",
            "toml": "status = 'ok'\nenabled = true",
            "sql": "SELECT 1;\nSELECT 2;",
            "sh": "#!/bin/sh\necho 'starting'\necho 'done'",
            "bat": "@echo off\necho starting\necho done",
            "ps1": "Write-Host 'starting'\nWrite-Host 'done'",
            "properties": "status = ok\nenabled = true",
            "log": "2026-05-24 INFO application_started\n2026-05-24 INFO task_completed",
            "bak": "backup content\nsecond line of backup",
            "tmp": "temporary content\nsecond line of temp",
            "temp": "temporary content\nsecond line of temp",
            "rtf": "{\\rtf1\\ansi\\deff0 Hello\nsecond line}",
            "ascii": "Hello ASCII\nsecond line of ascii",
        }
        content = content_map.get(ext, "Hello World\nSecond line of hello")
        path.write_text(content, encoding="utf-8")
    return path
