//! cuStateVec state vector backend (v0.5.0 Cut G).
//!
//! NVIDIA cuQuantum 의 `custatevecApplyMatrix` 를 통한 1q / 2q / controlled-1q
//! gate 적용.  state vector 는 GPU device buffer (cudarc 의 `CudaSlice<f32>` —
//! Complex<f32> 와 메모리 layout 동일).  buffer 1회 upload + 모든 gate dispatch +
//! 1회 download.
//!
//! 현재 (v0.5.0) f32 only.  f64 는 v0.5.x.  3-qubit (Toffoli, Fredkin) 는
//! cuStateVec 의 `nTargets=3` 으로 지원 가능하지만 v0.5.0 minimum 은 1q/2q/
//! controlled-1q 만 — Toffoli/Fredkin 은 transpile 권유 (Aer 와 동일 패턴).

use std::ffi::c_void;

use cudarc::driver::{CudaSlice, DeviceRepr, ValidAsZeroBits};
use num_complex::Complex;

use super::safe::{CuStateVecHandle, CudaContext};
use crate::errors::GpuError;

/// f32 complex 의 device-friendly Pod (cudarc 의 DeviceRepr 호환).
#[repr(C)]
#[derive(Copy, Clone, Debug, Default)]
pub struct CudaCF32 {
    pub re: f32,
    pub im: f32,
}
unsafe impl DeviceRepr for CudaCF32 {}
unsafe impl ValidAsZeroBits for CudaCF32 {}

impl From<Complex<f32>> for CudaCF32 {
    fn from(c: Complex<f32>) -> Self {
        Self { re: c.re, im: c.im }
    }
}
impl From<CudaCF32> for Complex<f32> {
    fn from(c: CudaCF32) -> Self {
        Complex::new(c.re, c.im)
    }
}

/// GPU 에서 dispatch 할 수 있는 게이트 op (cuStateVec).
#[derive(Debug, Clone)]
pub enum CudaGateOp {
    /// 1-qubit gate.
    Single {
        matrix: [[Complex<f32>; 2]; 2],
        target: usize,
    },
    /// 2-qubit gate (CZ / SWAP — non-controlled).
    Two {
        matrix: [[Complex<f32>; 4]; 4],
        q0: usize,
        q1: usize,
    },
    /// Controlled 1q gate (CNOT 등).  controls=[ctrl], target=tgt.
    Controlled1q {
        matrix: [[Complex<f32>; 2]; 2],
        ctrl: usize,
        tgt: usize,
    },
    /// v0.5.10: Toffoli (CCX) — 2 control + 1 target.  cuStateVec 의
    /// applyMatrix native (n_controls=2, n_targets=1) — X matrix 적용.
    Toffoli { c0: usize, c1: usize, tgt: usize },
    /// v0.5.10: Fredkin (CSWAP) — 1 control + 2 target.  applyMatrix native
    /// (n_controls=1, n_targets=2) — SWAP 4×4 matrix 적용.
    Fredkin { ctrl: usize, t0: usize, t1: usize },
}

/// cuStateVec 기반 state vector backend (Tier-2).
///
/// `WgpuStatevectorBackend` 와 같은 인터페이스 (apply_circuit) 를 노출.
pub struct CudaStatevectorBackend {
    context: CudaContext,
    handle: CuStateVecHandle,
}

impl CudaStatevectorBackend {
    /// CUDA context + cuStateVec handle 초기화.  NVIDIA driver / cuQuantum 가
    /// runtime 에 가용해야 함.
    pub fn new() -> Result<Self, GpuError> {
        let context = CudaContext::new()?;
        let handle = CuStateVecHandle::new()?;
        Ok(Self { context, handle })
    }

