use crate::file_upload::{
    detect_mime_type, format_upload_dialog_instruction, validate_mime_type, ActiveUpload,
    UploadConfig, UploadEngine, UploadInfo, UploadManager, UploadRequest, UploadState,
};

#[test]
fn test_extension_validation() {
    let config = UploadConfig::default();

    assert!(!config.is_extension_allowed("exe"));
    assert!(!config.is_extension_allowed("EXE"));
    assert!(!config.is_extension_allowed("bat"));
    assert!(!config.is_extension_allowed("ps1"));
    assert!(!config.is_extension_allowed("vbs"));
    assert!(!config.is_extension_allowed("msi"));
    assert!(!config.is_extension_allowed("dll"));
    assert!(!config.is_extension_allowed("scr"));

    assert!(config.is_extension_allowed("pdf"));
    assert!(config.is_extension_allowed("txt"));
    assert!(config.is_extension_allowed("png"));
    assert!(config.is_extension_allowed("docx"));
}

#[test]
fn test_extension_allowlist() {
    let config = UploadConfig {
        enabled: true,
        allowed_extensions: vec!["pdf".to_string(), "txt".to_string()],
        ..Default::default()
    };

    assert!(config.is_extension_allowed("pdf"));
    assert!(config.is_extension_allowed("txt"));
    assert!(config.is_extension_allowed("PDF"));
    assert!(!config.is_extension_allowed("png"));
    assert!(!config.is_extension_allowed("exe"));
}

#[test]
fn test_size_validation() {
    let config = UploadConfig {
        max_size: 1024,
        ..Default::default()
    };

    assert!(config.is_size_allowed(0));
    assert!(config.is_size_allowed(512));
    assert!(config.is_size_allowed(1024));
    assert!(!config.is_size_allowed(1025));
    assert!(!config.is_size_allowed(1024 * 1024));
}

