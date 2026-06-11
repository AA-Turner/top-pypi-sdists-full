//! `qsim-mps` — Matrix Product State (MPS, 1D tensor network) backend for
//! panta-sim.  Stage 1 (v0.6.0-alpha) provides the standalone MPS data
//! structure with single-qubit gates, adjacent two-qubit gates with SVD
//! truncation, and a debug `statevector()` round-trip.  Simulator engine
//! integration and Python bindings are deferred to Stage 2.
//!
//! # Conventions
//!
//! - Qubit ordering: little-endian (qubit 0 = LSB).  Statevector index
//!   `b = s_0 + s_1·2 + ... + s_{n-1}·2^{n-1}`, matching
//!   `qsim_core::StateVector`.
//! - Tensor `T_i` shape `[chi_left, 2, chi_right]` stored row-major in a
//!   flat `Vec<Complex<f64>>`: `T[l, p, r] = data[l * 2 * right + p * right + r]`.
//! - Bond sentinel: site 0 has `chi_left = 1`, site `n - 1` has
//!   `chi_right = 1`; both are not stored separately — `MPS::bond_dim(i)`
//!   returns the chi between site `i - 1` and `i` (or 1 at the boundaries).
//! - Precision: generic over `F: Real` since v0.6.5 — both `f32` and
//!   `f64` are supported.  Convenience type aliases [`MpsF64`] and
//!   [`MpsF32`] are provided.  `truncation_error_sum` is always
//!   accumulated in `f64` regardless of `F` to avoid catastrophic
//!   cancellation when many tiny ε² values are summed.
//!
//! See `docs/plan.md` (v0.6 — Tensor Network / MPS section) for the full
//! roadmap.

#![allow(clippy::many_single_char_names)]

use std::collections::HashMap;
use std::sync::Arc;

use nalgebra::DMatrix;
use num_complex::Complex;
use num_traits::Zero;
use qsim_core::complex::Real;
use rand::Rng;
use rayon::prelude::*;

/// Threshold above which hot loops switch to rayon parallel iteration
/// (v0.6.5).  Below this, rayon's task-spawn overhead exceeds the gain on
/// the small inner kernels — chosen by the same rule of thumb as the
/// v0.2.0 statevector rayon tuning.  Compared against `chi_l * chi_r` or
/// equivalent product of the parallel-by extent and the inner-reduce
/// extent.
const PAR_THRESHOLD: usize = 32;

/// Scalars usable for [`Mps`] — currently `f32` and `f64`.  This combines
/// the qsim_core [`Real`] trait (numeric ops + rayon `Send` / `Sync`)
/// with `nalgebra::RealField`, which is required so that
/// `nalgebra::ComplexField<RealField = F>` holds for `Complex<F>` and we
/// can call `DMatrix::<Complex<F>>::svd` (v0.6.5 generic refactor).
pub trait MpsScalar: Real + nalgebra::RealField {}

/// Pluggable thin-SVD provider for the truncating SVD step inside
/// [`Mps::apply_two_qubit_adjacent`] and [`Mps::right_canonicalize`]
/// (v0.6.6 Cut 6).
///
/// Allows swapping the default CPU (`nalgebra`) implementation for a
/// GPU one (`qsim_gpu::wgpu_thin_svd`).
///
/// # Convention
/// - `m_row_major`: input matrix, shape `rows × cols`, row-major.
/// - `max_keep`: hard cap on returned singular values (e.g.
///   `max_bond_dim`).
/// - `trunc_threshold`: drop singular values `s_i < trunc_threshold`
///   (set `0.0` to disable eps-rank cutoff).  `f64` so the user can
///   write a single small literal regardless of `F`.
///
/// Returned `keep = min(true_rank_by_eps, max_keep).max(1)` — must
/// always be `>= 1`.  `trunc_error_sq = Σ_{j >= keep} s_j²` in `f64`.
pub trait MpsSvdProvider<F: MpsScalar>: std::fmt::Debug + Send + Sync {
    fn thin_svd(
        &self,
        m_row_major: &[Complex<F>],
        rows: usize,
        cols: usize,
        max_keep: usize,
        trunc_threshold: f64,
    ) -> MpsSvdProviderOutput<F>;
}

/// Output of [`MpsSvdProvider::thin_svd`].
#[derive(Debug, Clone)]
pub struct MpsSvdProviderOutput<F: MpsScalar> {
    /// `rows × keep` row-major.  Orthonormal columns.
    pub u_row_major: Vec<Complex<F>>,
    /// `keep` singular values, descending.
    pub s: Vec<F>,
    /// `keep × cols` row-major.  `V^H` (Hermitian transpose of `V`).
    pub vt_row_major: Vec<Complex<F>>,
    /// Accumulated truncation error `Σ_{j >= keep} s_j²` (always `f64`).
    pub trunc_error_sq: f64,
    /// Actual rank kept after truncation (`>= 1`).
    pub keep: usize,
}

/// Default CPU thin-SVD provider — `nalgebra::DMatrix::svd` (v0.6.6 Cut 6).
///
/// This is what every `Mps<F>` uses by default; matches v0.6.5
/// byte-for-byte.
#[derive(Debug, Default, Clone, Copy)]
pub struct CpuSvdProvider;

impl<F: MpsScalar> MpsSvdProvider<F> for CpuSvdProvider {
    fn thin_svd(
        &self,
        m_row_major: &[Complex<F>],
        rows: usize,
        cols: usize,
        max_keep: usize,
        trunc_threshold: f64,
    ) -> MpsSvdProviderOutput<F> {
        debug_assert_eq!(m_row_major.len(), rows * cols);
        let m_mat = DMatrix::<Complex<F>>::from_row_slice(rows, cols, m_row_major);
        // v0.7 fix: nalgebra's Golub–Reinsch `.svd()` can **silently return a
        // wrong factorisation** for near-rank-deficient matrices (large entries
        // mixed with ~1e-16 noise — common in an MPS after several gates): it
        // over-converges and yields `U·Σ·Vᴴ ≠ M` (observed σ₁ = 1.4487 for a
        // matrix with ‖M‖_F = √2, impossible), silently corrupting the MPS
        // (norm ≠ 1).  [`reliable_svd`] validates the reconstruction and falls
        // back to a Gram-matrix Hermitian eigendecomposition (numerically
        // robust) when nalgebra's iterative SVD misbehaves.
        let (u_svd, sv, v_t) = reliable_svd::<F>(&m_mat);
        let k = sv.len();

        let eps_rank = if trunc_threshold > 0.0 {
            let eps_f = F::from(trunc_threshold).unwrap_or_else(F::zero);
            // singular values are descending → count the leading run ≥ eps.
            sv.iter().take_while(|&&s| s >= eps_f).count()
        } else {
            k
        };
        let keep = k.min(max_keep).min(eps_rank).max(1);

        let trunc_error_sq: f64 = if keep < k {
            (keep..k)
                .map(|j| {
                    let s = sv[j].to_f64().unwrap_or(0.0);
                    s * s
                })
                .sum()
        } else {
            0.0
        };

        // Pack U as `rows × keep` row-major.
        let mut u_row_major = vec![Complex::<F>::zero(); rows * keep];
        for r in 0..rows {
            for b in 0..keep {
                u_row_major[r * keep + b] = u_svd[(r, b)];
            }
        }
        // Pack V^H as `keep × cols` row-major.
        let mut vt_row_major = vec![Complex::<F>::zero(); keep * cols];
        for b in 0..keep {
            for c in 0..cols {
                vt_row_major[b * cols + c] = v_t[(b, c)];
            }
        }
        let s: Vec<F> = (0..keep).map(|j| sv[j]).collect();

        MpsSvdProviderOutput {
            u_row_major,
            s,
            vt_row_major,
            trunc_error_sq,
            keep,
        }
    }
}
impl MpsScalar for f32 {}
impl MpsScalar for f64 {}

/// Numerically robust thin SVD `M = U Σ Vᴴ` returning `(U: rows×k, Σ: len k,
/// Vᴴ: k×cols)` with `k = min(rows, cols)`, singular values descending.
///
/// Fast path: nalgebra `try_svd` with a loosened convergence epsilon, then
/// **validate** the reconstruction.  If the iterative SVD misbehaves (it can,
/// for near-rank-deficient matrices — see the v0.7 bug note in
/// `apply_two_qubit_adjacent`), fall back to [`gram_svd`], which derives the
/// factorisation from the Hermitian eigendecomposition of the smaller Gram
/// matrix (`M Mᴴ` or `Mᴴ M`) — numerically reliable in nalgebra.
fn reliable_svd<F: MpsScalar>(
    m: &DMatrix<Complex<F>>,
) -> (DMatrix<Complex<F>>, Vec<F>, DMatrix<Complex<F>>) {
    let (rows, cols) = m.shape();
    let eps0 = F::epsilon() * F::from_f64(64.0).unwrap_or_else(F::one);
    if let Some(svd) = m.clone().try_svd(true, true, eps0, 0) {
        if let (Some(u), Some(vt)) = (svd.u, svd.v_t) {
            let s: Vec<F> = svd.singular_values.iter().cloned().collect();
            if svd_reconstructs::<F>(m, &u, &s, &vt) {
                return (u, s, vt);
            }
        }
    }
    gram_svd::<F>(m, rows, cols)
}

/// `‖U Σ Vᴴ − M‖_F ≤ tol · ‖M‖_F` with a precision-appropriate relative
/// tolerance (`√ε`: ~1.5e-8 for f64, ~3.4e-4 for f32).
fn svd_reconstructs<F: MpsScalar>(
    m: &DMatrix<Complex<F>>,
    u: &DMatrix<Complex<F>>,
    s: &[F],
    vt: &DMatrix<Complex<F>>,
) -> bool {
    let (rows, cols) = m.shape();
    let k = s.len();
    if u.ncols() < k || vt.nrows() < k {
        return false;
    }
    let mut err = 0.0f64;
    let mut nrm = 0.0f64;
    for i in 0..rows {
        for j in 0..cols {
            let mut acc = Complex::<F>::zero();
            for (b, &sb) in s.iter().enumerate().take(k) {
                acc += u[(i, b)] * Complex::new(sb, F::zero()) * vt[(b, j)];
            }
            err += (acc - m[(i, j)]).norm_sqr().to_f64().unwrap_or(0.0);
            nrm += m[(i, j)].norm_sqr().to_f64().unwrap_or(0.0);
        }
    }
    let tol = F::epsilon().to_f64().unwrap_or(1e-16).sqrt();
    err.sqrt() <= tol * nrm.sqrt() + 1e-30
}

/// Gram-matrix SVD fallback (Hermitian eigendecomposition of the smaller of
/// `M Mᴴ` / `Mᴴ M`).  Singular values descending, reconstruction exact up to
/// eigensolver precision.
fn gram_svd<F: MpsScalar>(
    m: &DMatrix<Complex<F>>,
    rows: usize,
    cols: usize,
) -> (DMatrix<Complex<F>>, Vec<F>, DMatrix<Complex<F>>) {
    let kdim = rows.min(cols);
    if rows <= cols {
        // G = M Mᴴ  (rows×rows Hermitian PSD).  G = W Λ Wᴴ → U = W, σ = √Λ,
        // Vᴴ = diag(1/σ) Uᴴ M (rows with σ≈0 left zero — they carry no weight).
        let g = m * m.adjoint();
        let eig = g.symmetric_eigen();
        let order = sorted_desc::<F>(&eig.eigenvalues);
        let mut u = DMatrix::<Complex<F>>::zeros(rows, kdim);
        let mut s = vec![F::zero(); kdim];
        for (newc, &oldc) in order.iter().enumerate().take(kdim) {
            let lam = eig.eigenvalues[oldc];
            s[newc] = if lam > F::zero() {
                num_traits::Float::sqrt(lam)
            } else {
                F::zero()
            };
            for r in 0..rows {
                u[(r, newc)] = eig.eigenvectors[(r, oldc)];
            }
        }
        let uh_m = u.adjoint() * m; // kdim×cols
        let mut vt = DMatrix::<Complex<F>>::zeros(kdim, cols);
        let thresh = s.first().copied().unwrap_or_else(F::zero)
            * F::epsilon()
            * F::from_f64(16.0).unwrap_or_else(F::one);
        for i in 0..kdim {
            if s[i] > thresh {
                let inv = Complex::new(F::one() / s[i], F::zero());
                for j in 0..cols {
                    vt[(i, j)] = uh_m[(i, j)] * inv;
                }
            }
        }
        (u, s, vt)
    } else {
        // G = Mᴴ M  (cols×cols Hermitian PSD).  G = V Λ Vᴴ → Vᴴ = Vᴴ, σ = √Λ,
        // U = M V diag(1/σ).
        let g = m.adjoint() * m;
        let eig = g.symmetric_eigen();
        let order = sorted_desc::<F>(&eig.eigenvalues);
        let mut vmat = DMatrix::<Complex<F>>::zeros(cols, kdim);
        let mut s = vec![F::zero(); kdim];
        for (newc, &oldc) in order.iter().enumerate().take(kdim) {
            let lam = eig.eigenvalues[oldc];
            s[newc] = if lam > F::zero() {
                num_traits::Float::sqrt(lam)
            } else {
                F::zero()
            };
            for r in 0..cols {
                vmat[(r, newc)] = eig.eigenvectors[(r, oldc)];
            }
        }
        let m_v = m * &vmat; // rows×kdim
        let mut u = DMatrix::<Complex<F>>::zeros(rows, kdim);
        let thresh = s.first().copied().unwrap_or_else(F::zero)
            * F::epsilon()
            * F::from_f64(16.0).unwrap_or_else(F::one);
        for i in 0..kdim {
            if s[i] > thresh {
                let inv = Complex::new(F::one() / s[i], F::zero());
                for r in 0..rows {
                    u[(r, i)] = m_v[(r, i)] * inv;
                }
            }
        }
        let vt = vmat.adjoint(); // kdim×cols
        (u, s, vt)
    }
}

/// Indices that sort `vals` in descending order.
fn sorted_desc<F: MpsScalar>(vals: &nalgebra::DVector<F>) -> Vec<usize> {
    let mut idx: Vec<usize> = (0..vals.len()).collect();
    idx.sort_by(|&a, &b| {
        vals[b]
            .partial_cmp(&vals[a])
            .unwrap_or(std::cmp::Ordering::Equal)
    });
    idx
}

/// Construct a [`Complex<F>`] from two `f64` real / imag parts via
/// [`num_traits::cast`].  All gate coefficients flow through this helper
/// — gate matrices are written as `Complex<f64>` literals in user code
/// (and in the simulator's gate library) and need converting to `Complex<F>`
/// on the way into the MPS for the f32 generic path.
#[inline]
fn cf<F: MpsScalar>(re: f64, im: f64) -> Complex<F> {
    Complex::new(
        F::from(re).expect("real part must fit in F"),
        F::from(im).expect("imag part must fit in F"),
    )
}

/// Convert one element of a `Complex<f64>` gate matrix to `Complex<F>`.
#[inline]
fn gconv<F: MpsScalar>(z: Complex<f64>) -> Complex<F> {
    cf::<F>(z.re, z.im)
}

