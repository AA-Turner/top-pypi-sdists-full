//! cuStateVec safe Rust wrapper (v0.5.0 Cut F).
//!
//! Manual FFI 위에 RAII handle / Result-returning safe wrapper 를 얹는다.
//! cudarc 0.16.x 의 driver / runtime API 와 결합 — device buffer 관리는 cudarc,
//! gate 적용 / 측정은 cuStateVec.

#![allow(clippy::missing_safety_doc)]

use std::ffi::c_void;
use std::ptr;

use super::ffi::{self, custatevecHandle_t, custatevecStatus_t, CUSTATEVEC_STATUS_SUCCESS};
use crate::errors::GpuError;

/// cuStateVec status → `Result` 변환.
fn check_status(status: custatevecStatus_t, ctx: &str) -> Result<(), GpuError> {
    if status == CUSTATEVEC_STATUS_SUCCESS {
        Ok(())
    } else {
        Err(GpuError::Other(format!(
            "{ctx}: cuStateVec status code {status}"
        )))
    }
}

/// CUDA device context (cudarc 의 CudaContext alias 또는 wrapper).
///
/// cudarc 0.16.x 의 driver API 가 thread-local context 를 관리.  여기서는
/// CudaContext 를 wrap 해 backend 의 lifetime 동안 보관.
pub struct CudaContext {
    pub(crate) inner: std::sync::Arc<cudarc::driver::CudaContext>,
}

impl CudaContext {
    /// Default device (ordinal 0) 의 CUDA context 를 생성.
    pub fn new() -> Result<Self, GpuError> {
        let ctx = cudarc::driver::CudaContext::new(0)
            .map_err(|e| GpuError::DeviceCreation(format!("CUDA context: {e:?}")))?;
        Ok(Self { inner: ctx })
    }

    /// 첫 stream (default).
    pub fn default_stream(&self) -> std::sync::Arc<cudarc::driver::CudaStream> {
        self.inner.default_stream()
    }
}

/// cuStateVec handle (RAII).  Drop 시 자동 destroy.
pub struct CuStateVecHandle {
    handle: custatevecHandle_t,
}

impl CuStateVecHandle {
    /// 새 handle 생성.  CUDA context 가 활성화되어 있어야 함 (CudaContext::new
    /// 결과 보유).
    pub fn new() -> Result<Self, GpuError> {
        let mut handle: custatevecHandle_t = ptr::null_mut();
        let status = unsafe { ffi::custatevecCreate(&mut handle) };
        check_status(status, "custatevecCreate")?;
        Ok(Self { handle })
    }

    pub fn raw(&self) -> custatevecHandle_t {
        self.handle
    }

