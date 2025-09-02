// Copyright (c) 2025 Ross Gardiner
//
// SPDX-License-Identifier: BSD-3-Clause

//! Time utilities that work across different targets including WASM.

pub use std::time::Duration;

#[cfg(not(target_arch = "wasm32"))]
pub use std::time::Instant;

#[cfg(target_arch = "wasm32")]
pub use web_time::Instant;
