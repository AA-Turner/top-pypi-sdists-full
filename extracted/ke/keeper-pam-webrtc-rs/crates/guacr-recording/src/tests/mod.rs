// Unit tests for guacr-recording, organized by source module.
// Each sub-module corresponds to a source file of the same base name.

mod asciicast_tests;
#[cfg(unix)]
mod async_fifo_tests;
mod config_tests;
mod helpers_tests;
mod multi_tests;
mod ses_tests;
mod writer_thread_tests;
#[cfg(feature = "zmq-transport")]
mod zmq_transport_tests;
