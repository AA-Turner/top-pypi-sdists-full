//! CUDA + cuStateVec FFI (v0.5.0 Cut F-G, Tier-2 GPU).
//!
//! NVIDIA cuQuantum SDK 의 cuStateVec library (libcustatevec.so) 를 manual
//! `extern "C"` declaration + safe Rust wrapper 로 사용한다.  cudarc 0.16.x
//! 의 driver / runtime API 와 결합.
//!
//! **빌드 / 실행 환경**:
//! - Cargo feature `gpu-cuda` 로 conditional compile.  default off.
//! - `LD_LIBRARY_PATH` 또는 build.rs 가 cuQuantum SDK 의 lib 경로 검출.
//! - Runtime 시 NVIDIA driver (`libcuda.so`) + cuStateVec
//!   (`libcustatevec.so`) 가 로드 가능해야 함.
//!
//! **현재 검증 상태** (v0.5.0):
//! - sandbox 에선 NVIDIA driver / cuQuantum SDK 부재 → feature off 로
//!   컴파일 통과만 검증.
//! - NVIDIA + cuQuantum 환경에서 사용자 검증 후 v0.5.x patch 에서 fix.
//!
//! 핵심 API (cuQuantum 23.x ~ 25.x 기준):
//! - `custatevecCreate` / `custatevecDestroy` — handle RAII.
//! - `custatevecApplyMatrix` — 1q / 2q / N-q gate 적용 (controlled 포함).
//! - `custatevecAbs2SumOnZBasis` / `custatevecCollapseOnZBasis` /
//!   `custatevecMeasureOnZBasis` — 측정 + 상태 붕괴.

#![cfg(feature = "gpu-cuda")]

pub mod ffi;
pub mod safe;
pub mod statevector;

pub use safe::{CuStateVecHandle, CudaContext};
pub use statevector::{CudaGateOp, CudaGateOpF64, CudaStatevectorBackend};
