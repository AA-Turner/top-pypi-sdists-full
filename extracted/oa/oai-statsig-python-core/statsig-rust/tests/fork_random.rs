// A single-threaded executable keeps the fork probe independent of the Rust
// test harness and any async runtime threads.
#[cfg(unix)]
#[path = "../src/utils/random.rs"]
mod random;

#[cfg(unix)]
fn main() {
    use rand::RngExt;
    // Cover both upstream RNG use before the SDK and SDK use before fork.
    let _: u64 = rand::rng().random();
    check_fork();
    let _: u64 = random::rng().random();
    check_fork();
}

#[cfg(unix)]
fn check_fork() {
    use rand::RngExt;
    let mut pipe = [0; 2];
    assert_eq!(unsafe { libc::pipe(pipe.as_mut_ptr()) }, 0);
    let pid = unsafe { libc::fork() };
    assert!(pid >= 0);
    let samples: [u64; 64] = std::array::from_fn(|_| random::rng().random());
    let bytes = std::mem::size_of_val(&samples);
    if pid == 0 {
        unsafe {
            libc::close(pipe[0]);
            let written = libc::write(pipe[1], samples.as_ptr().cast(), bytes);
            libc::_exit(if written == bytes as isize { 0 } else { 1 });
        }
    }
    let mut child_samples = [0_u64; 64];
    let mut status = 0;
    unsafe {
        libc::close(pipe[1]);
        assert_eq!(
            libc::read(pipe[0], child_samples.as_mut_ptr().cast(), bytes),
            bytes as isize
        );
        libc::close(pipe[0]);
        assert_eq!(libc::waitpid(pid, &mut status, 0), pid);
    }
    assert_eq!(status, 0);
    assert_ne!(
        samples, child_samples,
        "child reused the parent's random stream"
    );
}

#[cfg(not(unix))]
fn main() {}