#[test]
fn test_upload_manager_basic() {
    let config = UploadConfig {
        enabled: true,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let request = manager.handle_dialog_request(false, vec!["image/*".to_string()]);
    assert!(request.is_some());
    assert!(manager.is_dialog_shown());

    let request = request.unwrap();

    let result = manager.start_upload(&request.id, "test.png", "image/png", 1024);
    assert!(result.is_ok());

    let upload_id = result.unwrap();

    assert_eq!(manager.get_progress(&upload_id), Some(0.0));

    assert!(manager.handle_chunk(&upload_id, &[0u8; 512]).is_ok());
    assert_eq!(manager.get_progress(&upload_id), Some(0.5));

    assert!(manager.complete_upload(&upload_id).is_ok());

    let info = manager.get_upload(&upload_id).unwrap();
    assert_eq!(info.state, UploadState::Completed);
}

#[test]
fn test_upload_manager_disabled() {
    let config = UploadConfig {
        enabled: false,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let request = manager.handle_dialog_request(false, vec![]);
    assert!(request.is_none());
}

#[test]
fn test_upload_manager_concurrent_limit() {
    let config = UploadConfig {
        enabled: true,
        max_concurrent: 2,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let r1 = manager.handle_dialog_request(false, vec![]).unwrap();
    manager
        .start_upload(&r1.id, "f1.txt", "text/plain", 100)
        .unwrap();

    let r2 = manager.handle_dialog_request(false, vec![]).unwrap();
    manager
        .start_upload(&r2.id, "f2.txt", "text/plain", 100)
        .unwrap();

    let r3 = manager.handle_dialog_request(false, vec![]);
    assert!(r3.is_none());
}

#[test]
fn test_upload_manager_blocked_extension() {
    let config = UploadConfig {
        enabled: true,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let request = manager.handle_dialog_request(false, vec![]).unwrap();

    let result = manager.start_upload(&request.id, "malware.exe", "application/x-msdownload", 1024);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("not allowed"));
}

#[test]
fn test_upload_manager_size_limit() {
    let config = UploadConfig {
        enabled: true,
        max_size: 1024,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let request = manager.handle_dialog_request(false, vec![]).unwrap();

    let result = manager.start_upload(&request.id, "huge.pdf", "application/pdf", 2048);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("too large"));
}

#[test]
fn test_upload_manager_cancel() {
    let config = UploadConfig {
        enabled: true,
        ..Default::default()
    };
    let mut manager = UploadManager::new(config);

    let request = manager.handle_dialog_request(false, vec![]).unwrap();
    let upload_id = manager
        .start_upload(&request.id, "test.txt", "text/plain", 1024)
        .unwrap();

    assert!(manager.cancel_upload(&upload_id).is_ok());

    let info = manager.get_upload(&upload_id).unwrap();
    assert_eq!(info.state, UploadState::Cancelled);
}

#[test]
fn test_mime_type_detection() {
    assert_eq!(detect_mime_type("photo.png"), "image/png");
    assert_eq!(detect_mime_type("photo.jpg"), "image/jpeg");
    assert_eq!(detect_mime_type("photo.JPEG"), "image/jpeg");
    assert_eq!(detect_mime_type("icon.gif"), "image/gif");
    assert_eq!(detect_mime_type("modern.webp"), "image/webp");

    assert_eq!(detect_mime_type("doc.pdf"), "application/pdf");
    assert_eq!(
        detect_mime_type("doc.docx"),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    );
    assert_eq!(
        detect_mime_type("sheet.xlsx"),
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    );

    assert_eq!(detect_mime_type("readme.txt"), "text/plain");
    assert_eq!(detect_mime_type("data.csv"), "text/csv");
    assert_eq!(detect_mime_type("config.json"), "application/json");
    assert_eq!(detect_mime_type("page.html"), "text/html");

    assert_eq!(detect_mime_type("files.zip"), "application/zip");
    assert_eq!(detect_mime_type("backup.tar"), "application/x-tar");
    assert_eq!(detect_mime_type("backup.gz"), "application/gzip");

    assert_eq!(detect_mime_type("data.xyz"), "application/octet-stream");
    assert_eq!(detect_mime_type("noext"), "application/octet-stream");
}

#[test]
fn test_mime_type_validation() {
    assert!(validate_mime_type("image/png", &["*/*".to_string()]));
    assert!(validate_mime_type("text/plain", &["*/*".to_string()]));

    assert!(validate_mime_type("image/png", &[]));

    assert!(validate_mime_type("image/png", &["image/png".to_string()]));
    assert!(!validate_mime_type(
        "image/png",
        &["image/jpeg".to_string()]
    ));

    assert!(validate_mime_type("image/png", &["image/*".to_string()]));
    assert!(validate_mime_type("image/jpeg", &["image/*".to_string()]));
    assert!(!validate_mime_type("text/plain", &["image/*".to_string()]));

    assert!(validate_mime_type("application/pdf", &[".pdf".to_string()]));
    assert!(!validate_mime_type("image/png", &[".pdf".to_string()]));

    assert!(validate_mime_type(
        "image/png",
        &["image/*".to_string(), ".pdf".to_string()]
    ));
    assert!(validate_mime_type(
        "application/pdf",
        &["image/*".to_string(), ".pdf".to_string()]
    ));
    assert!(!validate_mime_type(
        "text/plain",
        &["image/*".to_string(), ".pdf".to_string()]
    ));
}

#[test]
fn test_active_upload() {
    let info = UploadInfo {
        id: "test".to_string(),
        filename: "test.txt".to_string(),
        mimetype: "text/plain".to_string(),
        total_size: 100,
        uploaded_bytes: 0,
        state: UploadState::InProgress,
    };

    let mut active = ActiveUpload::new(info);

    assert!(!active.is_complete());
    assert_eq!(active.progress_percent(), 0.0);

    active.append_chunk(&[0u8; 50]).unwrap();
    assert_eq!(active.progress_percent(), 50.0);
    assert!(!active.is_complete());

    active.append_chunk(&[0u8; 50]).unwrap();
    assert_eq!(active.progress_percent(), 100.0);
    assert!(active.is_complete());

    let result = active.append_chunk(&[0u8; 1]);
    assert!(result.is_err());
}

#[test]
fn test_upload_engine() {
    let config = UploadConfig {
        enabled: true,
        ..Default::default()
    };
    let mut engine = UploadEngine::new(config);

    assert_eq!(engine.active_count(), 0);

    let request = engine
        .manager_mut()
        .handle_dialog_request(false, vec![])
        .unwrap();
    let upload_id = engine
        .start_upload(&request.id, "test.txt", "text/plain", 100)
        .unwrap();

    assert_eq!(engine.active_count(), 1);
    assert_eq!(engine.total_active_bytes(), 100);

    let progress = engine.handle_chunk(&upload_id, &[0u8; 50]).unwrap();
    assert_eq!(progress, 50.0);

    let progress = engine.handle_chunk(&upload_id, &[1u8; 50]).unwrap();
    assert_eq!(progress, 100.0);

    let (info, data) = engine.complete_upload(&upload_id).unwrap();
    assert_eq!(info.filename, "test.txt");
    assert_eq!(data.len(), 100);
    assert_eq!(&data[..50], &[0u8; 50]);
    assert_eq!(&data[50..], &[1u8; 50]);

    assert_eq!(engine.active_count(), 0);
}

#[test]
fn test_upload_request_format() {
    let request = UploadRequest {
        id: "upload-1".to_string(),
        multiple: true,
        accept: vec!["image/*".to_string(), ".pdf".to_string()],
    };

    let instr = format_upload_dialog_instruction(&request);
    let instr_str = String::from_utf8_lossy(&instr);

    assert!(instr_str.contains("pipe"));
    assert!(instr_str.contains("upload-request"));
}

#[test]
fn test_upload_zero_size() {
    let info = UploadInfo {
        id: "test".to_string(),
        filename: "empty.txt".to_string(),
        mimetype: "text/plain".to_string(),
        total_size: 0,
        uploaded_bytes: 0,
        state: UploadState::InProgress,
    };

    let active = ActiveUpload::new(info);

    assert!(active.is_complete());
    assert_eq!(active.progress_percent(), 100.0);
}
