//! GPU-resident MPS state container (v0.6.7 Cut 8a).
//!
//! [`GpuMpsTensors`] keeps all N site tensors in pre-allocated GPU buffers,
//! enabling gate-to-gate execution without host↔GPU round-trips (except for
//! the SVD step, which stays on host per v0.6.6.2 lesson).
//!
//! # Design
//! - **Pre-allocation**: each buffer = `max_bond_dim × 2 × max_bond_dim × 8`
//!   bytes.  At χ=256, N=30: ~30 MiB total GPU memory.
//! - **Bond dim tracking**: `bond_dims[i] = (left, right)` tracks the actual
//!   tensor shape within the pre-allocated buffer.
//! - **No qsim-mps dependency**: upload/download use raw `Complex<f32>`
//!   slices.  The engine (qsim-simulator) bridges via `Mps::tensor_data_slice`
//!   / `Mps::set_tensor`.
//! - **SVD callback**: two-qubit gate + right-canonicalize take a
//!   [`GpuSvdProvider`] trait object to run host SVD without importing
//!   qsim-mps.

use std::sync::Arc;

use num_complex::Complex;
use wgpu::util::DeviceExt as _;

use super::absorb::dispatch_absorb_us;
use super::backend::WgpuMpsBackend;
use super::contraction::dispatch_two_site_contract;
use super::one_qubit::dispatch_one_qubit_gate;

// ---- SVD callback trait (mirrors MpsSvdProvider<f32> without qsim-mps dep) ----

/// Output from a thin SVD computation.
#[derive(Debug, Clone)]
pub struct GpuSvdOutput {
    /// `rows × keep` row-major U matrix.
    pub u_row_major: Vec<Complex<f32>>,
    /// `keep` singular values, descending.
    pub s: Vec<f32>,
    /// `keep × cols` row-major V^H matrix.
    pub vt_row_major: Vec<Complex<f32>>,
    /// Truncation error `Σ_{j>=keep} s_j²`.
    pub trunc_error_sq: f64,
    /// Actual rank kept.
    pub keep: usize,
}

/// Trait for host-side SVD — same semantics as `qsim_mps::MpsSvdProvider<f32>`
/// but defined in qsim-gpu to avoid circular deps.
pub trait GpuSvdProvider: std::fmt::Debug + Send + Sync {
    fn thin_svd(
        &self,
        m_row_major: &[Complex<f32>],
        rows: usize,
        cols: usize,
        max_keep: usize,
        trunc_threshold: f64,
    ) -> GpuSvdOutput;
}

// ---- CPU fallback threshold ----

/// χ below which the engine should skip GPU dispatch and use CPU fallback.
/// Exposed for the engine integration (Cut 8b).
pub const GPU_CHI_THRESHOLD: usize = 8;

// ---- Helper: Complex<f32> ↔ GPU buffer ----

fn complex_to_raw(src: &[Complex<f32>]) -> Vec<[f32; 2]> {
    src.iter().map(|c| [c.re, c.im]).collect()
}

fn raw_to_complex(src: &[[f32; 2]]) -> Vec<Complex<f32>> {
    src.iter().map(|&[re, im]| Complex::new(re, im)).collect()
}

// ---- SWAP gate (LSB convention, same as engine.rs) ----

fn swap_matrix_4x4() -> [[Complex<f64>; 4]; 4] {
    let z = Complex::new(0.0, 0.0);
    let o = Complex::new(1.0, 0.0);
    [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]]
}

// ============================================================================
// GpuMpsTensors
// ============================================================================

/// GPU-resident MPS state.  Each site's tensor lives in a pre-allocated
/// GPU buffer; bond dimensions are tracked on the host side.
pub struct GpuMpsTensors {
    n_qubits: usize,
    max_bond_dim: usize,
    /// One GPU buffer per site — pre-allocated to max size.
    buffers: Vec<wgpu::Buffer>,
    /// `(left_bond_dim, right_bond_dim)` per site.
    bond_dims: Vec<(usize, usize)>,
    backend: Arc<WgpuMpsBackend>,
}

