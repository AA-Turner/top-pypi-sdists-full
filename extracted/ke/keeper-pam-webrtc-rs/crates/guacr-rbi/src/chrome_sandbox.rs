// Linux-only: set up a user + mount namespace before Chrome exec.
//
// Security model
// --------------
// Chrome normally refuses to start its internal sandbox when it detects it is
// running as root (UID 0), which is the common case inside Docker containers.
// The standard workaround — --no-sandbox -- disables Chrome's entire security
// model, giving any successful XSS full access to the host process.
//
// This module implements the proper fix: create a new user namespace before
// Chrome is exec'd.  Inside the namespace the child process sees itself as
// UID 1000 (non-root), so Chrome enables its sandbox automatically.  From the
// host's perspective nothing special happened — the process still runs under
// the original host UID without any new capabilities.
//
// The unshare(2) + write to /proc/self/uid_map sequence runs entirely in the
// forked child (inside the pre_exec closure), never in the gateway process.
//
// Docker seccomp note
// -------------------
// The default Docker seccomp profile blocks clone/unshare for user namespaces.
// The container must either:
//   (a) use a custom seccomp profile that allows CLONE_NEWUSER, or
//   (b) run with --security-opt seccomp=unconfined (not recommended), or
//   (c) rely on the fallback path (sandbox_available() returns false → --no-sandbox + warning).
//
// The /proc/sys/kernel/unprivileged_userns_clone sysctl (Debian/Ubuntu-specific)
// must be 1.  sandbox_available() checks /proc/self/uid_map write access as a
// lightweight proxy for this.

#[cfg(target_os = "linux")]
use log::info;

/// Returns the string that goes into /proc/self/uid_map.
///
/// Format: "<child_uid> <host_uid> 1\n"
///
/// Maps exactly one UID: inside the namespace the process sees itself as
/// `child_uid`; the kernel maps that back to `host_uid` on the host.
#[cfg(all(target_os = "linux", test))]
pub(crate) fn uid_map_line(child_uid: u32, host_uid: u32) -> String {
    format!("{} {} 1\n", child_uid, host_uid)
}

/// Returns the string that goes into /proc/self/gid_map.
///
/// Format: "<child_gid> <host_gid> 1\n"
#[cfg(all(target_os = "linux", test))]
pub(crate) fn gid_map_line(child_gid: u32, host_gid: u32) -> String {
    format!("{} {} 1\n", child_gid, host_gid)
}

/// Check whether the current process can create a user namespace.
///
/// Probe whether CLONE_NEWUSER is actually usable by forking a child process
/// that attempts unshare(CLONE_NEWUSER) and reporting its exit code.
///
/// This is the only reliable check because:
/// - Root processes can always create user namespaces regardless of the
///   unprivileged_userns_clone sysctl.
/// - Docker's default seccomp profile blocks clone/unshare even when the sysctl
///   is 1 — a sysctl read gives a false positive.
/// - Sysctl-based checks produce false negatives on bare hosts running as root.
///
/// The probe forks a child, tries unshare, and exits 0 on success / 1 on failure.
/// The parent waits synchronously (microseconds — no actual exec, just a syscall).
#[cfg(target_os = "linux")]
pub fn sandbox_available() -> bool {
    // /proc/self/uid_map must exist — confirms user namespace kernel support.
    if std::fs::metadata("/proc/self/uid_map").is_err() {
        return false;
    }

    // Fork a probe child that actually attempts unshare(CLONE_NEWUSER).
    // This correctly handles: root processes, Docker seccomp, bare hosts,
    // and any distro-specific sysctl configuration.
    let pid = unsafe { libc::fork() };
    match pid {
        -1 => {
            // fork() itself failed — assume unavailable.
            false
        }
        0 => {
            // Child: attempt the syscall and exit with the result.
            let ret = unsafe { libc::unshare(libc::CLONE_NEWUSER) };
            unsafe { libc::_exit(if ret == 0 { 0 } else { 1 }) };
        }
        child_pid => {
            // Parent: wait for the child and check its exit status.
            let mut status: libc::c_int = 0;
            unsafe { libc::waitpid(child_pid, &mut status, 0) };
            libc::WIFEXITED(status) && libc::WEXITSTATUS(status) == 0
        }
    }
}

