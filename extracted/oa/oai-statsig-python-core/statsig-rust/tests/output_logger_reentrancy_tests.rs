use parking_lot::Mutex;
use serial_test::serial;
use statsig_rust::output_logger::{
    LogLevel, OutputLogProvider, has_valid_log_level, initialize_output_logger, log_message,
    shutdown_output_logger,
};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::mpsc;
use std::time::Duration;

struct CallbackProvider {
    initialize: Box<dyn Fn() + Send + Sync>,
    warn: Box<dyn Fn() + Send + Sync>,
    shutdown: Box<dyn Fn() + Send + Sync>,
}

impl Default for CallbackProvider {
    fn default() -> Self {
        Self {
            initialize: Box::new(|| {}),
            warn: Box::new(|| {}),
            shutdown: Box::new(|| {}),
        }
    }
}

impl OutputLogProvider for CallbackProvider {
    fn initialize(&self) {
        (self.initialize)();
    }

    fn debug(&self, _: &str, _: String) {}
    fn info(&self, _: &str, _: String) {}

    fn warn(&self, _: &str, _: String) {
        (self.warn)();
    }

    fn error(&self, _: &str, _: String) {}

    fn shutdown(&self) {
        (self.shutdown)();
    }
}

#[test]
#[serial]
fn shutdown_from_a_log_callback_waits_for_that_callback_to_finish() {
    shutdown_output_logger();
    let warning_finished = Arc::new(AtomicBool::new(false));
    let shutdowns = Arc::new(AtomicUsize::new(0));
    let shutdown_during_warning = Arc::new(AtomicBool::new(false));
    let provider = CallbackProvider {
        warn: {
            let finished = warning_finished.clone();
            Box::new(move || {
                // A binding callback can collect an old SDK whose destructor shuts down logging.
                shutdown_output_logger();
                finished.store(true, Ordering::SeqCst);
            })
        },
        shutdown: {
            let finished = warning_finished.clone();
            let shutdowns = shutdowns.clone();
            let premature = shutdown_during_warning.clone();
            Box::new(move || {
                premature.store(!finished.load(Ordering::SeqCst), Ordering::SeqCst);
                shutdowns.fetch_add(1, Ordering::SeqCst);
            })
        },
        ..CallbackProvider::default()
    };
    initialize_output_logger(&Some(LogLevel::Warn), Some(Arc::new(provider)));
    log_message(
        "reentrant",
        LogLevel::Warn,
        "collecting a retired SDK".into(),
    );

    assert!(warning_finished.load(Ordering::SeqCst));
    assert_eq!(shutdowns.load(Ordering::SeqCst), 1);
    assert!(!shutdown_during_warning.load(Ordering::SeqCst));
    shutdown_output_logger();
    assert_eq!(shutdowns.load(Ordering::SeqCst), 2);
}

#[test]
#[serial]
fn lifecycle_callbacks_can_reenter_logger_state() {
    shutdown_output_logger();
    let initialized_with_level = Arc::new(AtomicBool::new(false));
    let shutdown_with_level = Arc::new(AtomicBool::new(false));
    let later_messages = Arc::new(AtomicUsize::new(0));
    let provider = CallbackProvider {
        initialize: {
            let initialized = initialized_with_level.clone();
            Box::new(move || {
                initialized.store(has_valid_log_level(&LogLevel::Warn), Ordering::SeqCst);
            })
        },
        shutdown: {
            let stopped = shutdown_with_level.clone();
            Box::new(move || {
                stopped.store(has_valid_log_level(&LogLevel::Warn), Ordering::SeqCst);
                shutdown_output_logger();
            })
        },
        warn: {
            let messages = later_messages.clone();
            Box::new(move || {
                messages.fetch_add(1, Ordering::SeqCst);
            })
        },
    };
    initialize_output_logger(&Some(LogLevel::Warn), Some(Arc::new(provider)));
    shutdown_output_logger();

    assert!(initialized_with_level.load(Ordering::SeqCst));
    assert!(shutdown_with_level.load(Ordering::SeqCst));
    // Other SDK instances still use the process-wide provider after one shuts down.
    log_message("still-selected", LogLevel::Warn, "later diagnostic".into());
    assert_eq!(later_messages.load(Ordering::SeqCst), 1);
}

