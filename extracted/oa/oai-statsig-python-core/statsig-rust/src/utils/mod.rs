pub(crate) mod random;

#[cfg(all(test, target_os = "linux", target_env = "gnu"))]
mod heap_trim_tests;

#[cfg(target_env = "gnu")]
use crate::log_d;

// Manually free memory
#[cfg(target_env = "gnu")]
extern "C" {
    fn malloc_trim(pad: libc::size_t) -> libc::c_int;
}

#[cfg(target_env = "gnu")]
pub fn try_release_unused_heap_memory() {
    if matches!(
        std::env::var("NO_MALLOC_TRIM").as_deref(),
        Ok("1") | Ok("true")
    ) {
        return;
    }

    // Return free pages that glibc may retain after deserializing large configs.
    unsafe {
        // Free as much memory as possible
        let result = malloc_trim(0);
        if result == 0 {
            log_d!("MemoryUtils", "No memory was released by malloc_trim.");
        } else {
            log_d!("MemoryUtils", "Memory was released by malloc_trim.");
        }
    }
}
#[cfg(not(target_env = "gnu"))]
pub fn try_release_unused_heap_memory() {
    // No-op only glibc supports malloc_trim function
}

const LOGGABLE_KEY_PREFIX_LENGTH: usize = 13;

pub(crate) fn get_loggable_sdk_key(sdk_key: &str) -> String {
    sdk_key.chars().take(LOGGABLE_KEY_PREFIX_LENGTH).collect()
}