impl GpuMpsTensors {
    /// Allocate GPU-resident storage for an N-qubit MPS.
    ///
    /// Each site buffer is pre-allocated to hold a tensor of shape
    /// `[max_bond_dim, 2, max_bond_dim]`.  Initial bond dims are all
    /// `(1, 1)` — matching `|0...0⟩`.
    pub fn new(backend: Arc<WgpuMpsBackend>, n_qubits: usize, max_bond_dim: usize) -> Self {
        let buf_size = (max_bond_dim * 2 * max_bond_dim * 8) as u64;

        let mut buffers = Vec::with_capacity(n_qubits);
        for i in 0..n_qubits {
            let buf = backend.device().create_buffer(&wgpu::BufferDescriptor {
                label: Some(&format!("mps_site_{i}")),
                size: buf_size,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            });
            buffers.push(buf);
        }

        let bond_dims = vec![(1, 1); n_qubits];

        Self {
            n_qubits,
            max_bond_dim,
            buffers,
            bond_dims,
            backend,
        }
    }

    pub fn n_qubits(&self) -> usize {
        self.n_qubits
    }

    pub fn max_bond_dim(&self) -> usize {
        self.max_bond_dim
    }

    /// Current bond dimensions `(left, right)` for site `i`.
    pub fn bond_dims(&self, site: usize) -> (usize, usize) {
        self.bond_dims[site]
    }

    /// Maximum actual χ across the two target sites (for threshold check).
    pub fn max_chi_at(&self, sites: &[usize]) -> usize {
        sites
            .iter()
            .map(|&s| {
                let (l, r) = self.bond_dims[s];
                l.max(r)
            })
            .max()
            .unwrap_or(1)
    }

    // ---- Upload / Download ----

    /// Upload raw tensor data for a single site.
    pub fn upload_tensor(&mut self, site: usize, data: &[Complex<f32>], left: usize, right: usize) {
        debug_assert_eq!(data.len(), left * 2 * right);
        let raw = complex_to_raw(data);
        self.backend
            .queue()
            .write_buffer(&self.buffers[site], 0, bytemuck::cast_slice(&raw));
        self.bond_dims[site] = (left, right);
    }

    /// Upload all site tensors from raw data slices.
    ///
    /// `tensors` is `[(data, left, right)]` for each site.
    pub fn upload_all(&mut self, tensors: &[(&[Complex<f32>], usize, usize)]) {
        assert_eq!(tensors.len(), self.n_qubits);
        for (i, &(data, left, right)) in tensors.iter().enumerate() {
            self.upload_tensor(i, data, left, right);
        }
    }

    /// Download a single site tensor from GPU.
    pub fn download_tensor(&self, site: usize) -> (Vec<Complex<f32>>, usize, usize) {
        let (left, right) = self.bond_dims[site];
        let n_elems = left * 2 * right;
        let data = self.download_buffer(&self.buffers[site], n_elems);
        (data, left, right)
    }

    /// Download all site tensors from GPU.
    ///
    /// Returns `Vec<(data, left, right)>` for each site.
    pub fn download_all(&self) -> Vec<(Vec<Complex<f32>>, usize, usize)> {
        (0..self.n_qubits)
            .map(|i| self.download_tensor(i))
            .collect()
    }

    // ---- One-qubit gate ----

    /// Apply a one-qubit gate on `qubit` in-place on GPU.  No host transfer.
    pub fn apply_one_qubit(&self, qubit: usize, gate: &[[Complex<f64>; 2]; 2]) {
        let (left, right) = self.bond_dims[qubit];
        dispatch_one_qubit_gate(
            &self.backend,
            self.backend.one_qubit_pipeline(),
            self.backend.one_qubit_bgl(),
            &self.buffers[qubit],
            gate,
            left,
            right,
        );
    }

    // ---- Two-qubit gate (adjacent) ----

