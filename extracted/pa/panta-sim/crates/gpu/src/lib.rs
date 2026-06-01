//! GPU 백엔드 (v0.5.0).
//!
//! Tier-1 (wgpu) 와 Tier-2 (cudarc + cuStateVec) GPU 백엔드.  state vector +
//! density matrix 양쪽 path.  panta-sim 의 statevector 백엔드와 동일 의미
//! (qubit-wise gate update) 를 GPU compute shader 로 구현.
//!
//! 환경:
//! - **wgpu**: cross-platform (NVIDIA / AMD / Intel / Apple Metal / 소프트웨어
//!   lavapipe).  WGSL compute shader.  feature gate 없이 default 빌드.
//! - **cuStateVec** (Tier-2, v0.5.0 후반): NVIDIA 한정 추가 성능, libcustatevec.so
//!   동적 link.  feature flag `gpu-cuda`.

pub mod errors;
pub mod wgpu_backend;
pub mod wgpu_mps;

#[cfg(feature = "gpu-cuda")]
pub mod cuda;

pub use errors::GpuError;
pub use wgpu_backend::{WgpuDensityBackend, WgpuDensityOp, WgpuStatevectorBackend};
pub use wgpu_mps::{
    wgpu_thin_svd, GpuMpsTensors, GpuSvdOutput, GpuSvdProvider, WgpuMpsBackend, WgpuMpsError,
    WgpuSvdResult, GPU_CHI_THRESHOLD,
};

#[cfg(feature = "gpu-cuda")]
pub use cuda::{CudaGateOp, CudaGateOpF64, CudaStatevectorBackend};

// ============================================================================
// Process-wide cached backends (v0.5.1)
// ============================================================================
//
// wgpu adapter / device / pipeline 초기화 비용 (~수백 ms) 을 매 `qc.run()` 호출
// 마다 지불하지 않도록 process 내 singleton.  thread-safe (`OnceLock` + `Arc`).
//
// 첫 호출에서 init, 이후 호출은 cached `Arc<Backend>` 재사용.  init 실패 시
// 에러를 cache 하지 않음 — 다음 호출에서 재시도 가능.

use std::sync::{Arc, Mutex, OnceLock};

static WGPU_STATEVECTOR_BACKEND: OnceLock<Mutex<Option<Arc<WgpuStatevectorBackend>>>> =
    OnceLock::new();
static WGPU_DENSITY_BACKEND: OnceLock<Mutex<Option<Arc<WgpuDensityBackend>>>> = OnceLock::new();
// v0.6.6 Cut 2: wgpu MPS 백엔드 process-wide singleton.  statevector /
// density 와 별도 device (사용자가 wgpu_mps 만 쓸 때 statevector pipeline
// 강제 init 회피).  Cut 3/5 부터 svd / contract pipeline 이 채워짐.
static WGPU_MPS_BACKEND: OnceLock<Mutex<Option<Arc<WgpuMpsBackend>>>> = OnceLock::new();

/// Process-wide cached `WgpuStatevectorBackend`.  첫 호출에서 init (수백 ms),
/// 이후 호출은 즉시 (~µs).
///
/// adapter / device 가 한번 만들어지면 process 종료 까지 유지 — 일반적인
/// wgpu 사용 패턴 (Vulkan / Metal device 는 cheap to keep alive).
pub fn cached_wgpu_statevector_backend() -> Result<Arc<WgpuStatevectorBackend>, GpuError> {
    let cell = WGPU_STATEVECTOR_BACKEND.get_or_init(|| Mutex::new(None));
    let mut guard = cell
        .lock()
        .map_err(|e| GpuError::Other(format!("statevector backend mutex poisoned: {e}")))?;
    if let Some(backend) = guard.as_ref() {
        return Ok(Arc::clone(backend));
    }
    let backend = Arc::new(WgpuStatevectorBackend::new()?);
    *guard = Some(Arc::clone(&backend));
    Ok(backend)
}

/// Process-wide cached `WgpuDensityBackend`.
pub fn cached_wgpu_density_backend() -> Result<Arc<WgpuDensityBackend>, GpuError> {
    let cell = WGPU_DENSITY_BACKEND.get_or_init(|| Mutex::new(None));
    let mut guard = cell
        .lock()
        .map_err(|e| GpuError::Other(format!("density backend mutex poisoned: {e}")))?;
    if let Some(backend) = guard.as_ref() {
        return Ok(Arc::clone(backend));
    }
    let backend = Arc::new(WgpuDensityBackend::new()?);
    *guard = Some(Arc::clone(&backend));
    Ok(backend)
}

/// Process-wide cached `WgpuMpsBackend` (v0.6.6 Cut 2).  첫 호출에서
/// adapter / device 초기화 (~수백 ms), 이후 호출은 즉시.  init 실패 시
/// 에러를 cache 하지 않음 — 다음 호출에서 재시도 가능.
pub fn cached_wgpu_mps_backend() -> Result<Arc<WgpuMpsBackend>, GpuError> {
    let cell = WGPU_MPS_BACKEND.get_or_init(|| Mutex::new(None));
    let mut guard = cell
        .lock()
        .map_err(|e| GpuError::Other(format!("MPS backend mutex poisoned: {e}")))?;
    if let Some(backend) = guard.as_ref() {
        return Ok(Arc::clone(backend));
    }
    let backend = Arc::new(WgpuMpsBackend::new()?);
    *guard = Some(Arc::clone(&backend));
    Ok(backend)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// v0.6.6 Cut 2: process-wide singleton 이 두 번째 호출에서 같은
    /// `Arc<WgpuMpsBackend>` 를 반환해야 한다 (init cost 회피의 핵심).
    /// adapter 가 없는 sandbox 환경에선 NoAdapter 가 cache 되지 않음을
    /// 확인.
    #[test]
    fn cached_wgpu_mps_backend_is_singleton() {
        match cached_wgpu_mps_backend() {
            Ok(b1) => {
                let b2 = cached_wgpu_mps_backend().expect("second call should succeed");
                assert!(
                    Arc::ptr_eq(&b1, &b2),
                    "cached_wgpu_mps_backend() must return same Arc on subsequent calls"
                );
            }
            Err(GpuError::NoAdapter) => {
                // sandbox 에 adapter 없음 — 두 번째 호출도 같은 에러여야 함
                // (NoAdapter 는 cache 되지 않으므로 두 번째 호출도 init 재시도).
                assert!(matches!(
                    cached_wgpu_mps_backend(),
                    Err(GpuError::NoAdapter)
                ));
            }
            Err(e) => panic!("unexpected init error: {e}"),
        }
    }
}
