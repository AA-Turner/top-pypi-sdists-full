//! wgpu density matrix backend (v0.5.0 Cut E).
//!
//! Density matrix `ρ ∈ ℂ^(2ⁿ × 2ⁿ)` (4ⁿ complex) 를 GPU buffer 에 보관.
//! 1q unitary / 2q unitary / controlled-1q / 1q Kraus channel 을 WGSL
//! compute shader 로 적용.  CPU `DensityMatrix` 와 동일 의미.
//!
//! 메모리: 4ⁿ × 8B (f32 complex) — N=10 1MB, N=12 16 MB, N=13 64 MB, N=14 256 MB.
//! GPU storage buffer 한계 (보통 256 MB ~ 1 GB) 가 N≤13 ~ N≤15 까지 허용.
//!
//! Cut E scope: 1q unitary + 2q unitary + controlled-1q + 1q Kraus.
//! 3-qubit (Toffoli, Fredkin) 은 거부 — 사용자가 transpile 후 호출 또는 CPU
//! 백엔드 사용.  density 측정 / partial_trace 는 download 후 CPU.

use bytemuck::{Pod, Zeroable};
use num_complex::Complex;
use pollster::FutureExt;
use wgpu::util::DeviceExt;

use crate::errors::GpuError;

/// Pod 표현 ((re, im)).
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
struct Density1qUniforms {
    qubit_stride: u32,
    dim: u32,
    n_qubits: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct Density2qUniforms {
    bit0: u32,
    bit1: u32,
    dim: u32,
    mask_lo: u32,
    mask_mid: u32,
    mask_hi: u32,
    n_groups: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    m: [[f32; 2]; 16],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct DensityControlled1qUniforms {
    ctrl_bit: u32,
    tgt_stride: u32,
    dim: u32,
    dispatches_x: u32, // v0.5.2 2D dispatch chunking
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable, Default)]
struct KrausOpUniform {
    m00: [f32; 2],
    m01: [f32; 2],
    m10: [f32; 2],
    m11: [f32; 2],
}

#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
struct DensityKraus1qUniforms {
    qubit_stride: u32,
    dim: u32,
    n_kraus: u32,
    dispatches_x: u32,          // v0.5.2 2D dispatch chunking
    kraus: [KrausOpUniform; 4], // 최대 4 Kraus ops (depolarizing).
}

/// v0.5.2 dispatch chunking helper (statevector.rs 와 동일).
/// **v0.5.3 fix**: 작은 회로면 dispatches_x=0 신호로 1D path 회복.
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
        let wg_x = MAX_WG_PER_DIM;
        let wg_y = workgroups.div_ceil(MAX_WG_PER_DIM);
        (wg_x, wg_y, wg_x)
    }
}

struct Pipeline {
    pipeline: wgpu::ComputePipeline,
    bgl: wgpu::BindGroupLayout,
}

/// GPU 에서 dispatch 할 수 있는 density backend op.
#[derive(Debug, Clone)]
pub enum WgpuDensityOp {
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
    Kraus1q {
        kraus: Vec<[[Complex<f32>; 2]; 2]>,
        target: usize,
    },
}

/// wgpu 기반 density matrix backend (Tier-1, v0.5.0).
pub struct WgpuDensityBackend {
    device: wgpu::Device,
    queue: wgpu::Queue,
    unitary_1q_row: Pipeline,
    unitary_1q_col: Pipeline,
    unitary_2q_row: Pipeline,
    unitary_2q_col: Pipeline,
    controlled_1q_row: Pipeline,
    controlled_1q_col: Pipeline,
    kraus_1q: Pipeline,
}

impl WgpuDensityBackend {
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
        // v0.5.1: adapter.limits() 사용 — discrete GPU 의 큰 buffer / dispatch 한계 활용.
        let adapter_limits = adapter.limits();
        let (device, queue) = adapter
            .request_device(&wgpu::DeviceDescriptor {
                label: Some("panta-sim wgpu density device"),
                required_features: wgpu::Features::empty(),
                required_limits: adapter_limits,
                experimental_features: wgpu::ExperimentalFeatures::default(),
                memory_hints: wgpu::MemoryHints::Performance,
                trace: wgpu::Trace::Off,
            })
            .block_on()
            .map_err(|e| GpuError::DeviceCreation(format!("{e:?}")))?;

