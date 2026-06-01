//! Two-site contraction GPU dispatch (v0.6.7 Cut 5).
//!
//! [`dispatch_two_site_contract`] uploads `T_left`, `T_right`, and a 4×4
//! gate matrix, dispatches the `mps_two_site_contract.wgsl` compute shader,
//! and writes the fused result into `m_out_buf`.  The output is a row-major
//! `(chi_l·2) × (2·chi_r)` complex f32 matrix — ready for host SVD.
//!
//! This replaces Steps 1-3 of `Mps::apply_two_qubit_adjacent` on GPU.

use bytemuck::{Pod, Zeroable};
use num_complex::Complex;

use super::backend::WgpuMpsBackend;

/// Pod uniform for the contraction shader.
#[repr(C)]
#[derive(Copy, Clone, Debug, Pod, Zeroable)]
pub(crate) struct ContractParams {
    pub chi_l: u32,
    pub chi_m: u32,
    pub chi_r: u32,
    pub total: u32,
}

/// Build the two-site contraction pipeline + bind group layout.
pub(crate) fn build_contract_pipeline(
    device: &wgpu::Device,
) -> (wgpu::ComputePipeline, wgpu::BindGroupLayout) {
    let bgl = device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
        label: Some("mps_contract BGL"),
        entries: &[
            // binding 0: t_left (storage, read)
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
            // binding 1: t_right (storage, read)
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
            // binding 2: m_out (storage, read_write)
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
            // binding 4: gate (storage, read)
            wgpu::BindGroupLayoutEntry {
                binding: 4,
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
        label: Some("mps_contract layout"),
        bind_group_layouts: &[Some(&bgl)],
        immediate_size: 0,
    });
    let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
        label: Some("mps_contract shader"),
        source: wgpu::ShaderSource::Wgsl(
            include_str!("shaders/mps_two_site_contract.wgsl").into(),
        ),
    });
    let pipeline = device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
        label: Some("mps_contract pipeline"),
        layout: Some(&layout),
        module: &shader,
        entry_point: Some("main"),
        compilation_options: wgpu::PipelineCompilationOptions::default(),
        cache: None,
    });
    (pipeline, bgl)
}

