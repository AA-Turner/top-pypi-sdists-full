#[cfg(unix)]
#[path = "utils/fork_runtime.rs"]
mod fork_runtime;

#[cfg(unix)]
fn main() {
    use fork_runtime::{assert_task_completes, has_runtime, run_probe, wait_for_child};
    use statsig_rust::{Statsig, StatsigOptions, StatsigRuntime, statsig_global::StatsigGlobal};
    use std::sync::Arc;

    fn initialize_and_shutdown() {
        let statsig = Statsig::new(
            "secret-fork-lifecycle",
            Some(Arc::new(StatsigOptions {
                disable_network: Some(true),
                disable_disk_access: Some(true),
                disable_all_logging: Some(true),
                sdk_runtime_thread_count: Some(1),
                ..StatsigOptions::default()
            })),
        );
        let runtime = StatsigRuntime::get_runtime();
        let handle = runtime.get_handle().unwrap();
        handle.block_on(statsig.initialize()).unwrap();
        assert!(statsig.is_initialized());
        assert_task_completes();
        handle.block_on(statsig.shutdown()).unwrap();
    }

    run_probe("test_shutdown_reset_fork_reinitialize", || {
        let original_pid = StatsigGlobal::get().pid;
        assert!(!has_runtime());
        initialize_and_shutdown();

        // SDK shutdown leaves the shared runtime alive. The Python pre-fork
        // hook calls reset to drop it and join its workers before fork.
        let old_runtime = Arc::downgrade(
            StatsigGlobal::get()
                .tokio_runtime
                .try_lock()
                .unwrap()
                .as_ref()
                .expect("shutdown should retain the shared runtime"),
        );
        StatsigGlobal::reset();
        assert!(
            old_runtime.upgrade().is_none(),
            "reset must drop the runtime"
        );
        assert!(!has_runtime());

        let pid = unsafe { libc::fork() };
        if pid == 0 {
            unsafe { libc::alarm(10) };
            assert_ne!(StatsigGlobal::get().pid, original_pid);
            assert!(!has_runtime());
            initialize_and_shutdown();
            unsafe { libc::_exit(0) };
        }

        wait_for_child(pid);
        assert_eq!(StatsigGlobal::get().pid, original_pid);
        assert!(!has_runtime());
        initialize_and_shutdown();
        StatsigGlobal::reset();
        assert!(!has_runtime());
    });
}

#[cfg(not(unix))]
fn main() {}
