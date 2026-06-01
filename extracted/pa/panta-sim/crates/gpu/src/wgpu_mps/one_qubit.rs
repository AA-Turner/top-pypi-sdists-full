//! One-qubit gate GPU dispatch (v0.6.7 Cut 5b).
//!
//! [`dispatch_one_qubit_gate`] applies a 2×2 unitary in-place on a single
//! MPS site tensor stored in a GPU buffer.  No host transfer needed.

use bytemuck::{Pod, Zeroable};
use num_complex::Complex;

use super::backend::WgpuMpsBackend;

/// Pod uniform for the one-qubit gate shader.
///
/// Layout matches the WGSL `Params` struct:
///   left, right, _pad0, _pad1, g00, g01, g10, g11
/// Total 48 bytes (16 + 4×8).
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
pub(crate) struct OneQubitParams {
    pub left: u32,
    pub right: u32,
    pub _pad0: u32,
    pub _pad1: u32,
    pub g00_re: f32,
    pub g00_im: f32,
    pub g01_re: f32,
    pub g01_im: f32,
    pub g10_re: f32,
    pub g10_im: f32,
    pub g11_re: f32,
    pub g11_im: f32,
}

/// Build the one-qubit gate pipeline + bind group layout.
pub(crate) fn build_one_qubit_pipeline(
    device: &wgpu::Device,
) -> (wgpu::ComputePipeline, wgpu::BindGroupLayout) {
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some("mps_1q BGL"),
        entries: &[
            // binding 0: tensor (storage, read_write)
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
            // binding 1: params (uniform, 48 bytes)
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
        label: Some("mps_1q layout"),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("mps_1q shader"),
        source: wgpu::ShaderSource::Wgsl(
            include_str!("shaders/mps_one_qubit_gate.wgsl").into(),
        ),
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("mps_1q pipeline"),
        layout: Some(&layout),
        module: &shader,
        entry_point: Some("main"),
        compilation_options: wgpu::PipelineCompilationOptions::default(),
        cache: None,
    });
    (pipeline, bgl)
}

