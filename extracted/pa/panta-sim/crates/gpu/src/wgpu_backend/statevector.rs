//! wgpu state vector backend (v0.5.0 Cut D).
//!
//! state vector 를 GPU buffer 에 올리고 1-qubit / 2-qubit / controlled-1q
//! gate 를 WGSL compute shader 로 적용한다.  현재 f32 만 지원 (wgpu 29.x 의
//! storage f64 는 일부 백엔드에서 미지원).
//!
//! Cut D.2: 단위 gate API (per-gate buffer round-trip).  성능보다 정확성 우선.
//! Cut D.3 (apply_circuit): 한 buffer 에 모든 gate dispatch → 1 회 download.

use bytemuck::{Pod, Zeroable};
use num_complex::Complex;
use pollster::FutureExt;
use wgpu::util::DeviceExt;

use crate::errors::GpuError;

/// `Complex<f32>` 의 Pod 표현 ((re, im)).
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable, Default)]
struct CF32 {
    re: f32,
    im: f32,
}

impl From<Complex<f32>> for CF32 {
    fn from(c: Complex<f32>) -> Self {
        Self { re: c.re, im: c.im }
    }
}

impl From<CF32> for Complex<f32> {
    fn from(c: CF32) -> Self {
        Complex::new(c.re, c.im)
    }
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct SingleQubitUniforms {
    qubit_stride: u32,
    n_amplitudes: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    _pad1: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct TwoQubitUniforms {
    bit0: u32,
    bit1: u32,
    n_amplitudes: u32,
    mask_lo: u32,
    mask_mid: u32,
    mask_hi: u32,
    n_groups: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    m: [[f32; 2]; 16], // 4×4 row-major flat
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct Controlled1qUniforms {
    ctrl_bit: u32,
    tgt_stride: u32,
    n_amplitudes: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

// =====================================================================
// v0.5.5: K=2 buffer-split Uniform structs.
// =====================================================================

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct SingleQubitK2Uniforms {
    qubit_stride: u32,
    n_amplitudes: u32,
    half_dim: u32,
    split_target: u32,
    dispatches_x: u32,
    _pad1: u32,
    _pad2: u32,
    _pad3: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct TwoQubitK2Uniforms {
    bit0: u32,
    bit1: u32,
    n_amplitudes: u32,
    mask_lo: u32,
    mask_mid: u32,
    mask_hi: u32,
    n_groups: u32,
    half_dim: u32,
    split_q1: u32,
    dispatches_x: u32,
    _pad1: u32,
    _pad2: u32,
    _pad3: u32,
    _pad4: u32,
    _pad5: u32,
    _pad6: u32,
    m: [[f32; 2]; 16],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct Controlled1qK2Uniforms {
    ctrl_bit: u32,
    tgt_stride: u32,
    n_amplitudes: u32,
    half_dim: u32,
    split_ctrl: u32,
    split_tgt: u32,
    dispatches_x: u32,
    _pad0: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

// =====================================================================
// v0.5.6: K=4 buffer-split Uniform structs.  generic switch shader 라
// split_target 같은 분기 flag 불필요 — buffer index 가 amplitude 의 high
// 2 bits 로 자동 결정.
// =====================================================================

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct SingleQubitK8Uniforms {
    qubit_stride: u32,
    n_amplitudes: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

// v0.5.17: K=16 Uniform structs.  K=8 과 동일 layout — offset_bits 만 다름.
type SingleQubitK16Uniforms = SingleQubitK8Uniforms;
type TwoQubitK16Uniforms = TwoQubitK8Uniforms;
type Controlled1qK16Uniforms = Controlled1qK8Uniforms;

// v0.5.18: K=32 Uniform structs.  layout 동일.
type SingleQubitK32Uniforms = SingleQubitK8Uniforms;
type TwoQubitK32Uniforms = TwoQubitK8Uniforms;
type Controlled1qK32Uniforms = Controlled1qK8Uniforms;

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct TwoQubitK8Uniforms {
    bit0: u32,
    bit1: u32,
    n_amplitudes: u32,
    mask_lo: u32,
    mask_mid: u32,
    mask_hi: u32,
    n_groups: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
    _pad3: u32,
    _pad4: u32,
    _pad5: u32,
    m: [[f32; 2]; 16],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct Controlled1qK8Uniforms {
    ctrl_bit: u32,
    tgt_stride: u32,
    n_amplitudes: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct SingleQubitK4Uniforms {
    qubit_stride: u32,
    n_amplitudes: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct TwoQubitK4Uniforms {
    bit0: u32,
    bit1: u32,
    n_amplitudes: u32,
    mask_lo: u32,
    mask_mid: u32,
    mask_hi: u32,
    n_groups: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
    _pad3: u32,
    _pad4: u32,
    _pad5: u32,
    m: [[f32; 2]; 16],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct Controlled1qK4Uniforms {
    ctrl_bit: u32,
    tgt_stride: u32,
    n_amplitudes: u32,
    offset_bits: u32,
    offset_mask: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

/// v0.5.13: norm reduction shader 의 uniform.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct NormReductionUniforms {
    n_amplitudes: u32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
}

/// v0.5.14: collapse + renormalize shader 의 uniform.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct CollapseRenormalizeUniforms {
    target_bit: u32,
    outcome: u32,
    n_amplitudes: u32,
    inv_sqrt_prob: f32,
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
}

/// v0.5.15: qubit prob reduction shader 의 uniform.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct QubitProbReductionUniforms {
    n_amplitudes: u32,
    target_bit: u32,
    dispatches_x: u32,
    _pad0: u32,
}

/// v0.5.2 dispatch chunking helper.  workgroup-count-per-dimension 65535 한계를
/// 우회해 2D dispatch (X, Y, 1) 로 바꾼다.  shader 가 `dispatches_x` 가
/// 0 이면 1D path (`gid.x` 그대로), 양수면 2D path (`gid.x + gid.y *
/// dispatches_x * 64`) 로 자동 분기.  GPU 의 uniform branching 은 invocation
/// 모두 같은 분기라 divergence cost 0.
///
/// **v0.5.3 fix**: 작은 회로 (N≤21, K ≤ 32768) 에서 v0.5.2 의 2D 산수 overhead
/// 를 회피.  큰 회로는 2D chunking path 그대로 동작.  반환 `(wg_x, wg_y,
/// dispatches_x_uniform)` — `dispatches_x_uniform == 0` 이 1D 신호.
const MAX_WG_PER_DIM: u32 = 65535;

#[inline]
fn dispatch_2d(workgroups: u32) -> (u32, u32, u32) {
    if workgroups == 0 {
        return (1, 1, 0);
    }
    if workgroups <= MAX_WG_PER_DIM {
        // 1D path — shader 가 `gid.x` 그대로 사용 (dispatches_x = 0 신호).
        (workgroups, 1, 0)
    } else {
        // 2D chunking — shader 가 `gid.x + gid.y * dispatches_x * 64` 로 복원.
        let wg_x = MAX_WG_PER_DIM;
        let wg_y = workgroups.div_ceil(MAX_WG_PER_DIM);
        (wg_x, wg_y, wg_x)
    }
}

/// 단일 pipeline + bgl 묶음.
struct Pipeline {
    pipeline: wgpu::ComputePipeline,
    bgl: wgpu::BindGroupLayout,
}

/// GPU 에서 dispatch 할 수 있는 게이트 op (Cut D.3).
///
/// `apply_circuit` 의 입력.  panta-sim 의 `Gate` 와 분리된 GPU-friendly form:
/// - `Single`: 1×1 matrix + target qubit.
/// - `Two`: 4×4 matrix + 두 qubit (CZ, SWAP 같은 비-controlled 2q gate).
/// - `Controlled1q`: 1×1 matrix + control + target (CNOT, CY, CH, CRx, CRy,
///   CRz, CP, CU3, CU).
///
/// Toffoli / Fredkin 같은 3-qubit 은 v0.5.0 시점 거부 — 사용자가 panta-sim
/// 측에서 transpile 후 호출하거나 후속 cut 에서 추가.
#[derive(Debug, Clone)]
pub enum WgpuGateOp {
    Single {
        matrix: [[Complex<f32>; 2]; 2],
        target: usize,
    },
    Two {
        matrix: [[Complex<f32>; 4]; 4],
        q0: usize,
        q1: usize,
    },
    Controlled1q {
        matrix: [[Complex<f32>; 2]; 2],
        ctrl: usize,
        tgt: usize,
    },
}

/// wgpu 기반 state vector backend (Tier-1, v0.5.0).
///
/// state vector 는 `Vec<Complex<f32>>` (CPU) ↔ GPU storage buffer 사이를
/// upload/download 한다.  단일 gate API 는 매 호출마다 round-trip — circuit
/// 단위 batching 은 [`apply_circuit`] (Cut D.3 예정).
pub struct WgpuStatevectorBackend {
    device: wgpu::Device,
    queue: wgpu::Queue,
    single_qubit: Pipeline,
    two_qubit: Pipeline,
    controlled_1q: Pipeline,
    // v0.5.5: K=2 buffer-split pipelines.  N≥28 일 때 사용.
    single_qubit_k2: Pipeline,
    two_qubit_k2: Pipeline,
    controlled_1q_k2: Pipeline,
    // v0.5.6: K=4 buffer-split pipelines.  N=30~31 일 때 사용.
    single_qubit_k4: Pipeline,
    two_qubit_k4: Pipeline,
    controlled_1q_k4: Pipeline,
    // v0.5.7: K=8 buffer-split pipelines.  N=30 일 때 사용 (v0.5.16 정정).
    single_qubit_k8: Pipeline,
    two_qubit_k8: Pipeline,
    controlled_1q_k8: Pipeline,
    // v0.5.17: K=16 buffer-split pipelines.  N=31 일 때 사용.
    single_qubit_k16: Pipeline,
    two_qubit_k16: Pipeline,
    controlled_1q_k16: Pipeline,
    // v0.5.18: K=32 buffer-split pipelines.  N=32 일 때 사용.  adapter 의
    // max_storage_buffers_per_shader_stage ≥ 33 면 Some(..), 아니면 None.
    single_qubit_k32: Option<Pipeline>,
    two_qubit_k32: Option<Pipeline>,
    controlled_1q_k32: Option<Pipeline>,
    // v0.5.13: norm reduction pipeline.  ‖ψ‖² 의 GPU 계산 (workgroup partial
    // sum + CPU final).  v0.5.14/15 의 토대.
    norm_reduction: Pipeline,
    // v0.5.14: collapse + renormalize pipeline.  measure outcome 결정 후
    // statevector 의 collapse + 1/√prob normalization.
    collapse_renormalize: Pipeline,
    // v0.5.15: per-qubit prob reduction.  outcome=0 amplitude 만의 ‖ψ‖²
    // (norm_reduction 의 outcome filter 변형).  measure 의 sampling 에 사용.
    qubit_prob_reduction: Pipeline,
    // v0.6.10: Philox4x32-10 counter-based RNG.  GPU-side uniform 생성 —
    // trajectory sampling 의 CPU RNG round-trip 제거 토대.  layout = result
    // storage(rw) + uniform → build_pipeline 과 동일.
    philox_rng: Pipeline,
}

/// v0.6.10: Philox uniform 생성 셰이더의 uniform.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable, Default)]
struct PhiloxUniforms {
    count: u32,
    seed_lo: u32,
    seed_hi: u32,
    _pad: u32,
}

impl WgpuStatevectorBackend {
    /// adapter / device 를 초기화하고 모든 pipeline 을 빌드한다.
    ///
    /// **v0.5.1 fix**: `adapter.limits()` 를 그대로 device 에 요청해 NVIDIA / AMD /
    /// Intel discrete GPU 의 큰 buffer / dispatch 한계를 모두 활용.  v0.5.0 의
    /// `Limits::default()` (downlevel 기본값) 은 `max_buffer_size=256 MB`,
    /// `max_storage_buffer_binding_size=128 MB`, `max_compute_workgroups_per_dimension=
    /// 65535` 라 N≥22 부터 dispatch 또는 buffer 한계로 panic 했음.
    /// (DGX Spark / NVIDIA GB10 보고에서 확인됨).
    pub fn new() -> Result<Self, GpuError> {
        let mut idesc = wgpu::InstanceDescriptor::new_without_display_handle();
        idesc.backends = wgpu::Backends::all();
        let instance = wgpu::Instance::new(idesc);
        let adapter = instance
            .request_adapter(&wgpu::RequestAdapterOptions {
                power_preference: wgpu::PowerPreference::HighPerformance,
                compatible_surface: None,
                force_fallback_adapter: false,
            })
            .block_on()
            .map_err(|_| GpuError::NoAdapter)?;
        let adapter_limits = adapter.limits();
        let (device, queue) = adapter
            .request_device(&wgpu::DeviceDescriptor {
                label: Some("panta-sim wgpu device"),
                required_features: wgpu::Features::empty(),
                required_limits: adapter_limits,
                experimental_features: wgpu::ExperimentalFeatures::default(),
                memory_hints: wgpu::MemoryHints::Performance,
                trace: wgpu::Trace::Off,
            })
            .block_on()
            .map_err(|e| GpuError::DeviceCreation(format!("{e:?}")))?;

        let single_qubit = build_pipeline(
            &device,
            "single_qubit",
            include_str!("shaders/single_qubit.wgsl"),
        );
        let two_qubit =
            build_pipeline(&device, "two_qubit", include_str!("shaders/two_qubit.wgsl"));
        let controlled_1q = build_pipeline(
            &device,
            "controlled_1q",
            include_str!("shaders/controlled_1q.wgsl"),
        );
        // v0.5.5: K=2 buffer-split 변종.
        let single_qubit_k2 = build_pipeline_k2(
            &device,
            "single_qubit_k2",
            include_str!("shaders/single_qubit_k2.wgsl"),
        );
        let two_qubit_k2 = build_pipeline_k2(
            &device,
            "two_qubit_k2",
            include_str!("shaders/two_qubit_k2.wgsl"),
        );
        let controlled_1q_k2 = build_pipeline_k2(
            &device,
            "controlled_1q_k2",
            include_str!("shaders/controlled_1q_k2.wgsl"),
        );
        // v0.5.6: K=4 buffer-split 변종.
        let single_qubit_k4 = build_pipeline_k4(
            &device,
            "single_qubit_k4",
            include_str!("shaders/single_qubit_k4.wgsl"),
        );
        let two_qubit_k4 = build_pipeline_k4(
            &device,
            "two_qubit_k4",
            include_str!("shaders/two_qubit_k4.wgsl"),
        );
        let controlled_1q_k4 = build_pipeline_k4(
            &device,
            "controlled_1q_k4",
            include_str!("shaders/controlled_1q_k4.wgsl"),
        );
        // v0.5.7: K=8 buffer-split 변종.
        let single_qubit_k8 = build_pipeline_k8(
            &device,
            "single_qubit_k8",
            include_str!("shaders/single_qubit_k8.wgsl"),
        );
        let two_qubit_k8 = build_pipeline_k8(
            &device,
            "two_qubit_k8",
            include_str!("shaders/two_qubit_k8.wgsl"),
        );
        let controlled_1q_k8 = build_pipeline_k8(
            &device,
            "controlled_1q_k8",
            include_str!("shaders/controlled_1q_k8.wgsl"),
        );
        // v0.5.17: K=16 buffer-split 변종.
        let single_qubit_k16 = build_pipeline_kn(
            &device,
            "single_qubit_k16",
            include_str!("shaders/single_qubit_k16.wgsl"),
            16,
        );
        let two_qubit_k16 = build_pipeline_kn(
            &device,
            "two_qubit_k16",
            include_str!("shaders/two_qubit_k16.wgsl"),
            16,
        );
        let controlled_1q_k16 = build_pipeline_kn(
            &device,
            "controlled_1q_k16",
            include_str!("shaders/controlled_1q_k16.wgsl"),
            16,
        );
        // v0.5.18: K=32 buffer-split 변종.  adapter 의
        // max_storage_buffers_per_shader_stage ≥ 33 면 build, 아니면 None
        // (NVIDIA / AMD desktop 만 지원, Apple Metal 31 / Intel Arc 16 / lavapipe 16 fail).
        let device_limits = device.limits();
        let k32_supported = device_limits.max_storage_buffers_per_shader_stage >= 33;
        let (single_qubit_k32, two_qubit_k32, controlled_1q_k32) = if k32_supported {
            (
                Some(build_pipeline_kn(
                    &device,
                    "single_qubit_k32",
                    include_str!("shaders/single_qubit_k32.wgsl"),
                    32,
                )),
                Some(build_pipeline_kn(
                    &device,
                    "two_qubit_k32",
                    include_str!("shaders/two_qubit_k32.wgsl"),
                    32,
                )),
                Some(build_pipeline_kn(
                    &device,
                    "controlled_1q_k32",
                    include_str!("shaders/controlled_1q_k32.wgsl"),
                    32,
                )),
            )
        } else {
            (None, None, None)
        };
        // v0.5.13: norm reduction pipeline.
        let norm_reduction = build_pipeline_norm_reduction(
            &device,
            "norm_reduction",
            include_str!("shaders/norm_reduction.wgsl"),
        );
        // v0.5.14: collapse + renormalize pipeline.  binding layout = state
        // (read_write) + uniform.  K=1 의 build_pipeline 그대로 재활용.
        let collapse_renormalize = build_pipeline(
            &device,
            "collapse_renormalize",
            include_str!("shaders/collapse_renormalize.wgsl"),
        );
        // v0.5.15: per-qubit prob reduction (norm_reduction 같은 binding layout).
        let qubit_prob_reduction = build_pipeline_norm_reduction(
            &device,
            "qubit_prob_reduction",
            include_str!("shaders/qubit_prob_reduction.wgsl"),
        );
        // v0.6.10: Philox RNG (result storage + uniform → build_pipeline layout).
        let philox_rng = build_pipeline(
            &device,
            "philox_rng",
            include_str!("shaders/philox_uniform.wgsl"),
        );

        Ok(Self {
            device,
            queue,
            single_qubit,
            two_qubit,
            controlled_1q,
            single_qubit_k2,
            two_qubit_k2,
            controlled_1q_k2,
            single_qubit_k4,
            two_qubit_k4,
            controlled_1q_k4,
            single_qubit_k8,
            two_qubit_k8,
            controlled_1q_k8,
            single_qubit_k16,
            two_qubit_k16,
            controlled_1q_k16,
            single_qubit_k32,
            two_qubit_k32,
            controlled_1q_k32,
            norm_reduction,
            collapse_renormalize,
            qubit_prob_reduction,
            philox_rng,
        })
    }

    /// v0.6.10: Philox4x32-10 으로 `count` 개의 `[0,1)` uniform 을 GPU 에서
    /// 생성해 반환한다.  [`crate::philox::philox_uniforms_cpu`] 와 bit-exact
    /// (동일 `seed` → 동일 sequence).  GPU-side sampling 의 RNG round-trip
    /// 제거 토대 (trajectory 통합은 engine 측에서 사용).
    ///
    /// 큰 `count` (≈ 1.6e7 초과) 는 1D dispatch 한계를 넘어 에러 — sampling
    /// 용도 (shots / qubit 수 규모) 에선 충분.
    pub fn generate_uniforms(&self, seed: u64, count: usize) -> Result<Vec<f32>, GpuError> {
        if count == 0 {
            return Ok(Vec::new());
        }
        let blocks = count.div_ceil(4) as u32; // invocation = block (4 uniform/block)
        let workgroups = blocks.div_ceil(64);
        if workgroups > MAX_WG_PER_DIM {
            return Err(GpuError::Buffer(format!(
                "generate_uniforms: count {count} 가 1D dispatch 한계를 초과"
            )));
        }
        let byte_size = (count * std::mem::size_of::<f32>()) as u64;
        let result_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("philox result"),
            size: byte_size.max(4),
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("philox staging"),
            size: byte_size.max(4),
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let uniforms = PhiloxUniforms {
            count: count as u32,
            seed_lo: seed as u32,
            seed_hi: (seed >> 32) as u32,
            _pad: 0,
        };
        let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
        let bg = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("philox bg"),
            layout: &self.philox_rng.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: result_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: ubuf.as_entire_binding(),
                },
            ],
        });
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("philox encoder"),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("philox rng"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.philox_rng.pipeline);
            pass.set_bind_group(0, &bg, &[]);
            pass.dispatch_workgroups(workgroups, 1, 1);
        }
        encoder.copy_buffer_to_buffer(&result_buf, 0, &staging, 0, byte_size.max(4));
        self.queue.submit(Some(encoder.finish()));

        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = slice.get_mapped_range();
        let floats: &[f32] = bytemuck::cast_slice(&data);
        let out = floats[..count].to_vec();
        drop(data);
        staging.unmap();
        Ok(out)
    }

    /// 단일 큐비트 gate (1q matrix `M`) 를 GPU 에서 적용.
    pub fn apply_single_qubit_gate(
        &self,
        state: &mut [Complex<f32>],
        matrix: &[[Complex<f32>; 2]; 2],
        target: usize,
    ) -> Result<(), GpuError> {
        let n = check_state_len(state)?;
        let stride = 1u32 << target;
        let pairs = (n / 2) as u32;
        let (wg_x, wg_y, dispatches_x) = dispatch_2d(pairs.div_ceil(64));
        let uniforms = SingleQubitUniforms {
            qubit_stride: stride,
            n_amplitudes: n as u32,
            dispatches_x,
            _pad1: 0,
            m00: [matrix[0][0].re, matrix[0][0].im],
            m01: [matrix[0][1].re, matrix[0][1].im],
            m10: [matrix[1][0].re, matrix[1][0].im],
            m11: [matrix[1][1].re, matrix[1][1].im],
        };
        self.dispatch_one(
            &self.single_qubit,
            state,
            bytemuck::bytes_of(&uniforms),
            (wg_x, wg_y),
            "single_qubit",
        )
    }

    /// 일반 2-큐비트 gate (4×4 matrix).  q0=lower, q1=higher (자동 정렬).
    pub fn apply_two_qubit_gate(
        &self,
        state: &mut [Complex<f32>],
        matrix: &[[Complex<f32>; 4]; 4],
        qubit0: usize,
        qubit1: usize,
    ) -> Result<(), GpuError> {
        let n = check_state_len(state)?;
        if qubit0 == qubit1 {
            return Err(GpuError::Unsupported(
                "apply_two_qubit_gate: qubit0 == qubit1".into(),
            ));
        }
        let bit0 = 1u32 << qubit0;
        let bit1 = 1u32 << qubit1;
        let (q_lo, q_hi) = if qubit0 < qubit1 {
            (qubit0, qubit1)
        } else {
            (qubit1, qubit0)
        };
        let mask_lo = (1u32 << q_lo) - 1;
        let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
        let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
        let n_groups = (n / 4) as u32;

        let mut m_flat = [[0.0_f32; 2]; 16];
        for i in 0..4 {
            for j in 0..4 {
                m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
            }
        }

        let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
        let uniforms = TwoQubitUniforms {
            bit0,
            bit1,
            n_amplitudes: n as u32,
            mask_lo,
            mask_mid,
            mask_hi,
            n_groups,
            dispatches_x,
            m: m_flat,
        };
        self.dispatch_one(
            &self.two_qubit,
            state,
            bytemuck::bytes_of(&uniforms),
            (wg_x, wg_y),
            "two_qubit",
        )
    }

    /// **2-큐비트 Kraus 채널 trajectory 적용 (GPU-native)**.
    ///
    /// 각 Kraus 연산자 `Kᵢ` (4×4) 에 대해 `pᵢ = ‖Kᵢ|ψ⟩‖²` 를 GPU 의 2q 게이트
    /// 커널(`two_qubit.wgsl`, 비유니터리 4×4 도 그대로 행렬·벡터곱)로 계산하고,
    /// `u∈[0,1)` 로 `pᵢ` 분포에서 하나를 샘플해 `|ψ⟩ ← Kᵢ|ψ⟩/√pᵢ` 로 collapse·
    /// 재정규화한다.  무거운 `O(2ⁿ)` 행렬 적용이 GPU 에서 수행된다 (이전엔
    /// CPU-hybrid).  norm 합산·샘플링·스케일은 가벼운 CPU 작업.
    ///
    /// `kraus` 는 trace-preserving (`Σ Kᵢ†Kᵢ = I`) 가정.  CPU
    /// [`qsim_core::operations`] 의 2q Kraus 와 분포 일치 (lavapipe 검증).
    pub fn apply_kraus_2q_trajectory(
        &self,
        state: &mut [Complex<f32>],
        kraus: &[[[Complex<f32>; 4]; 4]],
        qubit0: usize,
        qubit1: usize,
        u: f32,
    ) -> Result<(), GpuError> {
        if kraus.is_empty() {
            return Err(GpuError::Unsupported(
                "apply_kraus_2q_trajectory: Kraus 비어 있음".into(),
            ));
        }
        // pᵢ = ‖Kᵢ|ψ⟩‖² (GPU 로 Kᵢ 적용 후 host norm).
        let mut probs = Vec::with_capacity(kraus.len());
        for k in kraus {
            let mut tmp = state.to_vec();
            self.apply_two_qubit_gate(&mut tmp, k, qubit0, qubit1)?;
            let p: f32 = tmp.iter().map(|c| c.norm_sqr()).sum();
            probs.push(p);
        }
        let total: f32 = probs.iter().sum();
        // u·total 누적분포로 Kraus 샘플 (수치 안전: 마지막 인덱스 fallback).
        let target = u.clamp(0.0, 1.0) * total;
        let mut acc = 0.0_f32;
        let mut idx = kraus.len() - 1;
        for (i, &p) in probs.iter().enumerate() {
            acc += p;
            if target < acc {
                idx = i;
                break;
            }
        }
        // 선택된 Kᵢ 적용 + 재정규화.
        self.apply_two_qubit_gate(state, &kraus[idx], qubit0, qubit1)?;
        let nrm = probs[idx].sqrt();
        if nrm > 1e-12 {
            let inv = 1.0 / nrm;
            for a in state.iter_mut() {
                *a = Complex::new(a.re * inv, a.im * inv);
            }
        }
        Ok(())
    }

    /// Controlled 1-큐비트 gate (CNOT 등).  ctrl bit=1 인 amplitude pair 에만
    /// 1q matrix 적용.
    pub fn apply_controlled_1q(
        &self,
        state: &mut [Complex<f32>],
        matrix: &[[Complex<f32>; 2]; 2],
        ctrl: usize,
        tgt: usize,
    ) -> Result<(), GpuError> {
        let n = check_state_len(state)?;
        if ctrl == tgt {
            return Err(GpuError::Unsupported(
                "apply_controlled_1q: ctrl == tgt".into(),
            ));
        }
        let (wg_x, wg_y, dispatches_x) = dispatch_2d((n as u32).div_ceil(64));
        let uniforms = Controlled1qUniforms {
            ctrl_bit: 1u32 << ctrl,
            tgt_stride: 1u32 << tgt,
            n_amplitudes: n as u32,
            dispatches_x,
            m00: [matrix[0][0].re, matrix[0][0].im],
            m01: [matrix[0][1].re, matrix[0][1].im],
            m10: [matrix[1][0].re, matrix[1][0].im],
            m11: [matrix[1][1].re, matrix[1][1].im],
        };
        self.dispatch_one(
            &self.controlled_1q,
            state,
            bytemuck::bytes_of(&uniforms),
            (wg_x, wg_y),
            "controlled_1q",
        )
    }

    /// 회로 단위 batching (Cut D.3).
    ///
    /// state 를 한 번 GPU buffer 에 업로드한 후 모든 게이트 op 를 single
    /// command encoder 에 dispatch.  마지막에 1 회 download.  단일 gate API
    /// 의 N 회 round-trip 대비 큰 회로에서 성능 차이 결정적.
    ///
    /// 빈 ops 리스트는 state 그대로 (즉시 반환).
    ///
    /// **v0.5.5 buffer split**: N≥28 (sv ≥ 2 GB) 에서 NVIDIA Vulkan 의
    /// `maxStorageBufferRange` ≈ 2 GB 한계를 풀기 위해 statevector 를 K=2 buffer
    /// 로 분할 (high bit 으로 lo / hi).  shader 가 same-buffer / cross-buffer
    /// 동적 분기로 처리.  N≤27 은 기존 K=1 path 그대로 (회귀 0).
    pub fn apply_circuit(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
    ) -> Result<(), GpuError> {
        let n = check_state_len(state)?;
        if ops.is_empty() {
            return Ok(());
        }
        let n_qubits = bits_for_n(n);
        // v0.5.18: N=32 시 adapter 의 K=32 pipeline 가용성 확인.
        if n_qubits > 32 {
            return Err(GpuError::Unsupported(format!(
                "wgpu statevector: N={n_qubits} 는 single-GPU wgpu Tier-1 한계 \
                 (32 GiB statevector) 초과.  multi-GPU / out-of-core 영역 — \
                 backend='cpu' 또는 source 빌드 + cuda backend."
            )));
        }
        let k = compute_split_factor(n_qubits);
        if k == 32 {
            // N=32: K=32 pipeline 가용 GPU (NVIDIA / AMD desktop binding ≥ 33) 만.
            // Apple Metal 31 / Intel Arc 16 / lavapipe Mesa 16 등은 None.
            if self.single_qubit_k32.is_none() {
                let limit = self.device.limits().max_storage_buffers_per_shader_stage;
                return Err(GpuError::Unsupported(format!(
                    "wgpu statevector: N=32 는 K=32 buffer split 필요하지만 GPU 의 \
                     max_storage_buffers_per_shader_stage={limit} (≥33 필요).  \
                     Apple Metal (31) / Intel Arc (16) / lavapipe (16) 등에서 \
                     N=32 미지원.  N≤31 사용 또는 backend='cpu' / cuda."
                )));
            }
            return self.apply_circuit_k32(state, ops, n_qubits);
        }
        if k == 16 {
            return self.apply_circuit_k16(state, ops, n_qubits);
        }
        if k == 8 {
            return self.apply_circuit_k8(state, ops, n_qubits);
        }
        if k == 4 {
            return self.apply_circuit_k4(state, ops, n_qubits);
        }
        if k == 2 {
            return self.apply_circuit_k2(state, ops, n_qubits);
        }
        // k == 1: 기존 path (N≤27).

        // 1. State buffer 업로드.
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let state_bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("apply_circuit state"),
                contents: state_bytes,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("apply_circuit staging"),
            size: state_bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        // 2. 각 op 마다 uniform buffer + bind group 생성 (수명을 encoder submit
        // 까지 살려둠).  encoder 안에서 compute pass dispatch.
        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());
        // dispatches[i] = (pipeline_idx, wg_x, wg_y).  pipeline_idx ∈ {0=single,
        // 1=two, 2=controlled1q}.  v0.5.2 2D dispatch chunking 으로 65535 한계 우회.
        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= bits_for_n(n) {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} 가 범위 벗어남 (n_qubits={})",
                            bits_for_n(n)
                        )));
                    }
                    let stride = 1u32 << target;
                    let pairs = (n / 2) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(pairs.div_ceil(64));
                    let uniforms = SingleQubitUniforms {
                        qubit_stride: stride,
                        n_amplitudes: n as u32,
                        dispatches_x,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.single_qubit.bgl, &storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= bits_for_n(n) || *q1 >= bits_for_n(n) {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (n / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitUniforms {
                        bit0,
                        bit1,
                        n_amplitudes: n as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        dispatches_x,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.two_qubit.bgl, &storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= bits_for_n(n) || *tgt >= bits_for_n(n) {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d((n as u32).div_ceil(64));
                    let uniforms = Controlled1qUniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: n as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.controlled_1q.bgl, &storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        // 3. Encoder 안에서 모든 op compute pass dispatch.  pass 마다 새로
        //    begin/end (가장 안전 + 명확).
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit,
                1 => &self.two_qubit,
                _ => &self.controlled_1q,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, state_bytes.len() as u64);
        self.queue.submit(Some(encoder.finish()));

        // 4. Download.
        let buffer_slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        buffer_slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = buffer_slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        for (dst, src) in state.iter_mut().zip(result.iter()) {
            *dst = (*src).into();
        }
        drop(data);
        staging.unmap();
        // owned_bufs / owned_bgs drop → GPU resources 해제.
        Ok(())
    }

    /// v0.6.10: |0…0⟩ 로 초기화된 GPU-resident state buffer 를 만든다.
    ///
    /// `apply_ops_to_buffer` / `measure_qubit_gpu` / `collapse_qubit` 가 공유하는
    /// single storage buffer (K=1 path, N≤27).  trajectory 의 GPU-resident
    /// 실행에서 매 shot 1회 생성.
    pub fn create_zero_state_buffer(&self, n_amplitudes: usize) -> wgpu::Buffer {
        let mut pod = vec![CF32 { re: 0.0, im: 0.0 }; n_amplitudes];
        pod[0] = CF32 { re: 1.0, im: 0.0 };
        self.device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("resident state"),
                contents: bytemuck::cast_slice(&pod),
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            })
    }

    /// v0.6.10: GPU-resident state buffer → CPU `Vec<Complex<f32>>` 다운로드.
    pub fn download_state_buffer(
        &self,
        storage: &wgpu::Buffer,
        n_amplitudes: usize,
    ) -> Result<Vec<Complex<f32>>, GpuError> {
        let byte_size = (n_amplitudes * std::mem::size_of::<CF32>()) as u64;
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("resident download staging"),
            size: byte_size,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("resident download encoder"),
            });
        encoder.copy_buffer_to_buffer(storage, 0, &staging, 0, byte_size);
        self.queue.submit(Some(encoder.finish()));
        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        let out: Vec<Complex<f32>> = result.iter().map(|c| (*c).into()).collect();
        drop(data);
        staging.unmap();
        Ok(out)
    }

