mod interned_store_eval_value_tests;
mod interned_store_mmap_fetch_tests;
mod interned_store_mmap_optional_tests;
mod interned_store_mmap_v2_tests;
mod interned_store_preload_remote_tests;
mod interned_store_returnable_tests;
mod interned_store_string_tests;

#[cfg(unix)]
fn assert_child_exited_successfully(pid: libc::pid_t) {
    assert!(pid > 0, "fork failed");
    let mut status = 0;
    assert_eq!(unsafe { libc::waitpid(pid, &mut status, 0) }, pid);
    assert!(
        libc::WIFEXITED(status),
        "child terminated with status {status}"
    );
    assert_eq!(libc::WEXITSTATUS(status), 0);
}