/// Dispatch the one-qubit gate shader in-place on `tensor_buf`.
///
/// `gate` is the 2×2 unitary as `Complex<f64>` (converted to f32 in the
/// uniform upload).
///
/// # Buffer size
/// `tensor_buf`: `left * 2 * right * 8` bytes.
pub fn dispatch_one_qubit_gate(
    backend: &WgpuMpsBackend,
    pipeline: &wgpu::ComputePipeline,
    bgl: &wgpu::BindGroupLayout,
    tensor_buf: &wgpu::Buffer,
    gate: &[[Complex<f64>; 2]; 2],
    left: usize,
    right: usize,
) {
    let device = backend.device();
    let queue = backend.queue();

    let params = OneQubitParams {
        left: left as u32,
        right: right as u32,
        _pad0: 0,
        _pad1: 0,
        g00_re: gate[0][0].re as f32,
        g00_im: gate[0][0].im as f32,
        g01_re: gate[0][1].re as f32,
        g01_im: gate[0][1].im as f32,
        g10_re: gate[1][0].re as f32,
        g10_im: gate[1][0].im as f32,
        g11_re: gate[1][1].re as f32,
        g11_im: gate[1][1].im as f32,
    };
    let params_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("mps_1q params"),
        size: std::mem::size_of::<OneQubitParams>() as u64,
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    queue.write_buffer(&params_buf, 0, bytemuck::bytes_of(&params));

    let bg = device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("mps_1q BG"),
        layout: bgl,
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: tensor_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: params_buf.as_entire_binding(),
            },
        ],
    });

    let total = left * right;
    let workgroups = ((total as u32) + 63) / 64;
    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
        label: Some("mps_1q dispatch"),
    });
    {
        let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
            label: Some("mps_1q pass"),
            timestamp_writes: None,
        });
        pass.set_pipeline(pipeline);
        pass.set_bind_group(0, Some(&bg), &[]);
        pass.dispatch_workgroups(workgroups, 1, 1);
    }
    queue.submit(std::iter::once(encoder.finish()));
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cached_wgpu_mps_backend;
    use num_complex::Complex;
    use wgpu::util::DeviceExt as _;

    fn rand_complex(n: usize, seed: u64) -> Vec<Complex<f32>> {
        let mut state = seed;
        (0..n)
            .map(|_| {
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let re = ((state >> 33) as f32) / (u32::MAX as f32) * 2.0 - 1.0;
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let im = ((state >> 33) as f32) / (u32::MAX as f32) * 2.0 - 1.0;
                Complex::new(re, im)
            })
            .collect()
    }

    fn cpu_one_qubit(
        tensor: &mut [Complex<f32>],
        gate: &[[Complex<f64>; 2]; 2],
        left: usize,
        right: usize,
    ) {
        let g00 = Complex::new(gate[0][0].re as f32, gate[0][0].im as f32);
        let g01 = Complex::new(gate[0][1].re as f32, gate[0][1].im as f32);
        let g10 = Complex::new(gate[1][0].re as f32, gate[1][0].im as f32);
        let g11 = Complex::new(gate[1][1].re as f32, gate[1][1].im as f32);
        for l in 0..left {
            for r in 0..right {
                let idx0 = l * 2 * right + r;
                let idx1 = l * 2 * right + right + r;
                let v0 = tensor[idx0];
                let v1 = tensor[idx1];
                tensor[idx0] = g00 * v0 + g01 * v1;
                tensor[idx1] = g10 * v0 + g11 * v1;
            }
        }
    }

    fn download_buffer(
        device: &wgpu::Device,
        queue: &wgpu::Queue,
        buf: &wgpu::Buffer,
        n_elems: usize,
    ) -> Vec<Complex<f32>> {
        let size_bytes = (n_elems * 8) as u64;
        let staging = device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("test staging"),
            size: size_bytes,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
            label: Some("test download"),
        });
        encoder.copy_buffer_to_buffer(buf, 0, &staging, 0, size_bytes);
        queue.submit(std::iter::once(encoder.finish()));

        let slice = staging.slice(..);
        let (tx, rx) = std::sync::mpsc::channel();
        slice.map_async(wgpu::MapMode::Read, move |r| {
            let _ = tx.send(r);
        });
        device
            .poll(wgpu::PollType::wait_indefinitely())
            .expect("poll");
        rx.recv().expect("recv").expect("map");

        let data = slice.get_mapped_range();
        let floats: &[[f32; 2]] = bytemuck::cast_slice(&data);
        let result: Vec<Complex<f32>> = floats
            .iter()
            .map(|&[re, im]| Complex::new(re, im))
            .collect();
        drop(data);
        staging.unmap();
        result
    }

    fn rand_gate_2x2(seed: u64) -> [[Complex<f64>; 2]; 2] {
        let mut state = seed;
        let mut g = [[Complex::<f64>::new(0.0, 0.0); 2]; 2];
        for r in 0..2 {
            for c in 0..2 {
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let re = ((state >> 33) as f64) / (u32::MAX as f64) * 2.0 - 1.0;
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let im = ((state >> 33) as f64) / (u32::MAX as f64) * 2.0 - 1.0;
                g[r][c] = Complex::new(re, im);
            }
        }
        g
    }

    fn max_abs_error(a: &[Complex<f32>], b: &[Complex<f32>]) -> f32 {
        a.iter()
            .zip(b.iter())
            .map(|(x, y)| {
                let d = x - y;
                (d.re * d.re + d.im * d.im).sqrt()
            })
            .fold(0.0f32, f32::max)
    }

    #[test]
    fn one_qubit_matches_cpu_various_dims() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return;
        };
        let (pipeline, bgl) = build_one_qubit_pipeline(backend.device());

        for &(left, right) in &[(1, 1), (4, 4), (8, 16), (32, 32), (64, 64)] {
            let tensor_data = rand_complex(left * 2 * right, 42 + left as u64);
            let gate = rand_gate_2x2(137 + right as u64);

            // CPU reference
            let mut cpu_data = tensor_data.clone();
            cpu_one_qubit(&mut cpu_data, &gate, left, right);

            // GPU
            let raw: Vec<[f32; 2]> = tensor_data.iter().map(|c| [c.re, c.im]).collect();
            let tensor_buf =
                backend
                    .device()
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some("tensor"),
                        contents: bytemuck::cast_slice(&raw),
                        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
                    });

            dispatch_one_qubit_gate(
                &backend, &pipeline, &bgl, &tensor_buf, &gate, left, right,
            );

            let gpu_data = download_buffer(
                backend.device(),
                backend.queue(),
                &tensor_buf,
                left * 2 * right,
            );
            let err = max_abs_error(&gpu_data, &cpu_data);
            assert!(
                err < 1e-5,
                "1q gate ({left},{right}): max abs error {err} >= 1e-5"
            );
        }
    }
}