/// One MPS site tensor `T_i` of shape `[left, 2, right]`, stored row-major.
///
/// Indexing: `data[l * 2 * right + p * right + r]` for left-bond index
/// `l ∈ 0..left`, physical index `p ∈ {0, 1}`, right-bond index
/// `r ∈ 0..right`.  Generic over [`MpsScalar`] since v0.6.5.
#[derive(Debug, Clone)]
pub(crate) struct Tensor3<F: MpsScalar> {
    pub left: usize,
    pub right: usize,
    pub data: Vec<Complex<F>>,
}

impl<F: MpsScalar> Tensor3<F> {
    /// Construct a tensor with the given bond dimensions and pre-built
    /// row-major data buffer.  Panics if the buffer length does not match
    /// `left * 2 * right`.
    pub fn new(left: usize, right: usize, data: Vec<Complex<F>>) -> Self {
        assert_eq!(
            data.len(),
            left * 2 * right,
            "Tensor3 data length must equal left * 2 * right"
        );
        Self { left, right, data }
    }

    #[inline]
    pub fn idx(&self, l: usize, p: usize, r: usize) -> usize {
        l * 2 * self.right + p * self.right + r
    }

    #[inline]
    pub fn get(&self, l: usize, p: usize, r: usize) -> Complex<F> {
        self.data[self.idx(l, p, r)]
    }
}

/// Matrix Product State for an N-qubit pure state.
///
/// Stage 1 supports only adjacent two-qubit gates and provides a debug
/// `statevector()` for `n_qubits ≤ 20`.  See the module-level docs for
/// conventions.
#[derive(Debug, Clone)]
pub struct Mps<F: MpsScalar> {
    n_qubits: usize,
    tensors: Vec<Tensor3<F>>,
    max_bond_dim: usize,
    /// Singular-value cutoff (`s_i < trunc_threshold` are dropped).
    /// `0.0` (default) disables cutoff and falls back to the legacy
    /// "rank cap only" behaviour — bit-identical to v0.6.3.  v0.6.5
    /// (Schollwöck 2011 §4.5.3 ε-rank cutoff).  Stored as `f64`
    /// independent of `F` so the user can write a single small literal
    /// (e.g. `1e-10`) regardless of precision; the comparison happens
    /// against `F`-typed singular values via cast.
    trunc_threshold: f64,
    /// Cumulative absolute truncation error `Σ_{j>keep} sv_j²` — added
    /// across every truncating SVD inside [`Mps::apply_two_qubit_adjacent`]
    /// **and**, when `trunc_threshold > 0`, every cutoff drop inside
    /// [`Mps::right_canonicalize`].  Schollwöck 2011 §4.5.3 standard
    /// discarded-weight metric.  Stored as `f64` independent of `F` to
    /// avoid catastrophic cancellation when many tiny ε² values are
    /// summed across long circuits — even when the MPS itself runs in
    /// `f32`.  v0.6.3 / extended v0.6.5.
    truncation_error_sum: f64,
    /// SVD backend used by [`Mps::apply_two_qubit_adjacent`].  Default
    /// [`CpuSvdProvider`] (nalgebra).  v0.6.6 Cut 6 lets `qsim-simulator`
    /// swap in a GPU one for `Backend::WgpuMps`.
    svd_provider: Arc<dyn MpsSvdProvider<F>>,
}

/// 64-bit precision MPS — original Stage 1 type.
pub type MpsF64 = Mps<f64>;

/// 32-bit precision MPS (v0.6.5).  ~50 % memory savings at ~1e-6
/// statevector precision; SVD precision drops by ~9 decimal digits, so
/// `trunc_threshold = 1e-4` is the recommended default cutoff.
pub type MpsF32 = Mps<f32>;

impl<F: MpsScalar> Mps<F> {
    /// Create the product state `|0...0⟩` on `n_qubits` qubits with no
    /// singular-value cutoff — equivalent to
    /// `MpsF64::with_threshold(n_qubits, max_bond_dim, 0.0)`.
    ///
    /// Every site is initialised with the rank-1 tensor `[[1+0i], [0+0i]]`
    /// of shape `[1, 2, 1]`, so the initial bond dimension is 1
    /// everywhere.
    ///
    /// # Panics
    /// If `n_qubits == 0` or `max_bond_dim == 0`.
    pub fn new(n_qubits: usize, max_bond_dim: usize) -> Self {
        Self::with_threshold(n_qubits, max_bond_dim, 0.0)
    }

    /// Create the product state `|0...0⟩` on `n_qubits` qubits with both
    /// a rank cap (`max_bond_dim`) and a singular-value cutoff
    /// (`trunc_threshold`).  When both are non-trivial, the **stricter**
    /// of the two applies at every SVD: `keep = min(rank_cap, eps_rank)`.
    ///
    /// Setting `trunc_threshold = 0.0` recovers the v0.6.3 behaviour
    /// (rank cap only).  v0.6.5 (Schollwöck 2011 §4.5.3).
    ///
    /// # Panics
    /// If `n_qubits == 0`, `max_bond_dim == 0`, or `trunc_threshold` is
    /// negative or NaN.
    pub fn with_threshold(n_qubits: usize, max_bond_dim: usize, trunc_threshold: f64) -> Self {
        assert!(n_qubits >= 1, "Mps requires n_qubits >= 1");
        assert!(max_bond_dim >= 1, "Mps requires max_bond_dim >= 1");
        assert!(
            trunc_threshold.is_finite() && trunc_threshold >= 0.0,
            "Mps trunc_threshold must be finite and >= 0.0 (got {trunc_threshold})"
        );

        let mut tensors = Vec::with_capacity(n_qubits);
        for _ in 0..n_qubits {
            // |0⟩ at this site: T[0, 0, 0] = 1, T[0, 1, 0] = 0.
            let data = vec![
                Complex::new(F::one(), F::zero()),
                Complex::new(F::zero(), F::zero()),
            ];
            tensors.push(Tensor3::<F>::new(1, 1, data));
        }

        Self {
            n_qubits,
            tensors,
            max_bond_dim,
            trunc_threshold,
            truncation_error_sum: 0.0,
            svd_provider: Arc::new(CpuSvdProvider),
        }
    }

    /// Number of qubits (sites) in the MPS.
    pub fn num_qubits(&self) -> usize {
        self.n_qubits
    }

    /// Swap in a custom SVD provider (v0.6.6 Cut 6).  Used by
    /// `qsim-simulator` to route the truncating SVD inside
    /// [`Mps::apply_two_qubit_adjacent`] to GPU
    /// (`qsim_gpu::wgpu_thin_svd`).  Defaults to [`CpuSvdProvider`].
    pub fn set_svd_provider(&mut self, provider: Arc<dyn MpsSvdProvider<F>>) {
        self.svd_provider = provider;
    }

    /// Maximum bond dimension χ_max permitted at any cut.
    pub fn max_bond_dim(&self) -> usize {
        self.max_bond_dim
    }

    /// Singular-value cutoff threshold (`0.0` = disabled).  v0.6.5.
    pub fn trunc_threshold(&self) -> f64 {
        self.trunc_threshold
    }

    /// Largest **actually-occurring** internal bond dimension across all
    /// cuts.  With adaptive truncation (`trunc_threshold > 0`) this is
    /// typically smaller than [`Mps::max_bond_dim`] — the user-specified
    /// rank cap.  v0.6.5.
    pub fn observed_max_bond_dim(&self) -> usize {
        // tensors[i].right == tensors[i+1].left by invariant; either
        // suffices.  Boundaries are always 1, which we floor with .max(1)
        // for the n=1 edge case.
        self.tensors
            .iter()
            .map(|t| t.right.max(t.left))
            .max()
            .unwrap_or(1)
    }

    /// Cumulative discarded-weight truncation error
    /// `Σ_{SVDs} Σ_{j>keep} sv_j²` accumulated across every SVD
    /// truncation performed by [`Mps::apply_two_qubit_adjacent`]
    /// (Schollwöck 2011 §4.5.3).  Returns `0.0` for any MPS that has
    /// never lost amplitude — e.g. when `max_bond_dim` was sufficient
    /// for the actual Schmidt rank, or when only single-qubit gates
    /// were applied.
    ///
    /// `right_canonicalize` 도 `trunc_threshold > 0` 이면 singular value
    /// cutoff 로 잘린 가중치를 이 합계에 누적한다 (v0.6.5~).  threshold 0
    /// 이면 norm-preserving thin SVD 만 수행하므로 기여하지 않는다.
    pub fn truncation_error_sum(&self) -> f64 {
        self.truncation_error_sum
    }

    // ---- v0.6.7 Cut 8a: GPU-resident MPS accessor API ----

    /// Bond dimensions `(left, right)` for site `site`.
    ///
    /// Used by `GpuMpsTensors` to track per-site shape without exposing
    /// `Tensor3`.  v0.6.7.
    pub fn tensor_dims(&self, site: usize) -> (usize, usize) {
        assert!(site < self.n_qubits, "tensor_dims: site out of range");
        (self.tensors[site].left, self.tensors[site].right)
    }

    /// Read-only slice of the row-major tensor data at `site`.
    ///
    /// Length = `left * 2 * right` complex elements.  v0.6.7.
    pub fn tensor_data_slice(&self, site: usize) -> &[Complex<F>] {
        assert!(site < self.n_qubits, "tensor_data_slice: site out of range");
        &self.tensors[site].data
    }

    /// Overwrite the tensor at `site` with new bond dimensions and data.
    ///
    /// # Panics
    /// If `data.len() != left * 2 * right` or `site >= n_qubits`.
    /// v0.6.7.
    pub fn set_tensor(&mut self, site: usize, left: usize, right: usize, data: Vec<Complex<F>>) {
        assert!(site < self.n_qubits, "set_tensor: site out of range");
        self.tensors[site] = Tensor3::new(left, right, data);
    }

    /// Add to the cumulative truncation error sum.  Used by
    /// `GpuMpsTensors` to report GPU-side SVD truncation back to the
    /// MPS metadata.  v0.6.7.
    pub fn add_truncation_error(&mut self, error_sq: f64) {
        self.truncation_error_sum += error_sq;
    }

    /// Bond dimension at the cut to the left of site `i`.
    ///
    /// `bond_dim(0) = 1` (left boundary) and
    /// `bond_dim(n_qubits) = 1` (right boundary) — these are sentinel
    /// values implied by the open boundary condition.  For internal
    /// cuts `1 ≤ i < n_qubits`, returns `tensors[i].left` which equals
    /// `tensors[i-1].right` by invariant.
    ///
    /// # Panics
    /// If `i > n_qubits`.
    pub fn bond_dim(&self, i: usize) -> usize {
        assert!(i <= self.n_qubits, "bond_dim index out of range");
        if i == 0 || i == self.n_qubits {
            1
        } else {
            self.tensors[i].left
        }
    }

    /// Contract the entire MPS into a dense statevector.
    ///
    /// Index convention is little-endian: amplitude
    /// `state[s_0 + s_1·2 + ... + s_{n-1}·2^{n-1}]`.
    ///
    /// # Panics
    /// If `n_qubits > 20`.  This routine is for debugging and small-N
    /// cross-checking only; the resulting `Vec` would be 16 MiB at
    /// n=20 and grows as 2ⁿ thereafter.
    pub fn statevector(&self) -> Vec<Complex<F>> {
        assert!(
            self.n_qubits <= 20,
            "Mps::statevector() is debug-only and limited to n_qubits <= 20"
        );

        // Left-to-right contraction.  After processing site i (i.e. sites
        // 0..=i), `state` holds amplitudes indexed by
        // (s_0, ..., s_i, bond_r) flattened as
        // `state[basis_idx * bond_r_size + r]`, where
        // `basis_idx = s_0 + s_1·2 + ... + s_i·2^i` (little-endian).
        let mut state: Vec<Complex<F>> = vec![Complex::new(F::one(), F::zero())];
        let mut basis_size: usize = 1;
        let mut bond: usize = 1;

        for site in 0..self.n_qubits {
            let t = &self.tensors[site];
            assert_eq!(bond, t.left, "MPS bond dimension mismatch at site {site}");
            let chi_r = t.right;
            let new_basis = basis_size * 2;
            let mut new_state = vec![Complex::<F>::zero(); new_basis * chi_r];

            // v0.6.5: parallelize outer-by-`new_idx`.  `new_idx = (s << site) | k`
            // where `s ∈ {0, 1}` and `k ∈ 0..basis_size` — each new_idx
            // value is unique, so the chi_r-sized chunks of new_state are
            // disjoint write targets.  Inverse mapping: `s = (new_idx >> site) & 1`,
            // `k = new_idx & ((1 << site) - 1)`.
            let mask_k = (1usize << site).saturating_sub(1);
            let fill_chunk = |new_idx: usize, chunk: &mut [Complex<F>]| {
                let s = (new_idx >> site) & 1;
                let k = new_idx & mask_k;
                for (r, slot) in chunk.iter_mut().enumerate() {
                    let mut acc = Complex::<F>::zero();
                    for l in 0..t.left {
                        let s_val = state[k * t.left + l];
                        let t_val = t.get(l, s, r);
                        acc += s_val * t_val;
                    }
                    *slot = acc;
                }
            };
            if new_basis * chi_r >= PAR_THRESHOLD {
                new_state
                    .par_chunks_mut(chi_r)
                    .enumerate()
                    .for_each(|(new_idx, chunk)| fill_chunk(new_idx, chunk));
            } else {
                for (new_idx, chunk) in new_state.chunks_mut(chi_r).enumerate() {
                    fill_chunk(new_idx, chunk);
                }
            }

            state = new_state;
            basis_size = new_basis;
            bond = chi_r;
        }

        assert_eq!(bond, 1, "MPS final right bond must be 1, got {bond}");
        // state has shape (2^n, 1), already flat.
        state
    }

    /// Apply a single-qubit gate `gate` (2×2 matrix) to site `qubit`.
    ///
    /// The site tensor is updated in-place via the standard snapshot
    /// pattern `T'[l, p', r] = Σ_p U[p', p] · T[l, p, r]`.  Bond
    /// dimensions are unchanged, so neither neighbouring sites nor
    /// `bond_dim(i)` need adjustment.
    ///
    /// # Panics
    /// If `qubit >= n_qubits`.
    pub fn apply_one_qubit(&mut self, gate: &[[Complex<f64>; 2]; 2], qubit: usize) {
        assert!(
            qubit < self.n_qubits,
            "qubit {qubit} out of range for {} qubits",
            self.n_qubits
        );
        let t = &mut self.tensors[qubit];
        // v0.6.5: gate matrix arrives as Complex<f64> (the precision of
        // gate parameters in qsim_core::Gate) — convert once on entry.
        let m00 = gconv::<F>(gate[0][0]);
        let m01 = gconv::<F>(gate[0][1]);
        let m10 = gconv::<F>(gate[1][0]);
        let m11 = gconv::<F>(gate[1][1]);
        let left = t.left;
        let right = t.right;
        for l in 0..left {
            let row_base = l * 2 * right;
            for r in 0..right {
                let idx0 = row_base + r;
                let idx1 = row_base + right + r;
                let v0 = t.data[idx0];
                let v1 = t.data[idx1];
                t.data[idx0] = m00 * v0 + m01 * v1;
                t.data[idx1] = m10 * v0 + m11 * v1;
            }
        }
    }