    /// Apply a two-qubit gate to adjacent sites `q0` and `q0+1`.
    ///
    /// Steps:
    /// 1. GPU contraction shader → M' (chi_l*2 × 2*chi_r row-major)
    /// 2. Download M' to host
    /// 3. Host SVD via `svd_provider`
    /// 4. Upload new T_q0, T_q1 back to GPU
    ///
    /// Returns the truncation error from this SVD.
    pub fn apply_two_qubit_adjacent(
        &mut self,
        q0: usize,
        gate: &[[Complex<f64>; 4]; 4],
        max_bond_dim: usize,
        trunc_threshold: f64,
        svd: &dyn GpuSvdProvider,
    ) -> f64 {
        let q1 = q0 + 1;
        assert!(q1 < self.n_qubits, "q1 out of range");

        let chi_l = self.bond_dims[q0].0; // left bond of q0
        let chi_m = self.bond_dims[q0].1; // shared bond
        debug_assert_eq!(chi_m, self.bond_dims[q1].0);
        let chi_r = self.bond_dims[q1].1; // right bond of q1

        let rows = chi_l * 2;
        let cols = 2 * chi_r;
        let out_elems = rows * cols;

        // Step 1: GPU contraction
        let m_out_buf = self
            .backend
            .device()
            .create_buffer(&wgpu::BufferDescriptor {
                label: Some("mps_contract_out"),
                size: (out_elems * 8) as u64,
                usage: wgpu::BufferUsages::STORAGE
                    | wgpu::BufferUsages::COPY_SRC
                    | wgpu::BufferUsages::COPY_DST,
                mapped_at_creation: false,
            });

        dispatch_two_site_contract(
            &self.backend,
            self.backend.contract_pipeline(),
            self.backend.contract_bgl(),
            &self.buffers[q0],
            &self.buffers[q1],
            gate,
            chi_l,
            chi_m,
            chi_r,
            &m_out_buf,
        );

        // Step 2: Download M' for host SVD
        let m_data = self.download_buffer(&m_out_buf, out_elems);

        // Step 3: Host SVD
        let svd_out = svd.thin_svd(&m_data, rows, cols, max_bond_dim, trunc_threshold);
        let keep = svd_out.keep;

        // Step 4: Split into new T_q0, T_q1 and upload
        // T'_q0[a, pi', b] = U[(a*2+pi'), b]
        let mut new_l = vec![Complex::<f32>::new(0.0, 0.0); chi_l * 2 * keep];
        for a in 0..chi_l {
            for pip in 0..2 {
                let r_idx = a * 2 + pip;
                for b in 0..keep {
                    new_l[a * 2 * keep + pip * keep + b] = svd_out.u_row_major[r_idx * keep + b];
                }
            }
        }

        // T'_q1[b, pj', c] = sv[b] * V^H[b, pj'*chi_r + c]
        let mut new_r = vec![Complex::<f32>::new(0.0, 0.0); keep * 2 * chi_r];
        for b in 0..keep {
            let s_b = Complex::new(svd_out.s[b], 0.0f32);
            for pjp in 0..2 {
                for c in 0..chi_r {
                    let c_idx = pjp * chi_r + c;
                    new_r[b * 2 * chi_r + pjp * chi_r + c] =
                        s_b * svd_out.vt_row_major[b * cols + c_idx];
                }
            }
        }

        self.upload_tensor(q0, &new_l, chi_l, keep);
        self.upload_tensor(q1, &new_r, keep, chi_r);

        svd_out.trunc_error_sq
    }

    // ---- Two-qubit gate (general, with SWAP chain) ----

    /// Apply a two-qubit gate to sites `lo` and `hi` (lo < hi).
    ///
    /// If adjacent (hi == lo + 1), calls `apply_two_qubit_adjacent` directly.
    /// Otherwise, decomposes into a SWAP chain, all on GPU.
    ///
    /// Returns the total truncation error from all SVDs in this operation.
    pub fn apply_two_qubit_gate(
        &mut self,
        lo: usize,
        hi: usize,
        gate: &[[Complex<f64>; 4]; 4],
        max_bond_dim: usize,
        trunc_threshold: f64,
        svd: &dyn GpuSvdProvider,
    ) -> f64 {
        debug_assert!(lo < hi);
        if hi - lo == 1 {
            return self.apply_two_qubit_adjacent(lo, gate, max_bond_dim, trunc_threshold, svd);
        }

        let swap = swap_matrix_4x4();
        let mut total_err = 0.0;

        // Step 1: SWAP hi down to lo+1.
        for s in (lo + 1..hi).rev() {
            total_err +=
                self.apply_two_qubit_adjacent(s, &swap, max_bond_dim, trunc_threshold, svd);
        }

        // Step 2: Apply the actual gate at (lo, lo+1).
        total_err += self.apply_two_qubit_adjacent(lo, gate, max_bond_dim, trunc_threshold, svd);

        // Step 3: Undo SWAP chain.
        for s in lo + 1..hi {
            total_err +=
                self.apply_two_qubit_adjacent(s, &swap, max_bond_dim, trunc_threshold, svd);
        }

        total_err
    }

