//! wgpu MPS 백엔드 (v0.6.6).
//!
//! CPU MPS (qsim-mps, v0.6.5) 의 SVD 호출 두 곳 —
//! `apply_two_qubit_adjacent` (mps/src/lib.rs:524) 와
//! `right_canonicalize` (mps/src/lib.rs:897) — 을 wgpu compute shader
//! 로 옮긴 cross-platform GPU MPS.  Qiskit Aer / cuQuantum 에는 없는
//! NVIDIA / AMD / Apple Metal / Intel 동시 지원 GPU MPS.
//!
//! # v0.6.6 cuts
//! - **Cut 1** (이 commit): `Backend::WgpuMps` variant + Python
//!   `method="wgpu_mps"` arm 의 scaffolding.  실제 GPU 호출은 아직
//!   없고 CPU MPS 로 fallback — wiring 만 완료.
//! - Cut 2: `WgpuMpsBackend` singleton + pipeline cache.
//! - Cut 3: WGSL one-sided Jacobi SVD shader.
//! - Cut 4: thin-SVD + truncation wrapper.
//! - Cut 5: two-site contraction shader.
//! - Cut 6: `apply_two_qubit_adjacent` GPU path 통합.
//! - Cut 7: `right_canonicalize` GPU path.
//! - Cut 8: GPU-resident tensor lifetime.
//! - Cut 9: release.
//!
//! # 정밀도
//! wgpu 29.x 의 storage `f64` 미지원으로 **f32 only**.  `Mps<f64>`
//! 호출자는 CPU fallback (Cut 6 정책).

pub mod absorb;
pub mod backend;
pub mod contraction;
pub mod one_qubit;
pub mod resident;
pub mod svd;

pub use backend::WgpuMpsBackend;
pub use resident::{GpuMpsTensors, GpuSvdOutput, GpuSvdProvider, GPU_CHI_THRESHOLD};
pub use svd::{wgpu_thin_svd, WgpuMpsError, WgpuSvdResult};