    /// Apply a two-qubit gate to **adjacent** sites `q0` and `q1 = q0 + 1`,
    /// truncating the bond between them to at most `self.max_bond_dim`
    /// singular values.
    ///
    /// # Gate convention
    ///
    /// The 4×4 matrix follows the same little-endian column ordering as
    /// `qsim_core::operations::apply_two_qubit_gate` (see
    /// `crates/core/src/operations.rs:213-237`):
    ///
    /// ```text
    /// col / row  = (q1 << 1) | q0   with q0 = LSB
    /// ```
    ///
    /// In particular, `qsim_core::Gate::cnot_matrix` corresponds to a
    /// CNOT in which the **higher-indexed qubit** (`q1`) is the control
    /// and the **lower-indexed qubit** (`q0`) is the target.
    ///
    /// # Algorithm (Schollwöck 2011 §4.5)
    ///
    /// 1. Contract `T_{q0} ⊗ T_{q1}` over the shared bond.
    /// 2. Apply `U` to the two physical legs.
    /// 3. Reshape into a `(chi_l · 2) × (2 · chi_r)` matrix.
    /// 4. SVD (singular values returned in descending order by nalgebra).
    /// 5. Truncate to `keep = min(k, max_bond_dim).max(1)`.
    /// 6. Split back into two rank-3 tensors; the new bond dimension is
    ///    `keep`.
    ///
    /// # Pitfalls
    ///
    /// `nalgebra::DMatrix` stores data column-major, so the
    /// reshape steps use element-wise `mat[(i, j)]` indexing — never
    /// `as_slice()` copies — to round-trip the row-major flat tensor
    /// layout safely.
    ///
    /// # Panics
    /// If `q0 + 1 >= n_qubits` (only adjacent gates are supported in
    /// Stage 1; non-adjacent gates via SWAP decomposition are deferred
    /// to v0.6.4 — originally planned for v0.6.3 but pushed back one
    /// release because v0.6.2 became a silent-bug-fix release).
    pub fn apply_two_qubit_adjacent(&mut self, gate: &[[Complex<f64>; 4]; 4], q0: usize) {
        let q1 = q0 + 1;
        assert!(
            q1 < self.n_qubits,
            "apply_two_qubit_adjacent: q0={q0} q1={q1} out of range for {} qubits (Stage 1 supports only adjacent sites)",
            self.n_qubits
        );

        // v0.6.5: convert the f64 gate matrix to Complex<F> once on entry.
        let gate_f: [[Complex<F>; 4]; 4] = {
            let mut g = [[Complex::<F>::zero(); 4]; 4];
            for i in 0..4 {
                for j in 0..4 {
                    g[i][j] = gconv::<F>(gate[i][j]);
                }
            }
            g
        };

        let chi_l = self.tensors[q0].left;
        let chi_m = self.tensors[q0].right;
        debug_assert_eq!(chi_m, self.tensors[q1].left);
        let chi_r = self.tensors[q1].right;

        // ---- Step 1: contract T_{q0} ⊗ T_{q1} → M[a, pi, pj, c] ----
        // Layout: row-major `a * 4 * chi_r + pi * 2 * chi_r + pj * chi_r + c`.
        // v0.6.5: parallelize outer-by-`a` when chi_l * chi_r is large
        // enough to amortize rayon overhead.  Each `a`-slab writes into a
        // disjoint contiguous chunk of `m`, so the parallel write is safe.
        let m_len = chi_l * 4 * chi_r;
        let mut m = vec![Complex::<F>::zero(); m_len];
        {
            let t_l = &self.tensors[q0];
            let t_r = &self.tensors[q1];
            let slab = 4 * chi_r;
            let fill_slab = |a: usize, slab_buf: &mut [Complex<F>]| {
                for pi in 0..2 {
                    for pj in 0..2 {
                        for c in 0..chi_r {
                            let mut acc = Complex::<F>::zero();
                            for b in 0..chi_m {
                                acc += t_l.get(a, pi, b) * t_r.get(b, pj, c);
                            }
                            slab_buf[pi * 2 * chi_r + pj * chi_r + c] = acc;
                        }
                    }
                }
            };
            if chi_l * chi_r >= PAR_THRESHOLD {
                m.par_chunks_mut(slab)
                    .enumerate()
                    .for_each(|(a, slab_buf)| fill_slab(a, slab_buf));
            } else {
                for (a, slab_buf) in m.chunks_mut(slab).enumerate() {
                    fill_slab(a, slab_buf);
                }
            }
        }

        // ---- Step 2: apply 4×4 gate U on physical legs ----
        // row = (pj' << 1) | pi',  col = (pj << 1) | pi   (LSB convention).
        // v0.6.5: parallelize outer-by-`a`.  Each `a`-slab in `m2` is a
        // disjoint write target; reads of `m` use the same `a` index.
        let mut m2 = vec![Complex::<F>::zero(); m_len];
        let slab = 4 * chi_r;
        let fill_m2_slab = |a: usize, slab_buf: &mut [Complex<F>]| {
            for c in 0..chi_r {
                for pip in 0..2 {
                    for pjp in 0..2 {
                        let row = (pjp << 1) | pip;
                        let mut acc = Complex::<F>::zero();
                        for pi in 0..2 {
                            for pj in 0..2 {
                                let col = (pj << 1) | pi;
                                let m_idx = a * 4 * chi_r + pi * 2 * chi_r + pj * chi_r + c;
                                acc += gate_f[row][col] * m[m_idx];
                            }
                        }
                        slab_buf[pip * 2 * chi_r + pjp * chi_r + c] = acc;
                    }
                }
            }
        };
        if chi_l * chi_r >= PAR_THRESHOLD {
            m2.par_chunks_mut(slab)
                .enumerate()
                .for_each(|(a, slab_buf)| fill_m2_slab(a, slab_buf));
        } else {
            for (a, slab_buf) in m2.chunks_mut(slab).enumerate() {
                fill_m2_slab(a, slab_buf);
            }
        }

        // ---- Step 3: reshape M' → 2D matrix M_mat ----
        // R = a*2 + pi' (rows = chi_l*2),  C = pj'*chi_r + c (cols = 2*chi_r).
        let rows = chi_l * 2;
        let cols = 2 * chi_r;
        let mut row_major = vec![Complex::<F>::zero(); rows * cols];
        for a in 0..chi_l {
            for pip in 0..2 {
                let r_idx = a * 2 + pip;
                for pjp in 0..2 {
                    for c in 0..chi_r {
                        let c_idx = pjp * chi_r + c;
                        let m2_idx = a * 4 * chi_r + pip * 2 * chi_r + pjp * chi_r + c;
                        row_major[r_idx * cols + c_idx] = m2[m2_idx];
                    }
                }
            }
        }
        // ---- Step 4 + 5: SVD + truncate via pluggable provider (v0.6.6 Cut 6) ----
        // CpuSvdProvider (default) matches v0.6.5 byte-for-byte; WgpuSvdProvider
        // (installed by simulator for Backend::WgpuMps) routes to GPU.
        let svd_out = self.svd_provider.thin_svd(
            &row_major,
            rows,
            cols,
            self.max_bond_dim,
            self.trunc_threshold,
        );
        self.truncation_error_sum += svd_out.trunc_error_sq;
        let keep = svd_out.keep;
        let u_row = &svd_out.u_row_major;
        let vt_row = &svd_out.vt_row_major;
        let s_vec = &svd_out.s;

        // ---- Step 6: split into two new tensors ----
        // T'_{q0}[a, pi', b] = U[(a*2 + pi'), b]   for b in 0..keep
        let mut new_l = vec![Complex::<F>::zero(); chi_l * 2 * keep];
        for a in 0..chi_l {
            for pip in 0..2 {
                let r_idx = a * 2 + pip;
                for b in 0..keep {
                    let val = u_row[r_idx * keep + b];
                    let idx = a * 2 * keep + pip * keep + b;
                    new_l[idx] = val;
                }
            }
        }

        // T'_{q1}[b, pj', c] = sv[b] * V^H[(b), (pj' * chi_r + c)]
        let mut new_r = vec![Complex::<F>::zero(); keep * 2 * chi_r];
        for b in 0..keep {
            let s_b = Complex::new(s_vec[b], F::zero());
            for pjp in 0..2 {
                for c in 0..chi_r {
                    let c_idx = pjp * chi_r + c;
                    let val = s_b * vt_row[b * cols + c_idx];
                    let idx = b * 2 * chi_r + pjp * chi_r + c;
                    new_r[idx] = val;
                }
            }
        }

        self.tensors[q0] = Tensor3::<F>::new(chi_l, keep, new_l);
        self.tensors[q1] = Tensor3::<F>::new(keep, chi_r, new_r);
    }

    /// Squared L2 norm `<ψ|ψ>` of the (possibly-truncated) MPS.
    ///
    /// Computed via direct left-to-right transfer-matrix contraction —
    /// O(N · χ³) — **without** going through the dense 2ⁿ statevector,
    /// so it is safe for `n_qubits > 20`.  Independent of canonical form
    /// (works for arbitrary MPS).
    ///
    /// # Algorithm
    ///
    /// Maintain a running left environment `L: (χ_l, χ_l)` starting as
    /// the 1×1 identity.  At each site `i`:
    ///
    /// ```text
    /// L_new[a_r, a_r'] = Σ_{p, a_l, a_l'} M^p[a_l, a_r] · L[a_l, a_l'] · conj(M^p[a_l', a_r'])
    ///                  = Σ_p (M^p)^T · L · conj(M^p)        (matrix form)
    /// ```
    ///
    /// where `M^p` is the slice `T_i[:, p, :]` of shape `(χ_l, χ_r)`.
    /// At the end `L` is 1×1 and `<ψ|ψ> = trace(L).re`.
    pub fn norm_squared(&self) -> f64 {
        let mut left_env: DMatrix<Complex<F>> = DMatrix::identity(1, 1);
        for i in 0..self.n_qubits {
            left_env = update_left_env::<F>(&left_env, &self.tensors[i], None);
        }
        debug_assert_eq!(left_env.shape(), (1, 1));
        // v0.6.5: norm² always reported as f64 so callers don't have to
        // generic-handle it (matches mps_truncation_error_sum convention).
        left_env[(0, 0)].re.to_f64().unwrap_or(0.0)
    }

    /// `⟨ψ|P|ψ⟩` for a single Pauli string `P` (v0.7).
    ///
    /// `paulis[q] ∈ {0=I, 1=X, 2=Y, 3=Z}` and `paulis.len() == n_qubits`.
    /// Applies the single-qubit Paulis to a clone (1q gates leave bond
    /// dimensions unchanged) and contracts the overlap `⟨ψ|Pψ⟩` exactly via
    /// a left-environment sweep — **O(N · χ³)**, no canonical form or dense
    /// statevector required, so it works for any `N` (the basis for large-N
    /// VQE / QAOA on the MPS backend).
    ///
    /// Returns the **raw** (un-normalised) overlap to match the dense-
    /// statevector expectation path; for a normalised state (`⟨ψ|ψ⟩ = 1`)
    /// they coincide.  For a truncated state the caller may divide by
    /// [`Mps::norm_squared`] to renormalise.
    pub fn expectation_pauli(&self, paulis: &[u8]) -> Complex<f64> {
        assert_eq!(
            paulis.len(),
            self.n_qubits,
            "expectation_pauli: paulis len must equal n_qubits"
        );
        let c0 = Complex::new(0.0f64, 0.0);
        let c1 = Complex::new(1.0f64, 0.0);
        let ci = Complex::new(0.0f64, 1.0);
        let mut ket = self.clone();
        for (q, &p) in paulis.iter().enumerate() {
            let g: [[Complex<f64>; 2]; 2] = match p {
                0 => continue,              // I
                1 => [[c0, c1], [c1, c0]],  // X
                2 => [[c0, -ci], [ci, c0]], // Y
                3 => [[c1, c0], [c0, -c1]], // Z
                other => panic!("invalid Pauli code {other} (0=I,1=X,2=Y,3=Z)"),
            };
            ket.apply_one_qubit(&g, q);
        }
        overlap(self, &ket)
    }

    /// Sample a single bitstring outcome from the MPS (v0.6.1).
    ///
    /// Uses sequential single-site Bayes-conditional sampling — at each
    /// site, computes the marginal `p(s_i = 0)` / `p(s_i = 1)` given the
    /// outcomes already chosen for sites `0..i`, samples a bit, and
    /// updates the running left environment accordingly.  No dense
    /// statevector is built, so the cost is **O(N · χ³)** per shot
    /// regardless of N.
    ///
    /// # Output
    ///
    /// Returns `outcome: Vec<bool>` of length `n_qubits` where
    /// `outcome[i]` is the measurement result of qubit `i`
    /// (LSB-first / element-i convention, matching
    /// `qsim_core::StateVector` indexing).  v0.6.3 widened the outcome
    /// from `u64` to `Vec<bool>` to support N > 64.
    ///
    /// # Preconditions
    ///
    /// **The MPS must be in right-canonical form** (call
    /// [`Mps::right_canonicalize`] beforehand).  In right-canonical form
    /// the right-tail contraction `R_i` reduces to the identity, so the
    /// marginal weight at site `i` simplifies to `trace(L_{i+1}^p)` where
    /// `L_{i+1}^p` is the left environment update for physical state `p`.
    ///
    /// If the MPS is not right-canonical, the marginal probabilities
    /// will be biased — silent miscalibration, not a panic.
    ///
    /// # Truncated states
    ///
    /// If the MPS underwent SVD truncation that lost amplitude
    /// (`norm_squared() < 1`), the sampling distribution is the
    /// **renormalised** distribution of the truncated state — the
    /// missing amplitude is dropped.  Standard MIMIQ / Qiskit Aer
    /// semantics.
    pub fn sample_once<R: Rng>(&self, rng: &mut R) -> Vec<bool> {
        let mut left_env: DMatrix<Complex<F>> = DMatrix::identity(1, 1);
        let mut outcome: Vec<bool> = Vec::with_capacity(self.n_qubits);
        for i in 0..self.n_qubits {
            let l_for_p0 = update_left_env::<F>(&left_env, &self.tensors[i], Some(0));
            let l_for_p1 = update_left_env::<F>(&left_env, &self.tensors[i], Some(1));
            // Trace gives the marginal weight (right-tail = I in
            // right-canonical).  Compute the comparison in f64 so the RNG
            // draw uses the same precision for both f32 and f64 MPSes.
            let w0 = l_for_p0
                .diagonal()
                .iter()
                .map(|c| c.re.to_f64().unwrap_or(0.0))
                .sum::<f64>()
                .max(0.0);
            let w1 = l_for_p1
                .diagonal()
                .iter()
                .map(|c| c.re.to_f64().unwrap_or(0.0))
                .sum::<f64>()
                .max(0.0);
            let total = w0 + w1;
            // total must be > 0 unless the truncated state is identically 0,
            // which would itself be a misuse — fall back to a 50:50 sample.
            let bit_one = if total <= 0.0 {
                rng.gen::<f64>() >= 0.5
            } else {
                rng.gen::<f64>() >= (w0 / total)
            };
            outcome.push(bit_one);
            // Re-normalise so the running marginal stays at 1.
            let chosen_w = if bit_one { w1 } else { w0 };
            let chosen_l = if bit_one { l_for_p1 } else { l_for_p0 };
            if chosen_w > 0.0 {
                let scale = F::from(chosen_w).unwrap_or_else(F::one);
                left_env = chosen_l / Complex::new(scale, F::zero());
            } else {
                // Degenerate — keep the left env as-is for stability.
                left_env = chosen_l;
            }
        }
        outcome
    }

