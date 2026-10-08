use statsig_rust::{StatsigRuntime, statsig_global::StatsigGlobal};
use std::io::{Read, Write};
use std::os::unix::net::UnixStream;
use std::time::Duration;

pub fn run_probe(name: &str, probe: impl FnOnce()) {
    // Expose a single test to nextest without adding libtest worker threads.
    if std::env::args().any(|arg| arg == "--ignored") {
        return;
    }
    if std::env::args().any(|arg| arg == "--list") {
        println!("{name}: test");
        return;
    }

    // Bound parent startup, reset, and waitpid as well as child failures.
    unsafe { libc::alarm(15) };
    probe();
    unsafe { libc::alarm(0) };
}

pub fn has_runtime() -> bool {
    StatsigGlobal::get()
        .tokio_runtime
        .try_lock()
        .expect("Failed to lock tokio runtime")
        .is_some()
}

pub fn assert_task_completes() {
    let runtime = StatsigRuntime::get_runtime();
    // A socket pair avoids reusing a thread-local channel parker after fork.
    let (mut reader, mut writer) = UnixStream::pair().unwrap();
    reader
        .set_read_timeout(Some(Duration::from_secs(5)))
        .unwrap();
    runtime
        .spawn("fork_probe", |_| async move {
            tokio::time::sleep(Duration::from_millis(1)).await;
            writer.write_all(&[1]).unwrap();
        })
        .unwrap();
    reader.read_exact(&mut [0]).unwrap();
}

pub fn wait_for_child(pid: libc::pid_t) {
    assert!(pid > 0, "fork failed");
    let mut status = 0;
    assert_eq!(unsafe { libc::waitpid(pid, &mut status, 0) }, pid);
    assert!(
        libc::WIFEXITED(status),
        "child terminated with status {status}"
    );
    assert_eq!(libc::WEXITSTATUS(status), 0);
}