    // ---- Right-canonicalize (GPU hybrid) ----

    /// Right-canonicalize the MPS in-place.
    ///
    /// For each site from right to left:
    ///   1. Download tensor → host SVD
    ///   2. Upload V† as new tensor for site i
    ///   3. Compute US = U · diag(S) on host
    ///   4. Upload US → GPU absorption shader to absorb into site i-1
    ///
    /// The absorption step (4) runs on GPU, saving host↔GPU transfers for
    /// the left tensor.  SVD stays on host (v0.6.6.2 lesson).
    ///
    /// Returns total truncation error from eps-rank cutoff.
    pub fn right_canonicalize_hybrid(
        &mut self,
        trunc_threshold: f64,
        svd: &dyn GpuSvdProvider,
    ) -> f64 {
        if self.n_qubits <= 1 {
            return 0.0;
        }

        let mut total_err = 0.0;

        for i in (1..self.n_qubits).rev() {
            let (chi_l, chi_r) = self.bond_dims[i];
            let cols = 2 * chi_r;

            // Step 1: Download T_i → reshape → SVD on host
            let (tensor_data, _, _) = self.download_tensor(i);

            // Reshape T_i[chi_l, 2, chi_r] → M[chi_l, 2*chi_r] row-major.
            // T_i is already row-major with stride p*chi_r, so data layout
            // is M[a, p*chi_r + c] = T[a, p, c] — identical memory layout!
            let true_rank = chi_l.min(cols);
            let svd_out = svd.thin_svd(&tensor_data, chi_l, cols, true_rank, trunc_threshold);
            total_err += svd_out.trunc_error_sq;
            let keep = svd_out.keep;

            // Step 2: V† → new T_i[keep, 2, chi_r]
            let mut new_t_i = vec![Complex::<f32>::new(0.0, 0.0); keep * 2 * chi_r];
            for b in 0..keep {
                for p in 0..2 {
                    for c in 0..chi_r {
                        new_t_i[b * 2 * chi_r + p * chi_r + c] =
                            svd_out.vt_row_major[b * cols + p * chi_r + c];
                    }
                }
            }
            self.upload_tensor(i, &new_t_i, keep, chi_r);

            // Step 3: Compute US = U · diag(S) on host.
            // U is chi_l × keep row-major.
            let mut us_data = vec![Complex::<f32>::new(0.0, 0.0); chi_l * keep];
            for l in 0..chi_l {
                for b in 0..keep {
                    us_data[l * keep + b] =
                        svd_out.u_row_major[l * keep + b] * Complex::new(svd_out.s[b], 0.0f32);
                }
            }

            // Step 4: GPU absorption shader — T'_{i-1} = T_{i-1} × US
            let chi_ll = self.bond_dims[i - 1].0;
            let chi_l_old = self.bond_dims[i - 1].1;
            debug_assert_eq!(
                chi_l_old, chi_l,
                "bond mismatch at site {i}: expected {chi_l}, got {chi_l_old}"
            );

            let out_elems = chi_ll * 2 * keep;
            let absorb_out_buf = self
                .backend
                .device()
                .create_buffer(&wgpu::BufferDescriptor {
                    label: Some("mps_absorb_out"),
                    size: (out_elems * 8) as u64,
                    usage: wgpu::BufferUsages::STORAGE
                        | wgpu::BufferUsages::COPY_SRC
                        | wgpu::BufferUsages::COPY_DST,
                    mapped_at_creation: false,
                });

            // Upload US matrix to a temporary buffer.
            let us_raw = complex_to_raw(&us_data);
            let us_buf =
                self.backend
                    .device()
                    .create_buffer_init(&wgpu::util::BufferInitDescriptor {
                        label: Some("mps_us_matrix"),
                        contents: bytemuck::cast_slice(&us_raw),
                        usage: wgpu::BufferUsages::STORAGE,
                    });

            dispatch_absorb_us(
                &self.backend,
                self.backend.absorb_pipeline(),
                self.backend.absorb_bgl(),
                &self.buffers[i - 1],
                &us_buf,
                chi_ll,
                chi_l,
                keep,
                &absorb_out_buf,
            );

            // Copy result back into the pre-allocated site buffer.
            let copy_size = (out_elems * 8) as u64;
            let mut encoder =
                self.backend
                    .device()
                    .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                        label: Some("mps_absorb_copy"),
                    });
            encoder.copy_buffer_to_buffer(&absorb_out_buf, 0, &self.buffers[i - 1], 0, copy_size);
            self.backend
                .queue()
                .submit(std::iter::once(encoder.finish()));
            self.bond_dims[i - 1] = (chi_ll, keep);
        }

        total_err
    }

    // ---- Internal helpers ----

    fn download_buffer(&self, buf: &wgpu::Buffer, n_elems: usize) -> Vec<Complex<f32>> {
        let device = self.backend.device();
        let queue = self.backend.queue();
        let size_bytes = (n_elems * 8) as u64;

        let staging = device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("mps_download_staging"),
            size: size_bytes,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
            label: Some("mps_download"),
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
            .expect("device.poll failed during MPS download");
        rx.recv()
            .expect("map recv failed")
            .expect("map_async failed");

        let data = slice.get_mapped_range();
        let floats: &[[f32; 2]] = bytemuck::cast_slice(&data);
        let result = raw_to_complex(floats);
        drop(data);
        staging.unmap();
        result
    }
}