    /// Multi-shot sampling wrapper — calls [`Mps::sample_once`] in a
    /// loop and aggregates outcomes into `HashMap<Vec<bool>, usize>`
    /// (v0.6.3, was `HashMap<u64, usize>` in v0.6.1/2).
    ///
    /// **Same preconditions as `sample_once`** — the MPS must be in
    /// right-canonical form.  The MPS itself is **not mutated** between
    /// shots; only the per-shot transient left-environment matrix is
    /// rebuilt, so `O(N · χ³ · shots)` total without re-canonicalising.
    pub fn sample<R: Rng>(&self, shots: usize, rng: &mut R) -> HashMap<Vec<bool>, usize> {
        let mut counts: HashMap<Vec<bool>, usize> = HashMap::new();
        for _ in 0..shots {
            let outcome = self.sample_once(rng);
            *counts.entry(outcome).or_insert(0) += 1;
        }
        counts
    }

    /// Marginal weight of measuring `|1⟩` on `target`, as the **raw trace**.
    ///
    /// 반환값은 정규화되지 않은 값이다 — norm 1 상태에서는 그대로 `p(1)` 이지만
    /// SVD truncation 으로 norm² < 1 인 상태에서는 `norm² × p(1)` 이다.  확률로
    /// 쓰려면 [`Mps::norm_squared`] 로 나눠야 한다 (simulator 의
    /// `mps_p_one_normalized` 헬퍼 참조).  v0.6.5 — trajectory-mode
    /// mid-circuit measurement 용.
    ///
    /// # Preconditions
    ///
    /// Same as [`Mps::sample_once`] — the MPS must be in right-canonical
    /// form (call [`Mps::right_canonicalize`] beforehand).  In that form
    /// the right-tail contraction reduces to the identity, so the
    /// marginal collapses to a single trace.
    ///
    /// # Panics
    /// If `target >= n_qubits`.
    pub fn single_qubit_probability(&self, target: usize) -> F {
        assert!(
            target < self.n_qubits,
            "single_qubit_probability: target out of range"
        );
        let mut left_env: DMatrix<Complex<F>> = DMatrix::identity(1, 1);
        for i in 0..target {
            left_env = update_left_env::<F>(&left_env, &self.tensors[i], None);
        }
        let l_for_p1 = update_left_env::<F>(&left_env, &self.tensors[target], Some(1));
        // trace(l_for_p1).re.max(0)  — clamp tiny negatives from FP error.
        let mut acc = F::zero();
        for i in 0..l_for_p1.nrows() {
            acc += l_for_p1[(i, i)].re;
        }
        if acc < F::zero() {
            F::zero()
        } else {
            acc
        }
    }

    /// Renormalize the entire state to `<ψ|ψ> = 1` by scaling the leftmost
    /// tensor.  Used after applying a non-unitary single-qubit "gate"
    /// (e.g. a Kraus operator) where the resulting norm is below 1.
    /// v0.6.5.
    ///
    /// No-op if `norm_squared() == 0` (degenerate state) — the caller is
    /// responsible for detecting that case.
    pub fn normalize(&mut self) {
        let n_sq = self.norm_squared();
        if n_sq <= 0.0 {
            return;
        }
        let scale = F::one() / num_traits::Float::sqrt(F::from(n_sq).unwrap_or(F::one()));
        for elem in self.tensors[0].data.iter_mut() {
            *elem *= Complex::new(scale, F::zero());
        }
    }

    /// Project the MPS onto the chosen `outcome` of a single-qubit
    /// measurement at site `target`, renormalising in place.  Returns
    /// the conditional probability `p(outcome)` (needed for trajectory
    /// weighting / debugging).  v0.6.5.
    ///
    /// # Behaviour
    ///
    /// - Computes the raw branch weight via
    ///   [`Mps::single_qubit_probability`] and the state norm² via
    ///   [`Mps::norm_squared`] — SVD truncation 이후 norm² < 1 인 상태에서도
    ///   `p(outcome)` 이 편향되지 않도록 raw weight 를 norm² 으로 정규화한다.
    /// - Sets the physical leg of `T_target` for `p != outcome` to zero
    ///   and rescales the kept leg by `1 / sqrt(raw weight)` — collapse 후
    ///   상태는 정확히 norm 1 이 된다.
    /// - Sites `0..target` and `target+1..n_qubits` are **not** modified —
    ///   if they were right-canonical before the call, they remain so on
    ///   the right of `target`.  Site `target` itself is no longer
    ///   guaranteed to be right-orthogonal; the caller should
    ///   [`Mps::right_canonicalize`] before subsequent sampling.
    ///
    /// If `p(outcome) <= 0` (impossible / numerically zero outcome) the
    /// MPS is left **unchanged** and the returned value is `0` — the
    /// caller should treat this as a degenerate state.
    ///
    /// # Preconditions
    ///
    /// MPS in right-canonical form (same as sampling).  v0.6.5 — needed
    /// for Cut 7's trajectory `Measure` / `Reset` / Kraus dispatch.
    ///
    /// # Panics
    /// If `target >= n_qubits`.
    pub fn collapse_qubit(&mut self, target: usize, outcome: bool) -> F {
        assert!(
            target < self.n_qubits,
            "collapse_qubit: target out of range"
        );
        let p1_raw = self.single_qubit_probability(target);
        let norm_sq = F::from(self.norm_squared()).unwrap_or(F::one());
        if norm_sq <= F::zero() {
            return F::zero();
        }
        // raw branch weight: truncation 으로 norm² < 1 이어도 p0+p1 = norm².
        // 이전의 `1 - p1` 은 norm 1 을 가정해 잃어버린 norm 전체가 outcome 0
        // 쪽으로 쏠리는 편향을 만들었다.
        let w_outcome = if outcome { p1_raw } else { norm_sq - p1_raw };
        if w_outcome <= F::zero() {
            return F::zero();
        }
        let p_outcome = w_outcome / norm_sq;
        let target_bit = usize::from(outcome);
        let scale = F::one() / num_traits::Float::sqrt(w_outcome);
        let t = &mut self.tensors[target];
        let left = t.left;
        let right = t.right;
        for l in 0..left {
            for r in 0..right {
                let keep_idx = t.idx(l, target_bit, r);
                let drop_idx = t.idx(l, 1 - target_bit, r);
                t.data[keep_idx] *= Complex::new(scale, F::zero());
                t.data[drop_idx] = Complex::<F>::zero();
            }
        }
        p_outcome
    }

    /// Bring the MPS to **right-canonical form** via a right-to-left thin
    /// SVD sweep (Schollwöck 2011 §4.4).
    ///
    /// After this call, every tensor `T_i` for `i >= 1` (i.e. all sites
    /// except possibly site 0) satisfies the right-orthogonality condition
    ///
    /// ```text
    /// Σ_{p, r} T_i[b, p, r] · conj(T_i[b', p, r])  =  δ_{b, b'}
    /// ```
    ///
    /// — equivalently, the matrix obtained by reshaping `T_i` to shape
    /// `[chi_left, 2 · chi_right]` has orthonormal rows.  The left-most
    /// site (site 0) carries the remaining norm: `<ψ|ψ> = ||T_0||²`.
    ///
    /// The sweep is **norm-preserving** (the underlying state vector is
    /// unchanged) and may **shrink** internal bonds when a tensor was
    /// over-bonded — `min(chi_left, 2 · chi_right)` is the maximum useful
    /// rank at each cut.  No additional truncation against `max_bond_dim`
    /// is performed (truncation happens only inside `apply_two_qubit_adjacent`).
    ///
    /// # Algorithm
    ///
    /// For `i = n-1, n-2, ..., 1`:
    /// 1. Reshape `T_i` (shape `[chi_l, 2, chi_r]`) row-major into a
    ///    `(chi_l, 2 · chi_r)` matrix `M`.
    /// 2. Thin SVD: `M = U · diag(S) · V†`, with `U: (chi_l, k)`,
    ///    `V†: (k, 2 · chi_r)`, `k = min(chi_l, 2 · chi_r)`.
    /// 3. Replace `T_i` with `V†` reshaped to `[k, 2, chi_r]` row-major
    ///    — now right-orthogonal.
    /// 4. Absorb `U · diag(S)` into the right bond of `T_{i-1}`:
    ///    `T_{i-1}'[a, p, b] = Σ_l T_{i-1}[a, p, l] · U[l, b] · S[b]`.
    ///    The new right bond of `T_{i-1}` (and left bond of `T_i`) is `k`.
    ///
    /// # Pitfalls
    ///
    /// `nalgebra::DMatrix` is column-major internally — element-wise
    /// indexing (`mat[(i, j)]`) is used everywhere to round-trip the
    /// row-major flat tensor layout safely.  `as_slice().copy_from_slice()`
    /// would silently transpose.
    ///
    /// # Cost
    ///
    /// O(N · χ³) — one thin SVD per site of an `(χ × 2χ)` matrix.
    pub fn right_canonicalize(&mut self) {
        if self.n_qubits <= 1 {
            // n=1: trivial — single site already "canonical".
            return;
        }

        for i in (1..self.n_qubits).rev() {
            // ---- Step 1: reshape T_i [chi_l, 2, chi_r] → (chi_l, 2·chi_r) row-major ----
            let chi_l = self.tensors[i].left;
            let chi_r = self.tensors[i].right;
            let cols = 2 * chi_r;
            let mut row_major = vec![Complex::<F>::zero(); chi_l * cols];
            for a in 0..chi_l {
                for p in 0..2 {
                    for c in 0..chi_r {
                        row_major[a * cols + p * chi_r + c] = self.tensors[i].get(a, p, c);
                    }
                }
            }
            // ---- Step 2: thin SVD via pluggable provider (v0.6.6 Cut 7) ----
            // `right_canonicalize` 자체는 norm-preserving 이라 rank cap 적용
            // 안 함 — `max_keep = chi_l.min(cols)` (true rank).  eps-rank
            // cap 만 `trunc_threshold > 0` 일 때 적용된다.
            let true_rank = chi_l.min(cols);
            let svd_out = self.svd_provider.thin_svd(
                &row_major,
                chi_l,
                cols,
                true_rank,
                self.trunc_threshold,
            );
            self.truncation_error_sum += svd_out.trunc_error_sq;
            let keep = svd_out.keep;
            let u_row = &svd_out.u_row_major; // chi_l × keep row-major
            let vt_row = &svd_out.vt_row_major; // keep × cols row-major
            let sv = &svd_out.s;

            // ---- Step 3: new T_i = V† reshaped (keep, 2, chi_r) ----
            // V^H[(b), (p · chi_r + c)] → T_i[b, p, c].
            let mut new_t_i = vec![Complex::<F>::zero(); keep * 2 * chi_r];
            for b in 0..keep {
                for p in 0..2 {
                    for c in 0..chi_r {
                        let val = vt_row[b * cols + p * chi_r + c];
                        let idx = b * 2 * chi_r + p * chi_r + c;
                        new_t_i[idx] = val;
                    }
                }
            }

            // ---- Step 4: absorb U · diag(S) into T_{i-1} right bond ----
            let chi_ll = self.tensors[i - 1].left;
            let chi_l_old = self.tensors[i - 1].right;
            debug_assert_eq!(chi_l_old, chi_l, "MPS bond mismatch at site {i}");
            // new T_{i-1}[a, p, b] = Σ_l T_{i-1}[a, p, l] · U[l, b] · S[b].
            // u_row is chi_l × keep row-major: u_row[l * keep + b] = U[l, b].
            let mut new_t_im1 = vec![Complex::<F>::zero(); chi_ll * 2 * keep];
            let slab_im1 = 2 * keep;
            let fill_im1_slab = |a: usize, slab_buf: &mut [Complex<F>]| {
                for p in 0..2 {
                    for b in 0..keep {
                        let mut acc = Complex::<F>::zero();
                        for l in 0..chi_l_old {
                            acc += self.tensors[i - 1].get(a, p, l) * u_row[l * keep + b];
                        }
                        acc *= Complex::new(sv[b], F::zero());
                        slab_buf[p * keep + b] = acc;
                    }
                }
            };
            if chi_ll * keep >= PAR_THRESHOLD {
                new_t_im1
                    .par_chunks_mut(slab_im1)
                    .enumerate()
                    .for_each(|(a, slab_buf)| fill_im1_slab(a, slab_buf));
            } else {
                for (a, slab_buf) in new_t_im1.chunks_mut(slab_im1).enumerate() {
                    fill_im1_slab(a, slab_buf);
                }
            }

            self.tensors[i] = Tensor3::<F>::new(keep, chi_r, new_t_i);
            self.tensors[i - 1] = Tensor3::<F>::new(chi_ll, keep, new_t_im1);
        }
    }
}

/// Update the running left environment matrix `L` by absorbing one site
/// tensor `T_i`.
///
/// If `physical = None` the result is the **summed-over-physical**
/// update used for `<ψ|ψ>` contraction:
/// `L_new = Σ_p (M^p)^T · L · conj(M^p)`.
///
/// If `physical = Some(p)` the result is the **fixed-physical** update
/// used during sampling:
/// `L_new = (M^p)^T · L · conj(M^p)`.
///
/// In either case `M^p` is the slice `T_i[:, p, :]` of shape
/// `(χ_left, χ_right)`, and the returned matrix has shape
/// `(χ_right, χ_right)`.
///
/// `nalgebra::DMatrix` is column-major internally — `M` is built via
/// element-wise indexing rather than `as_slice()` to round-trip the
/// row-major flat tensor layout safely.
/// `⟨bra|ket⟩` overlap of two MPSes with identical structure (v0.7).
///
/// Requires `bra` and `ket` to have the same qubit count and identical bond
/// dimensions site-by-site (satisfied when `ket` is a clone of `bra` with
/// only single-qubit gates applied, e.g. Pauli strings).
fn overlap<F: MpsScalar>(bra: &Mps<F>, ket: &Mps<F>) -> Complex<f64> {
    let mut left: DMatrix<Complex<F>> = DMatrix::identity(1, 1);
    for i in 0..bra.n_qubits {
        left = update_left_env_overlap::<F>(&left, &bra.tensors[i], &ket.tensors[i]);
    }
    debug_assert_eq!(left.shape(), (1, 1));
    let v = left[(0, 0)];
    Complex::new(v.re.to_f64().unwrap_or(0.0), v.im.to_f64().unwrap_or(0.0))
}

