//! `WgpuMpsBackend` — v0.6.6 Cut 2/3 의 GPU MPS 인프라 컨테이너.
//!
//! wgpu adapter / device / queue 를 초기화하고 SVD / contraction
//! pipeline 들을 들고 있는 구조체.
//!
//! ## 정책 메모
//! - **별도 device**: statevector backend 의 device 와 공유 가능하나,
//!   사용자가 `wgpu_mps` 만 쓸 때 statevector pipeline 까지 강제 init
//!   되는 부작용 회피를 위해 자체 device 사용.  init cost (~수백 ms) 는
//!   process-wide singleton 으로 한 번만.
//! - **f32 only**: storage `f64` 미지원 (wgpu 29.x).  device feature
//!   요구 없음.
//! - **adapter limits 적용**: statevector v0.5.1 fix 와 동일 — device
//!   에 adapter 의 limit 그대로 요청해 큰 buffer / dispatch 한계 활용.
//! - **pipeline build**: contraction / 1q / absorb 는 init 시 eager build
//!   (production hot path).  Jacobi SVD pipeline 은 v0.6.6.2 부터 production
//!   이 host nalgebra SVD 를 쓰므로 **lazy build** (v1.4) — [`wgpu_thin_svd`]
//!   가 처음 쓸 때 [`std::sync::OnceLock`] 으로 한 번만 build.
//!
//! [`wgpu_thin_svd`]: crate::wgpu_mps::svd::wgpu_thin_svd

use std::sync::OnceLock;

use pollster::FutureExt as _;

use crate::GpuError;

/// GPU MPS 백엔드.  Cut 3 까지 SVD pipeline + 인프라 보유.  Cut 5 부터
/// contraction pipeline 도 추가.
pub struct WgpuMpsBackend {
    device: wgpu::Device,
    queue: wgpu::Queue,
    adapter_info: wgpu::AdapterInfo,
    /// One-sided Jacobi SVD rotation kernel (v0.6.6 Cut 3).
    ///
    /// v0.6.6.2 부터 production SVD 는 host nalgebra — 이 pipeline 은
    /// [`crate::wgpu_mps::svd::wgpu_thin_svd`] (실험/검증 경로) 전용이라
    /// `method="wgpu_mps"` init 이 비용을 지불하지 않도록 첫 사용 시점에
    /// lazy build 한다 (v1.4).
    svd_jacobi: OnceLock<(wgpu::ComputePipeline, wgpu::BindGroupLayout)>,
    /// Two-site contraction + gate application (v0.6.7 Cut 5).
    contract_pipeline: wgpu::ComputePipeline,
    contract_bgl: wgpu::BindGroupLayout,
    /// One-qubit gate in-place (v0.6.7 Cut 5b).
    one_qubit_pipeline: wgpu::ComputePipeline,
    one_qubit_bgl: wgpu::BindGroupLayout,
    /// Absorption shader for right-canonicalize (v0.6.7 Cut 5c).
    absorb_pipeline: wgpu::ComputePipeline,
    absorb_bgl: wgpu::BindGroupLayout,
}

impl WgpuMpsBackend {
    /// 새 GPU MPS 백엔드를 만든다.
    ///
    /// adapter / device 초기화 (~수백 ms) + production pipeline (contraction /
    /// 1q / absorb) build.  Jacobi SVD pipeline 은 lazy (v1.4 — struct 필드
    /// doc 참조).  process-wide singleton 으로 한 번만 호출되도록
    /// [`crate::cached_wgpu_mps_backend`] 사용.
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
        let adapter_info = adapter.get_info();
        let adapter_limits = adapter.limits();
        let (device, queue) = adapter
            .request_device(&wgpu::DeviceDescriptor {
                label: Some("panta-sim wgpu MPS device"),
                required_features: wgpu::Features::empty(),
                required_limits: adapter_limits,
                experimental_features: wgpu::ExperimentalFeatures::default(),
                memory_hints: wgpu::MemoryHints::Performance,
                trace: wgpu::Trace::Off,
            })
            .block_on()
            .map_err(|e| GpuError::DeviceCreation(format!("{e:?}")))?;

        let (contract_pipeline, contract_bgl) =
            super::contraction::build_contract_pipeline(&device);
        let (one_qubit_pipeline, one_qubit_bgl) =
            super::one_qubit::build_one_qubit_pipeline(&device);
        let (absorb_pipeline, absorb_bgl) = super::absorb::build_absorb_pipeline(&device);