#[test]
#[serial]
fn shutdown_waits_for_inflight_callbacks_without_resetting_the_replacement() {
    for during_initialization in [true, false] {
        shutdown_output_logger();
        let (entered, started) = mpsc::sync_channel(0);
        let (release, resume) = mpsc::sync_channel(0);
        let resume = Mutex::new(resume);
        let block_callback = Box::new(move || {
            entered.send(()).unwrap();
            resume.lock().recv_timeout(Duration::from_secs(30)).unwrap();
        });
        let old_shutdowns = Arc::new(AtomicUsize::new(0));
        let mut old = CallbackProvider {
            shutdown: {
                let shutdowns = old_shutdowns.clone();
                Box::new(move || {
                    shutdowns.fetch_add(1, Ordering::SeqCst);
                })
            },
            ..CallbackProvider::default()
        };
        if during_initialization {
            old.initialize = block_callback;
        } else {
            old.warn = block_callback;
        }
        let old = Arc::new(old);
        if !during_initialization {
            initialize_output_logger(&Some(LogLevel::Warn), Some(old.clone()));
        }
        let worker = std::thread::spawn(move || {
            if during_initialization {
                initialize_output_logger(&Some(LogLevel::Warn), Some(old));
            } else {
                log_message("old", LogLevel::Warn, "in flight".into());
            }
        });
        started.recv_timeout(Duration::from_secs(10)).unwrap();

        shutdown_output_logger();
        let old_stopped_early = old_shutdowns.load(Ordering::SeqCst);
        let new_messages = Arc::new(AtomicUsize::new(0));
        let new_shutdowns = Arc::new(AtomicUsize::new(0));
        let replacement = CallbackProvider {
            warn: {
                let messages = new_messages.clone();
                Box::new(move || {
                    messages.fetch_add(1, Ordering::SeqCst);
                })
            },
            shutdown: {
                let shutdowns = new_shutdowns.clone();
                Box::new(move || {
                    shutdowns.fetch_add(1, Ordering::SeqCst);
                })
            },
            ..CallbackProvider::default()
        };
        initialize_output_logger(&Some(LogLevel::Warn), Some(Arc::new(replacement)));
        release.send(()).unwrap();
        worker.join().unwrap();

        // Do not deliver another message on the broken implementation's blocked old provider.
        assert_eq!(old_stopped_early, 0);
        assert_eq!(old_shutdowns.load(Ordering::SeqCst), 1);
        log_message("new", LogLevel::Warn, "replacement remains live".into());
        assert_eq!(new_messages.load(Ordering::SeqCst), 1);
        assert_eq!(new_shutdowns.load(Ordering::SeqCst), 0);
        shutdown_output_logger();
        assert_eq!(new_shutdowns.load(Ordering::SeqCst), 1);
    }
}

#[test]
#[serial]
fn reused_provider_stays_open_after_an_inflight_shutdown() {
    shutdown_output_logger();
    let open = Arc::new(AtomicBool::new(false));
    let messages = Arc::new(AtomicUsize::new(0));
    let shutdowns = Arc::new(AtomicUsize::new(0));
    let (entered, started) = mpsc::sync_channel(0);
    let (release, resume) = mpsc::sync_channel(0);
    let resume = Mutex::new(resume);
    let provider = Arc::new(CallbackProvider {
        initialize: {
            let open = open.clone();
            Box::new(move || open.store(true, Ordering::SeqCst))
        },
        warn: {
            let open = open.clone();
            let messages = messages.clone();
            Box::new(move || {
                if open.load(Ordering::SeqCst) {
                    messages.fetch_add(1, Ordering::SeqCst);
                }
            })
        },
        shutdown: {
            let open = open.clone();
            Box::new(move || {
                if shutdowns.fetch_add(1, Ordering::SeqCst) == 0 {
                    entered.send(()).unwrap();
                    resume.lock().recv_timeout(Duration::from_secs(30)).unwrap();
                }
                open.store(false, Ordering::SeqCst);
            })
        },
    });
    initialize_output_logger(&Some(LogLevel::Warn), Some(provider.clone()));
    let worker = std::thread::spawn(shutdown_output_logger);
    started.recv_timeout(Duration::from_secs(10)).unwrap();

    // Cloned StatsigOptions can give a new instance this same provider.
    initialize_output_logger(&Some(LogLevel::Warn), Some(provider));
    release.send(()).unwrap();
    worker.join().unwrap();

    log_message("reused", LogLevel::Warn, "new instance diagnostic".into());
    assert_eq!(messages.load(Ordering::SeqCst), 1);
    shutdown_output_logger();
}

#[test]
#[serial]
fn reused_provider_stays_open_after_reinitialization_inside_a_callback() {
    shutdown_output_logger();
    let open = Arc::new(AtomicBool::new(false));
    let messages = Arc::new(AtomicUsize::new(0));
    let first_warning = AtomicBool::new(true);
    let provider =
        Arc::new_cyclic(
            |provider: &std::sync::Weak<CallbackProvider>| CallbackProvider {
                initialize: {
                    let open = open.clone();
                    Box::new(move || open.store(true, Ordering::SeqCst))
                },
                warn: {
                    let open = open.clone();
                    let messages = messages.clone();
                    let provider = provider.clone();
                    Box::new(move || {
                        if open.load(Ordering::SeqCst) {
                            messages.fetch_add(1, Ordering::SeqCst);
                        }
                        if first_warning.swap(false, Ordering::SeqCst) {
                            shutdown_output_logger();
                            initialize_output_logger(
                                &Some(LogLevel::Warn),
                                provider.upgrade().map(|p| p as Arc<dyn OutputLogProvider>),
                            );
                        }
                    })
                },
                shutdown: {
                    let open = open.clone();
                    Box::new(move || open.store(false, Ordering::SeqCst))
                },
            },
        );
    initialize_output_logger(&Some(LogLevel::Warn), Some(provider));
    log_message("old", LogLevel::Warn, "replace the SDK".into());
    log_message("reused", LogLevel::Warn, "new instance diagnostic".into());

    assert_eq!(messages.load(Ordering::SeqCst), 2);
    shutdown_output_logger();
}
