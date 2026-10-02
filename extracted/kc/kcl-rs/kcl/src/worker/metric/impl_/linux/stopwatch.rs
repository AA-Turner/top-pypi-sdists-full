//! Minimal port of the Guava `Stopwatch` (+ `Ticker`) used by the Linux network
//! worker metrics to measure elapsed time between `capture()` calls.
//!
//! Only the surface the network metric needs is modeled: `is_running`,
//! `start`, `reset`, and `elapsed_nanos`. The injectable [`Ticker`] lets tests
//! feed a deterministic time source (Java `Stopwatch.createUnstarted(ticker)`).

use std::sync::Arc;
use std::sync::Mutex;
use std::time::Instant;

/// A nanosecond time source (Guava `Ticker`).
#[derive(Clone)]
pub struct Ticker {
    read: Arc<dyn Fn() -> i64 + Send + Sync>,
}

impl Ticker {
    /// A system ticker backed by [`Instant`].
    pub fn system() -> Self {
        let base = Instant::now();
        Self {
            read: Arc::new(move || base.elapsed().as_nanos() as i64),
        }
    }

    /// A ticker backed by an arbitrary closure returning nanos.
    pub fn from_fn(f: impl Fn() -> i64 + Send + Sync + 'static) -> Self {
        Self { read: Arc::new(f) }
    }

    /// The Guava test ticker: each `read()` returns `read_count * tick_millis`
    /// converted to nanos, where `read_count` starts at 1 and increments on
    /// every call (mirrors the Java anonymous `Ticker` in the network test).
    pub fn one_second_style(tick_millis: i64) -> Self {
        let count = Mutex::new(0i64);
        Self {
            read: Arc::new(move || {
                let mut c = count.lock().unwrap();
                *c += 1;
                *c * tick_millis * 1_000_000
            }),
        }
    }

    fn read(&self) -> i64 {
        (self.read)()
    }
}

impl std::fmt::Debug for Ticker {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("Ticker")
    }
}

/// A Guava-style stopwatch. Created **unstarted**; `elapsed_nanos` measures from
/// the last `start()` (which records a ticker read) to a fresh ticker read.
#[derive(Debug)]
pub struct Stopwatch {
    ticker: Ticker,
    is_running: bool,
    start_tick: i64,
}

impl Stopwatch {
    /// Create an unstarted stopwatch backed by `ticker` (Java
    /// `Stopwatch.createUnstarted(ticker)`).
    pub fn create_unstarted(ticker: Ticker) -> Self {
        Self {
            ticker,
            is_running: false,
            start_tick: 0,
        }
    }

    /// Whether the stopwatch is currently running.
    pub fn is_running(&self) -> bool {
        self.is_running
    }

    /// Start the stopwatch, recording the current tick.
    pub fn start(&mut self) -> &mut Self {
        self.is_running = true;
        self.start_tick = self.ticker.read();
        self
    }

    /// Reset the stopwatch to the stopped/zero state.
    pub fn reset(&mut self) -> &mut Self {
        self.is_running = false;
        self.start_tick = 0;
        self
    }

    /// Elapsed nanos since `start()` (reads the ticker again for "now").
    pub fn elapsed_nanos(&self) -> i64 {
        self.ticker.read() - self.start_tick
    }
}
