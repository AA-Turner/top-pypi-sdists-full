use std::fs;

use chrono::Utc;

use super::*;

static ENV_LOCK: std::sync::Mutex<()> = std::sync::Mutex::new(());

fn test_logger(process: &str) -> (ScaiLogger, tempfile::TempDir) {
    let dir = tempfile::tempdir().unwrap();
    let logger = ScaiLogger::init_in_dir(process, dir.path().to_path_buf()).unwrap();
    (logger, dir)
}

#[test]
fn log_level_ordering() {
    assert!(LogLevel::Debug < LogLevel::Info);
    assert!(LogLevel::Info < LogLevel::Warn);
    assert!(LogLevel::Warn < LogLevel::Error);
}

#[test]
fn log_level_from_str() {
    assert_eq!("debug".parse::<LogLevel>().unwrap(), LogLevel::Debug);
    assert_eq!("INFO".parse::<LogLevel>().unwrap(), LogLevel::Info);
    assert_eq!("Warn".parse::<LogLevel>().unwrap(), LogLevel::Warn);
    assert_eq!("warning".parse::<LogLevel>().unwrap(), LogLevel::Warn);
    assert_eq!("error".parse::<LogLevel>().unwrap(), LogLevel::Error);
    assert!("invalid".parse::<LogLevel>().is_err());
}

#[test]
fn logger_writes_to_file() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let (logger, _dir) = test_logger("CLI");

    logger.info("test message");
    logger.log(LogLevel::Warn, "structured", Some(r#"{"key":"value"}"#));

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(content.contains("[INF] ps=CLI: test message"));
    assert!(content.contains(r#"[WRN] ps=CLI: structured | {"key":"value"}"#));
}

#[test]
fn logger_with_project_id_includes_pr_tag() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let dir = tempfile::tempdir().unwrap();
    let logger =
        ScaiLogger::init_in_dir_with_project_id("CLI", "my-proj", dir.path().to_path_buf())
            .unwrap();

    logger.info("with project");

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(content.contains("[INF] ps=CLI pr=my-proj: with project"));
}

#[test]
fn logger_with_session_id_includes_sn_tag() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let dir = tempfile::tempdir().unwrap();
    let logger =
        ScaiLogger::init_in_dir_with_project_id("CLI", "my-proj", dir.path().to_path_buf())
            .unwrap()
            .with_session_id("abc-123");

    logger.info("with session");

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(content.contains("[INF] ps=CLI pr=my-proj sn=abc-123: with session"));
}

#[test]
fn is_enabled_reflects_min_level() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let (logger, _dir) = test_logger("TEST");

    assert!(!logger.is_enabled(LogLevel::Debug));
    assert!(logger.is_enabled(LogLevel::Info));
    assert!(logger.is_enabled(LogLevel::Warn));
    assert!(logger.is_enabled(LogLevel::Error));
}

#[test]
fn default_level_drops_debug() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let (logger, _dir) = test_logger("TEST");

    logger.debug("should be filtered");
    logger.info("should appear");

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(!content.contains("should be filtered"));
    assert!(content.contains("[INF] ps=TEST: should appear"));
}

#[test]
fn log_path_uses_compact_date() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::remove_var("SCAI_LOG_LEVEL");
    let (logger, _dir) = test_logger("CLI");

    let path = logger.log_path().to_string_lossy();
    let today = Utc::now().format("%Y%m%d").to_string();
    assert!(path.contains(&format!("scai{today}.log")));
}

#[test]
fn env_var_overrides_min_level() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::set_var("SCAI_LOG_LEVEL", "debug");
    let (logger, _dir) = test_logger("ENV");
    std::env::remove_var("SCAI_LOG_LEVEL");

    logger.debug("now visible");
    logger.info("also visible");

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(content.contains("[DBG] ps=ENV: now visible"));
    assert!(content.contains("[INF] ps=ENV: also visible"));
}

#[test]
fn env_var_error_level_drops_info_and_warn() {
    let _g = ENV_LOCK.lock().unwrap();
    std::env::set_var("SCAI_LOG_LEVEL", "error");
    let (logger, _dir) = test_logger("ENV2");
    std::env::remove_var("SCAI_LOG_LEVEL");

    logger.info("should be dropped");
    logger.warn("should be dropped");
    logger.error("should appear");

    let content = fs::read_to_string(logger.log_path()).unwrap();
    assert!(!content.contains("should be dropped"));
    assert!(content.contains("[ERR] ps=ENV2: should appear"));
}