impl std::fmt::Debug for GpuMpsTensors {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GpuMpsTensors")
            .field("n_qubits", &self.n_qubits)
            .field("max_bond_dim", &self.max_bond_dim)
            .field("bond_dims", &self.bond_dims)
            .finish()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cached_wgpu_mps_backend;

    /// Trivial SVD provider for tests — uses nalgebra directly.
    #[derive(Debug)]
    struct TestSvdProvider;

    impl GpuSvdProvider for TestSvdProvider {
        fn thin_svd(
            &self,
            m_row_major: &[Complex<f32>],
            rows: usize,
            cols: usize,
            max_keep: usize,
            trunc_threshold: f64,
        ) -> GpuSvdOutput {
            use nalgebra::DMatrix;
            let m = DMatrix::<Complex<f32>>::from_row_slice(rows, cols, m_row_major);
            // Loosened convergence epsilon — nalgebra's default `.svd()` can
            // over-converge and corrupt near-rank-deficient matrices (see the
            // v0.7 note in qsim_mps::CpuSvdProvider::thin_svd).
            let eps = f32::EPSILON * 64.0;
            let svd = m
                .clone()
                .try_svd(true, true, eps, 0)
                .unwrap_or_else(|| m.svd(true, true));
            let u_svd = svd.u.expect("U");
            let v_t = svd.v_t.expect("V^H");
            let sv = svd.singular_values;
            let k = sv.len();

            let eps_rank = if trunc_threshold > 0.0 {
                let eps = trunc_threshold as f32;
                sv.iter().take_while(|&&s| s >= eps).count()
            } else {
                k
            };
            let keep = k.min(max_keep).min(eps_rank).max(1);

            let trunc_error_sq: f64 = if keep < k {
                (keep..k).map(|j| (sv[j] as f64) * (sv[j] as f64)).sum()
            } else {
                0.0
            };

            let mut u_row_major = vec![Complex::<f32>::new(0.0, 0.0); rows * keep];
            for r in 0..rows {
                for b in 0..keep {
                    u_row_major[r * keep + b] = u_svd[(r, b)];
                }
            }
            let mut vt_row_major = vec![Complex::<f32>::new(0.0, 0.0); keep * cols];
            for b in 0..keep {
                for c in 0..cols {
                    vt_row_major[b * cols + c] = v_t[(b, c)];
                }
            }
            let s: Vec<f32> = (0..keep).map(|j| sv[j]).collect();

            GpuSvdOutput {
                u_row_major,
                s,
                vt_row_major,
                trunc_error_sq,
                keep,
            }
        }
    }

