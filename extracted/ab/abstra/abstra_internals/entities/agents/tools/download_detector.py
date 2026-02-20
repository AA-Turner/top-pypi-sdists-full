import os
import re
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class DownloadStatus(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class DownloadInfo:
    filename: str
    path: str
    size: int
    timestamp: float
    status: DownloadStatus
    error: Optional[str] = None
    trigger_action: Optional[str] = None
    url: Optional[str] = None

    def to_observation_string(self) -> str:
        if self.status == DownloadStatus.COMPLETED:
            return f"DOWNLOAD COMPLETED: '{self.filename}' ({self._format_size(self.size)}) saved to {self.path}"
        elif self.status == DownloadStatus.STARTED:
            return f"DOWNLOAD STARTED: '{self.filename}'"
        return f"DOWNLOAD FAILED: '{self.filename}' - {self.error}"

    def _format_size(self, size: int) -> str:
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        return f"{size / (1024 * 1024):.1f} MB"


DOWNLOAD_EXTENSIONS = (
    ".pdf",
    ".xlsx",
    ".xls",
    ".csv",
    ".zip",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".xml",
)

DOWNLOAD_CONTENT_TYPES = (
    "application/octet-stream",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats",
    "text/csv",
    "application/pdf",
    "application/zip",
)

BLOB_DOWNLOAD_INTERCEPTOR_JS = """
(function() {
    if (window.__blobDownloadInterceptor) return;
    window.__blobDownloadInterceptor = true;
    window.__interceptedBlobs = window.__interceptedBlobs || [];

    const originalCreateObjectURL = URL.createObjectURL;
    const blobUrlMap = new Map();

    URL.createObjectURL = function(blob) {
        const url = originalCreateObjectURL.call(URL, blob);
        if (blob instanceof Blob) {
            const reader = new FileReader();
            reader.onload = function() {
                const base64 = reader.result.split(',')[1] || '';
                blobUrlMap.set(url, {
                    data: base64, type: blob.type,
                    size: blob.size, timestamp: Date.now()
                });
            };
            reader.readAsDataURL(blob);
        }
        return url;
    };

    document.addEventListener('click', function(e) {
        const anchor = e.target.closest('a[href^="blob:"]');
        if (anchor) {
            const blobUrl = anchor.href;
            const downloadName = anchor.download || 'download';
            setTimeout(function() {
                const blobData = blobUrlMap.get(blobUrl);
                if (blobData) {
                    window.__interceptedBlobs.push({
                        filename: downloadName, data: blobData.data,
                        type: blobData.type, size: blobData.size,
                        timestamp: Date.now(), url: blobUrl
                    });
                }
            }, 500);
        }
    }, true);

    const originalClick = HTMLAnchorElement.prototype.click;
    HTMLAnchorElement.prototype.click = function() {
        if (this.href && this.href.startsWith('blob:')) {
            const blobUrl = this.href;
            const downloadName = this.download || 'download';
            setTimeout(function() {
                const blobData = blobUrlMap.get(blobUrl);
                if (blobData) {
                    window.__interceptedBlobs.push({
                        filename: downloadName, data: blobData.data,
                        type: blobData.type, size: blobData.size,
                        timestamp: Date.now(), url: blobUrl
                    });
                }
            }, 500);
        }
        return originalClick.call(this);
    };
})();
"""


class DownloadDetector:
    def __init__(self, downloads_dir: str):
        self.downloads_dir = downloads_dir
        self.known_files: Dict[str, float] = {}
        self.reported_files: Set[str] = set()
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self._snapshot_before_action: Dict[str, float] = {}
        self.event_downloads: List[DownloadInfo] = []
        self._reported_event_downloads: Set[str] = set()
        self._downloads_in_progress: int = 0
        self._download_lock = threading.Lock()
        self._download_complete_event = threading.Event()
        self._download_complete_event.set()
        self.has_filesystem_access = self._check_filesystem_access()
        if self.has_filesystem_access:
            self._initialize_known_files()

    def _check_filesystem_access(self) -> bool:
        try:
            os.makedirs(self.downloads_dir, exist_ok=True)
            test_file = os.path.join(self.downloads_dir, ".access_test")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except Exception:
            return False

    def _initialize_known_files(self) -> None:
        if not os.path.exists(self.downloads_dir):
            os.makedirs(self.downloads_dir, exist_ok=True)
            return
        for filename in os.listdir(self.downloads_dir):
            filepath = os.path.join(self.downloads_dir, filename)
            if os.path.isfile(filepath):
                self.known_files[filename] = os.path.getmtime(filepath)
                self.reported_files.add(filename)

    def snapshot_before_action(self) -> None:
        self._snapshot_before_action = self._get_current_files()

    def _get_current_files(self) -> Dict[str, float]:
        files: Dict[str, float] = {}
        if os.path.exists(self.downloads_dir):
            for filename in os.listdir(self.downloads_dir):
                filepath = os.path.join(self.downloads_dir, filename)
                if os.path.isfile(filepath):
                    try:
                        files[filename] = os.path.getmtime(filepath)
                    except OSError:
                        pass
        return files

    def detect_new_downloads(self, action: str = "") -> List[DownloadInfo]:
        if self._downloads_in_progress > 0:
            self.wait_for_pending_downloads(timeout=30.0)

        new_downloads: List[DownloadInfo] = []

        if self.has_filesystem_access:
            current_files = self._get_current_files()
            for filename, mtime in current_files.items():
                is_new = filename not in self._snapshot_before_action
                is_modified = (
                    filename in self._snapshot_before_action
                    and mtime > self._snapshot_before_action[filename]
                )
                is_unreported = filename not in self.reported_files
                if (is_new or is_modified) and is_unreported:
                    filepath = os.path.join(self.downloads_dir, filename)
                    try:
                        size = os.path.getsize(filepath)
                    except OSError:
                        size = 0
                    meta = self.metadata.get(filename, {})
                    download_info = DownloadInfo(
                        filename=filename,
                        path=filepath,
                        size=size,
                        timestamp=meta.get("timestamp", mtime),
                        status=DownloadStatus.COMPLETED,
                        url=meta.get("url"),
                        trigger_action=action,
                    )
                    new_downloads.append(download_info)
                    self.reported_files.add(filename)
                    self.known_files[filename] = mtime

        if not new_downloads:
            for download in self.event_downloads:
                if download.filename not in self._reported_event_downloads:
                    download.trigger_action = action
                    new_downloads.append(download)
                    self._reported_event_downloads.add(download.filename)

        return new_downloads

    def download_started(self) -> None:
        with self._download_lock:
            self._downloads_in_progress += 1
            self._download_complete_event.clear()

    def download_finished(self, filepath: str, size: int, url: str = "") -> None:
        suggested = os.path.basename(filepath)
        self.metadata[suggested] = {
            "url": url,
            "timestamp": time.time(),
            "suggested_name": suggested,
        }
        download_info = DownloadInfo(
            filename=suggested,
            path=filepath,
            size=size,
            timestamp=time.time(),
            status=DownloadStatus.COMPLETED if size > 0 else DownloadStatus.FAILED,
            url=url,
        )
        self.event_downloads.append(download_info)

        with self._download_lock:
            self._downloads_in_progress = max(0, self._downloads_in_progress - 1)
            if self._downloads_in_progress == 0:
                self._download_complete_event.set()

    def wait_for_pending_downloads(self, timeout: float = 30.0) -> bool:
        if self._downloads_in_progress == 0:
            return True
        return self._download_complete_event.wait(timeout=timeout)

    def get_all_downloads(self) -> List[str]:
        all_files = set(self.known_files.keys())
        all_files.update(d.filename for d in self.event_downloads)
        return list(all_files)


def is_likely_download_url(url: str) -> bool:
    url_lower = url.lower()
    url_path = url_lower.split("?")[0].split("#")[0]
    if any(url_path.endswith(ext) for ext in DOWNLOAD_EXTENSIONS):
        return True
    download_keywords = ("download", "export", "attachment")
    path_segments = url_path.split("/")
    for seg in path_segments:
        for kw in download_keywords:
            if seg == kw:
                return True
    query = url_lower.split("?", 1)[1] if "?" in url_lower else ""
    if query:
        for param in query.split("&"):
            val = param.split("=", 1)[1] if "=" in param else param
            if any(kw in val for kw in download_keywords):
                return True
    return False


def is_download_response(content_type: str, content_disposition: str) -> bool:
    is_attachment = "attachment" in content_disposition.lower()
    is_download_type = any(t in content_type.lower() for t in DOWNLOAD_CONTENT_TYPES)
    return is_attachment or is_download_type


def extract_filename(url: str, content_type: str, content_disposition: str) -> str:
    filename = None
    if content_disposition:
        match = re.search(r'filename[*]?=["\']?([^"\';\n]+)["\']?', content_disposition)
        if match:
            filename = match.group(1).strip()
            if filename.startswith("UTF-8''"):
                filename = filename[7:]
                try:
                    from urllib.parse import unquote

                    filename = unquote(filename)
                except Exception:
                    pass
            filename = os.path.basename(filename)
    if not filename:
        url_path = url.split("?")[0].split("/")[-1]
        if "." in url_path:
            filename = url_path
        else:
            ext = ".bin"
            if "excel" in content_type or "spreadsheet" in content_type:
                ext = ".xlsx"
            elif "csv" in content_type:
                ext = ".csv"
            elif "pdf" in content_type:
                ext = ".pdf"
            elif "zip" in content_type:
                ext = ".zip"
            filename = f"download_{int(time.time())}{ext}"
    return filename