/// Left-environment update contracting distinct `bra` / `ket` site tensors
/// (the two-MPS generalisation of [`update_left_env`] with `physical=None`).
fn update_left_env_overlap<F: MpsScalar>(
    left_env: &DMatrix<Complex<F>>,
    bra_t: &Tensor3<F>,
    ket_t: &Tensor3<F>,
) -> DMatrix<Complex<F>> {
    debug_assert_eq!(
        bra_t.left, ket_t.left,
        "overlap: bra/ket left bond mismatch"
    );
    debug_assert_eq!(
        bra_t.right, ket_t.right,
        "overlap: bra/ket right bond mismatch"
    );
    let chi_l = ket_t.left;
    let chi_r = ket_t.right;
    debug_assert_eq!(left_env.shape(), (chi_l, chi_l));
    let mut acc: DMatrix<Complex<F>> = DMatrix::zeros(chi_r, chi_r);
    for p in 0..2 {
        let mut ket_data = Vec::with_capacity(chi_l * chi_r);
        let mut bra_data = Vec::with_capacity(chi_l * chi_r);
        for a in 0..chi_l {
            for c in 0..chi_r {
                ket_data.push(ket_t.get(a, p, c));
                bra_data.push(bra_t.get(a, p, c));
            }
        }
        let m_ket = DMatrix::from_row_slice(chi_l, chi_r, &ket_data);
        let m_bra = DMatrix::from_row_slice(chi_l, chi_r, &bra_data);
        let m_bra_conj = m_bra.map(|c| c.conj());
        acc += m_ket.transpose() * left_env * m_bra_conj;
    }
    acc
}

fn update_left_env<F: MpsScalar>(
    left_env: &DMatrix<Complex<F>>,
    t: &Tensor3<F>,
    physical: Option<usize>,
) -> DMatrix<Complex<F>> {
    let chi_l = t.left;
    let chi_r = t.right;
    debug_assert_eq!(left_env.shape(), (chi_l, chi_l));

    let mut acc: DMatrix<Complex<F>> = DMatrix::zeros(chi_r, chi_r);
    let physicals: &[usize] = match physical {
        Some(0) => &[0],
        Some(1) => &[1],
        Some(_) => unreachable!("physical must be 0 or 1"),
        None => &[0, 1],
    };
    for &p in physicals {
        // Build M^p of shape (chi_l, chi_r) row-major.
        let mut m_data = Vec::with_capacity(chi_l * chi_r);
        for a in 0..chi_l {
            for c in 0..chi_r {
                m_data.push(t.get(a, p, c));
            }
        }
        let m = DMatrix::from_row_slice(chi_l, chi_r, &m_data);
        let m_conj = m.map(|c| c.conj());
        let m_t = m.transpose();
        // (chi_r, chi_l) · (chi_l, chi_l) · (chi_l, chi_r)  =  (chi_r, chi_r).
        acc += m_t * left_env * m_conj;
    }
    acc
}

#[cfg(test)]
mod tests {
    use super::*;

    fn approx_eq(a: Complex<f64>, b: Complex<f64>, eps: f64) -> bool {
        (a - b).norm() < eps
    }

    /// Dense reference: `⟨ψ|P|ψ⟩` from the statevector via the explicit
    /// 2ⁿ × 2ⁿ Pauli matrix (little-endian Kron, qubit 0 = LSB).
    fn dense_pauli_expectation(sv: &[Complex<f64>], paulis: &[u8]) -> Complex<f64> {
        let n = paulis.len();
        let dim = 1usize << n;
        let p2 = |code: u8| -> DMatrix<Complex<f64>> {
            let z = Complex::new(0.0, 0.0);
            let o = Complex::new(1.0, 0.0);
            let i = Complex::new(0.0, 1.0);
            match code {
                0 => DMatrix::from_row_slice(2, 2, &[o, z, z, o]),
                1 => DMatrix::from_row_slice(2, 2, &[z, o, o, z]),
                2 => DMatrix::from_row_slice(2, 2, &[z, -i, i, z]),
                3 => DMatrix::from_row_slice(2, 2, &[o, z, z, -o]),
                _ => unreachable!(),
            }
        };
        // M = P_{n-1} ⊗ ... ⊗ P_0.
        let mut m = DMatrix::<Complex<f64>>::identity(1, 1);
        for q in (0..n).rev() {
            m = m.kronecker(&p2(paulis[q]));
        }
        let psi = DMatrix::from_column_slice(dim, 1, sv);
        let mpsi = &m * &psi;
        let mut acc = Complex::new(0.0, 0.0);
        for k in 0..dim {
            acc += psi[(k, 0)].conj() * mpsi[(k, 0)];
        }
        acc
    }

    /// v0.7 regression: a sequence of adjacent SWAP / CNOT gates that left the
    /// MPS non-normalised because nalgebra's default `.svd()` over-converged on
    /// a near-rank-deficient bond matrix (returned a wrong singular value).
    /// Fixed by loosening the SVD convergence epsilon in `CpuSvdProvider`.
    /// Norm and statevector must stay correct throughout.
    #[test]
    fn svd_over_convergence_regression_norm_preserved() {
        let z = Complex::new(0.0, 0.0);
        let o = Complex::new(1.0, 0.0);
        let s = 1.0 / 2.0_f64.sqrt();
        let x2 = [[z, o], [o, z]];
        let h2 = [
            [Complex::new(s, 0.0), Complex::new(s, 0.0)],
            [Complex::new(s, 0.0), Complex::new(-s, 0.0)],
        ];
        let swap = [[o, z, z, z], [z, z, o, z], [z, o, z, z], [z, z, z, o]];
        let cx_ctrl_lo = [[o, z, z, z], [z, z, z, o], [z, z, o, z], [z, o, z, z]];
        let cx_ctrl_hi = [[o, z, z, z], [z, o, z, z], [z, z, z, o], [z, z, o, z]];
        let mut mps = MpsF64::new(3, 64);
        mps.apply_one_qubit(&x2, 0);
        mps.apply_two_qubit_adjacent(&cx_ctrl_lo, 1);
        mps.apply_two_qubit_adjacent(&swap, 0);
        mps.apply_two_qubit_adjacent(&cx_ctrl_hi, 0);
        mps.apply_one_qubit(&h2, 1);
        mps.apply_two_qubit_adjacent(&swap, 0);
        assert!(
            (mps.norm_squared() - 1.0).abs() < 1e-9,
            "SWAP/SVD broke norm: {}",
            mps.norm_squared()
        );
        // Expected final state: |q2=0, q1=1> ⊗ |−>_q0 → indices 2,3 = ±1/√2.
        let sv = mps.statevector();
        let expect = 1.0 / 2.0_f64.sqrt();
        assert!((sv[2].re - expect).abs() < 1e-9);
        assert!((sv[3].re + expect).abs() < 1e-9);
        for (i, amp) in sv.iter().enumerate() {
            if i != 2 && i != 3 {
                assert!(amp.norm() < 1e-9, "spurious amplitude at {i}: {amp}");
            }
        }
    }

    #[test]
    fn expectation_pauli_zero_state() {
        let mps = MpsF64::new(2, 64);
        assert!(approx_eq(
            mps.expectation_pauli(&[3, 3]),
            Complex::new(1.0, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            mps.expectation_pauli(&[1, 1]),
            Complex::new(0.0, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            mps.expectation_pauli(&[0, 3]),
            Complex::new(1.0, 0.0),
            1e-12
        ));
    }

    #[test]
    fn expectation_pauli_bell_state() {
        // Bell: H on q0, CNOT(control q0, target q1).
        let mut mps = MpsF64::new(2, 64);
        let s = 1.0 / 2.0_f64.sqrt();
        let h = [
            [Complex::new(s, 0.0), Complex::new(s, 0.0)],
            [Complex::new(s, 0.0), Complex::new(-s, 0.0)],
        ];
        mps.apply_one_qubit(&h, 0);
        // CNOT 4x4 (|q1 q0>, q0 LSB), control q0 target q1.
        let z = Complex::new(0.0, 0.0);
        let o = Complex::new(1.0, 0.0);
        let cnot = [[o, z, z, z], [z, z, z, o], [z, z, o, z], [z, o, z, z]];
        mps.apply_two_qubit_adjacent(&cnot, 0);
        assert!(approx_eq(
            mps.expectation_pauli(&[3, 3]),
            Complex::new(1.0, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            mps.expectation_pauli(&[1, 1]),
            Complex::new(1.0, 0.0),
            1e-12
        ));
        assert!(approx_eq(
            mps.expectation_pauli(&[2, 2]),
            Complex::new(-1.0, 0.0),
            1e-12
        ));
    }

    #[test]
    fn expectation_pauli_matches_dense_random() {
        // Random-ish circuit, compare expectation_pauli vs dense reference.
        let mut mps = MpsF64::new(4, 64);
        let angles = [0.3, 1.1, 2.2, 0.7, 1.9, 0.5];
        let ry = |t: f64| {
            let c = (t / 2.0).cos();
            let s = (t / 2.0).sin();
            [
                [Complex::new(c, 0.0), Complex::new(-s, 0.0)],
                [Complex::new(s, 0.0), Complex::new(c, 0.0)],
            ]
        };
        for (q, &a) in angles.iter().take(4).enumerate() {
            mps.apply_one_qubit(&ry(a), q);
        }
        // entangle adjacent pairs with CNOTs.
        let z = Complex::new(0.0, 0.0);
        let o = Complex::new(1.0, 0.0);
        let cnot = [[o, z, z, z], [z, z, z, o], [z, z, o, z], [z, o, z, z]];
        mps.apply_two_qubit_adjacent(&cnot, 0);
        mps.apply_two_qubit_adjacent(&cnot, 1);
        mps.apply_one_qubit(&ry(angles[4]), 2);
        mps.apply_two_qubit_adjacent(&cnot, 2);

        let sv = mps.statevector();
        for paulis in [
            [3u8, 3, 0, 0],
            [1, 0, 1, 0],
            [2, 2, 0, 0],
            [3, 1, 2, 3],
            [0, 0, 0, 3],
            [1, 1, 1, 1],
        ] {
            let got = mps.expectation_pauli(&paulis);
            let want = dense_pauli_expectation(&sv, &paulis);
            assert!(
                approx_eq(got, want, 1e-10),
                "paulis {paulis:?}: mps {got} vs dense {want}"
            );
        }
    }

    #[test]
    fn init_state_zero_ket_n3() {
        let mps = MpsF64::new(3, 64);
        let sv = mps.statevector();
        assert_eq!(sv.len(), 8);
        assert!(approx_eq(sv[0], Complex::new(1.0, 0.0), 1e-15));
        for amp in &sv[1..] {
            assert!(approx_eq(*amp, Complex::new(0.0, 0.0), 1e-15));
        }
    }

    #[test]
    fn n_eq_1_edge() {
        let mps = MpsF64::new(1, 64);
        let sv = mps.statevector();
        assert_eq!(sv.len(), 2);
        assert!(approx_eq(sv[0], Complex::new(1.0, 0.0), 1e-15));
        assert!(approx_eq(sv[1], Complex::new(0.0, 0.0), 1e-15));
    }

    #[test]
    fn norm_squared_initial_state() {
        for n in 1..=8 {
            let mps = MpsF64::new(n, 64);
            assert!(
                (mps.norm_squared() - 1.0).abs() < 1e-15,
                "n={n} norm² = {}",
                mps.norm_squared()
            );
        }
    }

    #[test]
    fn bond_dims_initial_state() {
        let mps = MpsF64::new(5, 64);
        for i in 0..=5 {
            assert_eq!(mps.bond_dim(i), 1, "bond_dim({i}) at init");
        }
    }

    #[test]
    fn num_qubits_and_max_bond_dim() {
        let mps = MpsF64::new(7, 32);
        assert_eq!(mps.num_qubits(), 7);
        assert_eq!(mps.max_bond_dim(), 32);
    }

    // -------- Cut 3: 1q gate --------

    fn h_matrix() -> [[Complex<f64>; 2]; 2] {
        let s = std::f64::consts::FRAC_1_SQRT_2;
        [
            [Complex::new(s, 0.0), Complex::new(s, 0.0)],
            [Complex::new(s, 0.0), Complex::new(-s, 0.0)],
        ]
    }

    fn x_matrix() -> [[Complex<f64>; 2]; 2] {
        [
            [Complex::new(0.0, 0.0), Complex::new(1.0, 0.0)],
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
        ]
    }

    fn rx_matrix(theta: f64) -> [[Complex<f64>; 2]; 2] {
        let c = (theta / 2.0).cos();
        let s = (theta / 2.0).sin();
        [
            [Complex::new(c, 0.0), Complex::new(0.0, -s)],
            [Complex::new(0.0, -s), Complex::new(c, 0.0)],
        ]
    }

    #[test]
    fn apply_h_on_qubit_0_n2() {
        // H on q0 of |00⟩ → (|0⟩+|1⟩)/√2 ⊗ |0⟩.  Little-endian: indices
        // s_0 + s_1·2 with q0 as LSB → amplitudes at indices 0 and 1.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        let sv = mps.statevector();
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        assert!(approx_eq(sv[0], Complex::new(inv, 0.0), 1e-15));
        assert!(approx_eq(sv[1], Complex::new(inv, 0.0), 1e-15));
        assert!(approx_eq(sv[2], Complex::new(0.0, 0.0), 1e-15));
        assert!(approx_eq(sv[3], Complex::new(0.0, 0.0), 1e-15));
    }

    #[test]
    fn apply_h_on_qubit_1_n2() {
        // H on q1 of |00⟩ → |0⟩ ⊗ (|0⟩+|1⟩)/√2.  Little-endian: s_1 = 1
        // means index 2 (since q1 is bit 1).
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        let sv = mps.statevector();
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        assert!(approx_eq(sv[0], Complex::new(inv, 0.0), 1e-15));
        assert!(approx_eq(sv[1], Complex::new(0.0, 0.0), 1e-15));
        assert!(approx_eq(sv[2], Complex::new(inv, 0.0), 1e-15));
        assert!(approx_eq(sv[3], Complex::new(0.0, 0.0), 1e-15));
    }

    #[test]
    fn apply_x_each_qubit_n3() {
        // X on every qubit of |000⟩ → |111⟩.  Little-endian → index 7.
        let mut mps = MpsF64::new(3, 64);
        for q in 0..3 {
            mps.apply_one_qubit(&x_matrix(), q);
        }
        let sv = mps.statevector();
        for (i, amp) in sv.iter().enumerate() {
            let expected = if i == 7 { 1.0 } else { 0.0 };
            assert!(
                approx_eq(*amp, Complex::new(expected, 0.0), 1e-15),
                "sv[{i}] = {amp}, expected {expected}"
            );
        }
    }

    #[test]
    fn apply_rx_pi_n1() {
        // Rx(π) |0⟩ = -i|1⟩.
        let mut mps = MpsF64::new(1, 64);
        mps.apply_one_qubit(&rx_matrix(std::f64::consts::PI), 0);
        let sv = mps.statevector();
        assert!(approx_eq(sv[0], Complex::new(0.0, 0.0), 1e-15));
        assert!(approx_eq(sv[1], Complex::new(0.0, -1.0), 1e-15));
    }

    #[test]
    fn apply_h_twice_is_identity() {
        // H · H = I → applying H twice on a qubit recovers |0⟩.
        let mut mps = MpsF64::new(3, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        let sv = mps.statevector();
        assert!(approx_eq(sv[0], Complex::new(1.0, 0.0), 1e-14));
        for amp in &sv[1..] {
            assert!(approx_eq(*amp, Complex::new(0.0, 0.0), 1e-14));
        }
    }

    #[test]
    fn one_qubit_preserves_norm() {
        let mut mps = MpsF64::new(4, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.apply_one_qubit(&rx_matrix(0.7), 2);
        mps.apply_one_qubit(&h_matrix(), 3);
        assert!((mps.norm_squared() - 1.0).abs() < 1e-14);
    }

    // -------- Cut 4: 인접 2q gate + SVD truncation --------

    /// `qsim_core::Gate::cnot_matrix` equivalent.  Per the LSB column
    /// convention this represents a CNOT in which the **higher-indexed
    /// qubit is the control** and the lower-indexed qubit is the target.
    fn cnot_matrix() -> [[Complex<f64>; 4]; 4] {
        let zero = Complex::new(0.0, 0.0);
        let one = Complex::new(1.0, 0.0);
        [
            [one, zero, zero, zero],
            [zero, one, zero, zero],
            [zero, zero, zero, one],
            [zero, zero, one, zero],
        ]
    }

    fn cz_matrix() -> [[Complex<f64>; 4]; 4] {
        let zero = Complex::new(0.0, 0.0);
        let one = Complex::new(1.0, 0.0);
        let neg = Complex::new(-1.0, 0.0);
        [
            [one, zero, zero, zero],
            [zero, one, zero, zero],
            [zero, zero, one, zero],
            [zero, zero, zero, neg],
        ]
    }

    #[test]
    fn bell_state_sentinel_n2() {
        // |00⟩ → H q1 → (idx0 + idx2)/√2 = (|00⟩ + |q1=1⟩)/√2.
        // CNOT (q1 control, q0 target) swaps idx10 ↔ idx11 → idx2 ↔ idx3.
        // Result: (idx0 + idx3)/√2 = (|00⟩ + |11⟩)/√2 = Bell state.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let sv = mps.statevector();
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        assert!(
            approx_eq(sv[0], Complex::new(inv, 0.0), 1e-14),
            "sv[0] = {}",
            sv[0]
        );
        assert!(
            approx_eq(sv[1], Complex::new(0.0, 0.0), 1e-14),
            "sv[1] = {}",
            sv[1]
        );
        assert!(
            approx_eq(sv[2], Complex::new(0.0, 0.0), 1e-14),
            "sv[2] = {}",
            sv[2]
        );
        assert!(
            approx_eq(sv[3], Complex::new(inv, 0.0), 1e-14),
            "sv[3] = {}",
            sv[3]
        );
        assert!((mps.norm_squared() - 1.0).abs() < 1e-14);
    }

    #[test]
    fn bit_ordering_asymmetric_sentinel() {
        // Build (|01⟩ + |10⟩)/√2 — amplitude at indices 1 and 2 in
        // little-endian, indices 0 and 3 zero.  This is the asymmetric
        // sentinel that catches bit-reversal bugs which the symmetric
        // GHZ sequence would not detect.
        //
        // Sequence: H q1 + cnot_matrix(0, 1) → Bell (idx0 + idx3)/√2,
        // then X q0 flips bit 0: idx0 ↔ idx1 and idx2 ↔ idx3, giving
        // (idx1 + idx2)/√2.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_one_qubit(&x_matrix(), 0);
        let sv = mps.statevector();
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        assert!(
            approx_eq(sv[0], Complex::new(0.0, 0.0), 1e-14),
            "sv[0] = {}",
            sv[0]
        );
        assert!(
            approx_eq(sv[1], Complex::new(inv, 0.0), 1e-14),
            "sv[1] = {}",
            sv[1]
        );
        assert!(
            approx_eq(sv[2], Complex::new(inv, 0.0), 1e-14),
            "sv[2] = {}",
            sv[2]
        );
        assert!(
            approx_eq(sv[3], Complex::new(0.0, 0.0), 1e-14),
            "sv[3] = {}",
            sv[3]
        );
    }

    #[test]
    fn ghz_3_sentinel() {
        // |000⟩ → H q2 → (idx0 + idx4)/√2 = (|q2=0⟩ + |q2=1⟩)/√2.
        // cnot_matrix(q0=1, q1=2) [q2 control, q1 target] swaps idx?10 ↔ idx?11
        // in 3-qubit space (with q0 free): idx4 ↔ idx6, idx5 ↔ idx7.
        // Our state at idx4 → idx6.  State now (idx0 + idx6)/√2.
        // cnot_matrix(q0=0, q1=1) [q1 control, q0 target] swaps idx10 ↔ idx11
        // for the (q0, q1) pair, with q2 spectator: idx2 ↔ idx3, idx6 ↔ idx7.
        // idx6 → idx7.  Final: (idx0 + idx7)/√2 = (|000⟩ + |111⟩)/√2 GHZ-3.
        let mut mps = MpsF64::new(3, 64);
        mps.apply_one_qubit(&h_matrix(), 2);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 1); // sites (1, 2)
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0); // sites (0, 1)
        let sv = mps.statevector();
        let inv = std::f64::consts::FRAC_1_SQRT_2;
        for (i, amp) in sv.iter().enumerate() {
            let expected = if i == 0 || i == 7 {
                Complex::new(inv, 0.0)
            } else {
                Complex::new(0.0, 0.0)
            };
            assert!(
                approx_eq(*amp, expected, 1e-13),
                "sv[{i}] = {amp}, expected {expected}"
            );
        }
        assert!((mps.norm_squared() - 1.0).abs() < 1e-13);
    }

    #[test]
    fn cnot_squared_is_identity() {
        // CNOT² = I.  Apply twice and confirm we return to a basis state.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&x_matrix(), 1); // |q0=0, q1=1⟩ = idx2
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0); // → idx3
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0); // → idx2 again
        let sv = mps.statevector();
        for (i, amp) in sv.iter().enumerate() {
            let expected = if i == 2 { 1.0 } else { 0.0 };
            assert!(
                approx_eq(*amp, Complex::new(expected, 0.0), 1e-13),
                "sv[{i}] = {amp}"
            );
        }
    }

    #[test]
    fn cz_phases_basis_state() {
        // CZ |11⟩ = -|11⟩.  In MPS with q0=1, q1=1 → idx3.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&x_matrix(), 0);
        mps.apply_one_qubit(&x_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cz_matrix(), 0);
        let sv = mps.statevector();
        assert!(approx_eq(sv[0], Complex::new(0.0, 0.0), 1e-14));
        assert!(approx_eq(sv[1], Complex::new(0.0, 0.0), 1e-14));
        assert!(approx_eq(sv[2], Complex::new(0.0, 0.0), 1e-14));
        assert!(approx_eq(sv[3], Complex::new(-1.0, 0.0), 1e-14));
    }

    #[test]
    fn two_qubit_preserves_norm() {
        // Mixed 1q + 2q sequence on n=4.
        let mut mps = MpsF64::new(4, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 1);
        mps.apply_one_qubit(&rx_matrix(0.4), 2);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 2);
        assert!(
            (mps.norm_squared() - 1.0).abs() < 1e-13,
            "norm² = {}",
            mps.norm_squared()
        );
    }

