//! Port of `software.amazon.kinesis.utils.Cgroup`.
//!
//! Linux cgroup filesystem helpers used by the CPU worker metrics. Reads a
//! single line from a cgroup file and parses cpuset range-lists.
//!
//! Java's static methods read from an absolute path; the port keeps the same
//! signatures (`read_single_line_file(path)` / `get_available_cpus_from_effective_cpu_set(cpu_set)`)
//! and the CPU-metric implementations inject the file paths, so tests point at
//! fixture files under a temp directory.

use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

/// Read the first line of the file at `path`.
///
/// Port of `Cgroup.readSingleLineFile`. **Panics** (Java throws
/// `IllegalArgumentException`) if the file does not exist or cannot be read,
/// with the same messages as Java:
/// - `"Failed to read file. {path} does not exist"` when the file is absent,
/// - `"Failed to read file."` for any other read error.
pub fn read_single_line_file(path: &str) -> String {
    if !Path::new(path).exists() {
        panic!("Failed to read file. {} does not exist", path);
    }
    let file = match File::open(path) {
        Ok(f) => f,
        Err(_) => panic!("Failed to read file."),
    };
    let mut reader = BufReader::new(file);
    let mut line = String::new();
    match reader.read_line(&mut line) {
        Ok(_) => {}
        Err(_) => panic!("Failed to read file."),
    }
    // Java's BufferedReader.readLine() strips the trailing line terminator.
    while line.ends_with('\n') || line.ends_with('\r') {
        line.pop();
    }
    line
}

/// Compute the number of available CPUs from a cgroup cpuset string.
///
/// Port of `Cgroup.getAvailableCpusFromEffectiveCpuSet`. See
/// <https://docs.kernel.org/admin-guide/cgroup-v2.html#cpuset>.
/// `"0-7"` -> 8 cores; `"0-4,6,8-10"` -> 9 cores. No validation of malformed
/// input (matches Java, which lets `NumberFormatException` propagate — here a
/// parse failure panics).
pub fn get_available_cpus_from_effective_cpu_set(cpu_set: &str) -> i32 {
    let mut sum_cpus = 0;
    for cpu_set_group in cpu_set.split(',') {
        if cpu_set_group.contains('-') {
            let parts: Vec<&str> = cpu_set_group.split('-').collect();
            // Values are inclusive.
            let lo: i32 = parts[0].parse().expect("invalid cpuset range lower bound");
            let hi: i32 = parts[1].parse().expect("invalid cpuset range upper bound");
            sum_cpus += hi - lo + 1;
        } else {
            sum_cpus += 1;
        }
    }
    sum_cpus
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_available_cpus_from_effective_cpu_set() {
        assert_eq!(8, get_available_cpus_from_effective_cpu_set("0-7"));
        assert_eq!(9, get_available_cpus_from_effective_cpu_set("0-4,6,8-10"));
        assert_eq!(4, get_available_cpus_from_effective_cpu_set("0,6,8,10"));
        assert_eq!(5, get_available_cpus_from_effective_cpu_set("1-2,8,10,11"));
        assert_eq!(1, get_available_cpus_from_effective_cpu_set("0"));
    }

    #[test]
    fn read_single_line_reads_first_line() {
        let dir = std::env::temp_dir().join(format!("cgroup-test-{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let path = dir.join("single");
        std::fs::write(&path, "first line\nsecond line\n").unwrap();
        assert_eq!(read_single_line_file(path.to_str().unwrap()), "first line");
        std::fs::remove_dir_all(&dir).ok();
    }

    #[test]
    #[should_panic(expected = "does not exist")]
    fn read_single_line_missing_file_panics() {
        read_single_line_file("/nonexistent/path/for/cgroup/test");
    }
}
