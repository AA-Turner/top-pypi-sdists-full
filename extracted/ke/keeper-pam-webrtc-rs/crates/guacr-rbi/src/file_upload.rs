// File Upload support for RBI
//
// Provides file upload handling for isolated browser sessions.
// Based on KCM's rbi-file-upload branch implementation.
//
// Key features:
// - Upload size limits
// - File type restrictions (whitelist/blacklist)
// - Progress tracking
// - MIME type validation
// - Secure temporary file handling

use bytes::Bytes;
use log::{debug, info, warn};
use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;

/// Maximum file size for upload (128 MB default)
pub const MAX_UPLOAD_SIZE: usize = 128 * 1024 * 1024;

/// Maximum number of concurrent uploads
pub const MAX_CONCURRENT_UPLOADS: usize = 5;

/// Upload state
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UploadState {
    /// Waiting for file selection
    Pending,
    /// Upload in progress
    InProgress,
    /// Upload completed successfully
    Completed,
    /// Upload failed
    Failed,
    /// Upload cancelled by user
    Cancelled,
}

/// File upload configuration
#[derive(Debug, Clone)]
pub struct UploadConfig {
    /// Whether uploads are enabled
    pub enabled: bool,
    /// Maximum file size in bytes
    pub max_size: usize,
    /// Allowed file extensions (empty = allow all)
    pub allowed_extensions: Vec<String>,
    /// Blocked file extensions
    pub blocked_extensions: Vec<String>,
    /// Maximum concurrent uploads
    pub max_concurrent: usize,
}

impl Default for UploadConfig {
    fn default() -> Self {
        Self {
            enabled: false, // Disabled by default for security
            max_size: MAX_UPLOAD_SIZE,
            allowed_extensions: Vec::new(),
            blocked_extensions: vec![
                "exe".to_string(),
                "bat".to_string(),
                "cmd".to_string(),
                "ps1".to_string(),
                "vbs".to_string(),
                "js".to_string(),
                "msi".to_string(),
                "dll".to_string(),
                "scr".to_string(),
            ],
            max_concurrent: MAX_CONCURRENT_UPLOADS,
        }
    }
}

impl UploadConfig {
    /// Check if a file extension is allowed
    pub fn is_extension_allowed(&self, extension: &str) -> bool {
        let ext = extension.to_lowercase();

        // Check blocked list first
        if self
            .blocked_extensions
            .iter()
            .any(|e| e.to_lowercase() == ext)
        {
            return false;
        }

        // If allowlist is empty, allow all (except blocked)
        if self.allowed_extensions.is_empty() {
            return true;
        }

        // Check allowlist
        self.allowed_extensions
            .iter()
            .any(|e| e.to_lowercase() == ext)
    }

    /// Check if file size is within limits
    pub fn is_size_allowed(&self, size: usize) -> bool {
        size <= self.max_size
    }
}

/// Information about a file being uploaded
#[derive(Debug, Clone)]
pub struct UploadInfo {
    /// Unique identifier for this upload
    pub id: String,
    /// Original filename
    pub filename: String,
    /// MIME type
    pub mimetype: String,
    /// Total file size
    pub total_size: usize,
    /// Bytes uploaded so far
    pub uploaded_bytes: usize,
    /// Upload state
    pub state: UploadState,
}

/// File upload request from browser
#[derive(Debug, Clone)]
pub struct UploadRequest {
    /// Request ID
    pub id: String,
    /// Whether multiple files are accepted
    pub multiple: bool,
    /// Accepted MIME types
    pub accept: Vec<String>,
}

/// File upload manager
pub struct UploadManager {
    config: UploadConfig,
    /// Active uploads: upload_id -> UploadInfo
    uploads: HashMap<String, UploadInfo>,
    /// Pending upload requests from browser
    pending_requests: Vec<UploadRequest>,
    /// Counter for generating upload IDs
    next_id: u64,
    /// Whether upload dialog is currently shown
    dialog_shown: Arc<AtomicBool>,
    /// Total bytes currently being uploaded
    total_uploading_bytes: Arc<AtomicU64>,
}

impl UploadManager {
    pub fn new(config: UploadConfig) -> Self {
        Self {
            config,
            uploads: HashMap::new(),
            pending_requests: Vec::new(),
            next_id: 1,
            dialog_shown: Arc::new(AtomicBool::new(false)),
            total_uploading_bytes: Arc::new(AtomicU64::new(0)),
        }
    }