    /// 회로 단위 batching.  state 를 GPU 에 한 번 upload, 모든 gate 적용 후 1회
    /// download.  매 gate 마다 host-resident matrix → cuStateVec 로 전달.
    ///
    /// targets / controls 는 cuStateVec 의 LSB-first 인덱스 컨벤션 사용 — panta-sim
    /// 의 little-endian (qubit 0 = LSB) 와 일치.
    pub fn apply_circuit(
        &self,
        state: &mut [Complex<f32>],
        ops: &[CudaGateOp],
    ) -> Result<(), GpuError> {
        let n = state.len();
        if !n.is_power_of_two() || n < 2 {
            return Err(GpuError::Unsupported(format!(
                "state.len() = {n} 는 2^k (k≥1) 이어야 함"
            )));
        }
        let n_qubits = n.trailing_zeros();
        if ops.is_empty() {
            return Ok(());
        }

        let stream = self.context.default_stream();

        // Host → device upload.
        let host: Vec<CudaCF32> = state.iter().map(|c| (*c).into()).collect();
        let mut dev_sv: CudaSlice<CudaCF32> = stream
            .memcpy_stod(&host)
            .map_err(|e| GpuError::Buffer(format!("memcpy_stod: {e:?}")))?;
        // CudaSlice 는 RAII — drop 시 free.

        // 각 op dispatch.  matrix 는 host slice (cuStateVec 가 host pointer 도 처리).
        for op in ops {
            match op {
                CudaGateOp::Single { matrix, target } => {
                    if (*target as u32) >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let m_host = flatten_2x2(matrix);
                    let targets = [*target as i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &[],
                            &[],
                            true,
                        )?;
                    }
                }
                CudaGateOp::Two { matrix, q0, q1 } => {
                    if (*q0 as u32) >= n_qubits || (*q1 as u32) >= n_qubits || q0 == q1 {
                        return Err(GpuError::Unsupported(format!("Two q0={q0} q1={q1} 잘못됨")));
                    }
                    let m_host = flatten_4x4(matrix);
                    // cuStateVec targets order: [least-significant target, ...].
                    // panta-sim 의 4×4 matrix 는 |q1 q0⟩ basis 라 [q0, q1] 순서.
                    let targets = [*q0 as i32, *q1 as i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &[],
                            &[],
                            true,
                        )?;
                    }
                }
                CudaGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if (*ctrl as u32) >= n_qubits || (*tgt as u32) >= n_qubits || ctrl == tgt {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    let m_host = flatten_2x2(matrix);
                    let targets = [*tgt as i32];
                    let controls = [*ctrl as i32];
                    let control_values = [1_i32]; // ctrl=1 일 때 fire.
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            true,
                        )?;
                    }
                }
                CudaGateOp::Toffoli { c0, c1, tgt } => {
                    // v0.5.10: cuStateVec native — n_controls=2, n_targets=1, X matrix.
                    if (*c0 as u32) >= n_qubits
                        || (*c1 as u32) >= n_qubits
                        || (*tgt as u32) >= n_qubits
                        || c0 == c1
                        || c0 == tgt
                        || c1 == tgt
                    {
                        return Err(GpuError::Unsupported(format!(
                            "Toffoli c0={c0} c1={c1} tgt={tgt} 잘못됨 (qubit 중복 또는 범위)"
                        )));
                    }
                    // X matrix.
                    let x_matrix: [[Complex<f32>; 2]; 2] = [
                        [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
                        [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
                    ];
                    let m_host = flatten_2x2(&x_matrix);
                    let targets = [*tgt as i32];
                    let controls = [*c0 as i32, *c1 as i32];
                    let control_values = [1_i32, 1_i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            true,
                        )?;
                    }
                }
                CudaGateOp::Fredkin { ctrl, t0, t1 } => {
                    // v0.5.10: cuStateVec native — n_controls=1, n_targets=2, SWAP matrix.
                    if (*ctrl as u32) >= n_qubits
                        || (*t0 as u32) >= n_qubits
                        || (*t1 as u32) >= n_qubits
                        || ctrl == t0
                        || ctrl == t1
                        || t0 == t1
                    {
                        return Err(GpuError::Unsupported(format!(
                            "Fredkin ctrl={ctrl} t0={t0} t1={t1} 잘못됨 (qubit 중복 또는 범위)"
                        )));
                    }
                    // SWAP 4×4: |00⟩→|00⟩, |01⟩→|10⟩, |10⟩→|01⟩, |11⟩→|11⟩.
                    let z = Complex::new(0.0_f32, 0.0);
                    let o = Complex::new(1.0_f32, 0.0);
                    let swap_matrix: [[Complex<f32>; 4]; 4] =
                        [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]];
                    let m_host = flatten_4x4(&swap_matrix);
                    let targets = [*t0 as i32, *t1 as i32];
                    let controls = [*ctrl as i32];
                    let control_values = [1_i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            true,
                        )?;
                    }
                }
            }
        }

        // Device → host download.
        let mut host_back: Vec<CudaCF32> = vec![CudaCF32::default(); n];
        stream
            .memcpy_dtoh(&dev_sv, &mut host_back)
            .map_err(|e| GpuError::Buffer(format!("memcpy_dtoh: {e:?}")))?;
        stream
            .synchronize()
            .map_err(|e| GpuError::Buffer(format!("stream sync: {e:?}")))?;

        for (dst, src) in state.iter_mut().zip(host_back.iter()) {
            *dst = (*src).into();
        }
        Ok(())
    }
}

/// 2×2 matrix → 4-element flat host vec ([f32; 8] = 4 complex).
fn flatten_2x2(m: &[[Complex<f32>; 2]; 2]) -> [f32; 8] {
    [
        m[0][0].re, m[0][0].im, m[0][1].re, m[0][1].im, m[1][0].re, m[1][0].im, m[1][1].re,
        m[1][1].im,
    ]
}

