//! cuStateVec C API 의 manual `extern "C"` declaration (v0.5.0 Cut F).
//!
//! NVIDIA cuQuantum SDK 23.x ~ 25.x 의 `custatevec.h` 기준.  사용자 PC NVIDIA +
//! cuQuantum 환경에서만 link 가능.  sandbox 는 feature off 로 빌드 회피.
//!
//! **참고**: 이 declaration 의 정확성은 `bindgen` 으로 검증되지 않은 manual
//! 작성.  사용자 PC 에서 link / 동작 검증 시 mismatch 가 있으면 v0.5.x 에서 fix.

#![allow(
    non_camel_case_types,
    non_snake_case,
    dead_code,
    clippy::missing_safety_doc
)]

use std::os::raw::{c_int, c_void};

/// cuStateVec handle (opaque).
pub type custatevecHandle_t = *mut c_void;

/// cuStateVec status code.  CUSTATEVEC_STATUS_SUCCESS = 0.
pub type custatevecStatus_t = c_int;
pub const CUSTATEVEC_STATUS_SUCCESS: c_int = 0;

/// CUDA data type (cudaDataType_t enum).  Complex<f32> = 4 (CUDA_C_32F),
/// Complex<f64> = 5 (CUDA_C_64F).  cuStateVec 의 svDataType / matrixDataType.
pub type cudaDataType_t = c_int;
pub const CUDA_C_32F: c_int = 4;
pub const CUDA_C_64F: c_int = 5;

/// Matrix layout enum.  ROW = 0, COL = 1.  cuStateVec 가 row-major / column-major
/// 둘 다 처리 — 우리는 row-major (panta-sim 컨벤션).
pub type custatevecMatrixLayout_t = c_int;
pub const CUSTATEVEC_MATRIX_LAYOUT_COL: c_int = 0;
pub const CUSTATEVEC_MATRIX_LAYOUT_ROW: c_int = 1;

/// Compute type enum.  CUDA_C_32F (default) / CUDA_C_64F.  reuse cudaDataType_t.
pub type custatevecComputeType_t = cudaDataType_t;

/// Collapse op (post-measurement state).  NORMALIZE_AND_ZERO = 0 (apply collapse +
/// renormalize).  NONE = 1 (statevector 그대로).
pub type custatevecCollapseOp_t = c_int;
pub const CUSTATEVEC_COLLAPSE_NORMALIZE_AND_ZERO: c_int = 0;
pub const CUSTATEVEC_COLLAPSE_NONE: c_int = 1;

unsafe extern "C" {
    /// Handle 생성.
    pub fn custatevecCreate(handle: *mut custatevecHandle_t) -> custatevecStatus_t;

    /// Handle 해제.
    pub fn custatevecDestroy(handle: custatevecHandle_t) -> custatevecStatus_t;

    /// Workspace size 쿼리 (`custatevecApplyMatrix` 가 필요한 임시 buffer).
    pub fn custatevecApplyMatrixGetWorkspaceSize(
        handle: custatevecHandle_t,
        svDataType: cudaDataType_t,
        nIndexBits: u32,
        matrix: *const c_void,
        matrixDataType: cudaDataType_t,
        layout: custatevecMatrixLayout_t,
        adjoint: i32,
        nTargets: u32,
        nControls: u32,
        computeType: custatevecComputeType_t,
        extraWorkspaceSizeInBytes: *mut usize,
    ) -> custatevecStatus_t;

    /// 임의 N-qubit gate 적용 (controls 포함).  state vector 는 GPU device pointer.
    /// `targets[..nTargets]` 가 gate 적용 큐비트, `controls[..nControls]` 가 control
    /// 큐비트, `controlBitValues[..nControls]` 가 control 의 |0⟩/|1⟩ 매칭값.
    pub fn custatevecApplyMatrix(
        handle: custatevecHandle_t,
        sv: *mut c_void,
        svDataType: cudaDataType_t,
        nIndexBits: u32,
        matrix: *const c_void,
        matrixDataType: cudaDataType_t,
        layout: custatevecMatrixLayout_t,
        adjoint: i32,
        targets: *const i32,
        nTargets: u32,
        controls: *const i32,
        controlBitValues: *const i32,
        nControls: u32,
        computeType: custatevecComputeType_t,
        extraWorkspace: *mut c_void,
        extraWorkspaceSizeInBytes: usize,
    ) -> custatevecStatus_t;

    /// Z basis 측정의 \|amplitude\|² sum 계산 (parity=0 / parity=1).
    pub fn custatevecAbs2SumOnZBasis(
        handle: custatevecHandle_t,
        sv: *const c_void,
        svDataType: cudaDataType_t,
        nIndexBits: u32,
        abs2sum0: *mut f64,
        abs2sum1: *mut f64,
        basisBits: *const i32,
        nBasisBits: u32,
    ) -> custatevecStatus_t;

    /// Z basis collapse (post-measurement state 계산 + 재정규화).
    pub fn custatevecCollapseOnZBasis(
        handle: custatevecHandle_t,
        sv: *mut c_void,
        svDataType: cudaDataType_t,
        nIndexBits: u32,
        parity: i32,
        basisBits: *const i32,
        nBasisBits: u32,
        norm: f64,
    ) -> custatevecStatus_t;

    /// 측정 + collapse 통합.  randnum ∈ [0, 1) 를 받아 Z basis outcome (0/1) 반환.
    pub fn custatevecMeasureOnZBasis(
        handle: custatevecHandle_t,
        sv: *mut c_void,
        svDataType: cudaDataType_t,
        nIndexBits: u32,
        parity: *mut i32,
        basisBits: *const i32,
        nBasisBits: u32,
        randnum: f64,
        collapse: custatevecCollapseOp_t,
    ) -> custatevecStatus_t;
}