    #[test]
    fn upload_download_roundtrip() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return;
        };
        let mut gpu = GpuMpsTensors::new(backend, 3, 16);

        // Site 0: [1, 2, 1] = |0⟩
        let data0 = vec![Complex::new(1.0f32, 0.0), Complex::new(0.0, 0.0)];
        gpu.upload_tensor(0, &data0, 1, 1);

        let (dl, left, right) = gpu.download_tensor(0);
        assert_eq!(left, 1);
        assert_eq!(right, 1);
        assert_eq!(dl.len(), 2);
        assert!((dl[0].re - 1.0).abs() < 1e-7);
        assert!(dl[1].norm() < 1e-7);

        // Larger tensor
        let n = 4 * 2 * 8;
        let data1: Vec<Complex<f32>> = (0..n)
            .map(|i| Complex::new(i as f32, -(i as f32)))
            .collect();
        gpu.upload_tensor(1, &data1, 4, 8);

        let (dl1, l1, r1) = gpu.download_tensor(1);
        assert_eq!(l1, 4);
        assert_eq!(r1, 8);
        for (a, b) in dl1.iter().zip(data1.iter()) {
            assert!((a - b).norm() < 1e-5, "mismatch: {a} vs {b}");
        }
    }

    #[test]
    fn one_qubit_gate_on_gpu_resident() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return;
        };
        let mut gpu = GpuMpsTensors::new(backend, 2, 16);

        // |0⟩ state
        let data = vec![Complex::new(1.0f32, 0.0), Complex::new(0.0, 0.0)];
        gpu.upload_tensor(0, &data, 1, 1);

        // Apply Hadamard
        let inv_sqrt2 = 1.0 / std::f64::consts::SQRT_2;
        let h = [
            [Complex::new(inv_sqrt2, 0.0), Complex::new(inv_sqrt2, 0.0)],
            [Complex::new(inv_sqrt2, 0.0), Complex::new(-inv_sqrt2, 0.0)],
        ];
        gpu.apply_one_qubit(0, &h);

        let (result, _, _) = gpu.download_tensor(0);
        let expected = inv_sqrt2 as f32;
        assert!(
            (result[0].re - expected).abs() < 1e-6,
            "H|0⟩[0] = {}, expected {}",
            result[0].re,
            expected
        );
        assert!(
            (result[1].re - expected).abs() < 1e-6,
            "H|0⟩[1] = {}, expected {}",
            result[1].re,
            expected
        );
    }

    #[test]
    fn two_qubit_adjacent_cnot() {
        let Ok(backend) = cached_wgpu_mps_backend() else {
            return;
        };
        let svd = TestSvdProvider;
        let mut gpu = GpuMpsTensors::new(backend, 2, 16);

        // Start: |+⟩ ⊗ |0⟩ — should produce Bell state after CNOT.
        let inv_sqrt2 = 1.0 / std::f64::consts::SQRT_2;

        // Site 0 = |+⟩ = (|0⟩ + |1⟩)/√2
        let data0 = vec![
            Complex::new(inv_sqrt2 as f32, 0.0),
            Complex::new(inv_sqrt2 as f32, 0.0),
        ];
        gpu.upload_tensor(0, &data0, 1, 1);

        // Site 1 = |0⟩
        let data1 = vec![Complex::new(1.0f32, 0.0), Complex::new(0.0, 0.0)];
        gpu.upload_tensor(1, &data1, 1, 1);

        // CNOT (q1=control, q0=target) in LSB convention
        let z = Complex::new(0.0, 0.0);
        let o = Complex::new(1.0, 0.0);
        let cnot = [[o, z, z, z], [z, o, z, z], [z, z, z, o], [z, z, o, z]];

        let err = gpu.apply_two_qubit_adjacent(0, &cnot, 16, 0.0, &svd);
        assert!(err < 1e-10, "CNOT truncation error: {err}");

        // Bond dim should be 2 (Bell state).
        assert_eq!(gpu.bond_dims(0), (1, 2));
        assert_eq!(gpu.bond_dims(1), (2, 1));
    }
}