    /// Check if uploads are enabled
    pub fn is_enabled(&self) -> bool {
        self.config.enabled
    }

    /// Handle a file upload dialog request from browser
    pub fn handle_dialog_request(
        &mut self,
        multiple: bool,
        accept: Vec<String>,
    ) -> Option<UploadRequest> {
        if !self.config.enabled {
            warn!("RBI: Upload request rejected - uploads disabled");
            return None;
        }

        // Check concurrent upload limit
        let active_count = self
            .uploads
            .values()
            .filter(|u| u.state == UploadState::InProgress)
            .count();

        if active_count >= self.config.max_concurrent {
            warn!("RBI: Upload request rejected - too many concurrent uploads");
            return None;
        }

        let request = UploadRequest {
            id: format!("upload-{}", self.next_id),
            multiple,
            accept,
        };
        self.next_id += 1;

        info!(
            "RBI: Upload dialog request - id={}, multiple={}",
            request.id, multiple
        );
        self.pending_requests.push(request.clone());
        self.dialog_shown.store(true, Ordering::SeqCst);

        Some(request)
    }

    /// Start a file upload
    pub fn start_upload(
        &mut self,
        request_id: &str,
        filename: &str,
        mimetype: &str,
        size: usize,
    ) -> Result<String, String> {
        if !self.config.enabled {
            return Err("Uploads are disabled".to_string());
        }

        // Validate file size
        if !self.config.is_size_allowed(size) {
            return Err(format!(
                "File too large: {} bytes (max: {} bytes)",
                size, self.config.max_size
            ));
        }

        // Extract and validate extension
        let extension = filename.rsplit('.').next().unwrap_or("");

        if !self.config.is_extension_allowed(extension) {
            return Err(format!("File type not allowed: .{}", extension));
        }

        // Find and remove the pending request
        let request_idx = self
            .pending_requests
            .iter()
            .position(|r| r.id == request_id);

        if request_idx.is_none() {
            return Err("No pending upload request".to_string());
        }
        self.pending_requests.remove(request_idx.unwrap());

        let upload_id = format!("upload-{}", self.next_id);
        self.next_id += 1;

        let info = UploadInfo {
            id: upload_id.clone(),
            filename: filename.to_string(),
            mimetype: mimetype.to_string(),
            total_size: size,
            uploaded_bytes: 0,
            state: UploadState::InProgress,
        };

        info!(
            "RBI: Upload started - id={}, file={}, size={}",
            upload_id, filename, size
        );

        self.uploads.insert(upload_id.clone(), info);
        self.total_uploading_bytes
            .fetch_add(size as u64, Ordering::SeqCst);

        Ok(upload_id)
    }

    /// Handle upload data chunk
    pub fn handle_chunk(&mut self, upload_id: &str, data: &[u8]) -> Result<(), String> {
        let info = self
            .uploads
            .get_mut(upload_id)
            .ok_or_else(|| "Unknown upload".to_string())?;

        if info.state != UploadState::InProgress {
            return Err("Upload not in progress".to_string());
        }

        info.uploaded_bytes += data.len();

        debug!(
            "RBI: Upload chunk - id={}, bytes={}/{}",
            upload_id, info.uploaded_bytes, info.total_size
        );

        Ok(())
    }

    /// Complete an upload
    pub fn complete_upload(&mut self, upload_id: &str) -> Result<(), String> {
        let info = self
            .uploads
            .get_mut(upload_id)
            .ok_or_else(|| "Unknown upload".to_string())?;

        info.state = UploadState::Completed;
        self.total_uploading_bytes
            .fetch_sub(info.total_size as u64, Ordering::SeqCst);

        info!(
            "RBI: Upload completed - id={}, file={}",
            upload_id, info.filename
        );

        Ok(())
    }

    /// Cancel an upload
    pub fn cancel_upload(&mut self, upload_id: &str) -> Result<(), String> {
        let info = self
            .uploads
            .get_mut(upload_id)
            .ok_or_else(|| "Unknown upload".to_string())?;

        info.state = UploadState::Cancelled;
        self.total_uploading_bytes
            .fetch_sub(info.total_size as u64, Ordering::SeqCst);

        info!("RBI: Upload cancelled - id={}", upload_id);

        Ok(())
    }

