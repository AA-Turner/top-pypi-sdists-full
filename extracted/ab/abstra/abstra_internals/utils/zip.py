import io
import zipfile
from pathlib import Path


def zip_folder_to_buffer(folder: Path) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in folder.rglob("*"):
            if file_path.is_symlink():
                continue
            if not file_path.is_file():
                continue
            if not file_path.resolve().is_relative_to(folder.resolve()):
                continue
            zip_file.write(file_path, file_path.relative_to(folder))
    buf.seek(0)
    return buf