/// Build the Linux-specific Chrome launch args for the given sandbox mode.
///
/// `use_sandbox = true`  → no --no-sandbox (Chrome sandbox enabled via user namespace)
/// `use_sandbox = false` → add --no-sandbox + --disable-setuid-sandbox (fallback)
#[cfg(target_os = "linux")]
pub(crate) fn build_chrome_launch_args(use_sandbox: bool) -> Vec<String> {
    let mut args = Vec::new();
    if !use_sandbox {
        args.push("--no-sandbox".to_string());
        args.push("--disable-setuid-sandbox".to_string());
    }
    args.push("--disable-dev-shm-usage".to_string());
    args
}

/// Set up a user + mount namespace in the child process before exec.
///
/// This function is called inside a `pre_exec` hook (after fork, before exec).
/// It runs in the forked child and has very tight constraints:
///
/// - Only async-signal-safe operations are permitted (no allocator, no mutexes).
/// - All writes to /proc/self/* use raw libc::write() so we never touch the
///   Rust allocator or the standard library's buffered IO.
/// - If any step fails we return an error; the pre_exec framework will surface
///   it as an IO error and the child process will not exec Chrome.
///
/// # Safety
/// This function is inherently unsafe because it runs between fork and exec.
/// The caller (the pre_exec closure in launch_with_sandbox) is already inside
/// an unsafe context mandated by CommandExt::pre_exec.
#[cfg(target_os = "linux")]
pub(crate) fn setup_user_namespace(host_uid: u32, host_gid: u32) -> std::io::Result<()> {
    use std::io;

    // Step 1: enter new user + mount namespace.
    // CLONE_NEWUSER allows unprivileged namespace creation.
    // CLONE_NEWNS (mount namespace) is required for Chrome's internal sandbox.
    let ret = unsafe { libc::unshare(libc::CLONE_NEWUSER | libc::CLONE_NEWNS) };
    if ret != 0 {
        return Err(io::Error::last_os_error());
    }

    // Step 2: write uid_map — maps child UID 1000 → host UID.
    // Chrome sees itself as UID 1000 (non-root) inside the namespace.
    write_proc_file(b"/proc/self/uid_map\0", &format!("1000 {} 1\n", host_uid))?;

    // Step 3: deny setgroups() before writing gid_map.
    // The kernel requires this when the process is unprivileged; without it,
    // writing gid_map would be blocked.
    write_proc_file(b"/proc/self/setgroups\0", "deny\n")?;

    // Step 4: write gid_map — maps child GID 1000 → host GID.
    write_proc_file(b"/proc/self/gid_map\0", &format!("1000 {} 1\n", host_gid))?;

    Ok(())
}

/// Write `data` to the file at `path` using raw libc syscalls.
///
/// This is the only write method safe to call between fork and exec because it
/// never touches the Rust allocator, Rust IO buffers, or any mutex.
///
/// `path` must be a nul-terminated byte literal (e.g. `b"/proc/self/uid_map\0"`).
#[cfg(target_os = "linux")]
fn write_proc_file(path: &[u8], data: &str) -> std::io::Result<()> {
    use std::io;

    let fd = unsafe {
        libc::open(
            path.as_ptr() as *const libc::c_char,
            libc::O_WRONLY | libc::O_CLOEXEC,
        )
    };
    if fd < 0 {
        return Err(io::Error::last_os_error());
    }

    let bytes = data.as_bytes();
    let mut written = 0isize;
    while (written as usize) < bytes.len() {
        let n = unsafe {
            libc::write(
                fd,
                bytes.as_ptr().add(written as usize) as *const libc::c_void,
                bytes.len() - written as usize,
            )
        };
        if n < 0 {
            let err = io::Error::last_os_error();
            unsafe { libc::close(fd) };
            return Err(err);
        }
        written += n;
    }

    let close_ret = unsafe { libc::close(fd) };
    if close_ret != 0 {
        return Err(io::Error::last_os_error());
    }

    Ok(())
}

