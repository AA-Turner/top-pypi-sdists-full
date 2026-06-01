//! wgpu 기반 GPU 백엔드 (Tier-1, v0.5.0).
//!
//! WGSL compute shader 로 single-qubit / 2-qubit gate 적용.  wgpu 29.x 의
//! request_adapter (HighPerformance 우선, 없으면 software lavapipe fallback).
//!
//! state vector 는 GPU buffer 에 `Vec<vec2<f32>>` (interleaved re/im, complex64) 로
//! 보관.  CPU ↔ GPU transfer 는 `apply_gates` 호출 끝에서 한 번만 (gate 마다
//! 매번 X).  f64 (complex128) 는 v0.5.0 시점 wgpu 29.x 의 storage f64 가 일부
//! 백엔드에서 미지원 → f32 path 만 우선 지원.

pub mod density;
pub mod statevector;

pub use density::{WgpuDensityBackend, WgpuDensityOp};
pub use statevector::{WgpuGateOp, WgpuStatevectorBackend};