        Ok(Self {
            device,
            queue,
            adapter_info,
            svd_jacobi: OnceLock::new(),
            contract_pipeline,
            contract_bgl,
            one_qubit_pipeline,
            one_qubit_bgl,
            absorb_pipeline,
            absorb_bgl,
        })
    }

    pub fn device(&self) -> &wgpu::Device {
        &self.device
    }

    pub fn queue(&self) -> &wgpu::Queue {
        &self.queue
    }

    pub fn adapter_info(&self) -> &wgpu::AdapterInfo {
        &self.adapter_info
    }

    /// Jacobi SVD pipeline + BGL — 첫 호출에서 lazy build (v1.4).
    fn svd_jacobi(&self) -> &(wgpu::ComputePipeline, wgpu::BindGroupLayout) {
        self.svd_jacobi
            .get_or_init(|| build_svd_jacobi_pipeline(&self.device))
    }

    pub(crate) fn svd_jacobi_pipeline(&self) -> &wgpu::ComputePipeline {
        &self.svd_jacobi().0
    }

    pub(crate) fn svd_jacobi_bgl(&self) -> &wgpu::BindGroupLayout {
        &self.svd_jacobi().1
    }

    /// Two-site contraction pipeline (v0.6.7 Cut 5).
    pub fn contract_pipeline(&self) -> &wgpu::ComputePipeline {
        &self.contract_pipeline
    }

    /// Bind group layout for [`Self::contract_pipeline`].
    pub fn contract_bgl(&self) -> &wgpu::BindGroupLayout {
        &self.contract_bgl
    }

    /// One-qubit gate pipeline (v0.6.7 Cut 5b).
    pub fn one_qubit_pipeline(&self) -> &wgpu::ComputePipeline {
        &self.one_qubit_pipeline
    }

    /// Bind group layout for [`Self::one_qubit_pipeline`].
    pub fn one_qubit_bgl(&self) -> &wgpu::BindGroupLayout {
        &self.one_qubit_bgl
    }

    /// Absorption pipeline for right-canonicalize (v0.6.7 Cut 5c).
    pub fn absorb_pipeline(&self) -> &wgpu::ComputePipeline {
        &self.absorb_pipeline
    }

    /// Bind group layout for [`Self::absorb_pipeline`].
    pub fn absorb_bgl(&self) -> &wgpu::BindGroupLayout {
        &self.absorb_bgl
    }
}

/// One-sided Jacobi SVD rotation pipeline.
///
/// bindings:
///   0: M (storage, read_write, vec2<f32>)
///   1: V (storage, read_write, vec2<f32>)
///   2: params (uniform)
///   3: pair_schedule (storage, read, u32)
fn build_svd_jacobi_pipeline(
    device: &wgpu::Device,
) -> (wgpu::ComputePipeline, wgpu::BindGroupLayout) {
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some("svd_jacobi BGL"),
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
            wgpu::BindGroupLayoutEntry {
                binding: 3,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: true },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
        ],
    });
    let layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
        label: Some("svd_jacobi layout"),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("svd_jacobi shader"),
        source: wgpu::ShaderSource::Wgsl(include_str!("shaders/svd_jacobi.wgsl").into()),
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("svd_jacobi pipeline"),
        layout: Some(&layout),
        module: &shader,
        entry_point: Some("main"),
        compilation_options: wgpu::PipelineCompilationOptions::default(),
        cache: None,
    });
    (pipeline, bgl)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn try_new() -> Option<WgpuMpsBackend> {
        match WgpuMpsBackend::new() {
            Ok(b) => Some(b),
            Err(GpuError::NoAdapter) => None,
            Err(e) => panic!("backend init failed: {e}"),
        }
    }

    #[test]
    fn backend_new_succeeds_when_adapter_available() {
        let Some(backend) = try_new() else {
            return;
        };
        let info = backend.adapter_info();
        assert!(!info.name.is_empty(), "adapter name should be non-empty");
    }

    #[test]
    fn backend_device_and_queue_accessible() {
        let Some(backend) = try_new() else {
            return;
        };
        let _ = backend.device();
        let _ = backend.queue();
    }

    #[test]
    fn backend_builds_svd_jacobi_pipeline_lazily() {
        let Some(backend) = try_new() else {
            return;
        };
        // v1.4: init 시점에는 미빌드 (lazy) — 첫 accessor 호출이 build.
        assert!(backend.svd_jacobi.get().is_none());
        let _pipeline = backend.svd_jacobi_pipeline();
        let _bgl = backend.svd_jacobi_bgl();
        assert!(backend.svd_jacobi.get().is_some());
    }
}