    #[test]
    fn bond_dim_grows_after_entangling_gate() {
        // Bell sequence — bond between q0 and q1 should grow from 1 to 2.
        let mut mps = MpsF64::new(2, 64);
        assert_eq!(mps.bond_dim(1), 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        assert_eq!(mps.bond_dim(1), 1, "1q gate must not change bond dim");
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        assert_eq!(mps.bond_dim(1), 2, "Bell state requires bond dim 2");
    }

    // -------- Cut 5: cross-check + truncation 정확성 --------

    fn y_matrix() -> [[Complex<f64>; 2]; 2] {
        [
            [Complex::new(0.0, 0.0), Complex::new(0.0, -1.0)],
            [Complex::new(0.0, 1.0), Complex::new(0.0, 0.0)],
        ]
    }

    fn z_matrix() -> [[Complex<f64>; 2]; 2] {
        [
            [Complex::new(1.0, 0.0), Complex::new(0.0, 0.0)],
            [Complex::new(0.0, 0.0), Complex::new(-1.0, 0.0)],
        ]
    }

    fn rz_matrix(theta: f64) -> [[Complex<f64>; 2]; 2] {
        let c = (theta / 2.0).cos();
        let s = (theta / 2.0).sin();
        [
            [Complex::new(c, -s), Complex::new(0.0, 0.0)],
            [Complex::new(0.0, 0.0), Complex::new(c, s)],
        ]
    }

    /// Run circuit `ops` on a fresh `qsim_core::StateVector<f64>` and
    /// return its amplitudes in little-endian order — identical to the
    /// convention used by `Mps::statevector()`.
    fn reference_statevector(n_qubits: usize, ops: &[Op]) -> Vec<Complex<f64>> {
        use qsim_core::operations::{apply_single_qubit_gate, apply_two_qubit_gate};
        use qsim_core::StateVector;
        let mut sv: StateVector<f64> = StateVector::new(n_qubits);
        for op in ops {
            match *op {
                Op::OneQ { ref gate, qubit } => {
                    apply_single_qubit_gate(&mut sv, gate, qubit);
                }
                Op::TwoQ { ref gate, q0, q1 } => {
                    apply_two_qubit_gate(&mut sv, gate, q0, q1);
                }
            }
        }
        sv.amplitudes().to_vec()
    }

    fn apply_to_mps(mps: &mut MpsF64, ops: &[Op]) {
        for op in ops {
            match *op {
                Op::OneQ { ref gate, qubit } => mps.apply_one_qubit(gate, qubit),
                Op::TwoQ { ref gate, q0, q1 } => {
                    debug_assert_eq!(q1, q0 + 1, "Stage 1: adjacent only");
                    mps.apply_two_qubit_adjacent(gate, q0);
                }
            }
        }
    }

    #[derive(Clone)]
    enum Op {
        OneQ {
            gate: [[Complex<f64>; 2]; 2],
            qubit: usize,
        },
        TwoQ {
            gate: [[Complex<f64>; 4]; 4],
            q0: usize,
            q1: usize,
        },
    }

    /// Build a depth-`depth` random circuit on `n` qubits.  Each step is
    /// either a random 1q gate (H/X/Y/Z/Rz with a random angle) on a
    /// random qubit, or an adjacent CNOT.
    fn random_circuit(seed: u64, n: usize, depth: usize) -> Vec<Op> {
        use rand::rngs::StdRng;
        use rand::{Rng, SeedableRng};
        let mut rng = StdRng::seed_from_u64(seed);
        let mut ops = Vec::with_capacity(depth);
        for _ in 0..depth {
            // Need at least 2 qubits for the 2q branch; otherwise force 1q.
            let pick_two = n >= 2 && rng.gen::<bool>();
            if pick_two {
                let q0 = rng.gen_range(0..n - 1);
                ops.push(Op::TwoQ {
                    gate: cnot_matrix(),
                    q0,
                    q1: q0 + 1,
                });
            } else {
                let qubit = rng.gen_range(0..n);
                let g = rng.gen_range(0..5);
                let gate = match g {
                    0 => h_matrix(),
                    1 => x_matrix(),
                    2 => y_matrix(),
                    3 => z_matrix(),
                    _ => rz_matrix(rng.gen::<f64>() * std::f64::consts::TAU),
                };
                ops.push(Op::OneQ { gate, qubit });
            }
        }
        ops
    }

    fn max_diff(a: &[Complex<f64>], b: &[Complex<f64>]) -> f64 {
        assert_eq!(a.len(), b.len());
        a.iter()
            .zip(b.iter())
            .map(|(x, y)| (x - y).norm())
            .fold(0.0_f64, f64::max)
    }

    #[test]
    fn ghz_n_consistency_2_to_8() {
        // GHZ-N built with the LSB cnot_matrix convention requires the
        // initial Hadamard on the highest-indexed qubit (since
        // cnot_matrix has q1 control / q0 target, "moving down").
        for n in 2..=8 {
            let mut ops = vec![Op::OneQ {
                gate: h_matrix(),
                qubit: n - 1,
            }];
            for i in (0..n - 1).rev() {
                ops.push(Op::TwoQ {
                    gate: cnot_matrix(),
                    q0: i,
                    q1: i + 1,
                });
            }
            let mut mps = MpsF64::new(n, 64);
            apply_to_mps(&mut mps, &ops);
            let mps_sv = mps.statevector();
            let ref_sv = reference_statevector(n, &ops);
            let diff = max_diff(&mps_sv, &ref_sv);
            assert!(
                diff < 1e-12,
                "n={n} GHZ MPS vs StateVector max abs diff = {diff:e}"
            );
            // Sanity: GHZ has amplitude only at indices 0 and 2^n - 1.
            let inv = std::f64::consts::FRAC_1_SQRT_2;
            assert!(approx_eq(mps_sv[0], Complex::new(inv, 0.0), 1e-12));
            assert!(approx_eq(
                mps_sv[(1 << n) - 1],
                Complex::new(inv, 0.0),
                1e-12
            ));
        }
    }

    #[test]
    fn random_circuit_consistency_n4_depth10() {
        for seed in 0..30 {
            let ops = random_circuit(seed, 4, 10);
            let mut mps = MpsF64::new(4, 64);
            apply_to_mps(&mut mps, &ops);
            let mps_sv = mps.statevector();
            let ref_sv = reference_statevector(4, &ops);
            let diff = max_diff(&mps_sv, &ref_sv);
            assert!(
                diff < 1e-10,
                "seed={seed} MPS vs StateVector max abs diff = {diff:e}"
            );
        }
    }

    #[test]
    fn random_circuit_norm_preservation() {
        for seed in 0..30 {
            let n = 2 + (seed as usize % 5); // n ∈ [2, 6]
            let ops = random_circuit(seed, n, 8);
            let mut mps = MpsF64::new(n, 64);
            apply_to_mps(&mut mps, &ops);
            let norm_sq = mps.norm_squared();
            assert!(
                (norm_sq - 1.0).abs() < 1e-10,
                "seed={seed} n={n} norm² = {norm_sq}"
            );
        }
    }

    #[test]
    fn truncation_chi_max_2_ghz_lossless() {
        // GHZ-N has Schmidt rank 2 across every cut → max_bond_dim = 2
        // is sufficient and must produce zero truncation error.
        for n in 2..=6 {
            let mut ops = vec![Op::OneQ {
                gate: h_matrix(),
                qubit: n - 1,
            }];
            for i in (0..n - 1).rev() {
                ops.push(Op::TwoQ {
                    gate: cnot_matrix(),
                    q0: i,
                    q1: i + 1,
                });
            }
            let mut mps = MpsF64::new(n, 2);
            apply_to_mps(&mut mps, &ops);
            assert!(
                (mps.norm_squared() - 1.0).abs() < 1e-12,
                "GHZ-{n} chi=2 norm² = {}",
                mps.norm_squared()
            );
            let mps_sv = mps.statevector();
            let ref_sv = reference_statevector(n, &ops);
            let diff = max_diff(&mps_sv, &ref_sv);
            assert!(diff < 1e-12, "GHZ-{n} chi=2 vs StateVector diff = {diff:e}");
        }
    }

    // -------- Cut 6: edge cases (#[should_panic]) --------

    #[test]
    #[should_panic(expected = "n_qubits >= 1")]
    fn new_panics_on_zero_qubits() {
        let _ = MpsF64::new(0, 64);
    }

    #[test]
    #[should_panic(expected = "max_bond_dim >= 1")]
    fn new_panics_on_zero_max_bond_dim() {
        let _ = MpsF64::new(4, 0);
    }

    #[test]
    #[should_panic(expected = "qubit 5 out of range")]
    fn apply_one_qubit_panics_on_out_of_range() {
        let mut mps = MpsF64::new(3, 64);
        mps.apply_one_qubit(&h_matrix(), 5);
    }

    #[test]
    #[should_panic(expected = "out of range")]
    fn apply_two_qubit_adjacent_panics_at_right_boundary() {
        // q0 = n_qubits - 1 ⇒ q1 = n_qubits is out of range — the only
        // way to violate adjacency in Stage 1 since the API takes a
        // single `q0` and forces `q1 = q0 + 1`.
        let mut mps = MpsF64::new(4, 64);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 3);
    }