    /// Fail an upload
    pub fn fail_upload(&mut self, upload_id: &str, reason: &str) {
        if let Some(info) = self.uploads.get_mut(upload_id) {
            info.state = UploadState::Failed;
            self.total_uploading_bytes
                .fetch_sub(info.total_size as u64, Ordering::SeqCst);
            warn!("RBI: Upload failed - id={}, reason={}", upload_id, reason);
        }
    }

    /// Close dialog (user cancelled or completed selection)
    pub fn close_dialog(&mut self, request_id: &str) {
        self.pending_requests.retain(|r| r.id != request_id);

        if self.pending_requests.is_empty() {
            self.dialog_shown.store(false, Ordering::SeqCst);
        }

        debug!("RBI: Upload dialog closed - request_id={}", request_id);
    }

    /// Get upload progress (0.0 to 1.0)
    pub fn get_progress(&self, upload_id: &str) -> Option<f64> {
        self.uploads.get(upload_id).map(|info| {
            if info.total_size == 0 {
                1.0
            } else {
                info.uploaded_bytes as f64 / info.total_size as f64
            }
        })
    }

    /// Get upload info
    pub fn get_upload(&self, upload_id: &str) -> Option<&UploadInfo> {
        self.uploads.get(upload_id)
    }

    /// Check if dialog is currently shown
    pub fn is_dialog_shown(&self) -> bool {
        self.dialog_shown.load(Ordering::SeqCst)
    }
}

/// Generate Guacamole instruction for upload dialog
pub fn format_upload_dialog_instruction(request: &UploadRequest) -> Bytes {
    // Use Guacamole's pipe instruction for file upload dialog
    // Format: 4.pipe,<stream>,<mimetype>,<name>;
    let accept = request.accept.join(",");
    let instr = format!(
        "4.pipe,0.{},11.application,15.upload-request,{}.{};",
        request.id.len(),
        accept.len(),
        accept
    );
    Bytes::from(instr)
}

/// Detect MIME type from filename
pub fn detect_mime_type(filename: &str) -> &'static str {
    let ext = filename.rsplit('.').next().unwrap_or("").to_lowercase();
    match ext.as_str() {
        // Images
        "png" => "image/png",
        "jpg" | "jpeg" => "image/jpeg",
        "gif" => "image/gif",
        "webp" => "image/webp",
        "svg" => "image/svg+xml",
        "ico" => "image/x-icon",
        "bmp" => "image/bmp",
        "tiff" | "tif" => "image/tiff",

        // Documents
        "pdf" => "application/pdf",
        "doc" => "application/msword",
        "docx" => "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls" => "application/vnd.ms-excel",
        "xlsx" => "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ppt" => "application/vnd.ms-powerpoint",
        "pptx" => "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "odt" => "application/vnd.oasis.opendocument.text",
        "ods" => "application/vnd.oasis.opendocument.spreadsheet",

        // Text
        "txt" => "text/plain",
        "csv" => "text/csv",
        "html" | "htm" => "text/html",
        "css" => "text/css",
        "xml" => "application/xml",
        "json" => "application/json",
        "yaml" | "yml" => "application/x-yaml",
        "md" => "text/markdown",

        // Archives
        "zip" => "application/zip",
        "tar" => "application/x-tar",
        "gz" | "gzip" => "application/gzip",
        "rar" => "application/vnd.rar",
        "7z" => "application/x-7z-compressed",

        // Audio/Video
        "mp3" => "audio/mpeg",
        "wav" => "audio/wav",
        "ogg" => "audio/ogg",
        "mp4" => "video/mp4",
        "webm" => "video/webm",
        "avi" => "video/x-msvideo",
        "mov" => "video/quicktime",

        // Other
        "wasm" => "application/wasm",

        _ => "application/octet-stream",
    }
}

/// Validate MIME type against accept filter
pub fn validate_mime_type(mimetype: &str, accept: &[String]) -> bool {
    if accept.is_empty() || accept.iter().any(|a| a == "*/*") {
        return true;
    }

    for pattern in accept {
        // Exact match
        if pattern == mimetype {
            return true;
        }

        // Wildcard match (e.g., "image/*")
        if pattern.ends_with("/*") {
            let prefix = &pattern[..pattern.len() - 1]; // "image/"
            if mimetype.starts_with(prefix) {
                return true;
            }
        }

        // Extension match (e.g., ".pdf")
        if let Some(ext) = pattern.strip_prefix('.') {
            if detect_mime_type(&format!("file.{}", ext)) == mimetype {
                return true;
            }
        }
    }

    false
}