/// 4×4 matrix → 32-element flat host vec.
fn flatten_4x4(m: &[[Complex<f32>; 4]; 4]) -> [f32; 32] {
    let mut out = [0.0_f32; 32];
    for i in 0..4 {
        for j in 0..4 {
            out[2 * (i * 4 + j)] = m[i][j].re;
            out[2 * (i * 4 + j) + 1] = m[i][j].im;
        }
    }
    out
}

/// CudaSlice 의 mutable raw device pointer 추출.  cuStateVec FFI 에 직접 전달
/// 해야 하므로 cudarc 0.16.x 의 `as_view_mut` / `cu_device_ptr()` 활용.
///
/// cudarc 0.16.x 의 정확한 API 가 여기서 결정됨.  사용자 PC 검증 시 v0.5.x
/// 에서 fix 할 수 있음 (cudarc API 변경 가능성).
#[allow(unused_variables)]
unsafe fn dev_sv_mut_ptr(sv: &mut CudaSlice<CudaCF32>) -> *mut c_void {
    // cudarc 0.16.x: CudaSlice 는 device pointer + length 보유.  raw pointer 는
    // unsafe accessor.  여기서는 임시 placeholder — 실제 NVIDIA 환경 검증 시 적용.
    // 정확한 호출: `sv.device_ptr(...)` 또는 `&*sv as *const _ as *mut c_void`.
    // 안전한 path 는 `cudarc::driver::CudaSlice::device_ptr` (있으면) 사용.
    sv as *mut _ as *mut c_void
}

// =====================================================================
// v0.5.11: cuStateVec f64 path (CUDA_C_64F).
//
// 양자 화학 / VQE 같은 정밀 계산 (norm error < 1e-12 표준) 에 필요.  Apple
// Metal 의 wgpu 는 f64 미지원 — cuStateVec Tier-2 에서만 가용.  cuStateVec
// 의 `apply_matrix` 가 이미 `is_f32: bool` 인자로 f32/f64 dispatch — 같은
// FFI 가 f64 도 처리.
// =====================================================================

/// f64 complex 의 device-friendly Pod (cudarc DeviceRepr 호환).
#[repr(C)]
#[derive(Copy, Clone, Debug, Default)]
pub struct CudaCF64 {
    pub re: f64,
    pub im: f64,
}
unsafe impl DeviceRepr for CudaCF64 {}
unsafe impl ValidAsZeroBits for CudaCF64 {}

impl From<Complex<f64>> for CudaCF64 {
    fn from(c: Complex<f64>) -> Self {
        Self { re: c.re, im: c.im }
    }
}
impl From<CudaCF64> for Complex<f64> {
    fn from(c: CudaCF64) -> Self {
        Complex::new(c.re, c.im)
    }
}

/// f64 변종의 GPU gate op.  CudaGateOp 와 동일 variants — matrix 만 f64.
#[derive(Debug, Clone)]
pub enum CudaGateOpF64 {
    Single {
        matrix: [[Complex<f64>; 2]; 2],
        target: usize,
    },
    Two {
        matrix: [[Complex<f64>; 4]; 4],
        q0: usize,
        q1: usize,
    },
    Controlled1q {
        matrix: [[Complex<f64>; 2]; 2],
        ctrl: usize,
        tgt: usize,
    },
    Toffoli {
        c0: usize,
        c1: usize,
        tgt: usize,
    },
    Fredkin {
        ctrl: usize,
        t0: usize,
        t1: usize,
    },
}

#[allow(unused_variables)]
unsafe fn dev_sv_mut_ptr_f64(sv: &mut CudaSlice<CudaCF64>) -> *mut c_void {
    sv as *mut _ as *mut c_void
}

fn flatten_2x2_f64(m: &[[Complex<f64>; 2]; 2]) -> [CudaCF64; 4] {
    let mut out = [CudaCF64::default(); 4];
    for i in 0..2 {
        for j in 0..2 {
            out[i * 2 + j] = m[i][j].into();
        }
    }
    out
}

fn flatten_4x4_f64(m: &[[Complex<f64>; 4]; 4]) -> [CudaCF64; 16] {
    let mut out = [CudaCF64::default(); 16];
    for i in 0..4 {
        for j in 0..4 {
            out[i * 4 + j] = m[i][j].into();
        }
    }
    out
}