    /// 임의 N-qubit gate 적용.
    ///
    /// 매개변수:
    /// - `sv`: GPU device pointer (statevector buffer).
    /// - `n_qubits`: log2(state.len()).
    /// - `matrix`: GPU 또는 host 가능한 row-major matrix.  `2^nTargets × 2^nTargets` size.
    /// - `targets`: gate 적용 큐비트.
    /// - `controls`: control 큐비트 (예: CNOT 의 control).  비어 있으면 단순 N-target.
    /// - `is_f32`: state / matrix 가 f32 (`CUDA_C_32F`) 면 true, f64 면 false.
    ///
    /// safety: `sv` 는 valid GPU pointer, `matrix` 는 host (CPU) pointer 또는
    /// page-locked memory 둘 다 가능.  cuStateVec 가 자동 dispatch.
    #[allow(clippy::too_many_arguments)]
    pub unsafe fn apply_matrix(
        &self,
        sv: *mut c_void,
        n_qubits: u32,
        matrix: *const c_void,
        targets: &[i32],
        controls: &[i32],
        control_values: &[i32],
        is_f32: bool,
    ) -> Result<(), GpuError> {
        let dtype = if is_f32 {
            ffi::CUDA_C_32F
        } else {
            ffi::CUDA_C_64F
        };
        // computeType 은 cudaDataType_t 와 다른 enum (ffi.rs 참조).
        let compute = if is_f32 {
            ffi::CUSTATEVEC_COMPUTE_32F
        } else {
            ffi::CUSTATEVEC_COMPUTE_64F
        };
        // Workspace size 쿼리.
        let mut ws_size: usize = 0;
        let status = unsafe {
            ffi::custatevecApplyMatrixGetWorkspaceSize(
                self.handle,
                dtype,
                n_qubits,
                matrix,
                dtype,
                ffi::CUSTATEVEC_MATRIX_LAYOUT_ROW,
                0,
                targets.len() as u32,
                controls.len() as u32,
                compute,
                &mut ws_size,
            )
        };
        check_status(status, "custatevecApplyMatrixGetWorkspaceSize")?;

        // Workspace allocation (필요 시).  cuQuantum 가 0 byte workspace 도 허용 —
        // null pointer 통과.  > 0 byte 면 GPU 에 할당해야 함 — v0.5.0 minimum
        // path 는 0-byte 만 가정.  > 0 면 v0.5.x 에서 cudarc allocator 사용.
        let ws_ptr: *mut c_void = ptr::null_mut();
        if ws_size > 0 {
            return Err(GpuError::Unsupported(format!(
                "custatevecApplyMatrix: workspace size {ws_size} > 0 미지원 (v0.5.x)"
            )));
        }

        let status = unsafe {
            ffi::custatevecApplyMatrix(
                self.handle,
                sv,
                dtype,
                n_qubits,
                matrix,
                dtype,
                ffi::CUSTATEVEC_MATRIX_LAYOUT_ROW,
                0, // adjoint = false
                targets.as_ptr(),
                targets.len() as u32,
                controls.as_ptr(),
                control_values.as_ptr(),
                controls.len() as u32,
                compute,
                ws_ptr,
                ws_size,
            )
        };
        check_status(status, "custatevecApplyMatrix")
    }

    /// Z basis 측정 + collapse 통합.  outcome (0 or 1) 반환.
    ///
    /// safety: `sv` 는 valid GPU pointer.
    pub unsafe fn measure_z_basis(
        &self,
        sv: *mut c_void,
        n_qubits: u32,
        basis_bits: &[i32],
        randnum: f64,
        is_f32: bool,
    ) -> Result<i32, GpuError> {
        let dtype = if is_f32 {
            ffi::CUDA_C_32F
        } else {
            ffi::CUDA_C_64F
        };
        let mut parity: i32 = 0;
        let status = unsafe {
            ffi::custatevecMeasureOnZBasis(
                self.handle,
                sv,
                dtype,
                n_qubits,
                &mut parity,
                basis_bits.as_ptr(),
                basis_bits.len() as u32,
                randnum,
                ffi::CUSTATEVEC_COLLAPSE_NORMALIZE_AND_ZERO,
            )
        };
        check_status(status, "custatevecMeasureOnZBasis")?;
        Ok(parity)
    }

    /// Z basis 의 abs² sum (parity=0 / parity=1 양쪽).
    pub unsafe fn abs2_sum_z_basis(
        &self,
        sv: *const c_void,
        n_qubits: u32,
        basis_bits: &[i32],
        is_f32: bool,
    ) -> Result<(f64, f64), GpuError> {
        let dtype = if is_f32 {
            ffi::CUDA_C_32F
        } else {
            ffi::CUDA_C_64F
        };
        let mut s0 = 0.0_f64;
        let mut s1 = 0.0_f64;
        let status = unsafe {
            ffi::custatevecAbs2SumOnZBasis(
                self.handle,
                sv,
                dtype,
                n_qubits,
                &mut s0,
                &mut s1,
                basis_bits.as_ptr(),
                basis_bits.len() as u32,
            )
        };
        check_status(status, "custatevecAbs2SumOnZBasis")?;
        Ok((s0, s1))
    }
}

impl Drop for CuStateVecHandle {
    fn drop(&mut self) {
        if !self.handle.is_null() {
            // Safety: handle 은 custatevecCreate 결과.  destroy 결과는 무시
            // (Drop 에서 panic 회피).
            unsafe {
                let _ = ffi::custatevecDestroy(self.handle);
            }
        }
    }
}

// Send + Sync 는 cuStateVec handle 의 thread-safety 가 명시적으로 보장 안 됨.
// 보수적으로 not impl Send + Sync (single-thread use).
