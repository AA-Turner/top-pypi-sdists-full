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

    let path = logger.log_path();
    let path = path.to_string_lossy();
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

// ── Size cap, UTC day and shared lock ───────────────────────────────────
//
// Error lines pass any `SCAI_LOG_LEVEL` floor, so these tests need no ENV_LOCK.

thread_local! {
    static DAY: std::cell::RefCell<String> = std::cell::RefCell::new("20261031".to_string());
}

fn test_day() -> String {
    DAY.with(|d| d.borrow().clone())
}

fn set_day(day: &str) {
    DAY.with(|d| *d.borrow_mut() = day.to_string());
}

fn capped_logger(dir: &tempfile::TempDir, max: u64) -> ScaiLogger {
    ScaiLogger::create_with("plugin", None, dir.path().to_path_buf(), max, test_day).unwrap()
}

fn read(path: &Path) -> String {
    fs::read_to_string(path).unwrap_or_default()
}

#[test]
fn stops_writing_once_the_file_reaches_the_cap() {
    let dir = tempfile::tempdir().unwrap();
    let logger = capped_logger(&dir, 1000);

    for i in 0..100 {
        logger.error(&format!("line {i} with some padding to fill the file"));
    }

    let text = read(&logger.log_path());
    assert!(
        text.len() <= 1000,
        "file grew to {} bytes:\n{text}",
        text.len()
    );
    assert_eq!(text.matches("writes no more to it").count(), 1, "{text}");
    assert!(!text.contains("line 99 "), "{text}");
}

#[test]
fn empty_entries_stop_at_the_cap_too() {
    let dir = tempfile::tempdir().unwrap();
    let logger = capped_logger(&dir, 1000);

    for _ in 0..100 {
        logger.error("");
        logger.log(LogLevel::Error, "", Some(""));
    }

    let text = read(&logger.log_path());
    assert!(
        text.len() <= 1000,
        "file grew to {} bytes:\n{text}",
        text.len()
    );
    assert_eq!(text.matches("writes no more to it").count(), 1, "{text}");
}

#[test]
fn the_entry_that_crosses_the_cap_writes_the_notice() {
    let dir = tempfile::tempdir().unwrap();
    let logger = capped_logger(&dir, 1000);

    logger.error(&"x".repeat(2000));

    let text = read(&logger.log_path());
    assert!(text.len() <= 1000, "file grew to {} bytes", text.len());
    assert!(text.contains("x… [truncated "), "{text}");
    assert_eq!(text.matches("writes no more to it").count(), 1, "{text}");
}

#[test]
fn a_renamed_open_log_still_obeys_the_cap() {
    let dir = tempfile::tempdir().unwrap();
    let logger = capped_logger(&dir, 1000);
    logger.error("first line");
    let renamed = dir.path().join("renamed.log");
    fs::rename(logger.log_path(), &renamed).unwrap();

    for _ in 0..20 {
        logger.error(&"x".repeat(2000));
    }

    let len = fs::metadata(&renamed).unwrap().len();
    assert!(len <= 1000, "renamed open log grew to {len} bytes");
}

#[test]
fn a_new_utc_day_moves_to_that_days_file() {
    let dir = tempfile::tempdir().unwrap();
    set_day("20261031");
    let logger = capped_logger(&dir, 1000);
    for i in 0..100 {
        logger.error(&format!("day one line {i} with padding to fill the file"));
    }
    let day_one = logger.log_path();

    set_day("20261101");
    logger.error("day two first line");

    assert!(day_one.ends_with("scai20261031.log"));
    assert!(read(&day_one).contains("writes no more to it"));
    assert_eq!(logger.log_path(), dir.path().join("scai20261101.log"));
    assert!(read(&logger.log_path()).contains("[ERR] ps=plugin: day two first line"));
}

#[test]
fn an_oversized_entry_is_cut_to_fit_under_the_cap() {
    let dir = tempfile::tempdir().unwrap();
    let max = 4096;
    let logger = ScaiLogger::create_with(
        "plugin",
        Some("proj"),
        dir.path().to_path_buf(),
        max,
        test_day,
    )
    .unwrap()
    .with_session_id("s1");

    logger.log(
        LogLevel::Error,
        &"x".repeat(1024 * 1024),
        Some(&"y".repeat(1024 * 1024)),
    );
    for _ in 0..10 {
        logger.error(&"z".repeat(1024 * 1024));
    }

    let text = read(&logger.log_path());
    assert!(
        text.len() as u64 <= max,
        "file grew to {} bytes",
        text.len()
    );
    assert!(text.contains("x… [truncated "), "{text}");
    assert!(text.contains("y… [truncated "), "{text}");
    assert_eq!(text.matches("writes no more to it").count(), 1, "{text}");
}

#[test]
fn a_large_entry_under_the_cap_is_written_whole() {
    let dir = tempfile::tempdir().unwrap();
    let logger = capped_logger(&dir, 4 * 1024 * 1024);
    let response = format!("{}ERROR: tail of the response", "x".repeat(1024 * 1024));

    logger.log(LogLevel::Error, "scai failed", Some(&response));

    let text = read(&logger.log_path());
    assert!(text.contains("ERROR: tail of the response"));
    assert!(!text.contains("truncated"));
}

#[test]
fn a_file_another_process_filled_to_the_cap_gets_nothing_more() {
    let dir = tempfile::tempdir().unwrap();
    let max = 4096;
    let logger = capped_logger(&dir, max);
    fs::write(logger.log_path(), "s".repeat(max as usize - 64)).unwrap();

    logger.error(&"x".repeat(1024 * 1024));

    assert!(fs::metadata(logger.log_path()).unwrap().len() <= max);
}

fn assert_concurrent_writes_share_the_cap(dir: &tempfile::TempDir) {
    // Spawned threads start on DAY's default; keep this thread on the same day.
    set_day("20261031");
    let max = 4 * 1024 * 1024;
    let loggers: Vec<_> = (0..16)
        .map(|i| {
            ScaiLogger::create_with("app", None, dir.path().to_path_buf(), max, test_day)
                .unwrap()
                .with_session_id(&format!("s{i}"))
        })
        .collect();
    let path = loggers[0].log_path();
    let barrier = std::sync::Barrier::new(loggers.len());
    let message = "x".repeat(1024 * 1024);

    std::thread::scope(|s| {
        for logger in &loggers {
            s.spawn(|| {
                barrier.wait();
                logger.error(&message);
            });
        }
    });

    let size = fs::metadata(&path).unwrap().len();
    assert!(size > 0, "no concurrent write reached the shared file");
    assert!(
        size <= max,
        "shared file grew to {size} bytes above cap {max}"
    );
}

#[test]
fn concurrent_loggers_on_one_file_share_the_cap() {
    assert_concurrent_writes_share_the_cap(&tempfile::tempdir().unwrap());
}

#[cfg(unix)]
#[test]
fn a_read_only_lock_file_still_serializes_writers() {
    use std::os::unix::fs::PermissionsExt;
    let dir = tempfile::tempdir().unwrap();
    let lock = dir.path().join(LOCK_FILE);
    fs::write(&lock, "").unwrap();
    fs::set_permissions(&lock, fs::Permissions::from_mode(0o444)).unwrap();
    assert_concurrent_writes_share_the_cap(&dir);
}

#[test]
fn nothing_is_written_without_the_shared_lock() {
    let dir = tempfile::tempdir().unwrap();
    fs::create_dir(dir.path().join(LOCK_FILE)).unwrap();
    let logger = capped_logger(&dir, 4096);

    logger.error("unserialized");

    assert!(!read(&logger.log_path()).contains("unserialized"));
}