        let unitary_1q_row = build_pipeline(
            &device,
            "density_unitary_1q_row",
            include_str!("shaders/density_unitary_1q_row.wgsl"),
        );
        let unitary_1q_col = build_pipeline(
            &device,
            "density_unitary_1q_col",
            include_str!("shaders/density_unitary_1q_col.wgsl"),
        );
        let unitary_2q_row = build_pipeline(
            &device,
            "density_unitary_2q_row",
            include_str!("shaders/density_unitary_2q_row.wgsl"),
        );
        let unitary_2q_col = build_pipeline(
            &device,
            "density_unitary_2q_col",
            include_str!("shaders/density_unitary_2q_col.wgsl"),
        );
        let controlled_1q_row = build_pipeline(
            &device,
            "density_controlled_1q_row",
            include_str!("shaders/density_controlled_1q_row.wgsl"),
        );
        let controlled_1q_col = build_pipeline(
            &device,
            "density_controlled_1q_col",
            include_str!("shaders/density_controlled_1q_col.wgsl"),
        );
        let kraus_1q = build_pipeline(
            &device,
            "density_kraus_1q",
            include_str!("shaders/density_kraus_1q.wgsl"),
        );

        Ok(Self {
            device,
            queue,
            unitary_1q_row,
            unitary_1q_col,
            unitary_2q_row,
            unitary_2q_col,
            controlled_1q_row,
            controlled_1q_col,
            kraus_1q,
        })
    }

    /// 회로 단위 batching (Cut E).
    ///
    /// rho 는 `Vec<Complex<f32>>` (length = 4ⁿ, row-major flat) — CPU 에서
    /// `DensityMatrix::data()` 호출 후 conversion 또는 직접 |0⟩⟨0| 초기화.
    /// 모든 op 를 single command encoder 안에 dispatch.
    pub fn apply_circuit(
        &self,
        rho: &mut [Complex<f32>],
        n_qubits: usize,
        ops: &[WgpuDensityOp],
    ) -> Result<(), GpuError> {
        let dim = 1usize << n_qubits;
        if rho.len() != dim * dim {
            return Err(GpuError::Unsupported(format!(
                "rho.len() = {} 가 dim²={} 와 다름",
                rho.len(),
                dim * dim
            )));
        }
        if ops.is_empty() {
            return Ok(());
        }

        let pod: Vec<CF32> = rho.iter().map(|c| (*c).into()).collect();
        let bytes: &[u8] = bytemuck::cast_slice(&pod);
        let storage = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("density apply_circuit storage"),
                contents: bytes,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
            });
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("density staging"),
            size: bytes.len() as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        let mut owned_bufs: Vec<wgpu::Buffer> = Vec::new();
        let mut owned_bgs: Vec<wgpu::BindGroup> = Vec::new();
        // (pipeline_idx, wg_x, wg_y).  pipeline_idx ∈ {0=u1q_row, 1=u1q_col,
        // 2=u2q_row, 3=u2q_col, 4=c1q_row, 5=c1q_col, 6=kraus_1q}.  v0.5.2 2D
        // dispatch chunking.
        let mut dispatches: Vec<(usize, u32, u32)> = Vec::new();

        for op in ops {
            match op {
                WgpuDensityOp::Single { matrix, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Single target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    let stride = 1u32 << target;
                    let pairs_per_col = (dim / 2) as u32;
                    let total = pairs_per_col * dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    // Row pass uniforms.
                    let row_u = Density1qUniforms {
                        qubit_stride: stride,
                        dim: dim as u32,
                        n_qubits: n_qubits as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let row_buf = self.uniform_buf(bytemuck::bytes_of(&row_u));
                    let row_bg = self.bind_group(&self.unitary_1q_row.bgl, &storage, &row_buf);
                    owned_bufs.push(row_buf);
                    owned_bgs.push(row_bg);
                    dispatches.push((0, wg_x, wg_y));

                    // Col pass uniforms (use conj of M as right multiplier).
                    let col_u = Density1qUniforms {
                        qubit_stride: stride,
                        dim: dim as u32,
                        n_qubits: n_qubits as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, -matrix[0][0].im],
                        m01: [matrix[0][1].re, -matrix[0][1].im],
                        m10: [matrix[1][0].re, -matrix[1][0].im],
                        m11: [matrix[1][1].re, -matrix[1][1].im],
                    };
                    let col_buf = self.uniform_buf(bytemuck::bytes_of(&col_u));
                    let col_bg = self.bind_group(&self.unitary_1q_col.bgl, &storage, &col_buf);
                    owned_bufs.push(col_buf);
                    owned_bgs.push(col_bg);
                    dispatches.push((1, wg_x, wg_y));
                }
                WgpuDensityOp::Two { matrix, q0, q1 } => {
                    if *q0 >= n_qubits || *q1 >= n_qubits || *q0 == *q1 {
                        return Err(GpuError::Unsupported(format!("Two q0={q0} q1={q1} 잘못됨")));
                    }
                    let bit0 = 1u32 << q0;
                    let bit1 = 1u32 << q1;
                    let (q_lo, q_hi) = if q0 < q1 { (*q0, *q1) } else { (*q1, *q0) };
                    let mask_lo = (1u32 << q_lo) - 1;
                    let mask_mid = ((1u32 << (q_hi - 1)).wrapping_sub(1)) ^ mask_lo;
                    let mask_hi = !((1u32 << (q_hi - 1)).wrapping_sub(1));
                    let n_groups = (dim / 4) as u32;
                    let total = n_groups * dim as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));

                    let mut m_flat = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            m_flat[i * 4 + j] = [matrix[i][j].re, matrix[i][j].im];
                        }
                    }
                    let row_u = Density2qUniforms {
                        bit0,
                        bit1,
                        dim: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        dispatches_x,
                        m: m_flat,
                    };
                    let row_buf = self.uniform_buf(bytemuck::bytes_of(&row_u));
                    let row_bg = self.bind_group(&self.unitary_2q_row.bgl, &storage, &row_buf);
                    owned_bufs.push(row_buf);
                    owned_bgs.push(row_bg);
                    dispatches.push((2, wg_x, wg_y));

                    // U† = transpose + conj.
                    let mut udag = [[0.0_f32; 2]; 16];
                    for i in 0..4 {
                        for j in 0..4 {
                            udag[i * 4 + j] = [matrix[j][i].re, -matrix[j][i].im];
                        }
                    }
                    let col_u = Density2qUniforms {
                        bit0,
                        bit1,
                        dim: dim as u32,
                        mask_lo,
                        mask_mid,
                        mask_hi,
                        n_groups,
                        dispatches_x,
                        m: udag,
                    };
                    let col_buf = self.uniform_buf(bytemuck::bytes_of(&col_u));
                    let col_bg = self.bind_group(&self.unitary_2q_col.bgl, &storage, &col_buf);
                    owned_bufs.push(col_buf);
                    owned_bgs.push(col_bg);
                    dispatches.push((3, wg_x, wg_y));
                }
                WgpuDensityOp::Controlled1q { matrix, ctrl, tgt } => {
                    if *ctrl >= n_qubits || *tgt >= n_qubits || *ctrl == *tgt {
                        return Err(GpuError::Unsupported(format!(
                            "Controlled1q ctrl={ctrl} tgt={tgt} 잘못됨"
                        )));
                    }
                    let total = (dim * dim) as u32;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total.div_ceil(64));
                    let row_u = DensityControlled1qUniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        dim: dim as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, matrix[0][0].im],
                        m01: [matrix[0][1].re, matrix[0][1].im],
                        m10: [matrix[1][0].re, matrix[1][0].im],
                        m11: [matrix[1][1].re, matrix[1][1].im],
                    };
                    let row_buf = self.uniform_buf(bytemuck::bytes_of(&row_u));
                    let row_bg = self.bind_group(&self.controlled_1q_row.bgl, &storage, &row_buf);
                    owned_bufs.push(row_buf);
                    owned_bgs.push(row_bg);
                    dispatches.push((4, wg_x, wg_y));

                    let col_u = DensityControlled1qUniforms {
                        ctrl_bit: 1u32 << ctrl,
                        tgt_stride: 1u32 << tgt,
                        dim: dim as u32,
                        dispatches_x,
                        m00: [matrix[0][0].re, -matrix[0][0].im],
                        m01: [matrix[0][1].re, -matrix[0][1].im],
                        m10: [matrix[1][0].re, -matrix[1][0].im],
                        m11: [matrix[1][1].re, -matrix[1][1].im],
                    };
                    let col_buf = self.uniform_buf(bytemuck::bytes_of(&col_u));
                    let col_bg = self.bind_group(&self.controlled_1q_col.bgl, &storage, &col_buf);
                    owned_bufs.push(col_buf);
                    owned_bgs.push(col_bg);
                    dispatches.push((5, wg_x, wg_y));
                }
                WgpuDensityOp::Kraus1q { kraus, target } => {
                    if *target >= n_qubits {
                        return Err(GpuError::Unsupported(format!(
                            "Kraus1q target {target} >= n_qubits {n_qubits}"
                        )));
                    }
                    if kraus.is_empty() || kraus.len() > 4 {
                        return Err(GpuError::Unsupported(format!(
                            "Kraus1q: ops 개수 {} (1..=4 만 지원)",
                            kraus.len()
                        )));
                    }
                    let mut k_arr = [KrausOpUniform::default(); 4];
                    for (idx, k) in kraus.iter().enumerate() {
                        k_arr[idx] = KrausOpUniform {
                            m00: [k[0][0].re, k[0][0].im],
                            m01: [k[0][1].re, k[0][1].im],
                            m10: [k[1][0].re, k[1][0].im],
                            m11: [k[1][1].re, k[1][1].im],
                        };
                    }
                    let blocks_per_row = (dim / 2) as u32;
                    let total_blocks = blocks_per_row * blocks_per_row;
                    let (wg_x, wg_y, dispatches_x) = dispatch_2d(total_blocks.div_ceil(64));
                    let u_data = DensityKraus1qUniforms {
                        qubit_stride: 1u32 << target,
                        dim: dim as u32,
                        n_kraus: kraus.len() as u32,
                        dispatches_x,
                        kraus: k_arr,
                    };
                    let buf = self.uniform_buf(bytemuck::bytes_of(&u_data));
                    let bg = self.bind_group(&self.kraus_1q.bgl, &storage, &buf);
                    owned_bufs.push(buf);
                    owned_bgs.push(bg);
                    dispatches.push((6, wg_x, wg_y));
                }
            }
        }

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("density apply_circuit encoder"),
            });
        for (i, (pipeline_idx, wg_x, wg_y)) in dispatches.iter().enumerate() {
            let pl = match pipeline_idx {
                0 => &self.unitary_1q_row,
                1 => &self.unitary_1q_col,
                2 => &self.unitary_2q_row,
                3 => &self.unitary_2q_col,
                4 => &self.controlled_1q_row,
                5 => &self.controlled_1q_col,
                _ => &self.kraus_1q,
            };
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("density op pass"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&pl.pipeline);
            pass.set_bind_group(0, &owned_bgs[i], &[]);
            pass.dispatch_workgroups(*wg_x, *wg_y, 1);
        }
        encoder.copy_buffer_to_buffer(&storage, 0, &staging, 0, bytes.len() as u64);
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
        for (dst, src) in rho.iter_mut().zip(result.iter()) {
            *dst = (*src).into();
        }
        drop(data);
        staging.unmap();
        Ok(())
    }

    fn uniform_buf(&self, bytes: &[u8]) -> wgpu::Buffer {
        self.device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("density uniform"),
                contents: bytes,
                usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
            })
    }

    fn bind_group(
        &self,
        layout: &wgpu::BindGroupLayout,
        storage: &wgpu::Buffer,
        uniform: &wgpu::Buffer,
    ) -> wgpu::BindGroup {
        self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("density bg"),
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

#[cfg(test)]
mod tests {
    use super::*;

    fn approx(a: Complex<f32>, b: Complex<f32>, eps: f32) -> bool {
        (a - b).norm() < eps
    }

    fn make_backend() -> Option<WgpuDensityBackend> {
        match WgpuDensityBackend::new() {
            Ok(b) => Some(b),
            Err(GpuError::NoAdapter) => None,
            Err(e) => panic!("density backend init: {e}"),
        }
    }

    fn x() -> [[Complex<f32>; 2]; 2] {
        [
            [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
        ]
    }
    fn h() -> [[Complex<f32>; 2]; 2] {
        let s = 1.0_f32 / 2.0_f32.sqrt();
        [
            [Complex::new(s, 0.0), Complex::new(s, 0.0)],
            [Complex::new(s, 0.0), Complex::new(-s, 0.0)],
        ]
    }

    /// |0⟩⟨0| (1 큐비트) 초기 ρ.
    fn init_zero(n: usize) -> Vec<Complex<f32>> {
        let dim = 1usize << n;
        let mut rho = vec![Complex::new(0.0_f32, 0.0); dim * dim];
        rho[0] = Complex::new(1.0, 0.0);
        rho
    }

    #[test]
    fn density_x_on_zero_gives_one() {
        let Some(b) = make_backend() else { return };
        let mut rho = init_zero(1);
        b.apply_circuit(
            &mut rho,
            1,
            &[WgpuDensityOp::Single {
                matrix: x(),
                target: 0,
            }],
        )
        .unwrap();
        // |1⟩⟨1| → ρ[1][1] = 1.
        assert!(approx(rho[3], Complex::new(1.0, 0.0), 1e-5));
        assert!(approx(rho[0], Complex::new(0.0, 0.0), 1e-5));
    }

    #[test]
    fn density_h_on_zero_gives_plus_plus() {
        let Some(b) = make_backend() else { return };
        let mut rho = init_zero(1);
        b.apply_circuit(
            &mut rho,
            1,
            &[WgpuDensityOp::Single {
                matrix: h(),
                target: 0,
            }],
        )
        .unwrap();
        // |+⟩⟨+| = [[0.5, 0.5], [0.5, 0.5]].
        for amp in &rho {
            assert!(approx(*amp, Complex::new(0.5, 0.0), 1e-5));
        }
    }

    #[test]
    fn density_bell_via_h_and_cnot() {
        let Some(b) = make_backend() else { return };
        let mut rho = init_zero(2);
        b.apply_circuit(
            &mut rho,
            2,
            &[
                WgpuDensityOp::Single {
                    matrix: h(),
                    target: 0,
                },
                WgpuDensityOp::Controlled1q {
                    matrix: x(),
                    ctrl: 0,
                    tgt: 1,
                },
            ],
        )
        .unwrap();
        // ρ_Bell: ρ[0][0] = ρ[3][3] = ρ[0][3] = ρ[3][0] = 0.5, 나머지 0.
        let dim = 4;
        let pairs = [(0, 0), (0, 3), (3, 0), (3, 3)];
        for i in 0..dim {
            for j in 0..dim {
                let v = rho[i * dim + j];
                if pairs.contains(&(i, j)) {
                    assert!(approx(v, Complex::new(0.5, 0.0), 1e-5));
                } else {
                    assert!(approx(v, Complex::new(0.0, 0.0), 1e-5));
                }
            }
        }
    }

    #[test]
    fn density_swap_via_two() {
        let Some(b) = make_backend() else { return };
        // |01⟩⟨01| → SWAP → |10⟩⟨10|.
        let mut rho = vec![Complex::new(0.0_f32, 0.0); 16];
        rho[5] = Complex::new(1.0, 0.0); // ρ[1][1] = 1 (|01⟩⟨01|).
        let z = Complex::new(0.0_f32, 0.0);
        let o = Complex::new(1.0_f32, 0.0);
        let swap = [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]];
        b.apply_circuit(
            &mut rho,
            2,
            &[WgpuDensityOp::Two {
                matrix: swap,
                q0: 0,
                q1: 1,
            }],
        )
        .unwrap();
        // ρ[2][2] = 1 (|10⟩⟨10|).
        assert!(approx(rho[2 * 4 + 2], o, 1e-5));
    }

    #[test]
    fn density_bit_flip_kraus() {
        let Some(b) = make_backend() else { return };
        // BitFlip(p=0.3) on |0⟩⟨0|: ρ' = diag(0.7, 0.3).
        let p = 0.3_f32;
        let q = (1.0 - p).sqrt();
        let s = p.sqrt();
        let z = Complex::new(0.0_f32, 0.0);
        let kraus = vec![
            [[Complex::new(q, 0.0), z], [z, Complex::new(q, 0.0)]],
            [[z, Complex::new(s, 0.0)], [Complex::new(s, 0.0), z]],
        ];
        let mut rho = init_zero(1);
        b.apply_circuit(&mut rho, 1, &[WgpuDensityOp::Kraus1q { kraus, target: 0 }])
            .unwrap();
        assert!(approx(rho[0], Complex::new(0.7, 0.0), 1e-5));
        assert!(approx(rho[1], z, 1e-5));
        assert!(approx(rho[2], z, 1e-5));
        assert!(approx(rho[3], Complex::new(0.3, 0.0), 1e-5));
    }
}
