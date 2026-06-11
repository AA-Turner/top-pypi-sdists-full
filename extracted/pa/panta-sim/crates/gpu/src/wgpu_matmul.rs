//! Complex dense matmul on wgpu — tensor network contraction 의 GPU 커널.
//!
//! Pairwise tensor contraction 은 permute(transpose) → reshape → matmul 로
//! 환원되며, 그 matmul `C[m×n] = A[m×k]·B[k×n]` 를 WGSL compute shader 로
//! offload 한다.  cross-platform (NVIDIA / AMD / Apple Metal / Intel /
//! lavapipe) — cuTensorNet (NVIDIA only) / cotengra (CPU) 와 달리 panta-sim 의
//! TN contraction 을 모든 GPU 에서 가속하는 USP.
//!
//! wgpu storage 는 f64 미지원 → **f32** 정밀도 (양자 진폭 ~1e-5).  permute 는
//! CPU (호출부), dominant FLOPs 인 matmul 만 GPU.

use num_complex::Complex64;
use pollster::FutureExt as _;

use crate::errors::GpuError;

#[repr(C)]
#[derive(Clone, Copy, bytemuck::Pod, bytemuck::Zeroable)]
struct MatmulParams {
    m: u32,
    k: u32,
    n: u32,
    total: u32,
    /// 0 = 1D dispatch, >0 = 2D chunking 의 x 차원 워크그룹 수 (셰이더가
    /// `gid.x + gid.y * dispatches_x * 64` 로 선형 인덱스 복원).
    dispatches_x: u32,
    _pad0: u32,
    _pad1: u32,
    _pad2: u32,
}

/// Complex matmul GPU 백엔드 (device/queue + matmul pipeline).  process-wide
/// singleton 으로 [`crate::cached_wgpu_matmul_backend`] 를 통해 쓴다.
pub struct WgpuMatmulBackend {
    device: wgpu::Device,
    queue: wgpu::Queue,
    pipeline: wgpu::ComputePipeline,
    bgl: wgpu::BindGroupLayout,
}

impl WgpuMatmulBackend {
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
        let limits = adapter.limits();
        let (device, queue) = adapter
            .request_device(&wgpu::DeviceDescriptor {
                label: Some("panta-sim wgpu matmul device"),
                required_features: wgpu::Features::empty(),
                required_limits: limits,
                experimental_features: wgpu::ExperimentalFeatures::default(),
                memory_hints: wgpu::MemoryHints::Performance,
                trace: wgpu::Trace::Off,
            })
            .block_on()
            .map_err(|e| GpuError::DeviceCreation(format!("{e:?}")))?;

        let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
            label: Some("complex_matmul bgl"),
            entries: &[
                storage_entry(0, true),
                storage_entry(1, true),
                storage_entry(2, false),
                wgpu::BindGroupLayoutEntry {
                    binding: 3,
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
            label: Some("complex_matmul layout"),
            bind_group_layouts: &[Some(&bgl)],
            immediate_size: 0,
        });
        let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
            label: Some("complex_matmul shader"),
            source: wgpu::ShaderSource::Wgsl(
                include_str!("wgpu_backend/shaders/complex_matmul.wgsl").into(),
            ),
        });
        let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
            label: Some("complex_matmul pipeline"),
            layout: Some(&layout),
            module: &shader,
            entry_point: Some("main"),
            compilation_options: wgpu::PipelineCompilationOptions::default(),
            cache: None,
        });

        Ok(Self {
            device,
            queue,
            pipeline,
            bgl,
        })
    }

    /// `C[m×n] = A[m×k] · B[k×n]` (row-major, complex).  GPU f32 정밀도.
    pub fn matmul(
        &self,
        m: usize,
        k: usize,
        n: usize,
        a: &[Complex64],
        b: &[Complex64],
    ) -> Vec<Complex64> {
        debug_assert_eq!(a.len(), m * k);
        debug_assert_eq!(b.len(), k * n);
        let total = m * n;
        if total == 0 {
            return vec![];
        }
        use wgpu::util::DeviceExt as _;
        let a_raw: Vec<[f32; 2]> = a.iter().map(|c| [c.re as f32, c.im as f32]).collect();
        let b_raw: Vec<[f32; 2]> = b.iter().map(|c| [c.re as f32, c.im as f32]).collect();
        let a_buf = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("matmul A"),
                contents: bytemuck::cast_slice(&a_raw),
                usage: wgpu::BufferUsages::STORAGE,
            });
        let b_buf = self
            .device
            .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                label: Some("matmul B"),
                contents: bytemuck::cast_slice(&b_raw),
                usage: wgpu::BufferUsages::STORAGE,
            });
        let c_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("matmul C"),
            size: (total * 8) as u64,
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });
        // adapter 의 max_compute_workgroups_per_dimension (보수적으로 65535)
        // 초과 시 2D chunking — width 23+ 중간 텐서 (m·n > 4.19e6) 에서
        // wgpu validation error 로 죽던 문제 (statevector dispatch_2d 와 동일
        // 패턴).
        const MAX_WG_PER_DIM: u32 = 65535;
        let workgroups_needed = (total as u32).div_ceil(64);
        let (wg_x, wg_y, dispatches_x) = if workgroups_needed <= MAX_WG_PER_DIM {
            (workgroups_needed.max(1), 1, 0)
        } else {
            (
                MAX_WG_PER_DIM,
                workgroups_needed.div_ceil(MAX_WG_PER_DIM),
                MAX_WG_PER_DIM,
            )
        };
        let params = MatmulParams {
            m: m as u32,
            k: k as u32,
            n: n as u32,
            total: total as u32,
            dispatches_x,
            _pad0: 0,
            _pad1: 0,
            _pad2: 0,
        };
        let params_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("matmul params"),
            size: std::mem::size_of::<MatmulParams>() as u64,
            usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        self.queue
            .write_buffer(&params_buf, 0, bytemuck::bytes_of(&params));

        let bg = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("matmul BG"),
            layout: &self.bgl,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: a_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: b_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: c_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 3,
                    resource: params_buf.as_entire_binding(),
                },
            ],
        });

        let mut encoder = self
            .device
            .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                label: Some("matmul dispatch"),
            });
        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("matmul pass"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.pipeline);
            pass.set_bind_group(0, Some(&bg), &[]);
            pass.dispatch_workgroups(wg_x, wg_y, 1);
        }
        // readback.
        let staging = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("matmul staging"),
            size: (total * 8) as u64,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        encoder.copy_buffer_to_buffer(&c_buf, 0, &staging, 0, (total * 8) as u64);
        self.queue.submit(std::iter::once(encoder.finish()));

        let slice = staging.slice(..);
        let (tx, rx) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            let _ = tx.send(r);
        });
        let _ = self.device.poll(wgpu::PollType::wait_indefinitely());
        rx.recv()
            .ok()
            .and_then(|r| r.ok())
            .expect("matmul staging map failed");
        let data = slice.get_mapped_range();
        let raw: &[[f32; 2]] = bytemuck::cast_slice(&data);
        let out: Vec<Complex64> = raw
            .iter()
            .map(|v| Complex64::new(v[0] as f64, v[1] as f64))
            .collect();
        drop(data);
        staging.unmap();
        out
    }
}