    /// v0.6.10: 이미 GPU 에 있는 state buffer 에 gate op 들을 적용한다
    /// (upload / download 없음, K=1 path, N≤27).
    ///
    /// [`apply_circuit`] 와 달리 state 가 GPU 에 상주한 채로 여러 gate batch +
    /// `measure_qubit_gpu` / `collapse_qubit` 을 round-trip 없이 연쇄할 수 있다 —
    /// trajectory 의 GPU-resident 실행에 사용.  buffer-split (N>27) 은 미지원.
    pub fn apply_ops_to_buffer(
        &self,
        storage: &wgpu::Buffer,
        ops: &[WgpuGateOp],
        n_amplitudes: usize,
    ) -> Result<(), GpuError> {
        if ops.is_empty() {
            return Ok(());
        }
        let n = n_amplitudes;
        let n_qubits = bits_for_n(n);
        if compute_split_factor(n_qubits) != 1 {
            return Err(GpuError::Unsupported(format!(
                "apply_ops_to_buffer: GPU-resident path 는 K=1 (N≤27) 만 지원 (N={n_qubits})"
            )));
        }
        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());
        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} 범위 초과 (n_qubits={n_qubits})"
                        )));
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(((n / 2) as u32).div_ceil(64));
                    let uniforms = SingleQubitUniforms {
                        qubit_stride: 1u32 << target,
                        n_amplitudes: n as u32,
                        dispatches_x,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.single_qubit.bgl, storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨"
                        )));
                    }
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let n_groups = (n / 4) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitUniforms {
                        bit0: 1u32 << q0,
                        bit1: 1u32 << q1,
                        n_amplitudes: n as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        dispatches_x,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.two_qubit.bgl, storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d((n as u32).div_ceil(64));
                    let uniforms = Controlled1qUniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: n as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group(&self.controlled_1q.bgl, storage, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_ops_to_buffer encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit,
                1 => &self.two_qubit,
                _ => &self.controlled_1q,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_ops_to_buffer op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        self.queue.submit(Some(encoder.finish()));
        Ok(())
    }

    /// v0.5.5: K=2 buffer-split apply_circuit path.
    ///
    /// statevector 를 두 buffer (state_lo / state_hi) 로 분할 — 각 buffer
    /// length = 2^(n_qubits - 1).  shader 가 same-buffer / cross-buffer 동적
    /// 분기로 처리 (split_target / split_q1 / split_ctrl / split_tgt uniform).
    fn apply_circuit_k2(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
        n_qubits: usize,
    ) -> Result<(), GpuError> {
        let dim = state.len(); // = 2^n_qubits
        let half_dim = dim / 2;
        let split_bit = n_qubits - 1;

        // 1. State 를 두 절반으로 split.  high bit = 0 → lo, high bit = 1 → hi.
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let lo_bytes: &[u8] = bytemuck::cast_slice(&pod[..half_dim]);
        let hi_bytes: &[u8] = bytemuck::cast_slice(&pod[half_dim..]);

        let storage_lo = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("apply_circuit_k2 state_lo"),
                contents: lo_bytes,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            });
        let storage_hi = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("apply_circuit_k2 state_hi"),
                contents: hi_bytes,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            });
        let staging_lo = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("apply_circuit_k2 staging_lo"),
            size: lo_bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let staging_hi = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("apply_circuit_k2 staging_hi"),
            size: hi_bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        // 2. Per-op uniform buffers + bind groups.
        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());
        // pipeline_idx ∈ {0=single_k2, 1=two_k2, 2=controlled_1q_k2}.

        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    // total pairs = dim / 2 = half_dim (각 buffer pair 또는 cross-buffer pair).
                    let total = half_dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = SingleQubitK2Uniforms {
                        qubit_stride: stride,
                        n_amplitudes: dim as u32,
                        half_dim: half_dim as u32,
                        split_target: if *target == split_bit { 1 } else { 0 },
                        dispatches_x,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k2(
                        &self.single_qubit_k2.bgl,
                        &storage_lo,
                        &storage_hi,
                        &ubuf,
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitK2Uniforms {
                        bit0,
                        bit1,
                        n_amplitudes: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        half_dim: half_dim as u32,
                        split_q1: if q_hi == split_bit { 1 } else { 0 },
                        dispatches_x,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        _pad4: 0,
                        _pad5: 0,
                        _pad6: 0,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k2(
                        &self.two_qubit_k2.bgl,
                        &storage_lo,
                        &storage_hi,
                        &ubuf,
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let total = dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = Controlled1qK2Uniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: dim as u32,
                        half_dim: half_dim as u32,
                        split_ctrl: if *ctrl == split_bit { 1 } else { 0 },
                        split_tgt: if *tgt == split_bit { 1 } else { 0 },
                        dispatches_x,
                        _pad0: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k2(
                        &self.controlled_1q_k2.bgl,
                        &storage_lo,
                        &storage_hi,
                        &ubuf,
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        // 3. Encoder + dispatch + 두 staging copy.
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit_k2 encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit_k2,
                1 => &self.two_qubit_k2,
                _ => &self.controlled_1q_k2,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit_k2 op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        encoder.copy_buffer_to_buffer(&storage_lo, 0, &staging_lo, 0, lo_bytes.len() as u64);
        encoder.copy_buffer_to_buffer(&storage_hi, 0, &staging_hi, 0, hi_bytes.len() as u64);
        self.queue.submit(Some(encoder.finish()));

        // 4. 두 staging download + state 재구성.
        let slice_lo = staging_lo.slice(..);
        let slice_hi = staging_hi.slice(..);
        let (sender_lo, receiver_lo) = std::sync::mpsc::channel();
        let (sender_hi, receiver_hi) = std::sync::mpsc::channel();
        slice_lo.map_async(wgpu::MapMode::Read, move |r| {
            sender_lo.send(r).ok();
        });
        slice_hi.map_async(wgpu::MapMode::Read, move |r| {
            sender_hi.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver_lo
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map lo: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async lo: {e:?}")))?;
        receiver_hi
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map hi: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async hi: {e:?}")))?;
        let data_lo = slice_lo.get_mapped_range();
        let data_hi = slice_hi.get_mapped_range();
        let result_lo: &[CF32] = bytemuck::cast_slice(&data_lo);
        let result_hi: &[CF32] = bytemuck::cast_slice(&data_hi);
        for (dst, src) in state.iter_mut().take(half_dim).zip(result_lo.iter()) {
            *dst = (*src).into();
        }
        for (dst, src) in state.iter_mut().skip(half_dim).zip(result_hi.iter()) {
            *dst = (*src).into();
        }
        drop(data_lo);
        drop(data_hi);
        staging_lo.unmap();
        staging_hi.unmap();
        Ok(())
    }

    fn create_bind_group_k2(
        &self,
        layout: &wgpu::BindGroupLayout,
        storage_lo: &wgpu::Buffer,
        storage_hi: &wgpu::Buffer,
        uniform: &wgpu::Buffer,
    ) -> wgpu::BindGroup {
        self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("k2 bg"),
            layout,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: storage_lo.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: storage_hi.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: uniform.as_entire_binding(),
                },
            ],
        })
    }

    /// v0.5.6: K=4 buffer-split apply_circuit path.
    ///
    /// statevector 를 4 buffer 로 분할 — high 2 bits 가 buffer index (0..3),
    /// 각 buffer length = 2^(n_qubits - 2).  shader 는 generic switch 로
    /// amplitude 의 buffer index 자동 결정.
    fn apply_circuit_k4(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
        n_qubits: usize,
    ) -> Result<(), GpuError> {
        let dim = state.len();
        let buf_dim = dim / 4;
        let offset_bits = (n_qubits - 2) as u32;
        let offset_mask = (1u32 << offset_bits).wrapping_sub(1);

        // 1. State 를 4 chunk 로 split + upload.
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let chunks: [&[CF32]; 4] = [
            &pod[0..buf_dim],
            &pod[buf_dim..2 * buf_dim],
            &pod[2 * buf_dim..3 * buf_dim],
            &pod[3 * buf_dim..4 * buf_dim],
        ];
        let chunk_bytes_len = std::mem::size_of_val(chunks[0]);
        let mut storages: Vec<wgpu::Buffer> = Vec::with_capacity(4);
        let mut stagings: Vec<wgpu::Buffer> = Vec::with_capacity(4);
        for (i, chunk) in chunks.iter().enumerate() {
            let bytes: &[u8] = bytemuck::cast_slice(chunk);
            storages.push(
                self.device
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some(&format!("apply_circuit_k4 state_b{i}")),
                        contents: bytes,
                        usage: wgpu::BufferUsages::STORAGE
                            | wgpu::BufferUsages::COPY_SRC
                            | wgpu::BufferUsages::COPY_DST,
                    }),
            );
            stagings.push(self.device.create_buffer(&wgpu::BufferDescriptor {
                label: Some(&format!("apply_circuit_k4 staging_b{i}")),
                size: bytes.len() as u64,
                usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            }));
        }

        // 2. Per-op uniform + bind group.
        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());
        // pipeline_idx ∈ {0=single_k4, 1=two_k4, 2=controlled_1q_k4}.

        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    let total_pairs = (dim / 2) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total_pairs.div_ceil(64));
                    let uniforms = SingleQubitK4Uniforms {
                        qubit_stride: stride,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k4(&self.single_qubit_k4.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitK4Uniforms {
                        bit0,
                        bit1,
                        n_amplitudes: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        _pad4: 0,
                        _pad5: 0,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k4(&self.two_qubit_k4.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let total = dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = Controlled1qK4Uniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg =
                        self.create_bind_group_k4(&self.controlled_1q_k4.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        // 3. Encoder + dispatch + 4 staging copy.
        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit_k4 encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit_k4,
                1 => &self.two_qubit_k4,
                _ => &self.controlled_1q_k4,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit_k4 op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        for i in 0..4 {
            encoder.copy_buffer_to_buffer(&storages[i], 0, &stagings[i], 0, chunk_bytes_len as u64);
        }
        self.queue.submit(Some(encoder.finish()));

        // 4. 4 staging download + state 재구성.
        let slices: Vec<wgpu::BufferSlice> = stagings.iter().map(|b| b.slice(..)).collect();
        let receivers: Vec<_> = slices
            .iter()
            .map(|s| {
                let (sender, receiver) = std::sync::mpsc::channel();
                s.map_async(wgpu::MapMode::Read, move |r| {
                    sender.send(r).ok();
                });
                receiver
            })
            .collect();
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        for (i, r) in receivers.into_iter().enumerate() {
            r.recv()
                .map_err(|e| GpuError::Buffer(format!("recv map b{i}: {e:?}")))?
                .map_err(|e| GpuError::Buffer(format!("map_async b{i}: {e:?}")))?;
        }
        let datas: Vec<wgpu::BufferView> = slices.iter().map(|s| s.get_mapped_range()).collect();
        for (i, data) in datas.iter().enumerate() {
            let chunk: &[CF32] = bytemuck::cast_slice(data);
            for (dst, src) in state
                .iter_mut()
                .skip(i * buf_dim)
                .take(buf_dim)
                .zip(chunk.iter())
            {
                *dst = (*src).into();
            }
        }
        drop(datas);
        for s in &stagings {
            s.unmap();
        }
        Ok(())
    }

    fn create_bind_group_k4(
        &self,
        layout: &wgpu::BindGroupLayout,
        storages: &[wgpu::Buffer],
        uniform: &wgpu::Buffer,
    ) -> wgpu::BindGroup {
        debug_assert_eq!(storages.len(), 4);
        self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("k4 bg"),
            layout,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: storages[0].as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: storages[1].as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: storages[2].as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 3,
                    resource: storages[3].as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 4,
                    resource: uniform.as_entire_binding(),
                },
            ],
        })
    }

    /// v0.5.7: K=8 buffer-split apply_circuit path.
    ///
    /// statevector 를 8 buffer 로 분할 — high 3 bits 가 buffer index (0..7),
    /// 각 buffer length = 2^(n_qubits - 3).  shader 는 8-way generic switch.
    fn apply_circuit_k8(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
        n_qubits: usize,
    ) -> Result<(), GpuError> {
        let dim = state.len();
        let buf_dim = dim / 8;
        let offset_bits = (n_qubits - 3) as u32;
        let offset_mask = (1u32 << offset_bits).wrapping_sub(1);

        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let mut storages: Vec<wgpu::Buffer> = Vec::with_capacity(8);
        let mut stagings: Vec<wgpu::Buffer> = Vec::with_capacity(8);
        let mut chunk_bytes_len = 0usize;
        for i in 0..8 {
            let chunk = &pod[i * buf_dim..(i + 1) * buf_dim];
            let bytes: &[u8] = bytemuck::cast_slice(chunk);
            chunk_bytes_len = bytes.len();
            storages.push(
                self.device
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some(&format!("apply_circuit_k8 state_b{i}")),
                        contents: bytes,
                        usage: wgpu::BufferUsages::STORAGE
                            | wgpu::BufferUsages::COPY_SRC
                            | wgpu::BufferUsages::COPY_DST,
                    }),
            );
            stagings.push(self.device.create_buffer(&wgpu::BufferDescriptor {
                label: Some(&format!("apply_circuit_k8 staging_b{i}")),
                size: bytes.len() as u64,
                usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            }));
        }

        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());

        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    let total_pairs = (dim / 2) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total_pairs.div_ceil(64));
                    let uniforms = SingleQubitK8Uniforms {
                        qubit_stride: stride,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k8(&self.single_qubit_k8.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitK8Uniforms {
                        bit0,
                        bit1,
                        n_amplitudes: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        _pad4: 0,
                        _pad5: 0,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_k8(&self.two_qubit_k8.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let total = dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = Controlled1qK8Uniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg =
                        self.create_bind_group_k8(&self.controlled_1q_k8.bgl, &storages, &ubuf);
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit_k8 encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit_k8,
                1 => &self.two_qubit_k8,
                _ => &self.controlled_1q_k8,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit_k8 op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        for i in 0..8 {
            encoder.copy_buffer_to_buffer(&storages[i], 0, &stagings[i], 0, chunk_bytes_len as u64);
        }
        self.queue.submit(Some(encoder.finish()));

        let slices: Vec<wgpu::BufferSlice> = stagings.iter().map(|b| b.slice(..)).collect();
        let receivers: Vec<_> = slices
            .iter()
            .map(|s| {
                let (sender, receiver) = std::sync::mpsc::channel();
                s.map_async(wgpu::MapMode::Read, move |r| {
                    sender.send(r).ok();
                });
                receiver
            })
            .collect();
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        for (i, r) in receivers.into_iter().enumerate() {
            r.recv()
                .map_err(|e| GpuError::Buffer(format!("recv map b{i}: {e:?}")))?
                .map_err(|e| GpuError::Buffer(format!("map_async b{i}: {e:?}")))?;
        }
        let datas: Vec<wgpu::BufferView> = slices.iter().map(|s| s.get_mapped_range()).collect();
        for (i, data) in datas.iter().enumerate() {
            let chunk: &[CF32] = bytemuck::cast_slice(data);
            for (dst, src) in state
                .iter_mut()
                .skip(i * buf_dim)
                .take(buf_dim)
                .zip(chunk.iter())
            {
                *dst = (*src).into();
            }
        }
        drop(datas);
        for s in &stagings {
            s.unmap();
        }
        Ok(())
    }

    /// v0.5.13: state 의 ‖ψ‖² 를 GPU 에서 계산.
    ///
    /// state 가 이미 GPU buffer 에 있을 때 사용.  workgroup 단위 partial sum 을
    /// 작은 buffer (size = num_workgroups) 에 누적 후 CPU 가 final sum.
    /// state buffer 전체 download (보통 MB ~ GB) 대비 partial sums (수십 KB) 만
    /// download — 양자 trajectory 의 noise / measure 정규화 단계에서 활용.
    ///
    /// 인자: `state_buffer` 는 `apply_circuit` 의 storage buffer 와 같은
    /// layout (`array<vec2<f32>>`, length = `n_amplitudes`).  caller 가
    /// usage 에 `STORAGE | COPY_SRC` 포함했을 것.
    ///
    /// 반환: f32 norm² 값.
    pub fn compute_norm_squared(
        &self,
        state_buffer: &wgpu::Buffer,
        n_amplitudes: usize,
    ) -> Result<f32, GpuError> {
        let n_amp = n_amplitudes as u32;
        let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_amp.div_ceil(64));
        let n_workgroups = (wg_x * wg_y) as usize;

        // partial sums buffer.
        let partial_size = (n_workgroups * std::mem::size_of::<f32>()) as u64;
        let partial_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("compute_norm partial"),
            size: partial_size.max(4),
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("compute_norm staging"),
            size: partial_size.max(4),
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        let uniforms = NormReductionUniforms {
            n_amplitudes: n_amp,
            dispatches_x,
            _pad0: 0,
            _pad1: 0,
        };
        let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
        let bg = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("norm bg"),
            layout: &self.norm_reduction.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: state_buffer.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: partial_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: ubuf.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("compute_norm encoder"),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("norm reduction"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.norm_reduction.pipeline);
            pass.set_bind_group(0, &bg, &[]);
            pass.dispatch_workgroups(wg_x, wg_y, 1);
        }
        encoder.copy_buffer_to_buffer(&partial_buf, 0, &staging, 0, partial_size.max(4));
        self.queue.submit(Some(encoder.finish()));

        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = slice.get_mapped_range();
        let partials: &[f32] = bytemuck::cast_slice(&data);
        let total: f32 = partials.iter().take(n_workgroups).sum();
        drop(data);
        staging.unmap();
        Ok(total)
    }

    /// v0.5.14: state buffer 의 qubit 측정 outcome 을 collapse + renormalize.
    ///
    /// caller 가 outcome (0 or 1) 결정 후 prob = P(outcome) 를 v0.5.13 의
    /// `compute_norm_squared` 또는 outcome filter 변형으로 미리 계산해
    /// `inv_sqrt_prob = 1/√prob` 로 전달.
    ///
    /// shader 안:
    ///   amp[i] := amp[i] / √prob   if (i bit qubit) == outcome
    ///   amp[i] := 0                otherwise
    ///
    /// state buffer 가 이미 GPU 위에 있을 때 사용 — `apply_circuit` 의 storage
    /// buffer 그대로 입력.  caller 가 buffer 의 usage 에 `STORAGE` 포함했어야.
    pub fn collapse_qubit(
        &self,
        state_buffer: &wgpu::Buffer,
        n_amplitudes: usize,
        qubit: usize,
        outcome: u8,
        inv_sqrt_prob: f32,
    ) -> Result<(), GpuError> {
        let n_amp = n_amplitudes as u32;
        let target_bit = 1u32 << qubit;
        let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_amp.div_ceil(64));

        let uniforms = CollapseRenormalizeUniforms {
            target_bit,
            outcome: outcome as u32,
            n_amplitudes: n_amp,
            inv_sqrt_prob,
            dispatches_x,
            _pad0: 0,
            _pad1: 0,
            _pad2: 0,
        };
        let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
        let bg = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("collapse bg"),
            layout: &self.collapse_renormalize.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: state_buffer.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: ubuf.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("collapse encoder"),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("collapse renormalize"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.collapse_renormalize.pipeline);
            pass.set_bind_group(0, &bg, &[]);
            pass.dispatch_workgroups(wg_x, wg_y, 1);
        }
        self.queue.submit(Some(encoder.finish()));
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        Ok(())
    }

    /// v0.5.15: state buffer 의 qubit 측정 prob (P(qubit=0)) 를 GPU 에서 계산.
    ///
    /// norm_reduction 의 outcome filter 변형 — `i bit qubit == 0` 인 amplitude
    /// 만 합산해 partial sums 에 write.  CPU 가 partial sums sum.
    ///
    /// 반환값 ∈ [0, 1].  P(qubit=1) = 1 - P(qubit=0).
    pub fn compute_qubit_prob_zero(
        &self,
        state_buffer: &wgpu::Buffer,
        n_amplitudes: usize,
        qubit: usize,
    ) -> Result<f32, GpuError> {
        let n_amp = n_amplitudes as u32;
        let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_amp.div_ceil(64));
        let n_workgroups = (wg_x * wg_y) as usize;

        let partial_size = (n_workgroups * std::mem::size_of::<f32>()) as u64;
        let partial_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("qubit_prob partial"),
            size: partial_size.max(4),
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("qubit_prob staging"),
            size: partial_size.max(4),
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        let uniforms = QubitProbReductionUniforms {
            n_amplitudes: n_amp,
            target_bit: 1u32 << qubit,
            dispatches_x,
            _pad0: 0,
        };
        let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
        let bg = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("qubit_prob bg"),
            layout: &self.qubit_prob_reduction.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: state_buffer.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: partial_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: ubuf.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("qubit_prob encoder"),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("qubit_prob reduction"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.qubit_prob_reduction.pipeline);
            pass.set_bind_group(0, &bg, &[]);
            pass.dispatch_workgroups(wg_x, wg_y, 1);
        }
        encoder.copy_buffer_to_buffer(&partial_buf, 0, &staging, 0, partial_size.max(4));
        self.queue.submit(Some(encoder.finish()));

        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = slice.get_mapped_range();
        let partials: &[f32] = bytemuck::cast_slice(&data);
        let prob: f32 = partials.iter().take(n_workgroups).sum();
        drop(data);
        staging.unmap();
        Ok(prob.clamp(0.0, 1.0))
    }

    /// v0.5.15: 합성 measure API — GPU prob 계산 + CPU outcome 결정 +
    /// GPU collapse 모두 수행.
    ///
    /// state buffer 가 GPU 에 있고 sampling 1회 (random uniform [0,1)) 가
    /// CPU 에서 결정될 때 사용.  state amplitude 자체는 download 안 됨 —
    /// prob (수십 KB partial sums → CPU sum 1 float) 만 round-trip.
    ///
    /// 인자:
    /// - `state_buffer`: 측정할 statevector (read_write storage).
    /// - `n_amplitudes`: 2^n.
    /// - `qubit`: 측정 qubit 인덱스.
    /// - `random_uniform`: caller 가 미리 결정한 [0, 1) 의 uniform.
    ///
    /// 반환: 측정 outcome (0 또는 1).  state buffer 는 collapse + renormalize 됨.
    pub fn measure_qubit_gpu(
        &self,
        state_buffer: &wgpu::Buffer,
        n_amplitudes: usize,
        qubit: usize,
        random_uniform: f32,
    ) -> Result<u8, GpuError> {
        let p_zero = self.compute_qubit_prob_zero(state_buffer, n_amplitudes, qubit)?;
        let outcome: u8 = if random_uniform < p_zero { 0 } else { 1 };
        let prob = if outcome == 0 { p_zero } else { 1.0 - p_zero };
        // numerically extreme: prob ≈ 0 인 outcome 은 발생 안 해야 (random_uniform
        // 분포로 차단) — 안전장치로 epsilon clamp.
        let safe_prob = prob.max(1e-30);
        let inv_sqrt_prob = 1.0 / safe_prob.sqrt();
        self.collapse_qubit(state_buffer, n_amplitudes, qubit, outcome, inv_sqrt_prob)?;
        Ok(outcome)
    }

    fn create_bind_group_k8(
        &self,
        layout: &wgpu::BindGroupLayout,
        storages: &[wgpu::Buffer],
        uniform: &wgpu::Buffer,
    ) -> wgpu::BindGroup {
        self.create_bind_group_kn(layout, storages, uniform, 8, "k8 bg")
    }

    /// v0.5.17: generic K-buffer bind group 헬퍼.  K=16/32 일 때 활용.
    fn create_bind_group_kn(
        &self,
        layout: &wgpu::BindGroupLayout,
        storages: &[wgpu::Buffer],
        uniform: &wgpu::Buffer,
        storage_count: usize,
        label: &str,
    ) -> wgpu::BindGroup {
        debug_assert_eq!(storages.len(), storage_count);
        let mut entries: Vec<wgpu::BindGroupEntry> = (0..storage_count)
            .map(|i| wgpu::BindGroupEntry {
                binding: i as u32,
                resource: storages[i].as_entire_binding(),
            })
            .collect();
        entries.push(wgpu::BindGroupEntry {
            binding: storage_count as u32,
            resource: uniform.as_entire_binding(),
        });
        self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some(label),
            layout,
            entries: &entries,
        })
    }

    /// v0.5.17: K=16 buffer-split apply_circuit path.  K=8 패턴 그대로.
    /// chunk size = 2^(n-4) × 8 byte ≤ 1 GiB (N≤31).
    fn apply_circuit_k16(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
        n_qubits: usize,
    ) -> Result<(), GpuError> {
        const K: usize = 16;
        let dim = state.len();
        let buf_dim = dim / K;
        let offset_bits = (n_qubits - 4) as u32;
        let offset_mask = (1u32 << offset_bits).wrapping_sub(1);

        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let mut storages: Vec<wgpu::Buffer> = Vec::with_capacity(K);
        let mut stagings: Vec<wgpu::Buffer> = Vec::with_capacity(K);
        let mut chunk_bytes_len = 0usize;
        for i in 0..K {
            let chunk = &pod[i * buf_dim..(i + 1) * buf_dim];
            let bytes: &[u8] = bytemuck::cast_slice(chunk);
            chunk_bytes_len = bytes.len();
            storages.push(
                self.device
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some(&format!("apply_circuit_k16 state_b{i}")),
                        contents: bytes,
                        usage: wgpu::BufferUsages::STORAGE
                            | wgpu::BufferUsages::COPY_SRC
                            | wgpu::BufferUsages::COPY_DST,
                    }),
            );
            stagings.push(self.device.create_buffer(&wgpu::BufferDescriptor {
                label: Some(&format!("apply_circuit_k16 staging_b{i}")),
                size: bytes.len() as u64,
                usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            }));
        }

        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());

        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    let total_pairs = (dim / 2) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total_pairs.div_ceil(64));
                    let uniforms = SingleQubitK16Uniforms {
                        qubit_stride: stride,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_kn(
                        &self.single_qubit_k16.bgl,
                        &storages,
                        &ubuf,
                        K,
                        "k16 bg",
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitK16Uniforms {
                        bit0,
                        bit1,
                        n_amplitudes: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        _pad4: 0,
                        _pad5: 0,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_kn(
                        &self.two_qubit_k16.bgl,
                        &storages,
                        &ubuf,
                        K,
                        "k16 bg",
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨 (n_qubits={n_qubits})"
                        )));
                    }
                    let total = dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = Controlled1qK16Uniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_kn(
                        &self.controlled_1q_k16.bgl,
                        &storages,
                        &ubuf,
                        K,
                        "k16 bg",
                    );
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit_k16 encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.single_qubit_k16,
                1 => &self.two_qubit_k16,
                _ => &self.controlled_1q_k16,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit_k16 op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        for i in 0..K {
            encoder.copy_buffer_to_buffer(&storages[i], 0, &stagings[i], 0, chunk_bytes_len as u64);
        }
        self.queue.submit(Some(encoder.finish()));

        let slices: Vec<wgpu::BufferSlice> = stagings.iter().map(|b| b.slice(..)).collect();
        let receivers: Vec<_> = slices
            .iter()
            .map(|s| {
                let (sender, receiver) = std::sync::mpsc::channel();
                s.map_async(wgpu::MapMode::Read, move |r| {
                    sender.send(r).ok();
                });
                receiver
            })
            .collect();
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        for (i, r) in receivers.into_iter().enumerate() {
            r.recv()
                .map_err(|e| GpuError::Buffer(format!("recv map b{i}: {e:?}")))?
                .map_err(|e| GpuError::Buffer(format!("map_async b{i}: {e:?}")))?;
        }
        let datas: Vec<wgpu::BufferView> = slices.iter().map(|s| s.get_mapped_range()).collect();
        for (i, data) in datas.iter().enumerate() {
            let chunk: &[CF32] = bytemuck::cast_slice(data);
            for (dst, src) in state
                .iter_mut()
                .skip(i * buf_dim)
                .take(buf_dim)
                .zip(chunk.iter())
            {
                *dst = (*src).into();
            }
        }
        drop(datas);
        for s in &stagings {
            s.unmap();
        }
        Ok(())
    }

    /// v0.5.18: K=32 buffer-split apply_circuit path.  K=16 패턴 그대로.
    /// chunk size = 2^(n-5) × 8 byte = 1 GiB (N=32).  pipeline 가용 GPU 만
    /// (NVIDIA / AMD desktop binding ≥ 33).  caller (apply_circuit) 가 이미
    /// pipeline 가용성 확인 후 호출.
    fn apply_circuit_k32(
        &self,
        state: &mut [Complex<f32>],
        ops: &[WgpuGateOp],
        n_qubits: usize,
    ) -> Result<(), GpuError> {
        const K: usize = 32;
        let single_pl = self
            .single_qubit_k32
            .as_ref()
            .ok_or_else(|| GpuError::Unsupported("K=32 pipeline 미가용".into()))?;
        let two_pl = self
            .two_qubit_k32
            .as_ref()
            .ok_or_else(|| GpuError::Unsupported("K=32 pipeline 미가용".into()))?;
        let ctrl_pl = self
            .controlled_1q_k32
            .as_ref()
            .ok_or_else(|| GpuError::Unsupported("K=32 pipeline 미가용".into()))?;

        let dim = state.len();
        let buf_dim = dim / K;
        let offset_bits = (n_qubits - 5) as u32;
        let offset_mask = (1u32 << offset_bits).wrapping_sub(1);

        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let mut storages: Vec<wgpu::Buffer> = Vec::with_capacity(K);
        let mut stagings: Vec<wgpu::Buffer> = Vec::with_capacity(K);
        let mut chunk_bytes_len = 0usize;
        for i in 0..K {
            let chunk = &pod[i * buf_dim..(i + 1) * buf_dim];
            let bytes: &[u8] = bytemuck::cast_slice(chunk);
            chunk_bytes_len = bytes.len();
            storages.push(
                self.device
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some(&format!("apply_circuit_k32 state_b{i}")),
                        contents: bytes,
                        usage: wgpu::BufferUsages::STORAGE
                            | wgpu::BufferUsages::COPY_SRC
                            | wgpu::BufferUsages::COPY_DST,
                    }),
            );
            stagings.push(self.device.create_buffer(&wgpu::BufferDescriptor {
                label: Some(&format!("apply_circuit_k32 staging_b{i}")),
                size: bytes.len() as u64,
                usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            }));
        }

        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::with_capacity(ops.len());
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::with_capacity(ops.len());
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::with_capacity(ops.len());

        for op in ops {
            match op {
                WgpuGateOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single: target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    let total_pairs = (dim / 2) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total_pairs.div_ceil(64));
                    // v0.6.2 fix: N=32 일 때 `dim as u32` 가 0 으로 wrap 되어 shader
                    // boundary check 가 모든 thread 를 silent return 시킴 (게이트
                    // no-op).  K=32 path 만 n_amplitudes slot 의 의미를 amplitude
                    // count 가 아닌 pair_count (= dim/2 = 2^(N-1)) 로 reinterpret 해
                    // u32 안전하게 한다.  shader 도 같은 의미로 수정됨.
                    let uniforms = SingleQubitK32Uniforms {
                        qubit_stride: stride,
                        n_amplitudes: total_pairs,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg =
                        self.create_bind_group_kn(&single_pl.bgl, &storages, &ubuf, K, "k32 bg");
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((0, wg_x, wg_y));
                }
                WgpuGateOp::Two { matrix, q0, q1 } => {
                    if *q0 == *q1 || *q0 >= n_qubits || *q1 >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Two: q0={q0} q1={q1} 잘못됨"
                        )));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(n_groups.div_ceil(64));
                    let uniforms = TwoQubitK32Uniforms {
                        bit0,
                        bit1,
                        n_amplitudes: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        _pad2: 0,
                        _pad3: 0,
                        _pad4: 0,
                        _pad5: 0,
                        m: m_flat,
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_kn(&two_pl.bgl, &storages, &ubuf, K, "k32 bg");
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuGateOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl == *tgt || *ctrl >= n_qubits || *tgt >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q: ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    // v0.6.2: K=32 controlled_1q shader 는 amplitude index 전체
                    // ([0, dim)) 를 work-unit 으로 사용한다.  N=32 (dim=2^32) 에서
                    // `dim as u32` 가 0 wrap → 모든 thread silent return.  shader
                    // re-design (work-unit 을 valid pair 단위로) 은 후속 PR 에서
                    // 별도 처리 — 우선 silent corruption 방지를 위해 명시 reject.
                    if n_qubits >= 32 {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q gate on N={n_qubits} (K=32 path) 는 \
                             v0.6.2 에서 미지원 — N≤31 까지 사용하거나 transpile \
                             로 single-qubit + Z 분해 후 실행하세요. 자세한 내용은 \
                             docs/v0.6.2-postmortem.md 참고."
                        )));
                    }
                    let total = dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let uniforms = Controlled1qK32Uniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        n_amplitudes: dim as u32,
                        offset_bits,
                        offset_mask,
                        dispatches_x,
                        _pad0: 0,
                        _pad1: 0,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let ubuf = self.create_uniform_buffer(bytemuck::bytes_of(&uniforms));
                    let bg = self.create_bind_group_kn(&ctrl_pl.bgl, &storages, &ubuf, K, "k32 bg");
                    owned_bufs.push(ubuf);
                    owned_bgs.push(bg);
                    dispatches.push((2, wg_x, wg_y));
                }
            }
        }

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("apply_circuit_k32 encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => single_pl,
                1 => two_pl,
                _ => ctrl_pl,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("apply_circuit_k32 op"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        for i in 0..K {
            encoder.copy_buffer_to_buffer(&storages[i], 0, &stagings[i], 0, chunk_bytes_len as u64);
        }
        self.queue.submit(Some(encoder.finish()));

        let slices: Vec<wgpu::BufferSlice> = stagings.iter().map(|b| b.slice(..)).collect();
        let receivers: Vec<_> = slices
            .iter()
            .map(|s| {
                let (sender, receiver) = std::sync::mpsc::channel();
                s.map_async(wgpu::MapMode::Read, move |r| {
                    sender.send(r).ok();
                });
                receiver
            })
            .collect();
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        for (i, r) in receivers.into_iter().enumerate() {
            r.recv()
                .map_err(|e| GpuError::Buffer(format!("recv map b{i}: {e:?}")))?
                .map_err(|e| GpuError::Buffer(format!("map_async b{i}: {e:?}")))?;
        }
        let datas: Vec<wgpu::BufferView> = slices.iter().map(|s| s.get_mapped_range()).collect();
        for (i, data) in datas.iter().enumerate() {
            let chunk: &[CF32] = bytemuck::cast_slice(data);
            for (dst, src) in state
                .iter_mut()
                .skip(i * buf_dim)
                .take(buf_dim)
                .zip(chunk.iter())
            {
                *dst = (*src).into();
            }
        }
        drop(datas);
        for s in &stagings {
            s.unmap();
        }
        Ok(())
    }

    fn create_uniform_buffer(&self, bytes: &[u8]) -> wgpu::Buffer {
        self.device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("uniform"),
                contents: bytes,
                usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
            })
    }

    fn create_bind_group(
        &self,
        layout: &wgpu::BindGroupLayout,
        storage: &wgpu::Buffer,
        uniform: &wgpu::Buffer,
    ) -> wgpu::BindGroup {
        self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("bg"),
            layout,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: storage.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: uniform.as_entire_binding(),
                },
            ],
        })
    }

    /// 한 pipeline 을 `state` 에 dispatch.  buffer upload + run + download.
    /// `workgroups` = (wg_x, wg_y) — 2D dispatch (Y=1 이면 사실상 1D).
    fn dispatch_one(
        &self,
        pl: &Pipeline,
        state: &mut [Complex<f32>],
        uniform_bytes: &[u8],
        workgroups: (u32, u32),
        label: &str,
    ) -> Result<(), GpuError> {
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let state_bytes: &[u8] = bytemuck::cast_slice(&pod);

        let storage = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some(&format!("{label} state")),
                contents: state_bytes,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some(&format!("{label} staging")),
            size: state_bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let uniform_buf = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some(&format!("{label} uniforms")),
                contents: uniform_bytes,
                usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
            });
        let bind_group = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some(&format!("{label} bg")),
            layout: &pl.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: storage.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: uniform_buf.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some(&format!("{label} encoder")),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some(&format!("{label} pass")),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &bind_group, &[]);
            pass.dispatch_workgroups(workgroups.0, workgroups.1, 1);
        }
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, state_bytes.len() as u64);
        self.queue.submit(Some(encoder.finish()));

        let buffer_slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        buffer_slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        self.device
            .poll(wgpu::PollType::wait_indefinitely())
            .map_err(|e| GpuError::Buffer(format!("device poll: {e:?}")))?;
        receiver
            .recv()
            .map_err(|e| GpuError::Buffer(format!("recv map: {e:?}")))?
            .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;
        let data = buffer_slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        for (dst, src) in state.iter_mut().zip(result.iter()) {
            *dst = (*src).into();
        }
        drop(data);
        staging.unmap();
        Ok(())
    }
}