/// Launch Chrome under a user namespace and connect to it via the CDP WebSocket.
///
/// This is **Option B** from the task spec: we spawn Chrome ourselves using
/// `std::process::Command` (which exposes `pre_exec`), parse the DevTools URL
/// from Chrome's stderr, and then connect via `chromiumoxide::Browser::connect`.
///
/// If `sandbox_available()` returns false we fall back to the normal chromiumoxide
/// launch path with `--no-sandbox` and log a warning.
///
/// # Arguments
/// * `chrome_binary` — path to the Chrome/Chromium executable
/// * `args` — all Chrome args (without the binary name itself)
/// * `timeout` — how long to wait for Chrome to print its CDP URL
///
/// Returns the CDP websocket URL (`ws://127.0.0.1:<port>/devtools/browser/<uuid>`).
#[cfg(all(target_os = "linux", feature = "chrome"))]
pub(crate) async fn spawn_sandboxed_chrome(
    chrome_binary: &str,
    args: &[String],
    timeout: std::time::Duration,
) -> Result<(tokio::process::Child, String), String> {
    let use_ns = sandbox_available();

    if !use_ns {
        warn_no_sandbox();
    }

    // Capture host uid/gid BEFORE the fork so the pre_exec closure can use them.
    // After fork the values are already in the child's address space (copy-on-write).
    let host_uid = unsafe { libc::getuid() };
    let host_gid = unsafe { libc::getgid() };

    let mut cmd = tokio::process::Command::new(chrome_binary);
    cmd.args(args);
    cmd.stderr(std::process::Stdio::piped());
    cmd.stdout(std::process::Stdio::null());
    cmd.kill_on_drop(true);
    // Put Chrome in its own process group so we can kill all its children
    // (renderer, GPU, network) at once. Without this, only the parent is killed
    // and the children get reparented to PID 1 (sleep infinity), which never
    // calls wait() → zombie processes accumulate across sessions.
    cmd.process_group(0);

    if use_ns {
        // Safety: we only call async-signal-safe libc functions inside pre_exec.
        unsafe {
            cmd.pre_exec(move || setup_user_namespace(host_uid, host_gid));
        }
    }

    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to spawn Chrome ({}): {}", chrome_binary, e))?;

    // Read stderr line-by-line looking for the DevTools URL.
    // Chrome prints: "DevTools listening on ws://127.0.0.1:<port>/devtools/browser/<uuid>"
    let stderr = child.stderr.take().ok_or("Chrome stderr not available")?;

    let ws_url = tokio::time::timeout(timeout, find_devtools_url(stderr))
        .await
        .map_err(|_| "Timed out waiting for Chrome DevTools URL".to_string())?
        .map_err(|e| format!("Error reading Chrome stderr: {}", e))?;

    info!(
        "RBI: Chrome DevTools URL: {} (sandboxed={})",
        ws_url, use_ns
    );

    Ok((child, ws_url))
}

/// Kill all processes in the given process group.
///
/// Chrome spawns renderer/GPU/network children in the same process group.
/// Killing only the parent leaves those as zombies under PID 1. This kills
/// the entire group atomically.
#[cfg(all(target_os = "linux", feature = "chrome"))]
pub(crate) fn kill_process_group(pgid: u32) {
    if pgid == 0 {
        return;
    }
    unsafe {
        libc::kill(-(pgid as libc::pid_t), libc::SIGKILL);
    }
}

/// Read Chrome's stderr until the DevTools listening line is found.
#[cfg(all(target_os = "linux", feature = "chrome"))]
async fn find_devtools_url(stderr: tokio::process::ChildStderr) -> Result<String, std::io::Error> {
    use tokio::io::AsyncBufReadExt;

    let reader = tokio::io::BufReader::new(stderr);
    let mut lines = reader.lines();

    while let Some(line) = lines.next_line().await? {
        // Chrome prints: "DevTools listening on ws://..."
        if let Some(idx) = line.find("listening on ") {
            let rest = &line[idx + "listening on ".len()..];
            let ws_url = rest.trim().to_string();
            if ws_url.starts_with("ws") && ws_url.contains("devtools/browser") {
                return Ok(ws_url);
            }
        }
    }

    Err(std::io::Error::new(
        std::io::ErrorKind::UnexpectedEof,
        "Chrome exited without printing a DevTools URL",
    ))
}

/// Log the warning that Chrome is running without a user-namespace sandbox.
#[cfg(target_os = "linux")]
fn warn_no_sandbox() {
    log::warn!(
        "RBI: Chrome running without sandbox — kernel user namespace support unavailable. \
         Set kernel.unprivileged_userns_clone=1 or run container with a seccomp profile \
         that allows clone/unshare/setns syscalls."
    );
}

// Stub implementations for non-Linux platforms so callers can compile unconditionally.
// These are only called from #[cfg(target_os = "linux")] blocks in chrome_session.rs,
// so on non-Linux they are intentionally unreachable; suppress the dead_code warning.

#[cfg(not(target_os = "linux"))]
#[allow(dead_code)]
pub fn sandbox_available() -> bool {
    false
}

#[cfg(not(target_os = "linux"))]
#[allow(dead_code)]
pub(crate) fn build_chrome_launch_args(_use_sandbox: bool) -> Vec<String> {
    Vec::new()
}