fn storage_entry(binding: u32, read_only: bool) -> wgpu::BindGroupLayoutEntry {
    wgpu::BindGroupLayoutEntry {
        binding,
        visibility: wgpu::ShaderStages::COMPUTE,
        ty: wgpu::BindingType::Buffer {
            ty: wgpu::BufferBindingType::Storage { read_only },
            has_dynamic_offset: false,
            min_binding_size: None,
        },
        count: None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cached_wgpu_matmul_backend;

    fn cpu_matmul(
        m: usize,
        k: usize,
        n: usize,
        a: &[Complex64],
        b: &[Complex64],
    ) -> Vec<Complex64> {
        let mut c = vec![Complex64::new(0.0, 0.0); m * n];
        for i in 0..m {
            for l in 0..k {
                let av = a[i * k + l];
                for j in 0..n {
                    c[i * n + j] += av * b[l * n + j];
                }
            }
        }
        c
    }

    /// 회귀: 출력이 65535 워크그룹 (= 4,194,240 원소) 을 넘으면 1D dispatch
    /// 가 wgpu validation error 로 죽던 문제 — 2D chunking 경로 검증.
    /// m·n = 2^23 (8.4M 원소, k=1) 로 chunking 경로를 강제한다.
    #[test]
    fn gpu_matmul_2d_chunked_dispatch_matches_cpu() {
        let backend = match cached_wgpu_matmul_backend() {
            Ok(b) => b,
            Err(_) => {
                eprintln!("no GPU adapter — skipping");
                return;
            }
        };
        let (m, k, n) = (1usize << 12, 1usize, 1usize << 11); // 8.4M 출력
        let a: Vec<Complex64> = (0..m * k)
            .map(|i| Complex64::new((i % 17) as f64 * 0.1, (i % 5) as f64 * 0.2))
            .collect();
        let b: Vec<Complex64> = (0..k * n)
            .map(|i| Complex64::new((i % 13) as f64 * 0.3, (i % 7) as f64 * 0.1))
            .collect();
        let gpu = backend.matmul(m, k, n, &a, &b);
        assert_eq!(gpu.len(), m * n);
        // k=1 이라 C[i,j] = A[i]·B[j] — 몇 지점 (chunk 경계 포함) 만 spot-check.
        for &idx in &[0usize, 4_194_240, 4_194_304, m * n - 1] {
            let (i, j) = (idx / n, idx % n);
            let expect = a[i] * b[j];
            assert!(
                (gpu[idx] - expect).norm() < 1e-4,
                "idx {idx}: {:?} vs {:?}",
                gpu[idx],
                expect
            );
        }
    }

    #[test]
    fn gpu_matmul_matches_cpu() {
        let backend = match cached_wgpu_matmul_backend() {
            Ok(b) => b,
            Err(_) => {
                eprintln!("no GPU adapter — skipping");
                return;
            }
        };
        let (m, k, n) = (5usize, 7usize, 4usize);
        let mut s = 12345u64;
        let mut nextc = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            let re = ((s >> 33) as f32 / u32::MAX as f32) as f64 * 2.0 - 1.0;
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            let im = ((s >> 33) as f32 / u32::MAX as f32) as f64 * 2.0 - 1.0;
            Complex64::new(re, im)
        };
        let a: Vec<Complex64> = (0..m * k).map(|_| nextc()).collect();
        let b: Vec<Complex64> = (0..k * n).map(|_| nextc()).collect();
        let gpu = backend.matmul(m, k, n, &a, &b);
        let cpu = cpu_matmul(m, k, n, &a, &b);
        for (g, c) in gpu.iter().zip(cpu.iter()) {
            assert!((g - c).norm() < 1e-4, "gpu {g} vs cpu {c}");
        }
    }
}
