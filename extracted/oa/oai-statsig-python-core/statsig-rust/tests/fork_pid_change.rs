#[cfg(unix)]
#[path = "utils/fork_runtime.rs"]
mod fork_runtime;

#[cfg(unix)]
fn main() {
    use fork_runtime::{assert_task_completes, has_runtime, run_probe, wait_for_child};
    use statsig_rust::{StatsigRuntime, statsig_global::StatsigGlobal};
    use std::sync::{Arc, Barrier};
    use std::time::Duration;

    run_probe("test_pid_change_resets_inherited_runtime", || {
        let original_pid = StatsigGlobal::get().pid;
        assert!(!has_runtime());

        // Exercise the fallback when the pre-fork reset is bypassed. Keep the
        // parent worker outside Tokio's parking_lot locks; arbitrary active
        // multithreaded forks can inherit locked process-global parking buckets.
        let worker_barrier = Arc::new(Barrier::new(2));
        let worker_callback_barrier = worker_barrier.clone();
        let original_rt = StatsigRuntime::get_runtime_with_options(
            Some(1),
            Some(Arc::new(move || {
                worker_callback_barrier.wait();
                worker_callback_barrier.wait();
            })),
        );
        worker_barrier.wait();
        original_rt
            .spawn("test", |_| async {
                tokio::time::sleep(Duration::from_secs(5)).await;
            })
            .unwrap();
        assert!(has_runtime());

        let pid = unsafe { libc::fork() };
        if pid == 0 {
            unsafe { libc::alarm(10) };
            assert_ne!(StatsigGlobal::get().pid, original_pid);
            assert!(!has_runtime());
            assert_task_completes();
            assert!(has_runtime());
            unsafe { libc::_exit(0) };
        }

        worker_barrier.wait();
        wait_for_child(pid);
        assert_eq!(StatsigGlobal::get().pid, original_pid);
        assert!(has_runtime());

        let another_rt = StatsigRuntime::get_runtime();
        another_rt.shutdown();
        drop(another_rt);
        assert!(has_runtime(), "The parent runtime should not be dropped");
    });
}

#[cfg(not(unix))]
fn main() {}
