use rand::rngs::ThreadRng;
use std::cell::Cell;

thread_local! {
    static RNG_PID: Cell<u32> = const { Cell::new(0) };
}

pub(crate) fn rng() -> ThreadRng {
    let mut rng = rand::rng();
    RNG_PID.with(|last_pid| {
        let pid = std::process::id();
        if last_pid.get() != pid {
            // Rand no longer reseeds automatically after fork. Never reuse the
            // parent's random stream for CMAB choices or diagnostics sampling.
            rng.reseed()
                .expect("failed to reseed randomness after fork");
            last_pid.set(pid);
        }
    });
    rng
}
