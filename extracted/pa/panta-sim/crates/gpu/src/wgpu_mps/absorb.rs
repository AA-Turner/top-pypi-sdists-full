//! Absorption shader dispatch for right-canonicalize (v0.6.7 Cut 5c).
//!
//! [`dispatch_absorb_us`] multiplies an MPS site tensor `T_{i-1}` by a
//! pre-computed `US` matrix (U·diag(S) from the SVD of the next site),
//! writing the result into a separate output buffer.

use bytemuck::{Pod, Zeroable};

use super::backend::WgpuMpsBackend;

/// Pod uniform for the absorption shader.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
pub(crate) struct AbsorbParams {
    pub chi_ll: u32,
    pub chi_l: u32,
    pub keep: u32,
    pub total: u32,
}

/// Build the absorption pipeline + bind group layout.
pub(crate) fn build_absorb_pipeline(
    device: &wgpu::Device,
) -> (wgpu::ComputePipeline, wgpu::BindGroupLayout) {
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some("mps_absorb BGL"),
        entries: &[
            // binding 0: tensor_in (storage, read)
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
            // binding 1: us_matrix (storage, read)
            wgpu::BindGroupLayoutEntry {
                binding: 1,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: true },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            // binding 2: tensor_out (storage, read_write)
            wgpu::BindGroupLayoutEntry {
                binding: 2,
                visibility: wgpu::ShaderStages::COMPUTE,
                ty: wgpu::BindingType::Buffer {
                    ty: wgpu::BufferBindingType::Storage { read_only: false },
                    has_dynamic_offset: false,
                    min_binding_size: None,
                },
                count: None,
            },
            // binding 3: params (uniform)
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
        label: Some("mps_absorb layout"),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("mps_absorb shader"),
        source: wgpu::ShaderSource::Wgsl(include_str!("shaders/mps_absorb_us.wgsl").into()),
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("mps_absorb pipeline"),
        layout: Some(&layout),
        module: &shader,
        entry_point: Some("main"),
        compilation_options: wgpu::PipelineCompilationOptions::default(),
        cache: None,
    });
    (pipeline, bgl)
}

/// Dispatch the absorption shader.
///
/// Computes `T'_{i-1}[a, p, b] = Σ_l T_{i-1}[a, p, l] · US[l, b]`.
///
/// # Buffer sizes
/// - `tensor_in_buf`:  `chi_ll * 2 * chi_l * 8` bytes
/// - `us_buf`:         `chi_l * keep * 8` bytes
/// - `tensor_out_buf`: `chi_ll * 2 * keep * 8` bytes
#[allow(clippy::too_many_arguments)]
pub fn dispatch_absorb_us(
    backend: &WgpuMpsBackend,
    pipeline: &wgpu::ComputePipeline,
    bgl: &wgpu::BindGroupLayout,
    tensor_in_buf: &wgpu::Buffer,
    us_buf: &wgpu::Buffer,
    chi_ll: usize,
    chi_l: usize,
    keep: usize,
    tensor_out_buf: &wgpu::Buffer,
) {
    let device = backend.device();
    let queue = backend.queue();

    let total = chi_ll * 2 * keep;
    let params = AbsorbParams {
        chi_ll: chi_ll as u32,
        chi_l: chi_l as u32,
        keep: keep as u32,
        total: total as u32,
    };
    let params_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("mps_absorb params"),
        size: 16,
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    queue.write_buffer(&params_buf, 0, bytemuck::bytes_of(&params));

    let bg = device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("mps_absorb BG"),
        layout: bgl,
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: tensor_in_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: us_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 2,
                resource: tensor_out_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 3,
                resource: params_buf.as_entire_binding(),
            },
        ],
    });

    let workgroups = (total as u32).div_ceil(64);
    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
        label: Some("mps_absorb dispatch"),
    });
    {
        let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
            label: Some("mps_absorb pass"),
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

    fn cpu_absorb(
        tensor_in: &[Complex<f32>],
        us_matrix: &[Complex<f32>],
        chi_ll: usize,
        chi_l: usize,
        keep: usize,
    ) -> Vec<Complex<f32>> {
        let mut out = vec![Complex::<f32>::new(0.0, 0.0); chi_ll * 2 * keep];
        for a in 0..chi_ll {
            for p in 0..2 {
                for b in 0..keep {
                    let mut acc = Complex::<f32>::new(0.0, 0.0);
                    for l in 0..chi_l {
                        let t_idx = a * 2 * chi_l + p * chi_l + l;
                        let us_idx = l * keep + b;
                        acc += tensor_in[t_idx] * us_matrix[us_idx];
                    }
                    let out_idx = a * 2 * keep + p * keep + b;
                    out[out_idx] = acc;
                }
            }
        }
        out
    }

    fn upload_complex(
        device: &wgpu::Device,
        label: &str,
        data: &[Complex<f32>],
        extra_usage: wgpu::BufferUsages,
    ) -> wgpu::Buffer {
        let raw: Vec<[f32; 2]> = data.iter().map(|c| [c.re, c.im]).collect();
        device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
            label: Some(label),
            contents: bytemuck::cast_slice(&raw),
            usage: wgpu::BufferUsages::STORAGE | extra_usage,
        })
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
    fn absorb_matches_cpu_various_dims() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return;
        };
        let (pipeline, bgl) = build_absorb_pipeline(backend.device());

        for &(chi_ll, chi_l, keep) in
            &[(1, 1, 1), (4, 4, 2), (8, 16, 8), (16, 32, 16), (32, 32, 24)]
        {
            let tensor_in = rand_complex(chi_ll * 2 * chi_l, 42 + chi_ll as u64);
            let us_matrix = rand_complex(chi_l * keep, 137 + keep as u64);

            let cpu_out = cpu_absorb(&tensor_in, &us_matrix, chi_ll, chi_l, keep);

            let tin_buf = upload_complex(
                backend.device(),
                "tin",
                &tensor_in,
                wgpu::BufferUsages::empty(),
            );
            let us_buf = upload_complex(
                backend.device(),
                "us",
                &us_matrix,
                wgpu::BufferUsages::empty(),
            );
            let out_len = chi_ll * 2 * keep;
            let tout_buf = backend.device().create_buffer(&wgpu::BufferDescriptor {
                label: Some("tout"),
                size: (out_len * 8) as u64,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            });

            dispatch_absorb_us(
                &backend, &pipeline, &bgl, &tin_buf, &us_buf, chi_ll, chi_l, keep, &tout_buf,
            );

            let gpu_out = download_buffer(backend.device(), backend.queue(), &tout_buf, out_len);
            let err = max_abs_error(&gpu_out, &cpu_out);
            assert!(
                err < 1e-4,
                "absorb ({chi_ll},{chi_l},{keep}): max abs error {err} >= 1e-4"
            );
        }
    }
}