    #[test]
    #[should_panic(expected = "n_qubits <= 20")]
    fn statevector_panics_above_20_qubits() {
        // The MPS itself is cheap (21 tensors of shape [1, 2, 1]); the
        // assertion fires before the dense 2^n buffer is allocated.
        let mps = MpsF64::new(21, 4);
        let _ = mps.statevector();
    }

    #[test]
    fn truncation_chi_max_1_bell_lossy() {
        // Bell has Schmidt rank 2 — capping at chi_max = 1 must lose
        // exactly half the squared norm (one of the two equal singular
        // values 1/√2 is dropped, contributing 1/2).
        let mut mps = MpsF64::new(2, 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        assert_eq!(mps.bond_dim(1), 1, "max_bond_dim=1 must cap the bond at 1");
        let norm_sq = mps.norm_squared();
        assert!(
            (norm_sq - 0.5).abs() < 1e-12,
            "Bell chi=1 norm² should be 0.5, got {norm_sq}"
        );
    }

    // -------- v0.6.3: truncation_error_sum accumulator --------

    #[test]
    fn truncation_error_sum_starts_at_zero() {
        // Fresh MPS has performed no SVDs yet.
        let mps = MpsF64::new(4, 64);
        assert_eq!(mps.truncation_error_sum(), 0.0);
    }

    #[test]
    fn truncation_error_lossless_unitary() {
        // GHZ-4 with chi_max=64 (≥ Schmidt rank 2 everywhere) → no SVD
        // ever discards any singular value → truncation error stays 0.
        let mut mps = MpsF64::new(4, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 2);
        assert!(
            mps.truncation_error_sum() < 1e-14,
            "lossless unitary should have ~0 truncation error, got {}",
            mps.truncation_error_sum()
        );
        // Sanity: norm² is preserved.
        assert!((mps.norm_squared() - 1.0).abs() < 1e-12);
    }

    #[test]
    fn truncation_error_chi_1_bell() {
        // Bell + chi_max=1 drops one singular value 1/√2 → discarded
        // weight = (1/√2)² = 0.5 (Schollwöck §4.5.3 absolute metric).
        let mut mps = MpsF64::new(2, 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let err = mps.truncation_error_sum();
        assert!(
            (err - 0.5).abs() < 1e-12,
            "Bell chi=1 truncation error should be 0.5, got {err}"
        );
    }

    #[test]
    fn truncation_error_accumulates() {
        // Two truncating SVDs on independent Bell pairs → discarded
        // weights add: 0.5 + 0.5 = 1.0.
        let mut mps = MpsF64::new(4, 1);
        // First Bell pair on (0, 1).
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let after_first = mps.truncation_error_sum();
        assert!((after_first - 0.5).abs() < 1e-12);
        // Second Bell pair on (2, 3).
        mps.apply_one_qubit(&h_matrix(), 3);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 2);
        let after_second = mps.truncation_error_sum();
        assert!(
            (after_second - 1.0).abs() < 1e-12,
            "two chi=1 Bell truncations should sum to 1.0, got {after_second}"
        );
    }

    #[test]
    fn truncation_error_canonicalize_does_not_accumulate() {
        // right_canonicalize uses thin SVDs that keep all singular
        // values (no rank cap below true Schmidt rank), so it must not
        // add to truncation_error_sum.  v0.6.5: this only holds when
        // trunc_threshold == 0.0 (the default for Mps::new).
        let mut mps = MpsF64::new(4, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 2);
        let before = mps.truncation_error_sum();
        mps.right_canonicalize();
        let after = mps.truncation_error_sum();
        assert_eq!(
            before, after,
            "canonicalize must not change truncation_error_sum"
        );
    }

    // -------- v0.6.5 Cut 1: trunc_threshold + observed_max_bond_dim --------

    /// Build an N-qubit GHZ state.  `cnot_matrix()` has control on the
    /// **higher** qubit, so the standard pattern is: H on the top qubit,
    /// then CNOTs propagating downward (`i = n-2, n-3, …, 0`), matching
    /// the existing `truncation_chi_max_2_ghz_lossless` test.  GHZ has
    /// Schmidt rank 2 at every cut, so an MPS with sufficient χ_max and
    /// any `trunc_threshold` below the surviving singular value
    /// (`1/√2 ≈ 0.707`) must keep exactly 2 modes.
    fn build_ghz(n: usize, max_bond_dim: usize, trunc_threshold: f64) -> MpsF64 {
        let mut mps = MpsF64::with_threshold(n, max_bond_dim, trunc_threshold);
        mps.apply_one_qubit(&h_matrix(), n - 1);
        for i in (0..n - 1).rev() {
            mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
        }
        mps
    }

    #[test]
    fn trunc_threshold_drops_tiny_sv() {
        // GHZ-6 with eps=1e-10 and χ_max=64 must collapse to χ=2 — the
        // Schmidt rank of GHZ.  Adaptive truncation is the entire point
        // of trunc_threshold.
        let mps = build_ghz(6, 64, 1e-10);
        assert_eq!(
            mps.observed_max_bond_dim(),
            2,
            "GHZ Schmidt rank is 2; observed χ = {}",
            mps.observed_max_bond_dim()
        );
        // Truncation error is the discarded weight: all dropped singular
        // values were < 1e-10, so |trunc_error_sum| < 1e-18.
        assert!(
            mps.truncation_error_sum() < 1e-18,
            "eps=1e-10 should drop only noise modes; got {}",
            mps.truncation_error_sum()
        );
    }

    #[test]
    fn trunc_threshold_zero_matches_v063() {
        // Default eps=0 must reproduce v0.6.3 byte-identically.  Compare
        // the statevector + truncation_error_sum + observed bond dim of
        // a small lossy circuit (χ=1 Bell) computed via Mps::new vs
        // explicit with_threshold(_, _, 0.0).
        let mut a = MpsF64::new(2, 1);
        a.apply_one_qubit(&h_matrix(), 0);
        a.apply_two_qubit_adjacent(&cnot_matrix(), 0);

        let mut b = MpsF64::with_threshold(2, 1, 0.0);
        b.apply_one_qubit(&h_matrix(), 0);
        b.apply_two_qubit_adjacent(&cnot_matrix(), 0);

        assert_eq!(a.trunc_threshold(), 0.0);
        assert_eq!(b.trunc_threshold(), 0.0);
        assert_eq!(a.truncation_error_sum(), b.truncation_error_sum());
        assert_eq!(a.observed_max_bond_dim(), b.observed_max_bond_dim());
        let sv_a = a.statevector();
        let sv_b = b.statevector();
        assert_eq!(sv_a.len(), sv_b.len());
        for (x, y) in sv_a.iter().zip(sv_b.iter()) {
            assert_eq!(x, y);
        }
    }

    #[test]
    fn trunc_threshold_zero_recovers_full_chi() {
        // GHZ-6 with eps=0 and χ_max=64: observed χ is still 2 (the true
        // Schmidt rank), proving the eps>0 path is not the only way to
        // get adaptive χ — the SVD itself happens to truncate to the
        // exact rank.  Sanity check that observed_max_bond_dim() reads
        // the correct bonds.
        let mps = build_ghz(6, 64, 0.0);
        assert_eq!(mps.observed_max_bond_dim(), 2);
    }

    #[test]
    fn with_threshold_rejects_invalid_input() {
        // Negative or NaN threshold must panic at construction.
        std::panic::set_hook(Box::new(|_| {})); // silence in test output
        let r = std::panic::catch_unwind(|| MpsF64::with_threshold(4, 64, -1.0));
        assert!(r.is_err(), "negative trunc_threshold must panic");
        let r = std::panic::catch_unwind(|| MpsF64::with_threshold(4, 64, f64::NAN));
        assert!(r.is_err(), "NaN trunc_threshold must panic");
        let _ = std::panic::take_hook();
    }

    #[test]
    fn observed_max_bond_dim_on_product_state() {
        // |0...0⟩ has bond dim 1 at every cut.
        let mps = MpsF64::new(8, 64);
        assert_eq!(mps.observed_max_bond_dim(), 1);
    }

    // -------- v0.6.5 Cut 5: f32 generic --------

    #[test]
    fn f32_init_state_zero_ket() {
        let mps = MpsF32::new(3, 64);
        let sv = mps.statevector();
        assert_eq!(sv.len(), 8);
        assert!((sv[0] - Complex::new(1.0_f32, 0.0)).norm() < 1e-6);
        for amp in &sv[1..] {
            assert!(amp.norm() < 1e-6);
        }
    }

    #[test]
    fn f32_ghz_4_bond_dim_2() {
        let mut mps = MpsF32::new(4, 64);
        mps.apply_one_qubit(&h_matrix(), 3);
        for i in (0..3).rev() {
            mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
        }
        assert_eq!(mps.observed_max_bond_dim(), 2);
        let norm = mps.norm_squared();
        assert!((norm - 1.0).abs() < 1e-5, "f32 GHZ-4 norm² = {norm}");
    }

    #[test]
    fn f32_f64_fidelity_ghz_6() {
        // Same circuit on f32 and f64 must produce states whose fidelity
        // exceeds 1 - 1e-4.
        let n = 6;
        let mut a64 = MpsF64::new(n, 64);
        let mut a32 = MpsF32::new(n, 64);
        a64.apply_one_qubit(&h_matrix(), n - 1);
        a32.apply_one_qubit(&h_matrix(), n - 1);
        for i in (0..n - 1).rev() {
            a64.apply_two_qubit_adjacent(&cnot_matrix(), i);
            a32.apply_two_qubit_adjacent(&cnot_matrix(), i);
        }
        let sv64 = a64.statevector();
        let sv32 = a32.statevector();
        let mut inner = Complex::<f64>::new(0.0, 0.0);
        for (x64, x32) in sv64.iter().zip(sv32.iter()) {
            let x32_as64 = Complex::<f64>::new(x32.re as f64, x32.im as f64);
            inner += x64.conj() * x32_as64;
        }
        let fidelity = inner.norm_sqr();
        assert!(fidelity > 1.0 - 1e-4, "f32/f64 fidelity = {fidelity}");
    }

    // -------- v0.6.5 Cut 6: collapse_qubit + single_qubit_probability --------

    #[test]
    fn single_qubit_probability_bell_q0() {
        // (|00⟩+|11⟩)/√2 — measuring q0: p(1) = 0.5.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.right_canonicalize();
        let p = mps.single_qubit_probability(0);
        assert!((p - 0.5).abs() < 1e-12, "Bell q0 p(1) = {p}");
    }

    #[test]
    fn collapse_bell_q0_to_zero() {
        // Bell + collapse(q0, 0) → |00⟩.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.right_canonicalize();
        let p = mps.collapse_qubit(0, false);
        assert!((p - 0.5).abs() < 1e-12);
        // norm after collapse should be 1 (we renormalised).
        let n = mps.norm_squared();
        assert!((n - 1.0).abs() < 1e-12, "post-collapse norm² = {n}");
        // statevector should be |00⟩ (only index 0 non-zero).
        let sv = mps.statevector();
        assert!((sv[0] - Complex::new(1.0, 0.0)).norm() < 1e-12);
        for amp in &sv[1..] {
            assert!(amp.norm() < 1e-12);
        }
    }

    #[test]
    fn collapse_bell_q0_to_one() {
        // Bell + collapse(q0, 1) → |11⟩.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.right_canonicalize();
        let p = mps.collapse_qubit(0, true);
        assert!((p - 0.5).abs() < 1e-12);
        let sv = mps.statevector();
        // |11⟩ has little-endian index 3.
        assert!((sv[3] - Complex::new(1.0, 0.0)).norm() < 1e-12);
        assert!(sv[0].norm() < 1e-12);
    }

    #[test]
    fn collapse_product_state_idempotent() {
        // |+⟩|0⟩ — collapse q0 onto 0 deterministically reduces to |0⟩|0⟩.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.right_canonicalize();
        let p = mps.collapse_qubit(0, false);
        assert!((p - 0.5).abs() < 1e-12);
        let sv = mps.statevector();
        assert!((sv[0] - Complex::new(1.0, 0.0)).norm() < 1e-12);
    }

    #[test]
    fn collapse_then_canonicalize_preserves_state() {
        // After collapse + re-canonicalize, the state must still be a
        // valid normalised MPS that contracts to the projected
        // statevector.
        let mut mps = MpsF64::new(3, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 1);
        mps.right_canonicalize();
        let _ = mps.collapse_qubit(1, true);
        mps.right_canonicalize();
        let n = mps.norm_squared();
        assert!((n - 1.0).abs() < 1e-12);
    }

    #[test]
    fn f32_truncation_error_sum_is_f64() {
        // truncation_error_sum always reported as f64 even for f32 MPS.
        let mut mps = MpsF32::new(2, 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let err = mps.truncation_error_sum();
        assert!((err - 0.5).abs() < 1e-4, "f32 chi=1 Bell err = {err}");
    }

    #[test]
    fn rayon_par_path_matches_sequential_large_n() {
        // v0.6.5: hot loops use rayon par_chunks_mut above PAR_THRESHOLD.
        // Running the same circuit twice must give byte-identical results
        // — rayon's outer-by-`a` + inner-sequential reduction is
        // deterministic (each output cell has exactly one writer).  We
        // pick an N large enough that PAR_THRESHOLD (32) is comfortably
        // exceeded at every cut.
        let n = 8;
        let mut a = MpsF64::new(n, 64);
        let mut b = MpsF64::new(n, 64);
        for q in 0..n {
            a.apply_one_qubit(&h_matrix(), q);
            b.apply_one_qubit(&h_matrix(), q);
        }
        for q in 0..n - 1 {
            a.apply_two_qubit_adjacent(&cnot_matrix(), q);
            b.apply_two_qubit_adjacent(&cnot_matrix(), q);
        }
        let sv_a = a.statevector();
        let sv_b = b.statevector();
        assert_eq!(sv_a.len(), sv_b.len());
        for (x, y) in sv_a.iter().zip(sv_b.iter()) {
            assert_eq!(x, y, "rayon par path must be bit-deterministic");
        }
        assert_eq!(a.truncation_error_sum(), b.truncation_error_sum());
    }

    #[test]
    fn trunc_threshold_stricter_than_chi_max() {
        // When eps drops the same modes that χ_max would drop, the
        // resulting MPS is identical.  Here χ_max=2 already keeps only
        // the dominant Schmidt mode; eps=0.1 (well below 1/√2 ≈ 0.707)
        // matches it.
        let mps_chi = build_ghz(4, 2, 0.0);
        let mps_eps = build_ghz(4, 64, 0.1);
        // Both observed χ = 2.
        assert_eq!(mps_chi.observed_max_bond_dim(), 2);
        assert_eq!(mps_eps.observed_max_bond_dim(), 2);
    }

    // -------- v0.6.1 Cut 1: right_canonicalize --------

    /// Verify that every site `i >= 1` is row-orthogonal after
    /// `right_canonicalize()` — i.e. the matrix obtained by reshaping
    /// `T_i` to shape `[chi_left, 2 · chi_right]` satisfies
    /// `M · M† = I_{chi_left}`.
    fn assert_right_canonical(mps: &MpsF64, eps: f64) {
        for i in 1..mps.n_qubits {
            let t = &mps.tensors[i];
            let chi_l = t.left;
            let chi_r = t.right;
            // Build M of shape (chi_l, 2·chi_r) row-major.
            let cols = 2 * chi_r;
            let mut m = vec![Complex::new(0.0, 0.0); chi_l * cols];
            for a in 0..chi_l {
                for p in 0..2 {
                    for c in 0..chi_r {
                        m[a * cols + p * chi_r + c] = t.get(a, p, c);
                    }
                }
            }
            // Compute M · M† element-wise: shape (chi_l, chi_l).
            for a in 0..chi_l {
                for ap in 0..chi_l {
                    let mut acc = Complex::new(0.0, 0.0);
                    for k in 0..cols {
                        acc += m[a * cols + k] * m[ap * cols + k].conj();
                    }
                    let expected = if a == ap {
                        Complex::new(1.0, 0.0)
                    } else {
                        Complex::new(0.0, 0.0)
                    };
                    assert!(
                        (acc - expected).norm() < eps,
                        "site {i} not right-orthogonal: M·M†[{a},{ap}] = {acc}, \
                         expected {expected}"
                    );
                }
            }
        }
    }

    #[test]
    fn right_canonicalize_init_state_noop() {
        // Initial state |0...0⟩ has all bond dims 1 — already trivially
        // right-canonical.  Sweep must not change anything.
        let mut mps = MpsF64::new(5, 64);
        let sv_before = mps.statevector();
        mps.right_canonicalize();
        let sv_after = mps.statevector();
        for (a, b) in sv_before.iter().zip(sv_after.iter()) {
            assert!((a - b).norm() < 1e-14);
        }
        assert_right_canonical(&mps, 1e-12);
    }

    #[test]
    fn right_canonicalize_n_eq_1_noop() {
        // n=1: trivial branch — no sweep, no panic.
        let mut mps = MpsF64::new(1, 64);
        mps.apply_one_qubit(&h_matrix(), 0);
        let sv_before = mps.statevector();
        mps.right_canonicalize();
        let sv_after = mps.statevector();
        for (a, b) in sv_before.iter().zip(sv_after.iter()) {
            assert!((a - b).norm() < 1e-14);
        }
    }

    #[test]
    fn right_canonicalize_bell_preserves_state() {
        // Bell: H q1 + CNOT(0,1).  After canonicalize, statevector must
        // be byte-identical (norm-preserving isometry).
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let sv_before = mps.statevector();
        mps.right_canonicalize();
        let sv_after = mps.statevector();
        for (a, b) in sv_before.iter().zip(sv_after.iter()) {
            assert!(
                (a - b).norm() < 1e-13,
                "Bell statevector changed by canonicalize: {a} vs {b}"
            );
        }
        assert_right_canonical(&mps, 1e-12);
    }

    #[test]
    fn right_canonicalize_ghz_n_preserves_state() {
        for n in 2..=8 {
            let mut mps = MpsF64::new(n, 64);
            mps.apply_one_qubit(&h_matrix(), n - 1);
            for i in (0..n - 1).rev() {
                mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
            }
            let sv_before = mps.statevector();
            mps.right_canonicalize();
            let sv_after = mps.statevector();
            let max_diff = sv_before
                .iter()
                .zip(sv_after.iter())
                .map(|(a, b)| (a - b).norm())
                .fold(0.0_f64, f64::max);
            assert!(max_diff < 1e-12, "GHZ-{n} canonicalize diff = {max_diff:e}");
            assert_right_canonical(&mps, 1e-11);
            // Norm² must be preserved at 1.0 (no truncation).
            assert!((mps.norm_squared() - 1.0).abs() < 1e-12);
        }
    }

    #[test]
    fn right_canonicalize_random_circuit_preserves_state() {
        // 30 random shallow circuits — the strongest sentinel for SVD
        // / col-major / bit-ordering bugs.
        for seed in 0..30 {
            let n = 4;
            let ops = random_circuit(seed, n, 12);
            let mut mps = MpsF64::new(n, 64);
            apply_to_mps(&mut mps, &ops);
            let sv_before = mps.statevector();
            mps.right_canonicalize();
            let sv_after = mps.statevector();
            let diff = max_diff(&sv_before, &sv_after);
            assert!(
                diff < 1e-11,
                "seed={seed} canonicalize state diff = {diff:e}"
            );
            assert_right_canonical(&mps, 1e-10);
        }
    }

    #[test]
    fn right_canonicalize_does_not_grow_bonds() {
        // Bond dim is bounded by min(chi_left, 2·chi_right) at each cut.
        // In particular, GHZ-N has Schmidt rank 2 → all internal bonds
        // become exactly 2 after canonicalize (compressing any over-bond
        // residual from earlier in the sweep).
        for n in 2..=6 {
            let mut mps = MpsF64::new(n, 64);
            mps.apply_one_qubit(&h_matrix(), n - 1);
            for i in (0..n - 1).rev() {
                mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
            }
            mps.right_canonicalize();
            for cut in 1..n {
                let chi = mps.bond_dim(cut);
                assert!(chi <= 2, "GHZ-{n} bond_dim({cut}) = {chi}, expected ≤ 2");
            }
        }
    }

    #[test]
    fn right_canonicalize_is_idempotent() {
        // Calling canonicalize twice must not change the state.
        let mut mps = MpsF64::new(4, 64);
        let ops = random_circuit(7, 4, 8);
        apply_to_mps(&mut mps, &ops);
        mps.right_canonicalize();
        let sv_first = mps.statevector();
        mps.right_canonicalize();
        let sv_second = mps.statevector();
        let diff = max_diff(&sv_first, &sv_second);
        assert!(diff < 1e-12, "idempotence violated: diff = {diff:e}");
    }

    // -------- v0.6.1 Cut 2: sample + norm_squared direct --------

    #[test]
    fn norm_squared_direct_initial_state() {
        for n in 1..=8 {
            let mps = MpsF64::new(n, 64);
            let nq = mps.norm_squared();
            assert!((nq - 1.0).abs() < 1e-15, "n={n} initial state norm² = {nq}");
        }
    }

    #[test]
    fn norm_squared_direct_matches_dense() {
        // Random shallow circuits — norm_squared (direct) must agree
        // with naive |sv|² sum for n ≤ 8.
        for seed in 0..20 {
            let n = 2 + (seed as usize % 5); // n ∈ [2, 6]
            let ops = random_circuit(seed, n, 10);
            let mut mps = MpsF64::new(n, 64);
            apply_to_mps(&mut mps, &ops);
            let direct = mps.norm_squared();
            let dense: f64 = mps.statevector().iter().map(|a| a.norm_sqr()).sum();
            assert!(
                (direct - dense).abs() < 1e-12,
                "seed={seed} direct={direct} dense={dense}"
            );
        }
    }

    #[test]
    fn norm_squared_direct_truncated_bell() {
        // Bell with χ=1 truncation → norm² = 0.5 (lossy), direct path
        // must report the same value the dense path does.
        let mut mps = MpsF64::new(2, 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        let direct = mps.norm_squared();
        assert!((direct - 0.5).abs() < 1e-12, "direct = {direct}");
    }

    #[test]
    fn norm_squared_direct_n_30_runs() {
        // N=30 χ=4 — dense statevector would need 16 GiB (panic on
        // statevector()).  Direct contraction must complete cheaply.
        // GHZ-30 specifically — Schmidt rank 2 keeps everything tiny.
        let n = 30;
        let mut mps = MpsF64::new(n, 4);
        mps.apply_one_qubit(&h_matrix(), n - 1);
        for i in (0..n - 1).rev() {
            mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
        }
        let nq = mps.norm_squared();
        assert!(
            (nq - 1.0).abs() < 1e-10,
            "GHZ-{n} χ=4 norm² = {nq}, expected ≈ 1.0"
        );
    }

    fn make_rng(seed: u64) -> rand::rngs::StdRng {
        use rand::SeedableRng;
        rand::rngs::StdRng::seed_from_u64(seed)
    }

    /// Test helper: convert a `u64` outcome value (LSB-first per qubit)
    /// to the `Vec<bool>` form used by `Mps::sample` since v0.6.3.
    fn u64_to_bits(value: u64, n: usize) -> Vec<bool> {
        (0..n).map(|i| (value >> i) & 1 == 1).collect()
    }

    #[test]
    fn sample_bell_distribution() {
        // Bell |00⟩ + |11⟩ → only outcomes [false, false] and [true, true].
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.right_canonicalize();
        let mut rng = make_rng(42);
        let counts = mps.sample(10_000, &mut rng);
        let n00 = counts.get(&u64_to_bits(0b00, 2)).copied().unwrap_or(0);
        let n11 = counts.get(&u64_to_bits(0b11, 2)).copied().unwrap_or(0);
        let n01 = counts.get(&u64_to_bits(0b01, 2)).copied().unwrap_or(0);
        let n10 = counts.get(&u64_to_bits(0b10, 2)).copied().unwrap_or(0);
        assert_eq!(n01, 0, "Bell should never produce |01⟩");
        assert_eq!(n10, 0, "Bell should never produce |10⟩");
        assert!((n00 as f64 / 10_000.0 - 0.5).abs() < 0.03, "n00 = {n00}");
        assert!((n11 as f64 / 10_000.0 - 0.5).abs() < 0.03, "n11 = {n11}");
    }

    #[test]
    fn sample_bit_ordering_asymmetric_sentinel() {
        // (|01⟩ + |10⟩)/√2 — outcome bits [true, false] and [false, true] only.
        // Catches any LSB-first / MSB-first reversal in sample_once
        // that the symmetric Bell sentinel cannot detect.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.apply_one_qubit(&x_matrix(), 0);
        mps.right_canonicalize();
        let mut rng = make_rng(7);
        let counts = mps.sample(2000, &mut rng);
        let n01 = counts.get(&u64_to_bits(0b01, 2)).copied().unwrap_or(0);
        let n10 = counts.get(&u64_to_bits(0b10, 2)).copied().unwrap_or(0);
        assert_eq!(counts.get(&u64_to_bits(0b00, 2)).copied().unwrap_or(0), 0);
        assert_eq!(counts.get(&u64_to_bits(0b11, 2)).copied().unwrap_or(0), 0);
        assert_eq!(n01 + n10, 2000);
    }

    #[test]
    fn sample_ghz_n_distribution() {
        // GHZ-N — only [false; N] and [true; N] outcomes.
        for n in 2..=10 {
            let mut mps = MpsF64::new(n, 64);
            mps.apply_one_qubit(&h_matrix(), n - 1);
            for i in (0..n - 1).rev() {
                mps.apply_two_qubit_adjacent(&cnot_matrix(), i);
            }
            mps.right_canonicalize();
            let mut rng = make_rng(123 + n as u64);
            let counts = mps.sample(2000, &mut rng);
            let all_zero = vec![false; n];
            let all_one = vec![true; n];
            let n0 = counts.get(&all_zero).copied().unwrap_or(0);
            let n_all = counts.get(&all_one).copied().unwrap_or(0);
            // every other outcome must be zero.
            for (k, &v) in &counts {
                assert!(
                    k == &all_zero || k == &all_one,
                    "GHZ-{n} unexpected outcome {k:?} count {v}"
                );
            }
            assert_eq!(n0 + n_all, 2000);
            // 50:50 sanity (loose tolerance for small N).
            assert!((n0 as f64 / 2000.0 - 0.5).abs() < 0.06, "GHZ-{n} n0 = {n0}");
        }
    }

    #[test]
    fn sample_random_n6_consistency() {
        // Random shallow circuits — sampled frequencies match
        // statevector probabilities within ~5σ for shots=10_000.
        for seed in 0..10 {
            let n = 6;
            let ops = random_circuit(seed, n, 10);
            let mut mps = MpsF64::new(n, 64);
            apply_to_mps(&mut mps, &ops);
            mps.right_canonicalize();
            let probs: Vec<f64> = mps.statevector().iter().map(|a| a.norm_sqr()).collect();

            let mut rng = make_rng(seed * 31 + 1);
            let shots = 10_000;
            let counts = mps.sample(shots, &mut rng);
            // L∞ distance between sampled freq and true probabilities.
            let mut max_dev = 0.0_f64;
            for (k, p) in probs.iter().enumerate() {
                let bits = u64_to_bits(k as u64, n);
                let f = counts.get(&bits).copied().unwrap_or(0) as f64 / shots as f64;
                max_dev = max_dev.max((f - p).abs());
            }
            // Expected sampling stderr per bin is sqrt(p(1-p)/shots) ≤ 0.005.
            // 5σ ≈ 0.025 for the worst single bin (with ~64 bins).
            assert!(
                max_dev < 0.05,
                "seed={seed} max sampled deviation = {max_dev:e}"
            );
        }
    }

    #[test]
    fn sample_swap_circuit_outcome() {
        // X q0 → swap(0, 1) → state |q0=0, q1=1⟩, outcome bit 1 set at site 1.
        // Vec<bool>: outcome[0] = false, outcome[1] = true.
        let mut mps = MpsF64::new(2, 64);
        mps.apply_one_qubit(&x_matrix(), 0);
        mps.apply_two_qubit_adjacent(&swap_matrix(), 0);
        mps.right_canonicalize();
        let mut rng = make_rng(0);
        let counts = mps.sample(50, &mut rng);
        assert_eq!(counts.get(&u64_to_bits(0b10, 2)).copied().unwrap_or(0), 50);
    }

    #[test]
    fn sample_truncated_bell_chi_1() {
        // χ=1 truncated Bell — half the amplitude is lost, but the
        // surviving (renormalised) distribution must produce a single
        // basis outcome (whichever singular vector survived) with
        // probability 1.  Either |00⟩ or |11⟩ depending on SVD ordering;
        // the test just asserts it's a single deterministic outcome.
        let mut mps = MpsF64::new(2, 1);
        mps.apply_one_qubit(&h_matrix(), 1);
        mps.apply_two_qubit_adjacent(&cnot_matrix(), 0);
        mps.right_canonicalize();
        let mut rng = make_rng(42);
        let counts = mps.sample(100, &mut rng);
        assert_eq!(counts.len(), 1, "χ=1 must collapse to one outcome");
        // norm² is 0.5 but sampling renormalises.
        assert!((mps.norm_squared() - 0.5).abs() < 1e-12);
    }

    /// Helper for swap_matrix in tests (CNOT/CZ already exist).
    fn swap_matrix() -> [[Complex<f64>; 4]; 4] {
        let zero = Complex::new(0.0, 0.0);
        let one = Complex::new(1.0, 0.0);
        [
            [one, zero, zero, zero],
            [zero, zero, one, zero],
            [zero, one, zero, zero],
            [zero, zero, zero, one],
        ]
    }
}