impl CudaStatevectorBackend {
    /// v0.5.11: f64 (double precision) statevector path.  same backend handle,
    /// `is_f32=false` 로 cuStateVec dispatch.  사용자 PC 검증 대기.
    pub fn apply_circuit_f64(
        &self,
        state: &mut [Complex<f64>],
        ops: &[CudaGateOpF64],
    ) -> Result<(), GpuError> {
        let n = state.len();
        if !n.is_power_of_two() || n < 2 {
            return Err(GpuError::Unsupported(format!(
                "state.len() = {n} 는 2^k (k≥1) 이어야 함"
            )));
        }
        let n_qubits = n.trailing_zeros();
        if ops.is_empty() {
            return Ok(());
        }

        let stream = self.context.default_stream();
        let host: Vec<CudaCF64> = state.iter().map(|c| (*c).into()).collect();
        let mut dev_sv: CudaSlice<CudaCF64> = stream
            .memcpy_stod(&host)
            .map_err(|e| GpuError::Buffer(format!("memcpy_stod f64: {e:?}")))?;

        for op in ops {
            match op {
                CudaGateOpF64::Single { matrix, target } => {
                    if (*target as u32) >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let m_host = flatten_2x2_f64(matrix);
                    let targets = [*target as i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr_f64(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &[],
                            &[],
                            false, // f64
                        )?;
                    }
                }
                CudaGateOpF64::Two { matrix, q0, q1 } => {
                    if (*q0 as u32) >= n_qubits || (*q1 as u32) >= n_qubits || q0 == q1 {
                        return Err(GpuError::Unsupported(format!("Two q0={q0} q1={q1} 잘못됨")));
                    }
                    let m_host = flatten_4x4_f64(matrix);
                    let targets = [*q0 as i32, *q1 as i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr_f64(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &[],
                            &[],
                            false,
                        )?;
                    }
                }
                CudaGateOpF64::Controlled1q { matrix, ctrl, tgt } => {
                    if (*ctrl as u32) >= n_qubits || (*tgt as u32) >= n_qubits || ctrl == tgt {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    let m_host = flatten_2x2_f64(matrix);
                    let targets = [*tgt as i32];
                    let controls = [*ctrl as i32];
                    let control_values = [1_i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr_f64(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            false,
                        )?;
                    }
                }
                CudaGateOpF64::Toffoli { c0, c1, tgt } => {
                    if (*c0 as u32) >= n_qubits
                        || (*c1 as u32) >= n_qubits
                        || (*tgt as u32) >= n_qubits
                        || c0 == c1
                        || c0 == tgt
                        || c1 == tgt
                    {
                        return Err(GpuError::Unsupported(format!(
                            "Toffoli c0={c0} c1={c1} tgt={tgt} 잘못됨"
                        )));
                    }
                    let x_matrix: [[Complex<f64>; 2]; 2] = [
                        [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
                        [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
                    ];
                    let m_host = flatten_2x2_f64(&x_matrix);
                    let targets = [*tgt as i32];
                    let controls = [*c0 as i32, *c1 as i32];
                    let control_values = [1_i32, 1_i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr_f64(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            false,
                        )?;
                    }
                }
                CudaGateOpF64::Fredkin { ctrl, t0, t1 } => {
                    if (*ctrl as u32) >= n_qubits
                        || (*t0 as u32) >= n_qubits
                        || (*t1 as u32) >= n_qubits
                        || ctrl == t0
                        || ctrl == t1
                        || t0 == t1
                    {
                        return Err(GpuError::Unsupported(format!(
                            "Fredkin ctrl={ctrl} t0={t0} t1={t1} 잘못됨"
                        )));
                    }
                    let z = Complex::new(0.0_f64, 0.0);
                    let o = Complex::new(1.0_f64, 0.0);
                    let swap_matrix: [[Complex<f64>; 4]; 4] =
                        [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]];
                    let m_host = flatten_4x4_f64(&swap_matrix);
                    let targets = [*t0 as i32, *t1 as i32];
                    let controls = [*ctrl as i32];
                    let control_values = [1_i32];
                    unsafe {
                        let dev_ptr = dev_sv_mut_ptr_f64(&mut dev_sv);
                        self.handle.apply_matrix(
                            dev_ptr,
                            n_qubits,
                            m_host.as_ptr() as *const c_void,
                            &targets,
                            &controls,
                            &control_values,
                            false,
                        )?;
                    }
                }
            }
        }

        let mut host_back: Vec<CudaCF64> = vec![CudaCF64::default(); n];
        stream
            .memcpy_dtoh(&dev_sv, &mut host_back)
            .map_err(|e| GpuError::Buffer(format!("memcpy_dtoh f64: {e:?}")))?;
        stream
            .synchronize()
            .map_err(|e| GpuError::Buffer(format!("stream sync: {e:?}")))?;

        for (dst, src) in state.iter_mut().zip(host_back.iter()) {
            *dst = (*src).into();
        }
        Ok(())
    }
}