/// Dispatch the two-site contraction shader.
///
/// Reads `t_left_buf` (T_q0) and `t_right_buf` (T_q1), applies the 4×4
/// `gate`, and writes the fused `(chi_l*2) × (2*chi_r)` row-major result
/// into `m_out_buf`.
///
/// # Buffer sizes
/// - `t_left_buf`:  `chi_l * 2 * chi_m * 8` bytes (vec2<f32> per element)
/// - `t_right_buf`: `chi_m * 2 * chi_r * 8` bytes
/// - `m_out_buf`:   `chi_l * 2 * 2 * chi_r * 8` bytes
///
/// All buffers must already be allocated on `backend.device()`.
pub fn dispatch_two_site_contract(
    backend: &WgpuMpsBackend,
    pipeline: &wgpu::ComputePipeline,
    bgl: &wgpu::BindGroupLayout,
    t_left_buf: &wgpu::Buffer,
    t_right_buf: &wgpu::Buffer,
    gate: &[[Complex<f64>; 4]; 4],
    chi_l: usize,
    chi_m: usize,
    chi_r: usize,
    m_out_buf: &wgpu::Buffer,
) {
    let device = backend.device();
    let queue = backend.queue();

    let total = chi_l * 2 * 2 * chi_r;

    // Upload gate as 16 vec2<f32> = 128 bytes.
    let gate_data: Vec<[f32; 2]> = (0..4)
        .flat_map(|r| (0..4).map(move |c| [gate[r][c].re as f32, gate[r][c].im as f32]))
        .collect();
    let gate_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("mps_contract gate"),
        size: 128,
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    queue.write_buffer(&gate_buf, 0, bytemuck::cast_slice(&gate_data));

    // Upload params uniform.
    let params = ContractParams {
        chi_l: chi_l as u32,
        chi_m: chi_m as u32,
        chi_r: chi_r as u32,
        total: total as u32,
    };
    let params_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("mps_contract params"),
        size: 16,
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    queue.write_buffer(&params_buf, 0, bytemuck::bytes_of(&params));

    // Bind group.
    let bg = device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("mps_contract BG"),
        layout: bgl,
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: t_left_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: t_right_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 2,
                resource: m_out_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 3,
                resource: params_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 4,
                resource: gate_buf.as_entire_binding(),
            },
        ],
    });

    // Dispatch.
    let workgroups = ((total as u32) + 63) / 64;
    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
        label: Some("mps_contract dispatch"),
    });
    {
        let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
            label: Some("mps_contract pass"),
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

    /// Reference CPU implementation of Steps 1-3 fused.
    fn cpu_two_site_contract(
        t_left: &[Complex<f32>],
        t_right: &[Complex<f32>],
        gate: &[[Complex<f64>; 4]; 4],
        chi_l: usize,
        chi_m: usize,
        chi_r: usize,
    ) -> Vec<Complex<f32>> {
        let rows = chi_l * 2;
        let cols = 2 * chi_r;
        let mut out = vec![Complex::<f32>::new(0.0, 0.0); rows * cols];
        for a in 0..chi_l {
            for pi_out in 0..2 {
                for pj_out in 0..2 {
                    for c in 0..chi_r {
                        let gate_row = (pj_out << 1) | pi_out;
                        let mut acc = Complex::<f32>::new(0.0, 0.0);
                        for pi_in in 0..2 {
                            for pj_in in 0..2 {
                                let gate_col = (pj_in << 1) | pi_in;
                                let g = Complex::new(
                                    gate[gate_row][gate_col].re as f32,
                                    gate[gate_row][gate_col].im as f32,
                                );
                                let mut inner = Complex::<f32>::new(0.0, 0.0);
                                for b in 0..chi_m {
                                    let l_idx = a * 2 * chi_m + pi_in * chi_m + b;
                                    let r_idx = b * 2 * chi_r + pj_in * chi_r + c;
                                    inner += t_left[l_idx] * t_right[r_idx];
                                }
                                acc += g * inner;
                            }
                        }
                        let row = a * 2 + pi_out;
                        let col = pj_out * chi_r + c;
                        out[row * cols + col] = acc;
                    }
                }
            }
        }
        out
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

    fn upload_complex(
        device: &wgpu::Device,
        label: &str,
        data: &[Complex<f32>],
    ) -> wgpu::Buffer {
        let raw: Vec<[f32; 2]> = data.iter().map(|c| [c.re, c.im]).collect();
        device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
            label: Some(label),
            contents: bytemuck::cast_slice(&raw),
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
        })
    }

    fn rand_complex(n: usize, seed: u64) -> Vec<Complex<f32>> {
        // Simple deterministic PRNG for tests.
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

    fn rand_gate(seed: u64) -> [[Complex<f64>; 4]; 4] {
        let mut state = seed;
        let mut g = [[Complex::<f64>::new(0.0, 0.0); 4]; 4];
        for r in 0..4 {
            for c in 0..4 {
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let re = ((state >> 33) as f64) / (u32::MAX as f64) * 2.0 - 1.0;
                state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                let im = ((state >> 33) as f64) / (u32::MAX as f64) * 2.0 - 1.0;
                g[r][c] = Complex::new(re, im);
            }
        }
        g
    }

    fn frobenius_rel_error(a: &[Complex<f32>], b: &[Complex<f32>]) -> f32 {
        let mut diff_sq = 0.0f64;
        let mut norm_sq = 0.0f64;
        for (x, y) in a.iter().zip(b.iter()) {
            let d = x - y;
            diff_sq += (d.re as f64) * (d.re as f64) + (d.im as f64) * (d.im as f64);
            norm_sq += (y.re as f64) * (y.re as f64) + (y.im as f64) * (y.im as f64);
        }
        if norm_sq == 0.0 {
            return diff_sq.sqrt() as f32;
        }
        (diff_sq / norm_sq).sqrt() as f32
    }

    #[test]
    fn contract_matches_cpu_various_chi() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return; // no GPU
        };
        let (pipeline, bgl) = build_contract_pipeline(backend.device());

        for &(chi_l, chi_m, chi_r) in &[
            (1, 1, 1),
            (2, 2, 2),
            (4, 8, 4),
            (8, 16, 8),
            (16, 32, 16),
            (32, 32, 32),
        ] {
            let t_left = rand_complex(chi_l * 2 * chi_m, 42 + chi_l as u64);
            let t_right = rand_complex(chi_m * 2 * chi_r, 137 + chi_r as u64);
            let gate = rand_gate(999 + chi_m as u64);

            let cpu_out = cpu_two_site_contract(&t_left, &t_right, &gate, chi_l, chi_m, chi_r);

            let tl_buf = upload_complex(backend.device(), "tl", &t_left);
            let tr_buf = upload_complex(backend.device(), "tr", &t_right);
            let out_len = chi_l * 2 * 2 * chi_r;
            let m_out_buf = backend.device().create_buffer(&wgpu::BufferDescriptor {
                label: Some("m_out"),
                size: (out_len * 8) as u64,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            });

            dispatch_two_site_contract(
                &backend, &pipeline, &bgl, &tl_buf, &tr_buf, &gate, chi_l, chi_m, chi_r,
                &m_out_buf,
            );

            let gpu_out = download_buffer(backend.device(), backend.queue(), &m_out_buf, out_len);
            let err = frobenius_rel_error(&gpu_out, &cpu_out);
            assert!(
                err < 1e-5,
                "contract chi=({chi_l},{chi_m},{chi_r}): rel error {err} >= 1e-5"
            );
        }
    }
}