/// Active upload with data buffer
pub struct ActiveUpload {
    pub info: UploadInfo,
    pub data: Vec<u8>,
    pub temp_path: Option<PathBuf>,
}

impl ActiveUpload {
    pub fn new(info: UploadInfo) -> Self {
        Self {
            data: Vec::with_capacity(info.total_size),
            info,
            temp_path: None,
        }
    }

    /// Append chunk data
    pub fn append_chunk(&mut self, chunk: &[u8]) -> Result<(), String> {
        if self.info.uploaded_bytes + chunk.len() > self.info.total_size {
            return Err("Chunk exceeds declared file size".to_string());
        }

        self.data.extend_from_slice(chunk);
        self.info.uploaded_bytes += chunk.len();

        Ok(())
    }

    /// Check if upload is complete
    pub fn is_complete(&self) -> bool {
        self.info.uploaded_bytes >= self.info.total_size
    }

    /// Get progress as percentage
    pub fn progress_percent(&self) -> f64 {
        if self.info.total_size == 0 {
            100.0
        } else {
            (self.info.uploaded_bytes as f64 / self.info.total_size as f64) * 100.0
        }
    }
}

/// Extended upload manager with active upload tracking
pub struct UploadEngine {
    manager: UploadManager,
    active_uploads: HashMap<String, ActiveUpload>,
    temp_dir: Option<PathBuf>,
}

impl UploadEngine {
    pub fn new(config: UploadConfig) -> Self {
        Self {
            manager: UploadManager::new(config),
            active_uploads: HashMap::new(),
            temp_dir: None,
        }
    }

    /// Set temporary directory for file storage
    pub fn set_temp_dir(&mut self, path: PathBuf) {
        self.temp_dir = Some(path);
    }

    /// Get the underlying manager
    pub fn manager(&self) -> &UploadManager {
        &self.manager
    }

    /// Get mutable reference to manager
    pub fn manager_mut(&mut self) -> &mut UploadManager {
        &mut self.manager
    }

    /// Start an upload with data tracking
    pub fn start_upload(
        &mut self,
        request_id: &str,
        filename: &str,
        mimetype: &str,
        size: usize,
    ) -> Result<String, String> {
        let upload_id = self
            .manager
            .start_upload(request_id, filename, mimetype, size)?;

        let info = self
            .manager
            .get_upload(&upload_id)
            .ok_or("Upload not found after creation")?
            .clone();

        let active = ActiveUpload::new(info);
        self.active_uploads.insert(upload_id.clone(), active);

        Ok(upload_id)
    }

    /// Handle chunk with data storage
    pub fn handle_chunk(&mut self, upload_id: &str, data: &[u8]) -> Result<f64, String> {
        self.manager.handle_chunk(upload_id, data)?;

        let active = self
            .active_uploads
            .get_mut(upload_id)
            .ok_or("Active upload not found")?;

        active.append_chunk(data)?;

        Ok(active.progress_percent())
    }

    /// Complete upload and return file data
    pub fn complete_upload(&mut self, upload_id: &str) -> Result<(UploadInfo, Vec<u8>), String> {
        self.manager.complete_upload(upload_id)?;

        let active = self
            .active_uploads
            .remove(upload_id)
            .ok_or("Active upload not found")?;

        if !active.is_complete() {
            return Err(format!(
                "Upload incomplete: {}/{} bytes",
                active.info.uploaded_bytes, active.info.total_size
            ));
        }

        Ok((active.info, active.data))
    }

    /// Cancel and cleanup
    pub fn cancel_upload(&mut self, upload_id: &str) -> Result<(), String> {
        self.manager.cancel_upload(upload_id)?;
        self.active_uploads.remove(upload_id);
        Ok(())
    }

    /// Get active upload count
    pub fn active_count(&self) -> usize {
        self.active_uploads.len()
    }

    /// Get total bytes currently being uploaded
    pub fn total_active_bytes(&self) -> usize {
        self.active_uploads
            .values()
            .map(|u| u.info.total_size)
            .sum()
    }
}