fn check_state_len(state: &[Complex<f32>]) -> Result<usize, GpuError> {
    let n = state.len();
    if !n.is_power_of_two() || n < 2 {
        return Err(GpuError::Unsupported(format!(
            "state.len() = {n} 는 2^k (k≥1) 이어야 함"
        )));
    }
    Ok(n)
}

/// log2(n) for power-of-two n.  qubit 수.
#[inline]
fn bits_for_n(n: usize) -> usize {
    n.trailing_zeros() as usize
}

fn build_pipeline(device: &wgpu::Device, name: &str, src: &str) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &[
            wgpu::BindGroupLayoutEntry {
                binding: 0,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: false },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            wgpu::BindGroupLayoutEntry {
                binding: 1,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Uniform,
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
        ],
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

/// v0.5.17: generic K-buffer pipeline 빌더.  storage_count storage binding +
/// 1 uniform.  K=16 (storage_count=16) 부터 사용.  K=2/4/8 도 같은 헬퍼로
/// 단순화 가능하지만 회귀 risk 회피 위해 기존 build_pipeline_k2/4/8 유지.
fn build_pipeline_kn(
    device: &wgpu::Device,
    name: &str,
    src: &str,
    storage_count: usize,
) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let mut entries = Vec::with_capacity(storage_count + 1);
    for binding in 0..storage_count {
        entries.push(wgpu::BindGroupLayoutEntry {
            binding: binding as u32,
            visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: false },
                has_dynamic_offset: false,
                min_binding_size: None,
            },
            count: None,
        });
    }
    entries.push(wgpu::BindGroupLayoutEntry {
        binding: storage_count as u32,
        visibility: wgpu::ShaderStages::COMPUTE,
        ty: wgpu::BindingType::Buffer {
            ty: wgpu::BufferBindingType::Uniform,
            has_dynamic_offset: false,
            min_binding_size: None,
        },
        count: None,
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &entries,
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

/// v0.5.7: K=8 pipeline 빌더 — 8 storage + 1 uniform binding.
///
/// **Driver 한계**: Vulkan 1.0 minimum `maxPerStageDescriptorStorageBuffers`
/// 가 4 라 일부 구형 device 에서 fail 가능.  현대 GPU (NVIDIA / AMD / Apple
/// Silicon / Intel Arc / lavapipe Mesa 26+) 모두 ≥ 8 — N=32 사용 시점에서
/// 그런 GPU 는 어차피 VRAM 부족이라 실용 영향 0.
fn build_pipeline_k8(device: &wgpu::Device, name: &str, src: &str) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let mut entries = Vec::with_capacity(9);
    for binding in 0..8 {
        entries.push(wgpu::BindGroupLayoutEntry {
            binding,
            visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: false },
                has_dynamic_offset: false,
                min_binding_size: None,
            },
            count: None,
        });
    }
    entries.push(wgpu::BindGroupLayoutEntry {
        binding: 8,
        visibility: wgpu::ShaderStages::COMPUTE,
        ty: wgpu::BindingType::Buffer {
            ty: wgpu::BufferBindingType::Uniform,
            has_dynamic_offset: false,
            min_binding_size: None,
        },
        count: None,
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &entries,
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

/// v0.5.6: K=4 pipeline 빌더 — 4 storage + 1 uniform binding.
/// v0.5.13: norm reduction pipeline 빌더.
/// binding 0 = state (read), binding 1 = partial sums (read_write), binding 2 = uniform.
fn build_pipeline_norm_reduction(device: &wgpu::Device, name: &str, src: &str) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &[
            wgpu::BindGroupLayoutEntry {
                binding: 0,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: true },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            wgpu::BindGroupLayoutEntry {
                binding: 1,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: false },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            wgpu::BindGroupLayoutEntry {
                binding: 2,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Uniform,
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
        ],
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

fn build_pipeline_k4(device: &wgpu::Device, name: &str, src: &str) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let mut entries = Vec::with_capacity(5);
    for binding in 0..4 {
        entries.push(wgpu::BindGroupLayoutEntry {
            binding,
            visibility: wgpu::ShaderStages::COMPUTE,
            ty: wgpu::BindingType::Buffer {
                ty: wgpu::BufferBindingType::Storage { read_only: false },
                has_dynamic_offset: false,
                min_binding_size: None,
            },
            count: None,
        });
    }
    entries.push(wgpu::BindGroupLayoutEntry {
        binding: 4,
        visibility: wgpu::ShaderStages::COMPUTE,
        ty: wgpu::BindingType::Buffer {
            ty: wgpu::BufferBindingType::Uniform,
            has_dynamic_offset: false,
            min_binding_size: None,
        },
        count: None,
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &entries,
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

/// v0.5.5: K=2 pipeline 빌더 — 2 storage buffer (state_lo / state_hi) + 1 uniform.
/// statevector 의 N≥28 buffer-split path 전용.
fn build_pipeline_k2(device: &wgpu::Device, name: &str, src: &str) -> Pipeline {
    let module = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some(&format!("{name} shader")),
        source: wgpu::ShaderSource::Wgsl(src.into()),
    });
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some(&format!("{name} bgl")),
        entries: &[
            // binding 0: state_lo
            wgpu::BindGroupLayoutEntry {
                binding: 0,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: false },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            // binding 1: state_hi
            wgpu::BindGroupLayoutEntry {
                binding: 1,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: false },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            // binding 2: uniform
            wgpu::BindGroupLayoutEntry {
                binding: 2,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Uniform,
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
        ],
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some(&format!("{name} pl")),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some(&format!("{name} pipeline")),
        layout: Some(&layout),
        module: &module,
        entry_point: Some("main"),
        compilation_options: Default::default(),
        cache: None,
    });
    Pipeline { pipeline, bgl }
}

/// v0.5.5~v0.5.18: N 따라 buffer split factor K 결정.
///
/// chunk size = 2^N × 8 / K ≤ 2 GiB - 4 (wgpu binding cap).
///
/// | N         | sv 크기 | K  | chunk 크기 | binding | 비고 |
/// |-----------|---------|-----|-----------|---------|------|
/// | N≤27      | ≤1 GiB  | 1  | ≤1 GiB    | 2       | 단일 buffer |
/// | N=28      | 2 GiB   | 2  | 1 GiB     | 3       | v0.5.5 |
/// | N=29      | 4 GiB   | 4  | 1 GiB     | 5       | v0.5.6/16 |
/// | N=30      | 8 GiB   | 8  | 1 GiB     | 9       | v0.5.7/16 |
/// | N=31      | 16 GiB  | 16 | 1 GiB     | 17      | v0.5.17 |
/// | N=32      | 32 GiB  | 32 | 1 GiB     | 33      | v0.5.18 (NVIDIA / AMD desktop only — Apple Metal 31 / Intel Arc 16 fail) |
#[inline]
fn compute_split_factor(n_qubits: usize) -> usize {
    if n_qubits <= 27 {
        1
    } else if n_qubits == 28 {
        2
    } else if n_qubits == 29 {
        4
    } else if n_qubits == 30 {
        8
    } else if n_qubits == 31 {
        16
    } else {
        // N=32 → K=32.  N>32 는 32 GiB+ 라 single-GPU wgpu Tier-1 영역 밖.
        32
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_complex::Complex;

    fn approx(a: Complex<f32>, b: Complex<f32>, eps: f32) -> bool {
        (a - b).norm() < eps
    }

    fn make_backend() -> Option<WgpuStatevectorBackend> {
        match WgpuStatevectorBackend::new() {
            Ok(b) => Some(b),
            Err(GpuError::NoAdapter) => None,
            Err(e) => panic!("backend init failed: {e}"),
        }
    }

    fn x() -> [[Complex<f32>; 2]; 2] {
        [
            [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
        ]
    }

    #[test]
    fn gpu_2q_kraus_trajectory_matches_dense() {
        let Some(b) = make_backend() else { return };
        let c = |re: f32, im: f32| Complex::new(re, im);
        let n = 3usize;
        let dim = 1usize << n;
        // 임의 정규화 상태.
        let mut psi: Vec<Complex<f32>> = (0..dim)
            .map(|i| c((i as f32 * 0.31).cos(), (i as f32 * 0.17).sin()))
            .collect();
        let nrm: f32 = psi.iter().map(|a| a.norm_sqr()).sum::<f32>().sqrt();
        for a in psi.iter_mut() {
            *a = Complex::new(a.re / nrm, a.im / nrm);
        }
        let (q0, q1) = (0usize, 1usize);
        let diag4 = |vals: [f32; 4]| {
            let mut m = [[c(0.0, 0.0); 4]; 4];
            for (i, row) in m.iter_mut().enumerate() {
                row[i] = c(vals[i], 0.0);
            }
            m
        };

        // (1) 비유니터리 4×4 적용 정확성: damping-류 K = diag(1, 0.6, 0.8, 0.5).
        let kd = diag4([1.0, 0.6, 0.8, 0.5]);
        let mut gpu_kd = psi.clone();
        b.apply_two_qubit_gate(&mut gpu_kd, &kd, q0, q1).unwrap();
        // dense 참조: index 의 (bit q1, bit q0) → diag 인덱스 2·bit(q1)+bit(q0).
        for (a, &amp) in psi.iter().enumerate() {
            let d = 2 * ((a >> q1) & 1) + ((a >> q0) & 1);
            let diag = [1.0_f32, 0.6, 0.8, 0.5][d];
            assert!(
                approx(gpu_kd[a], Complex::new(amp.re * diag, amp.im * diag), 1e-5),
                "비유니터리 4×4 적용 불일치 idx={a}"
            );
        }

        // (2) trajectory: 상관 dephasing {√(1-p)·I⊗I, √p·Z⊗Z}, p=0.3.
        let p = 0.3_f32;
        let s0 = (1.0 - p).sqrt();
        let s1 = p.sqrt();
        // Z⊗Z = diag(+,-,-,+) (index 2·q1+q0 → (-1)^(q0+q1)), ×s1.
        let kraus = [diag4([s0, s0, s0, s0]), diag4([s1, -s1, -s1, s1])];

        // u=0 → I 분기 → 상태 불변.
        let mut su0 = psi.clone();
        b.apply_kraus_2q_trajectory(&mut su0, &kraus, q0, q1, 0.0)
            .unwrap();
        for (a, &amp) in psi.iter().enumerate() {
            assert!(approx(su0[a], amp, 1e-5), "u=0 (I 분기) 불일치 idx={a}");
        }

        // u=0.99 → Z⊗Z 분기 → ZZ 적용 상태.
        let mut su1 = psi.clone();
        b.apply_kraus_2q_trajectory(&mut su1, &kraus, q0, q1, 0.99)
            .unwrap();
        for (a, &amp) in psi.iter().enumerate() {
            let sign = if (((a >> q0) & 1) + ((a >> q1) & 1)) % 2 == 1 {
                -1.0
            } else {
                1.0
            };
            assert!(
                approx(su1[a], Complex::new(amp.re * sign, amp.im * sign), 1e-5),
                "u→1 (ZZ 분기) 불일치 idx={a}"
            );
        }
    }
    fn h() -> [[Complex<f32>; 2]; 2] {
        let s = 1.0_f32 / 2.0_f32.sqrt();
        [
            [Complex::new(s, 0.0), Complex::new(s, 0.0)],
            [Complex::new(s, 0.0), Complex::new(-s, 0.0)],
        ]
    }

    #[test]
    fn x_gate_flips_qubit_zero() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![Complex::new(1.0_f32, 0.0), Complex::new(0.0, 0.0)];
        b.apply_single_qubit_gate(&mut s, &x(), 0).unwrap();
        assert!(approx(s[0], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(s[1], Complex::new(1.0, 0.0), 1e-6));
    }

    /// v0.6.10: GPU-resident apply_ops_to_buffer + download round-trip.
    /// |00⟩ 에 X(q0) → |01⟩ (index 1).
    #[test]
    fn resident_apply_x_and_download() {
        let Some(b) = make_backend() else { return };
        let dim = 4usize;
        let buf = b.create_zero_state_buffer(dim);
        b.apply_ops_to_buffer(
            &buf,
            &[WgpuGateOp::Single {
                matrix: x(),
                target: 0,
            }],
            dim,
        )
        .unwrap();
        let sv = b.download_state_buffer(&buf, dim).unwrap();
        assert!(approx(sv[1], Complex::new(1.0, 0.0), 1e-6));
        assert!(approx(sv[0], Complex::new(0.0, 0.0), 1e-6));
        // q0 = 1 이 확정이므로 measure_qubit_gpu 는 uniform 무관하게 outcome 1.
        let outcome = b.measure_qubit_gpu(&buf, dim, 0, 0.01).unwrap();
        assert_eq!(outcome, 1);
    }

    /// v0.6.10: GPU-resident Bell state — measure q0 / q1 outcome 이 항상 일치.
    #[test]
    fn resident_bell_measurements_correlated() {
        let Some(b) = make_backend() else { return };
        let dim = 4usize;
        for &u in &[0.1f32, 0.9] {
            let buf = b.create_zero_state_buffer(dim);
            b.apply_ops_to_buffer(
                &buf,
                &[
                    WgpuGateOp::Single {
                        matrix: h(),
                        target: 0,
                    },
                    WgpuGateOp::Controlled1q {
                        matrix: x(),
                        ctrl: 0,
                        tgt: 1,
                    },
                ],
                dim,
            )
            .unwrap();
            let o0 = b.measure_qubit_gpu(&buf, dim, 0, u).unwrap();
            // q0 측정 후 q1 은 q0 와 같은 값으로 확정 — uniform 무관.
            let o1 = b.measure_qubit_gpu(&buf, dim, 1, 0.5).unwrap();
            assert_eq!(o0, o1, "Bell correlation broken (u={u})");
        }
    }

    /// v0.6.10: GPU Philox uniform 이 CPU 레퍼런스와 bit-exact (GPU 환경에서만).
    #[test]
    fn philox_gpu_matches_cpu_reference() {
        let Some(b) = make_backend() else { return };
        for &(seed, count) in &[(0u64, 17usize), (0xdeadbeef, 256), (42, 1000)] {
            let gpu = b.generate_uniforms(seed, count).unwrap();
            let cpu = crate::philox::philox_uniforms_cpu(seed, count);
            assert_eq!(gpu.len(), cpu.len());
            for (i, (g, c)) in gpu.iter().zip(cpu.iter()).enumerate() {
                assert_eq!(
                    g.to_bits(),
                    c.to_bits(),
                    "philox GPU≠CPU at {i} (seed={seed}, count={count}): {g} vs {c}"
                );
            }
        }
    }

    #[test]
    fn h_gate_creates_superposition() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![Complex::new(1.0_f32, 0.0), Complex::new(0.0, 0.0)];
        b.apply_single_qubit_gate(&mut s, &h(), 0).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[1], Complex::new(inv, 0.0), 1e-6));
    }

    #[test]
    fn x_on_qubit_one_of_two() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![
            Complex::new(1.0_f32, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        b.apply_single_qubit_gate(&mut s, &x(), 1).unwrap();
        assert!(approx(s[2], Complex::new(1.0, 0.0), 1e-6));
        assert!(approx(s[0], Complex::new(0.0, 0.0), 1e-6));
    }

    /// v0.5.2: 2D dispatch chunking 검증.  N=22 (workgroup count = 32768 — single
    /// pass 에서 65535 미만이지만 dispatch_2d 헬퍼가 동작해야).  N=23 (workgroup
    /// count = 65536, 65535 초과) 가 진짜 chunking 검증.  software lavapipe 는
    /// 매우 느려 N=23 까지만.
    #[test]
    fn dispatch_chunking_n22() {
        let Some(b) = make_backend() else { return };
        // |0..0⟩ → H q0 → 0.5 (norm² check).
        let n = 22usize;
        let dim = 1usize << n;
        let mut s = vec![Complex::new(0.0_f32, 0.0); dim];
        s[0] = Complex::new(1.0, 0.0);
        b.apply_single_qubit_gate(&mut s, &h(), 0).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s[1], Complex::new(inv, 0.0), 1e-5));
        // 나머지 0.
        for amp in s.iter().take(8).skip(2) {
            assert!(approx(*amp, Complex::new(0.0, 0.0), 1e-5));
        }
    }

    #[test]
    fn dispatch_chunking_n23_above_65535() {
        let Some(b) = make_backend() else { return };
        // N=23: pairs = 2^22 = 4194304, /64 = 65536 workgroups (65535 + 1).
        // 2D chunking 없으면 실패해야 — chunking 으로 통과.
        let n = 23usize;
        let dim = 1usize << n;
        let mut s = vec![Complex::new(0.0_f32, 0.0); dim];
        s[0] = Complex::new(1.0, 0.0);
        b.apply_single_qubit_gate(&mut s, &h(), 0).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s[1], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn h_on_4_qubit_uniform() {
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        let mut s = vec![Complex::new(0.0_f32, 0.0); n];
        s[0] = Complex::new(1.0, 0.0);
        for q in 0..4 {
            b.apply_single_qubit_gate(&mut s, &h(), q).unwrap();
        }
        for amp in &s {
            assert!((amp.re - 0.25).abs() < 1e-5);
        }
    }

    /// CNOT via apply_controlled_1q: |10⟩ → |11⟩.
    #[test]
    fn cnot_via_controlled_1q() {
        let Some(b) = make_backend() else { return };
        // |00⟩ → X q1 → |10⟩ (index 2)
        let mut s = vec![
            Complex::new(0.0_f32, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        // CNOT(ctrl=q1, tgt=q0): q1=1 fires X on q0 → |10⟩=2 → |11⟩=3.
        b.apply_controlled_1q(&mut s, &x(), 1, 0).unwrap();
        assert!(approx(s[3], Complex::new(1.0, 0.0), 1e-6));
        assert!(approx(s[2], Complex::new(0.0, 0.0), 1e-6));
    }

    #[test]
    fn cnot_no_op_when_control_zero() {
        let Some(b) = make_backend() else { return };
        // |01⟩ (q0=1, q1=0) — ctrl=q1=0 → no op.
        let mut s = vec![
            Complex::new(0.0_f32, 0.0),
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        b.apply_controlled_1q(&mut s, &x(), 1, 0).unwrap();
        assert!(approx(s[1], Complex::new(1.0, 0.0), 1e-6));
    }

    /// SWAP via apply_two_qubit_gate: |01⟩ → |10⟩.
    #[test]
    fn swap_via_two_qubit() {
        let Some(b) = make_backend() else { return };
        let z = Complex::new(0.0_f32, 0.0);
        let o = Complex::new(1.0_f32, 0.0);
        let swap: [[Complex<f32>; 4]; 4] = [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]];
        let mut s = vec![z, o, z, z]; // |01⟩
        b.apply_two_qubit_gate(&mut s, &swap, 0, 1).unwrap();
        assert!(approx(s[2], o, 1e-6));
        assert!(approx(s[1], z, 1e-6));
    }

    /// CZ via apply_two_qubit_gate: |11⟩ → -|11⟩.
    #[test]
    fn cz_via_two_qubit() {
        let Some(b) = make_backend() else { return };
        let z = Complex::new(0.0_f32, 0.0);
        let o = Complex::new(1.0_f32, 0.0);
        let neg = Complex::new(-1.0_f32, 0.0);
        let cz: [[Complex<f32>; 4]; 4] = [[o, z, z, z], [z, o, z, z], [z, z, o, z], [z, z, z, neg]];
        let mut s = vec![z, z, z, o]; // |11⟩
        b.apply_two_qubit_gate(&mut s, &cz, 0, 1).unwrap();
        assert!(approx(s[3], neg, 1e-6));
    }

    /// apply_circuit: Bell state via batched ops.
    #[test]
    fn apply_circuit_bell_state() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![
            Complex::new(1.0_f32, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
        ];
        b.apply_circuit(&mut s, &ops).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[3], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[1], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(s[2], Complex::new(0.0, 0.0), 1e-6));
    }

    /// apply_circuit: GHZ-3 (H q0 + CX(0,1) + CX(0,2)) batched.
    #[test]
    fn apply_circuit_ghz3() {
        let Some(b) = make_backend() else { return };
        let n = 8;
        let mut s = vec![Complex::new(0.0_f32, 0.0); n];
        s[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2,
            },
        ];
        b.apply_circuit(&mut s, &ops).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        // GHZ: index 0 (|000⟩) and 7 (|111⟩) = inv, 나머지 0.
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[7], Complex::new(inv, 0.0), 1e-6));
        for amp in s.iter().take(7).skip(1) {
            assert!(approx(*amp, Complex::new(0.0, 0.0), 1e-6));
        }
    }

    /// apply_circuit: empty ops 는 state 그대로.
    #[test]
    fn apply_circuit_empty_noop() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![Complex::new(0.5_f32, 0.5), Complex::new(-0.5, 0.5)];
        let before = s.clone();
        b.apply_circuit(&mut s, &[]).unwrap();
        for (a, c) in s.iter().zip(before.iter()) {
            assert!((a.re - c.re).abs() < 1e-6 && (a.im - c.im).abs() < 1e-6);
        }
    }

    /// Bell |00⟩ → H q0 → CX(q0, q1).  H on q0 + controlled-X(ctrl=q0, tgt=q1).
    #[test]
    fn bell_state_via_h_and_cnot() {
        let Some(b) = make_backend() else { return };
        let mut s = vec![
            Complex::new(1.0_f32, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        b.apply_single_qubit_gate(&mut s, &h(), 0).unwrap();
        b.apply_controlled_1q(&mut s, &x(), 0, 1).unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s[0], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[3], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s[1], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(s[2], Complex::new(0.0, 0.0), 1e-6));
    }

    // =====================================================================
    // v0.5.5: K=2 buffer-split path tests
    //
    // sandbox 의 RAM 한계로 N=28 (sv 2 GB × 2 buffer = 4 GB) 직접 테스트는 어려워
    // small-N 에서 apply_circuit_k2 직접 호출로 path 검증 — N=4 GHZ + cross-buffer
    // gate (target = N-1) + same-buffer gate 모두 거치는 회로.
    // =====================================================================

    #[test]
    fn k2_compute_split_factor_thresholds() {
        // v0.5.18: N=32 → K=32 추가.  N≥33 은 single-GPU wgpu Tier-1 영역 밖.
        assert_eq!(super::compute_split_factor(20), 1);
        assert_eq!(super::compute_split_factor(27), 1);
        assert_eq!(super::compute_split_factor(28), 2);
        assert_eq!(super::compute_split_factor(29), 4);
        assert_eq!(super::compute_split_factor(30), 8);
        assert_eq!(super::compute_split_factor(31), 16);
        assert_eq!(super::compute_split_factor(32), 32);
    }

    #[test]
    fn k32_pipeline_availability() {
        // sandbox lavapipe (Mesa) 의 max_storage_buffers_per_shader_stage = 16 →
        // K=32 pipeline = None.  사용자 NVIDIA / AMD desktop (binding ≥ 33) 에서만 Some.
        let Some(b) = make_backend() else { return };
        let limit = b.device.limits().max_storage_buffers_per_shader_stage;
        if limit >= 33 {
            assert!(b.single_qubit_k32.is_some());
            assert!(b.two_qubit_k32.is_some());
            assert!(b.controlled_1q_k32.is_some());
        } else {
            assert!(b.single_qubit_k32.is_none());
            assert!(b.two_qubit_k32.is_none());
            assert!(b.controlled_1q_k32.is_none());
        }
    }

    // =====================================================================
    // v0.5.17: K=16 buffer-split path tests.
    // sandbox RAM 한계로 N=31 (sv 16 GB) 직접 검증 어려워 small-N 강제 K=16.
    // N=4 (16 amp / 16 buffer × 1 amp each) 가 K=16 의 minimum.
    // =====================================================================

    #[test]
    fn k16_force_n4_ghz_matches_k1() {
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        let mut s_k16 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k16[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 3,
            },
        ];
        b.apply_circuit_k16(&mut s_k16, &ops, 4).unwrap();

        let mut s_k1 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k1[0] = Complex::new(1.0, 0.0);
        b.apply_circuit(&mut s_k1, &ops).unwrap();

        for i in 0..n {
            let diff = (s_k16[i] - s_k1[i]).norm();
            assert!(diff < 1e-6, "K=16 vs K=1 mismatch at i={i}");
        }
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k16[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s_k16[15], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn k16_force_n5_target_each_position() {
        // N=5 (32 amp / 16 buffer × 2 amp each).  H q_t for t ∈ {0..4}.
        let Some(b) = make_backend() else { return };
        let n = 32usize;
        for &target in &[0_usize, 1, 2, 3, 4] {
            let mut s_k16 = vec![Complex::new(0.0_f32, 0.0); n];
            s_k16[0] = Complex::new(1.0, 0.0);
            b.apply_circuit_k16(
                &mut s_k16,
                &[WgpuGateOp::Single {
                    matrix: h(),
                    target,
                }],
                5,
            )
            .unwrap();
            let inv = 1.0_f32 / 2.0_f32.sqrt();
            assert!(
                approx(s_k16[0], Complex::new(inv, 0.0), 1e-6),
                "target={target}"
            );
            assert!(
                approx(s_k16[1 << target], Complex::new(inv, 0.0), 1e-6),
                "target={target}"
            );
        }
    }

    #[test]
    fn k2_force_n4_ghz_matches_k1() {
        // K=2 path 를 직접 호출 (compute_split_factor 우회).  N=4 GHZ 회로 결과가
        // K=1 (apply_circuit) 와 element-wise 1e-6 일치하는지.
        let Some(b) = make_backend() else { return };
        let n = 16usize; // 2^4
        let mut s_k2 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k2[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 3, // tgt == split_bit (N-1=3) — cross-buffer path
            },
        ];
        b.apply_circuit_k2(&mut s_k2, &ops, 4).unwrap();

        // K=1 reference.
        let mut s_k1 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k1[0] = Complex::new(1.0, 0.0);
        b.apply_circuit(&mut s_k1, &ops).unwrap();

        for i in 0..n {
            let diff = (s_k2[i] - s_k1[i]).norm();
            assert!(
                diff < 1e-6,
                "K=2 vs K=1 mismatch at i={i}: k2={:?} k1={:?}",
                s_k2[i],
                s_k1[i]
            );
        }

        // GHZ-4 analytic: |0000⟩ + |1111⟩ 둘 다 1/√2.
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k2[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s_k2[15], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn k2_force_n4_target_split_bit() {
        // Single qubit gate 가 split_bit (= N-1 = 3) 인 경우 cross-buffer path.
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        // |0000⟩ → H q3 → (|0000⟩ + |1000⟩) / √2
        let mut s_k2 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k2[0] = Complex::new(1.0, 0.0);
        b.apply_circuit_k2(
            &mut s_k2,
            &[WgpuGateOp::Single {
                matrix: h(),
                target: 3,
            }],
            4,
        )
        .unwrap();
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k2[0], Complex::new(inv, 0.0), 1e-6));
        assert!(approx(s_k2[8], Complex::new(inv, 0.0), 1e-6));
        for amp in s_k2.iter().take(8).skip(1) {
            assert!(approx(*amp, Complex::new(0.0, 0.0), 1e-6));
        }
    }

    // =====================================================================
    // v0.5.6: K=4 buffer-split path tests (small-N force).
    // sandbox 의 RAM 한계로 N=30 (sv 4 GB × 4 = 16 GB) 직접 테스트는 어려워
    // small-N 에서 apply_circuit_k4 직접 호출로 path 검증.  N=4 (16 amplitude,
    // 4 buffer × 4 amp each) 가 K=4 의 minimum scale.
    // =====================================================================

    #[test]
    fn k4_force_n4_ghz_matches_k1() {
        let Some(b) = make_backend() else { return };
        let n = 16usize; // 2^4
        let mut s_k4 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k4[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2, // == split bit 1 (N-2=2) — cross-buffer
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 3, // == split bit 0 (N-1=3) — cross-buffer
            },
        ];
        b.apply_circuit_k4(&mut s_k4, &ops, 4).unwrap();

        // K=1 reference (apply_circuit 의 K=1 path 강제 호출).
        let mut s_k1 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k1[0] = Complex::new(1.0, 0.0);
        // apply_circuit 의 entry 분기를 우회하려면 직접 호출 — 그러나 N=4 면
        // compute_split_factor=1 이라 자동으로 K=1 path.
        b.apply_circuit(&mut s_k1, &ops).unwrap();

        for i in 0..n {
            let diff = (s_k4[i] - s_k1[i]).norm();
            assert!(
                diff < 1e-6,
                "K=4 vs K=1 mismatch at i={i}: k4={:?} k1={:?}",
                s_k4[i],
                s_k1[i]
            );
        }

        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k4[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s_k4[15], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn k4_force_n4_target_each_split_bit() {
        // Single qubit gate 가 split bit 0 (=N-1=3) / split bit 1 (=N-2=2) /
        // 그 외 (target=0) 각각 cross / cross / same — generic switch path.
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        for &target in &[0_usize, 1, 2, 3] {
            let mut s_k4 = vec![Complex::new(0.0_f32, 0.0); n];
            s_k4[0] = Complex::new(1.0, 0.0);
            b.apply_circuit_k4(
                &mut s_k4,
                &[WgpuGateOp::Single {
                    matrix: h(),
                    target,
                }],
                4,
            )
            .unwrap();
            // H q_t 적용 후 |0⟩ + |2^target⟩ / √2.
            let inv = 1.0_f32 / 2.0_f32.sqrt();
            assert!(
                approx(s_k4[0], Complex::new(inv, 0.0), 1e-6),
                "target={target} amp[0] wrong: {:?}",
                s_k4[0]
            );
            assert!(
                approx(s_k4[1 << target], Complex::new(inv, 0.0), 1e-6),
                "target={target} amp[{}] wrong: {:?}",
                1 << target,
                s_k4[1 << target]
            );
        }
    }

    #[test]
    fn k4_force_n5_two_qubit_cross_split_bits() {
        // N=5 (32 amplitude, K=4 buffer 8 amp each).  CZ(q0, q4) 의 q1=split 0
        // (cross top bit) — 4-amplitude block 의 q1=0/q1=1 두 쌍이 다른 buffer.
        let Some(b) = make_backend() else { return };
        let n = 32usize;
        let mut s_k4 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k4[17] = Complex::new(1.0, 0.0); // index 17 = 0b10001: q0=1, q4=1
        let z = Complex::new(0.0_f32, 0.0);
        let o = Complex::new(1.0_f32, 0.0);
        let neg = Complex::new(-1.0_f32, 0.0);
        let cz = [[o, z, z, z], [z, o, z, z], [z, z, o, z], [z, z, z, neg]];
        b.apply_circuit_k4(
            &mut s_k4,
            &[WgpuGateOp::Two {
                matrix: cz,
                q0: 0,
                q1: 4,
            }],
            5,
        )
        .unwrap();
        assert!(approx(s_k4[17], neg, 1e-6));
    }

    // =====================================================================
    // v0.5.7: K=8 buffer-split path tests (small-N force).
    // sandbox 의 RAM 한계로 N=32 (sv 32 GB) 직접 테스트는 어려워 small-N 에서
    // apply_circuit_k8 직접 호출.  N=4 (16 amp, K=8 → 2 amp per buffer)
    // 가 K=8 의 minimum scale.
    // =====================================================================

    #[test]
    fn k8_force_n4_ghz_matches_k1() {
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        let mut s_k8 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k8[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1, // == split bit 2 (N-3=1) — cross-buffer
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2, // == split bit 1 (N-2=2) — cross-buffer
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 3, // == split bit 0 (N-1=3) — cross-buffer
            },
        ];
        b.apply_circuit_k8(&mut s_k8, &ops, 4).unwrap();

        let mut s_k1 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k1[0] = Complex::new(1.0, 0.0);
        b.apply_circuit(&mut s_k1, &ops).unwrap();

        for i in 0..n {
            let diff = (s_k8[i] - s_k1[i]).norm();
            assert!(
                diff < 1e-6,
                "K=8 vs K=1 mismatch at i={i}: k8={:?} k1={:?}",
                s_k8[i],
                s_k1[i]
            );
        }

        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k8[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s_k8[15], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn k8_force_n4_target_each_position() {
        // K=8 의 N=4 (offset_bits=1, buffer 8개 × 2 amp).  H q_t for t ∈ {0..3}.
        // 각 buffer 위치의 read/write switch 검증.
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        for &target in &[0_usize, 1, 2, 3] {
            let mut s_k8 = vec![Complex::new(0.0_f32, 0.0); n];
            s_k8[0] = Complex::new(1.0, 0.0);
            b.apply_circuit_k8(
                &mut s_k8,
                &[WgpuGateOp::Single {
                    matrix: h(),
                    target,
                }],
                4,
            )
            .unwrap();
            let inv = 1.0_f32 / 2.0_f32.sqrt();
            assert!(
                approx(s_k8[0], Complex::new(inv, 0.0), 1e-6),
                "target={target} amp[0] wrong: {:?}",
                s_k8[0]
            );
            assert!(
                approx(s_k8[1 << target], Complex::new(inv, 0.0), 1e-6),
                "target={target} amp[{}] wrong: {:?}",
                1 << target,
                s_k8[1 << target]
            );
        }
    }

    // =====================================================================
    // v0.5.13: norm reduction shader tests.
    // =====================================================================

    #[test]
    fn norm_reduction_normalized_state() {
        // 정규화된 state (|0⟩ + |1⟩)/√2 의 ‖ψ‖² ≈ 1.0.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, 0.0),
            Complex::new(inv, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("norm test state"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        let norm_sq = b.compute_norm_squared(&storage, n).unwrap();
        assert!((norm_sq - 1.0).abs() < 1e-5, "norm²={norm_sq}");
    }

    #[test]
    fn norm_reduction_unnormalized_state() {
        // 2|0⟩ + 0|1⟩ 의 ‖ψ‖² = 4.0.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let state: Vec<Complex<f32>> = vec![
            Complex::new(2.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("norm test state"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        let norm_sq = b.compute_norm_squared(&storage, n).unwrap();
        assert!((norm_sq - 4.0).abs() < 1e-5, "norm²={norm_sq}");
    }

    // =====================================================================
    // v0.5.14: collapse + renormalize shader tests.
    // =====================================================================

    // =====================================================================
    // v0.5.15: per-qubit prob shader + measure_qubit_gpu tests.
    // =====================================================================

    #[test]
    fn qubit_prob_zero_bell_state() {
        // (|00⟩ + |11⟩)/√2: P(q0=0) = 0.5, P(q0=1) = 0.5.
        // P(q1=0) = 0.5, P(q1=1) = 0.5.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(inv, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("qubit prob test"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        let p0_q0 = b.compute_qubit_prob_zero(&storage, n, 0).unwrap();
        let p0_q1 = b.compute_qubit_prob_zero(&storage, n, 1).unwrap();
        assert!((p0_q0 - 0.5).abs() < 1e-5, "P(q0=0)={p0_q0}");
        assert!((p0_q1 - 0.5).abs() < 1e-5, "P(q1=0)={p0_q1}");
    }

    #[test]
    fn qubit_prob_zero_pure_states() {
        // |00⟩: P(q0=0) = 1.0.  |11⟩: P(q0=0) = 0.0.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let zero_state: Vec<Complex<f32>> = vec![
            Complex::new(1.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        let pod: Vec<CF32> = zero_state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("|00⟩"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        assert!((b.compute_qubit_prob_zero(&storage, n, 0).unwrap() - 1.0).abs() < 1e-5);
        assert!((b.compute_qubit_prob_zero(&storage, n, 1).unwrap() - 1.0).abs() < 1e-5);

        let one_state: Vec<Complex<f32>> = vec![
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(1.0, 0.0),
        ];
        let pod2: Vec<CF32> = one_state.iter().map(|c| (*c).into()).collect();
        let bytes2: &[u8] = bytemuck::cast_slice(&pod2);
        let storage2 = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("|11⟩"),
                contents: bytes2,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        assert!(b.compute_qubit_prob_zero(&storage2, n, 0).unwrap() < 1e-5);
        assert!(b.compute_qubit_prob_zero(&storage2, n, 1).unwrap() < 1e-5);
    }

    #[test]
    fn measure_qubit_gpu_bell_collapse() {
        // (|00⟩ + |11⟩)/√2 + random=0.0 → outcome=0 → state collapse to |00⟩.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(inv, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("measure test"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });

        // random_uniform=0.0 → 0.0 < P(q0=0)=0.5 이므로 outcome=0.
        let outcome = b.measure_qubit_gpu(&storage, n, 0, 0.0).unwrap();
        assert_eq!(outcome, 0);

        // Read state back: |00⟩ amplitude = 1.0.
        let staging = b.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("readback"),
            size: bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = b
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("readback encoder"),
            });
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, bytes.len() as u64);
        b.queue.submit(Some(encoder.finish()));
        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        b.device.poll(wgpu::PollType::wait_indefinitely()).unwrap();
        receiver.recv().unwrap().unwrap();
        let data = slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        let result_complex: Vec<Complex<f32>> = result.iter().map(|c| (*c).into()).collect();
        assert!(approx(result_complex[0], Complex::new(1.0, 0.0), 1e-5));
        assert!(approx(result_complex[3], Complex::new(0.0, 0.0), 1e-6));
        drop(data);
        staging.unmap();
    }

    #[test]
    fn collapse_qubit_zero_outcome() {
        // (|00⟩ + |11⟩)/√2 → measure q0=0 → |00⟩.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, 0.0), // |00⟩
            Complex::new(0.0, 0.0), // |01⟩
            Complex::new(0.0, 0.0), // |10⟩
            Complex::new(inv, 0.0), // |11⟩
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("collapse test state"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        // P(q0=0) = |amp[0]|² + |amp[2]|² = 0.5.  inv_sqrt_prob = √2.
        b.collapse_qubit(&storage, n, 0, 0, 2.0_f32.sqrt()).unwrap();

        // Read state back.
        let staging = b.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("collapse readback"),
            size: bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = b
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("readback encoder"),
            });
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, bytes.len() as u64);
        b.queue.submit(Some(encoder.finish()));
        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        b.device.poll(wgpu::PollType::wait_indefinitely()).unwrap();
        receiver.recv().unwrap().unwrap();
        let data = slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        let result_complex: Vec<Complex<f32>> = result.iter().map(|c| (*c).into()).collect();
        // q0=0 outcome → |00⟩ amp = inv*√2 = 1.0, 그 외 0.
        assert!(approx(result_complex[0], Complex::new(1.0, 0.0), 1e-5));
        assert!(approx(result_complex[1], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(result_complex[2], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(result_complex[3], Complex::new(0.0, 0.0), 1e-6));
        drop(data);
        staging.unmap();
    }

    #[test]
    fn collapse_qubit_one_outcome() {
        // (|00⟩ + |11⟩)/√2 → measure q1=1 → |11⟩.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
            Complex::new(inv, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("collapse test state"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        // P(q1=1) = |amp[2]|² + |amp[3]|² = 0.5.  inv_sqrt_prob = √2.
        b.collapse_qubit(&storage, n, 1, 1, 2.0_f32.sqrt()).unwrap();

        let staging = b.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("collapse readback"),
            size: bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = b
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("readback encoder"),
            });
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, bytes.len() as u64);
        b.queue.submit(Some(encoder.finish()));
        let slice = staging.slice(..);
        let (sender, receiver) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            sender.send(r).ok();
        });
        b.device.poll(wgpu::PollType::wait_indefinitely()).unwrap();
        receiver.recv().unwrap().unwrap();
        let data = slice.get_mapped_range();
        let result: &[CF32] = bytemuck::cast_slice(&data);
        let result_complex: Vec<Complex<f32>> = result.iter().map(|c| (*c).into()).collect();
        // q1=1 outcome → only amp[3] (|11⟩) survives, = inv*√2 = 1.0.
        assert!(approx(result_complex[0], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(result_complex[1], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(result_complex[2], Complex::new(0.0, 0.0), 1e-6));
        assert!(approx(result_complex[3], Complex::new(1.0, 0.0), 1e-5));
        drop(data);
        staging.unmap();
    }

    #[test]
    fn norm_reduction_complex_amplitudes() {
        // (1+i)/√2 |0⟩ + (1-i)/√2 |1⟩ 의 ‖ψ‖² = 1+1 = 2.0.
        let Some(b) = make_backend() else { return };
        use wgpu::util::DeviceExt;
        let n = 4usize;
        let inv = 1.0_f32 / 2.0_f32.sqrt();
        let state: Vec<Complex<f32>> = vec![
            Complex::new(inv, inv),
            Complex::new(inv, -inv),
            Complex::new(0.0, 0.0),
            Complex::new(0.0, 0.0),
        ];
        let pod: Vec<CF32> = state.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = b
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("norm test state"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            });
        let norm_sq = b.compute_norm_squared(&storage, n).unwrap();
        assert!((norm_sq - 2.0).abs() < 1e-5, "norm²={norm_sq}");
    }

    #[test]
    fn k8_force_n5_ghz_full_circuit() {
        // N=5 K=8 (offset_bits=2, buffer 8개 × 4 amp).  GHZ-5 회로의 결과.
        let Some(b) = make_backend() else { return };
        let n = 32usize;
        let mut s_k8 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k8[0] = Complex::new(1.0, 0.0);
        let ops = vec![
            WgpuGateOp::Single {
                matrix: h(),
                target: 0,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 1,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 2,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 3,
            },
            WgpuGateOp::Controlled1q {
                matrix: x(),
                ctrl: 0,
                tgt: 4,
            },
        ];
        b.apply_circuit_k8(&mut s_k8, &ops, 5).unwrap();

        let mut s_k1 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k1[0] = Complex::new(1.0, 0.0);
        b.apply_circuit(&mut s_k1, &ops).unwrap();

        for i in 0..n {
            let diff = (s_k8[i] - s_k1[i]).norm();
            assert!(diff < 1e-6, "k8 vs k1 mismatch at i={i}");
        }

        let inv = 1.0_f32 / 2.0_f32.sqrt();
        assert!(approx(s_k8[0], Complex::new(inv, 0.0), 1e-5));
        assert!(approx(s_k8[31], Complex::new(inv, 0.0), 1e-5));
    }

    #[test]
    fn k2_force_n4_two_qubit_split_q1() {
        // 2-qubit gate 의 q_hi = split_bit 인 경우 cross-buffer.  CNOT(ctrl=q0, tgt=q3)
        // (Controlled1q path 인데 Two path 도 검증 — CZ 사용).
        let Some(b) = make_backend() else { return };
        let n = 16usize;
        // |1001⟩ = q0=1, q3=1 → CZ(q0, q3) → -|1001⟩ (둘 다 1 일 때만 phase).
        let mut s_k2 = vec![Complex::new(0.0_f32, 0.0); n];
        s_k2[9] = Complex::new(1.0, 0.0); // index 9 = 0b1001
        let z = Complex::new(0.0_f32, 0.0);
        let o = Complex::new(1.0_f32, 0.0);
        let neg = Complex::new(-1.0_f32, 0.0);
        let cz = [[o, z, z, z], [z, o, z, z], [z, z, o, z], [z, z, z, neg]];
        b.apply_circuit_k2(
            &mut s_k2,
            &[WgpuGateOp::Two {
                matrix: cz,
                q0: 0,
                q1: 3,
            }],
            4,
        )
        .unwrap();
        assert!(approx(s_k2[9], neg, 1e-6));
    }
}
