//! GPU thin-SVD for MPS truncation (v0.6.6).
//!
//! `wgpu_thin_svd` (Cut 4) 가 `(rows × cols)` complex f32 행렬 한 개의
//! thin SVD 를 GPU 에서 계산해 `(U, Σ, V†, trunc_error_sq, keep)` 를
//! 반환한다.  Cut 3 은 그 아래의 [`dispatch_jacobi_svd`] 를 통해 full
//! one-sided Jacobi SVD 를 노출 — truncation 없음.
//!
//! ## 인터페이스 정책
//! - **Column-major in / column-major out**: WGSL bind layout 의 자연스러운
//!   choice.  caller (Mps lib.rs) 가 row-major 면 transpose 가 필요하나,
//!   `wgpu_thin_svd` wrapper (Cut 4) 에서 host-side 한 번만 변환.
//! - **rows ≥ cols 가정**: thin SVD 일반 케이스.  caller 가 rows < cols
//!   이면 transpose (M^H) 후 호출하고 U/V swap.
//! - f32 only.
//!
//! ## Cut 3 상태
//! [`dispatch_jacobi_svd`] — 고정 sweep 수 (`N_SWEEPS = 30`) 의 one-sided
//! Jacobi.  convergence check 없음 (Cut 3b 에서 GPU off-diag norm shader
//! 추가 예정).  큰 cols 에서도 30 sweep 이면 보통 1e-6 정도 수렴.
//! [`wgpu_thin_svd`] (Cut 1 stub) 는 Cut 4 에서 본체 작성.

use bytemuck::{Pod, Zeroable};
use num_complex::Complex;
use wgpu::util::DeviceExt as _;

use crate::wgpu_mps::backend::WgpuMpsBackend;
use crate::GpuError;

/// `Complex<f32>` 의 Pod 래퍼 — wgpu storage buffer 용.
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

fn complex_to_cf32_vec(src: &[Complex<f32>]) -> Vec<CF32> {
    src.iter().copied().map(CF32::from).collect()
}

/// wgpu MPS 백엔드 에러.
#[derive(Debug)]
pub enum WgpuMpsError {
    /// 아직 구현되지 않은 path — Cut 6 까지 CPU fallback 으로 처리.
    NotImplemented,
    /// GPU 인프라 (adapter / device / pipeline) 초기화 실패.
    Gpu(GpuError),
    /// 잘못된 입력 (e.g., rows < cols, dim 0).
    InvalidInput(String),
}

impl std::fmt::Display for WgpuMpsError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            WgpuMpsError::NotImplemented => write!(
                f,
                "wgpu MPS path not yet implemented (v0.6.6 Cut 1 stub) — \
                 caller should fall back to CPU"
            ),
            WgpuMpsError::Gpu(e) => write!(f, "wgpu MPS infra: {e}"),
            WgpuMpsError::InvalidInput(s) => write!(f, "wgpu MPS invalid input: {s}"),
        }
    }
}

impl std::error::Error for WgpuMpsError {}

impl From<GpuError> for WgpuMpsError {
    fn from(e: GpuError) -> Self {
        WgpuMpsError::Gpu(e)
    }
}

/// GPU thin-SVD 결과 (Cut 4 의 wrapper).  shape:
/// - `u_row_major`: `rows × keep`
/// - `s`: `keep`
/// - `vt_row_major`: `keep × cols`
/// - `trunc_error_sq`: `Σ_{j>=keep} s_j²` (f64 누적)
#[derive(Debug, Clone)]
pub struct WgpuSvdResult {
    pub u_row_major: Vec<Complex<f32>>,
    pub s: Vec<f32>,
    pub vt_row_major: Vec<Complex<f32>>,
    pub trunc_error_sq: f64,
    pub keep: usize,
}

/// GPU thin-SVD with truncation (v0.6.6 Cut 4).
///
/// `m_row_major` 는 `rows × cols` complex f32, **row-major**.
/// `M[r, c] = m_row_major[r * cols + c]`.
///
/// 반환:
/// - `u_row_major`: `rows × keep` row-major.  orthonormal columns.
/// - `s`: descending 정렬된 `keep` 개 singular values.
/// - `vt_row_major`: `keep × cols` row-major. (= V^H)
/// - `trunc_error_sq`: `Σ_{j >= keep} s_j²` (f64).
/// - `keep`: 실제 keep 한 rank — `min(true_rank_by_eps, max_keep).max(1)`.
///
/// `max_keep` 또는 `trunc_threshold` 두 cap 중 더 strict 한 쪽 적용.
/// `trunc_threshold == 0` 이면 eps-rank cap 비활성 (max_keep 만).
///
/// `rows < cols` 도 지원 — 내부에서 `M^H` 로 swap 후 SVD 계산, U/V swap.
pub fn wgpu_thin_svd(
    m_row_major: &[Complex<f32>],
    rows: usize,
    cols: usize,
    max_keep: usize,
    trunc_threshold: f32,
) -> Result<WgpuSvdResult, WgpuMpsError> {
    if rows == 0 || cols == 0 {
        return Err(WgpuMpsError::InvalidInput(format!(
            "rows={rows}, cols={cols} 둘 다 ≥ 1 필요"
        )));
    }
    if m_row_major.len() != rows * cols {
        return Err(WgpuMpsError::InvalidInput(format!(
            "m_row_major.len()={} != rows*cols={}",
            m_row_major.len(),
            rows * cols
        )));
    }
    if !(trunc_threshold.is_finite() && trunc_threshold >= 0.0) {
        return Err(WgpuMpsError::InvalidInput(format!(
            "trunc_threshold must be finite and >= 0 (got {trunc_threshold})"
        )));
    }

    // dispatch_jacobi_svd 는 rows ≥ cols 만 받는다.  rows < cols 인 경우
    // M^H (cols × rows) 로 swap 해서 호출, 마지막에 U/V 다시 swap.
    let transpose = rows < cols;
    let (a_rows, a_cols, a_col_major) = if transpose {
        let mut transposed = vec![Complex::new(0.0_f32, 0.0); cols * rows];
        for r in 0..rows {
            for c in 0..cols {
                // M^H[c, r] = conj(M[r, c]).  M^H 의 (c, r) entry 를
                // column-major (cols × rows) layout 으로:
                //   index = r * cols + c   (column r, row c)
                transposed[r * cols + c] = m_row_major[r * cols + c].conj();
            }
        }
        (cols, rows, transposed)
    } else {
        // row-major (rows × cols) → column-major (rows × cols).
        let mut col_major = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        for r in 0..rows {
            for c in 0..cols {
                col_major[c * rows + r] = m_row_major[r * cols + c];
            }
        }
        (rows, cols, col_major)
    };

    let full = dispatch_jacobi_svd(&a_col_major, a_rows, a_cols)?;

    // ---- Sort singular values descending ----
    let mut order: Vec<usize> = (0..a_cols).collect();
    order.sort_by(|&i, &j| {
        full.s[j]
            .partial_cmp(&full.s[i])
            .unwrap_or(std::cmp::Ordering::Equal)
    });
    let s_sorted: Vec<f32> = order.iter().map(|&i| full.s[i]).collect();

    // ---- Determine keep ----
    let eps_rank = if trunc_threshold > 0.0 {
        let mut count = 0;
        for &v in &s_sorted {
            if v >= trunc_threshold {
                count += 1;
            } else {
                break;
            }
        }
        count
    } else {
        a_cols
    };
    let keep = a_cols.min(max_keep).min(eps_rank).max(1);

    // ---- Truncation error ----
    let trunc_error_sq: f64 = (keep..s_sorted.len())
        .map(|j| {
            let s = s_sorted[j] as f64;
            s * s
        })
        .sum();

    // ---- Permute + truncate U, V ----
    // U is rows(=a_rows) × cols(=a_cols) col-major.  Keep first `keep` columns
    // after reordering.
    let mut u_thin_col_major = vec![Complex::new(0.0_f32, 0.0); a_rows * keep];
    for (new_col, &old_col) in order.iter().take(keep).enumerate() {
        for r in 0..a_rows {
            u_thin_col_major[new_col * a_rows + r] = full.u_col_major[old_col * a_rows + r];
        }
    }
    // V is a_cols × a_cols col-major; keep `keep` columns.
    let mut v_thin_col_major = vec![Complex::new(0.0_f32, 0.0); a_cols * keep];
    for (new_col, &old_col) in order.iter().take(keep).enumerate() {
        for r in 0..a_cols {
            v_thin_col_major[new_col * a_cols + r] = full.v_col_major[old_col * a_cols + r];
        }
    }
    let s_thin: Vec<f32> = s_sorted.into_iter().take(keep).collect();

    // ---- Undo transpose if needed ----
    // If transpose=true, we computed SVD of M^H = U' Σ V'^H.
    //   M = (M^H)^H = V' Σ U'^H = V' Σ (U')^H
    //   So for original M: U_orig = V',  V_orig = U'.  Σ unchanged.
    let (final_u_col, final_v_col, u_rows_out, v_rows_out) = if transpose {
        (
            v_thin_col_major, // a_cols × keep = rows × keep ✓
            u_thin_col_major, // a_rows × keep = cols × keep ✓
            a_cols,
            a_rows,
        )
    } else {
        (u_thin_col_major, v_thin_col_major, a_rows, a_cols)
    };

    // ---- Convert to row-major output forms ----
    // U: `rows × keep` row-major (u_rows_out × keep).
    let rows_out = u_rows_out; // == rows
    let cols_out = v_rows_out; // == cols
    debug_assert_eq!(rows_out, rows);
    debug_assert_eq!(cols_out, cols);

    let mut u_row_major = vec![Complex::new(0.0_f32, 0.0); rows_out * keep];
    for col in 0..keep {
        for r in 0..rows_out {
            u_row_major[r * keep + col] = final_u_col[col * rows_out + r];
        }
    }
    // V^H: `keep × cols` row-major.
    //   V is cols × keep col-major.  V^H[b, c] = conj(V[c, b]).
    let mut vt_row_major = vec![Complex::new(0.0_f32, 0.0); keep * cols_out];
    for b in 0..keep {
        for c in 0..cols_out {
            vt_row_major[b * cols_out + c] = final_v_col[b * cols_out + c].conj();
        }
    }

    Ok(WgpuSvdResult {
        u_row_major,
        s: s_thin,
        vt_row_major,
        trunc_error_sq,
        keep,
    })
}

// ============================================================================
// Cut 3: dispatch_jacobi_svd — full SVD via one-sided Jacobi.
// ============================================================================

/// One-sided Jacobi 의 고정 sweep 수.  cols ≤ 256 의 모든 케이스에서 충분히
/// 수렴 (보통 5-10 sweep, complex / ill-conditioned 도 30 이면 안전).
/// Cut 3b 에서 GPU off-diag norm shader 추가로 early termination 도입 예정.
const N_SWEEPS: usize = 30;

/// Cut 3 의 full SVD 결과.  thin form (rows ≥ cols 가정):
/// - `u_col_major`: `rows × cols` (orthonormal columns)
/// - `s`: `cols` (NOT sorted descending — caller 가 정렬)
/// - `v_col_major`: `cols × cols` (unitary)
///
/// 관계: `M = U · diag(S) · V^H`.
#[derive(Debug, Clone)]
pub struct JacobiSvdResult {
    pub u_col_major: Vec<Complex<f32>>,
    pub s: Vec<f32>,
    pub v_col_major: Vec<Complex<f32>>,
}

/// GPU one-sided Jacobi SVD (Cut 3).
///
/// `m_col_major` 는 `rows × cols` complex f32, column-major.  `rows ≥ cols`
/// 필수 — caller 가 rows < cols 이면 `M^H` (전치 conjugate) 로 호출하고
/// U/V 스왑.
pub fn dispatch_jacobi_svd(
    m_col_major: &[Complex<f32>],
    rows: usize,
    cols: usize,
) -> Result<JacobiSvdResult, WgpuMpsError> {
    if rows == 0 || cols == 0 {
        return Err(WgpuMpsError::InvalidInput(format!(
            "rows={rows}, cols={cols} 둘 다 ≥ 1 필요"
        )));
    }
    if rows < cols {
        return Err(WgpuMpsError::InvalidInput(format!(
            "rows ({rows}) < cols ({cols}): caller must transpose first \
             (dispatch_jacobi_svd assumes thin shape)"
        )));
    }
    if m_col_major.len() != rows * cols {
        return Err(WgpuMpsError::InvalidInput(format!(
            "m_col_major.len()={} != rows*cols={}",
            m_col_major.len(),
            rows * cols
        )));
    }

    let backend_arc = crate::cached_wgpu_mps_backend()?;
    let backend: &WgpuMpsBackend = &backend_arc;
    let device = backend.device();
    let queue = backend.queue();

    // ---- Buffers ----
    let m_pod = complex_to_cf32_vec(m_col_major);
    let m_buf = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("svd_jacobi M"),
        contents: bytemuck::cast_slice(&m_pod),
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
    });

    // V = I (cols × cols, column-major).
    let mut v_init: Vec<CF32> = vec![CF32::default(); cols * cols];
    for i in 0..cols {
        v_init[i * cols + i] = CF32 { re: 1.0, im: 0.0 };
    }
    let v_buf = device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
        label: Some("svd_jacobi V"),
        contents: bytemuck::cast_slice(&v_init),
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
    });

    // params (16 bytes uniform).
    let params_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("svd_jacobi params"),
        size: std::mem::size_of::<JacobiParams>() as u64,
        usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });

    // pair_schedule: max length = ceil(cols/2) pairs * 2 u32 = cols u32 = cols * 4 bytes.
    // Ensure non-zero size (wgpu rejects empty storage buffers).
    let max_pair_bytes = ((cols.max(2) + 1) * 2 * std::mem::size_of::<u32>()) as u64;
    let pair_buf = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("svd_jacobi pair_schedule"),
        size: max_pair_bytes,
        usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });

    // ---- Bind group (one, reused across rounds) ----
    let bind_group = device.create_bind_group(&wgpu::BindGroupDescriptor {
        label: Some("svd_jacobi BG"),
        layout: backend.svd_jacobi_bgl(),
        entries: &[
            wgpu::BindGroupEntry {
                binding: 0,
                resource: m_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 1,
                resource: v_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 2,
                resource: params_buf.as_entire_binding(),
            },
            wgpu::BindGroupEntry {
                binding: 3,
                resource: pair_buf.as_entire_binding(),
            },
        ],
    });

    // ---- Sweep loop ----
    let rounds = chess_tournament_pairs(cols);
    let pipeline = backend.svd_jacobi_pipeline();

    // cols == 1 케이스: pair 없음, 회전 안 함.  바로 M, V 다운로드해서 norm 만.
    if cols >= 2 {
        for _ in 0..N_SWEEPS {
            for round in &rounds {
                if round.is_empty() {
                    continue;
                }
                let pair_count = round.len();
                let pairs_flat: Vec<u32> = round
                    .iter()
                    .flat_map(|(i, j)| [*i as u32, *j as u32])
                    .collect();
                queue.write_buffer(&pair_buf, 0, bytemuck::cast_slice(&pairs_flat));
                let params = JacobiParams {
                    rows: rows as u32,
                    cols: cols as u32,
                    pair_count: pair_count as u32,
                    skip_tol: 1.0e-14_f32,
                };
                queue.write_buffer(&params_buf, 0, bytemuck::bytes_of(&params));

                let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
                    label: Some("svd_jacobi encoder"),
                });
                {
                    let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                        label: Some("svd_jacobi pass"),
                        timestamp_writes: None,
                    });
                    pass.set_pipeline(pipeline);
                    pass.set_bind_group(0, &bind_group, &[]);
                    pass.dispatch_workgroups(pair_count as u32, 1, 1);
                }
                queue.submit(std::iter::once(encoder.finish()));
            }
        }
    }

    // ---- Download M, V ----
    let m_final = download_complex_buffer(device, queue, &m_buf, rows * cols)?;
    let _v_gpu_raw = download_complex_buffer(device, queue, &v_buf, cols * cols)?;

    // Extract S (column norms of M_final) and normalize → U.
    let mut s = vec![0.0_f32; cols];
    let mut u = m_final.clone();
    for col in 0..cols {
        let mut norm_sq: f32 = 0.0;
        for r in 0..rows {
            let z = u[col * rows + r];
            norm_sq += z.re * z.re + z.im * z.im;
        }
        let norm = norm_sq.sqrt();
        s[col] = norm;
        if norm > 1e-20 {
            let inv = 1.0 / norm;
            for r in 0..rows {
                u[col * rows + r] *= inv;
            }
        }
        // norm ≈ 0 (rank deficient column) → leave as zeros, S[col] = 0.
    }

    // v0.6.6.1 hotfix: recompute V on host from M_initial^H · U · Σ^{-1}.
    //
    // Why: the GPU-tracked V_accumulated accumulates f32 round-off over
    // N_SWEEPS * pairs rotations, breaking `V^H V = I` for large cols
    // (V^H V ε ~5.8e-5 at cols=256 vs ~3.8e-6 at cols=32).  This caused
    // ~10% fidelity loss in deep TFIM Trotter circuits where ~2000 SVDs
    // accumulate the V error.
    //
    // The fix: U is already exactly orthonormal (because it = normalized
    // columns of M_final), and S is accurate (column norms).  So we can
    // recover the unique V that satisfies M = U · diag(S) · V^H exactly
    // (within f32) by V = M^H · U · diag(S)^{-1}.
    //
    // Cost: O(rows · cols²) host-side, e.g. cols=256 / rows=256 → ~17M
    // complex mul-adds ≈ 30 ms — small fraction of GPU sweep cost.
    let mut v = vec![Complex::new(0.0f32, 0.0); cols * cols];
    for j in 0..cols {
        let s_j = s[j];
        if s_j < 1e-20 {
            // Degenerate singular value: arbitrary unit vector e_j.
            v[j * cols + j] = Complex::new(1.0, 0.0);
            continue;
        }
        let inv_s = 1.0 / s_j;
        for i in 0..cols {
            // V[i, j] = (Σ_r conj(M[r, i]) · U[r, j]) / S[j]
            let mut acc = Complex::new(0.0f32, 0.0);
            for r in 0..rows {
                let m_ri = m_col_major[i * rows + r];
                let u_rj = u[j * rows + r];
                acc += m_ri.conj() * u_rj;
            }
            v[j * cols + i] = acc * Complex::new(inv_s, 0.0);
        }
    }

    Ok(JacobiSvdResult {
        u_col_major: u,
        s,
        v_col_major: v,
    })
}

/// Chess tournament round-robin schedule for `n` players.
///
/// Returns a Vec of rounds; each round is a Vec of disjoint `(i, j)` pairs
/// with `i < j`.  After `n - 1` (or `n` if odd) rounds, every distinct
/// pair (i, j), i < j < n appears exactly once.
fn chess_tournament_pairs(n: usize) -> Vec<Vec<(usize, usize)>> {
    if n < 2 {
        return Vec::new();
    }
    let m = if n.is_multiple_of(2) { n } else { n + 1 };
    let mut perm: Vec<usize> = (0..m).collect();
    let mut rounds = Vec::with_capacity(m - 1);
    for _ in 0..(m - 1) {
        let mut pairs = Vec::with_capacity(m / 2);
        for k in 0..(m / 2) {
            let a = perm[k];
            let b = perm[m - 1 - k];
            if a < n && b < n {
                let (i, j) = if a < b { (a, b) } else { (b, a) };
                pairs.push((i, j));
            }
        }
        rounds.push(pairs);
        // Rotate: keep perm[0] fixed, rotate others left by 1.
        let last = perm.pop().unwrap();
        perm.insert(1, last);
    }
    rounds
}

#[repr(C)]
#[derive(Clone, Copy, Pod, Zeroable)]
struct JacobiParams {
    rows: u32,
    cols: u32,
    pair_count: u32,
    skip_tol: f32,
}

fn download_complex_buffer(
    device: &wgpu::Device,
    queue: &wgpu::Queue,
    buf: &wgpu::Buffer,
    n_elems: usize,
) -> Result<Vec<Complex<f32>>, WgpuMpsError> {
    let size_bytes = (n_elems * std::mem::size_of::<CF32>()) as u64;
    let staging = device.create_buffer(&wgpu::BufferDescriptor {
        label: Some("svd_jacobi staging"),
        size: size_bytes,
        usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
        mapped_at_creation: false,
    });
    let mut encoder = device.create_command_encoder(&wgpu::CommandEncoderDescriptor {
        label: Some("svd_jacobi download"),
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
        .map_err(|e| GpuError::Buffer(format!("device.poll: {e:?}")))?;
    rx.recv()
        .map_err(|e| GpuError::Buffer(format!("map recv: {e}")))?
        .map_err(|e| GpuError::Buffer(format!("map_async: {e:?}")))?;

    let data = slice.get_mapped_range();
    let parsed: &[CF32] = bytemuck::cast_slice(&data);
    let result: Vec<Complex<f32>> = parsed.iter().copied().map(Complex::<f32>::from).collect();
    drop(data);
    staging.unmap();
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn try_backend_available() -> bool {
        crate::cached_wgpu_mps_backend().is_ok()
    }

    #[test]
    fn error_display_mentions_cut1() {
        let err = WgpuMpsError::NotImplemented;
        let msg = format!("{err}");
        assert!(msg.contains("not yet implemented"));
        assert!(msg.contains("Cut 1"));
    }

    #[test]
    fn gpu_error_wraps_into_wgpu_mps_error() {
        let g = GpuError::NoAdapter;
        let w: WgpuMpsError = g.into();
        assert!(matches!(w, WgpuMpsError::Gpu(GpuError::NoAdapter)));
        let msg = format!("{w}");
        assert!(msg.contains("wgpu MPS infra"));
    }

    // -------- Chess tournament pairing --------

    #[test]
    fn chess_pairs_n_4_covers_all() {
        let rounds = chess_tournament_pairs(4);
        // Should be 3 rounds for n=4.
        assert_eq!(rounds.len(), 3);
        let mut all_pairs: Vec<(usize, usize)> = rounds.into_iter().flatten().collect();
        all_pairs.sort();
        // C(4,2) = 6 pairs total.
        assert_eq!(
            all_pairs,
            vec![(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        );
    }

    #[test]
    fn chess_pairs_n_5_odd_works() {
        let rounds = chess_tournament_pairs(5);
        let mut all_pairs: Vec<(usize, usize)> = rounds.into_iter().flatten().collect();
        all_pairs.sort();
        all_pairs.dedup();
        // C(5,2) = 10 distinct pairs.
        assert_eq!(all_pairs.len(), 10);
    }

    #[test]
    fn chess_pairs_disjoint_within_round() {
        for n in 2..=12 {
            let rounds = chess_tournament_pairs(n);
            for (rid, round) in rounds.iter().enumerate() {
                let mut seen = std::collections::HashSet::new();
                for &(i, j) in round {
                    assert!(i < j, "n={n} round {rid}: pair ({i},{j}) not i<j");
                    assert!(seen.insert(i), "n={n} round {rid}: dup index {i}");
                    assert!(seen.insert(j), "n={n} round {rid}: dup index {j}");
                }
            }
        }
    }

    // -------- Cut 3: dispatch_jacobi_svd correctness tests --------

    /// Helper: matmul `A · B^H` where A is rows×k col-major, B is cols×k col-major.
    fn mul_a_bdaggert(
        a: &[Complex<f32>],
        rows: usize,
        k: usize,
        b: &[Complex<f32>],
        cols: usize,
    ) -> Vec<Complex<f32>> {
        // result = A * B^H, shape rows × cols.
        let mut r = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        for col in 0..cols {
            for row in 0..rows {
                let mut s = Complex::new(0.0_f32, 0.0);
                for kk in 0..k {
                    let a_rk = a[kk * rows + row];
                    let b_ck = b[kk * cols + col];
                    s += a_rk * b_ck.conj();
                }
                r[col * rows + row] = s;
            }
        }
        r
    }

    fn frobenius_diff(a: &[Complex<f32>], b: &[Complex<f32>]) -> f32 {
        assert_eq!(a.len(), b.len());
        let mut s = 0.0_f32;
        for k in 0..a.len() {
            let d = a[k] - b[k];
            s += d.re * d.re + d.im * d.im;
        }
        s.sqrt()
    }

    fn frobenius(a: &[Complex<f32>]) -> f32 {
        let mut s = 0.0_f32;
        for z in a {
            s += z.re * z.re + z.im * z.im;
        }
        s.sqrt()
    }

    /// Check that U^H U == I (orthonormal columns of U).
    fn check_u_orthonormal(u: &[Complex<f32>], rows: usize, cols: usize, eps: f32) {
        for c1 in 0..cols {
            for c2 in 0..cols {
                let mut s = Complex::new(0.0_f32, 0.0);
                for r in 0..rows {
                    s += u[c1 * rows + r].conj() * u[c2 * rows + r];
                }
                let target = if c1 == c2 { 1.0 } else { 0.0 };
                let err = (s.re - target).abs() + s.im.abs();
                assert!(
                    err < eps,
                    "U^H U[{c1},{c2}] = {s:?}, expected {target} (eps={eps})"
                );
            }
        }
    }

    /// Generate pseudo-random complex matrix (LCG, deterministic by seed).
    fn random_complex(rows: usize, cols: usize, seed: u64) -> Vec<Complex<f32>> {
        let mut state = seed.wrapping_mul(0x9E3779B97F4A7C15);
        let mut next_f = || -> f32 {
            state = state
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            ((state >> 32) as u32 as f32) / (u32::MAX as f32) * 2.0 - 1.0
        };
        let mut m = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        for entry in m.iter_mut() {
            *entry = Complex::new(next_f(), next_f());
        }
        m
    }

    fn run_jacobi_or_skip(
        rows: usize,
        cols: usize,
        seed: u64,
    ) -> Option<(Vec<Complex<f32>>, JacobiSvdResult)> {
        if !try_backend_available() {
            return None;
        }
        let m = random_complex(rows, cols, seed);
        let result = dispatch_jacobi_svd(&m, rows, cols).expect("dispatch_jacobi_svd succeeded");
        Some((m, result))
    }

    #[test]
    fn dispatch_jacobi_svd_real_2x2_identity() {
        let Some(_) = (if !try_backend_available() {
            None
        } else {
            Some(())
        }) else {
            return;
        };
        // M = I_2.  Singular values = {1, 1}.
        let m = vec![
            Complex::new(1.0_f32, 0.0), // col 0 row 0
            Complex::new(0.0, 0.0),     // col 0 row 1
            Complex::new(0.0, 0.0),     // col 1 row 0
            Complex::new(1.0, 0.0),     // col 1 row 1
        ];
        let r = dispatch_jacobi_svd(&m, 2, 2).unwrap();
        let mut s = r.s.clone();
        s.sort_by(|a, b| b.partial_cmp(a).unwrap());
        assert!((s[0] - 1.0).abs() < 1e-5);
        assert!((s[1] - 1.0).abs() < 1e-5);
    }

    #[test]
    fn dispatch_jacobi_svd_diagonal_real() {
        if !try_backend_available() {
            return;
        }
        // M = diag(3, 2, 1).  SVs = {3, 2, 1}.
        let rows = 3;
        let cols = 3;
        let mut m = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        m[0] = Complex::new(3.0, 0.0);
        m[rows + 1] = Complex::new(2.0, 0.0);
        m[2 * rows + 2] = Complex::new(1.0, 0.0);
        let r = dispatch_jacobi_svd(&m, rows, cols).unwrap();
        let mut s = r.s.clone();
        s.sort_by(|a, b| b.partial_cmp(a).unwrap());
        assert!((s[0] - 3.0).abs() < 1e-5);
        assert!((s[1] - 2.0).abs() < 1e-5);
        assert!((s[2] - 1.0).abs() < 1e-5);
    }

    /// v0.6.6.1 hotfix regression guard.  Without host-side V recomputation
    /// (V = M^H · U · Σ^{-1}), large-cols SVD had `V^H V ε ≈ 5.8e-5` and
    /// `reconstruct ε ≈ 4.7e-5` at 256×256 — accumulating to ~10% fidelity
    /// loss in deep Trotter circuits (DGX Spark RC verification report
    /// 2026-05-26).  Post-fix: reconstruct ε ≈ 7.8e-7 (f32 machine epsilon).
    #[test]
    fn dispatch_jacobi_svd_reconstruct_large_v066_1_hotfix() {
        if !try_backend_available() {
            return;
        }
        // 128×128 random — the size where pre-hotfix ε ≈ 2e-5 was observed.
        let rows = 128;
        let cols = 128;
        let seed = 4242;
        let m = random_complex(rows, cols, seed);
        let r = dispatch_jacobi_svd(&m, rows, cols).unwrap();
        // Reconstruct U·diag(S)·V^H (col-major).
        let mut us = r.u_col_major.clone();
        for col in 0..cols {
            for row in 0..rows {
                us[col * rows + row].re *= r.s[col];
                us[col * rows + row].im *= r.s[col];
            }
        }
        let m_recon = mul_a_bdaggert(&us, rows, cols, &r.v_col_major, cols);
        let diff = frobenius_diff(&m, &m_recon);
        let norm = frobenius(&m);
        let rel = diff / norm.max(1e-30);
        // Hotfix gives ~1e-6.  Pre-hotfix would fail at ~2e-5.
        assert!(
            rel < 5e-6,
            "v0.6.6.1 regression: 128×128 reconstruct rel ε = {rel} (pre-hotfix ~2e-5)"
        );
    }

    #[test]
    fn dispatch_jacobi_svd_reconstruct_random() {
        for (rows, cols, seed) in [
            (4, 2, 11),
            (4, 4, 22),
            (8, 4, 33),
            (16, 8, 44),
            (32, 16, 55),
        ] {
            let Some((m, r)) = run_jacobi_or_skip(rows, cols, seed) else {
                return;
            };
            // Reconstruct: M' = U · diag(S) · V^H.
            //   U is rows × cols col-major.
            //   diag(S) · V^H : multiply each row of V^H by S[i].
            //   V is cols × cols col-major.  V^H[i, j] = conj(V[j, i]) = conj(V[i * cols + j]).
            //
            // Equivalent: let UΣ = U scaled column-wise by S, shape rows × cols col-major.
            //   M' = (UΣ) · V^H.
            let mut u_sigma = r.u_col_major.clone();
            for col in 0..cols {
                for row in 0..rows {
                    u_sigma[col * rows + row].re *= r.s[col];
                    u_sigma[col * rows + row].im *= r.s[col];
                }
            }
            // M' = (UΣ) · V^H. Use mul_a_bdaggert: result[row, col_out] = Σ_k UΣ[row, k] * conj(V[col_out, k]).
            let m_recon = mul_a_bdaggert(&u_sigma, rows, cols, &r.v_col_major, cols);
            let diff = frobenius_diff(&m, &m_recon);
            let norm = frobenius(&m);
            let rel = diff / norm.max(1e-30);
            assert!(
                rel < 5e-5,
                "rows={rows} cols={cols} seed={seed}: reconstruct ε_rel = {rel} (norm={norm})"
            );

            // Orthonormality of U columns.
            check_u_orthonormal(&r.u_col_major, rows, cols, 1e-4);
            // V is unitary — V^H V should be I.
            check_u_orthonormal(&r.v_col_major, cols, cols, 1e-4);

            // Singular values non-negative.
            for s_val in &r.s {
                assert!(*s_val >= 0.0, "negative singular value: {s_val}");
            }
        }
    }

    #[test]
    fn dispatch_jacobi_svd_rejects_invalid_shape() {
        if !try_backend_available() {
            return;
        }
        // rows < cols rejected.
        let m = vec![Complex::new(0.0_f32, 0.0); 2 * 3];
        assert!(matches!(
            dispatch_jacobi_svd(&m, 2, 3).unwrap_err(),
            WgpuMpsError::InvalidInput(_)
        ));
        // zero dim rejected.
        let m2: Vec<Complex<f32>> = Vec::new();
        assert!(matches!(
            dispatch_jacobi_svd(&m2, 0, 4).unwrap_err(),
            WgpuMpsError::InvalidInput(_)
        ));
    }

    // -------- Cut 4: wgpu_thin_svd (row-major + truncation wrapper) --------

    /// Convert column-major SVD result to row-major for cross-comparison.
    /// Reconstruct M from `wgpu_thin_svd` output and compare with input.
    fn reconstruct_row_major(
        u_row_major: &[Complex<f32>],
        s: &[f32],
        vt_row_major: &[Complex<f32>],
        rows: usize,
        keep: usize,
        cols: usize,
    ) -> Vec<Complex<f32>> {
        // M' = U · diag(S) · V^H, where U: rows×keep, S: keep, V^H: keep×cols.
        let mut out = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        for r in 0..rows {
            for c in 0..cols {
                let mut sum = Complex::new(0.0_f32, 0.0);
                for b in 0..keep {
                    let u_rb = u_row_major[r * keep + b];
                    let vt_bc = vt_row_major[b * cols + c];
                    sum += u_rb * Complex::new(s[b], 0.0) * vt_bc;
                }
                out[r * cols + c] = sum;
            }
        }
        out
    }

    fn frobenius_row_major(a: &[Complex<f32>], b: &[Complex<f32>]) -> f32 {
        assert_eq!(a.len(), b.len());
        let mut s = 0.0_f32;
        for k in 0..a.len() {
            let d = a[k] - b[k];
            s += d.re * d.re + d.im * d.im;
        }
        s.sqrt()
    }

    fn frobenius_row_major_single(a: &[Complex<f32>]) -> f32 {
        let mut s = 0.0_f32;
        for z in a {
            s += z.re * z.re + z.im * z.im;
        }
        s.sqrt()
    }

    /// Generate row-major random complex matrix.
    fn random_complex_row_major(rows: usize, cols: usize, seed: u64) -> Vec<Complex<f32>> {
        // Same generator as random_complex but row-major (just relabel).
        let mut state = seed.wrapping_mul(0x9E3779B97F4A7C15);
        let mut next_f = || -> f32 {
            state = state
                .wrapping_mul(6364136223846793005)
                .wrapping_add(1442695040888963407);
            ((state >> 32) as u32 as f32) / (u32::MAX as f32) * 2.0 - 1.0
        };
        let mut m = vec![Complex::new(0.0_f32, 0.0); rows * cols];
        for entry in m.iter_mut() {
            *entry = Complex::new(next_f(), next_f());
        }
        m
    }

    #[test]
    fn wgpu_thin_svd_reconstruct_random_no_truncation() {
        if !try_backend_available() {
            return;
        }
        for (rows, cols, seed) in [
            (4, 2, 71),
            (4, 4, 72),
            (8, 4, 73),
            (16, 8, 74),
            (32, 16, 75),
        ] {
            let m = random_complex_row_major(rows, cols, seed);
            // max_keep huge, trunc_threshold 0 → full SVD, keep == min(rows, cols).
            let r = wgpu_thin_svd(&m, rows, cols, 1024, 0.0).unwrap();
            assert_eq!(r.keep, rows.min(cols));
            assert!(r.trunc_error_sq.abs() < 1e-8);
            // Descending sort.
            for i in 1..r.s.len() {
                assert!(
                    r.s[i - 1] >= r.s[i] - 1e-5,
                    "S not descending at {i}: {:?}",
                    r.s
                );
            }
            // Reconstruct.
            let m_recon =
                reconstruct_row_major(&r.u_row_major, &r.s, &r.vt_row_major, rows, r.keep, cols);
            let diff = frobenius_row_major(&m, &m_recon);
            let norm = frobenius_row_major_single(&m);
            let rel = diff / norm.max(1e-30);
            assert!(
                rel < 5e-5,
                "rows={rows} cols={cols} seed={seed}: rel ε = {rel}"
            );
        }
    }

    #[test]
    fn wgpu_thin_svd_transpose_rows_lt_cols() {
        if !try_backend_available() {
            return;
        }
        // rows < cols path — internally transposes.
        for (rows, cols, seed) in [(2, 4, 81), (3, 8, 82), (4, 16, 83), (8, 32, 84)] {
            let m = random_complex_row_major(rows, cols, seed);
            let r = wgpu_thin_svd(&m, rows, cols, 1024, 0.0).unwrap();
            assert_eq!(r.keep, rows.min(cols));
            let m_recon =
                reconstruct_row_major(&r.u_row_major, &r.s, &r.vt_row_major, rows, r.keep, cols);
            let diff = frobenius_row_major(&m, &m_recon);
            let norm = frobenius_row_major_single(&m);
            let rel = diff / norm.max(1e-30);
            assert!(
                rel < 5e-5,
                "transpose path rows={rows} cols={cols} seed={seed}: rel ε = {rel}"
            );
        }
    }

    #[test]
    fn wgpu_thin_svd_truncate_max_keep_only() {
        if !try_backend_available() {
            return;
        }
        // Random 16×8, max_keep=4 → keep=4, trunc_error_sq = Σ s_j² for j>=4.
        let m = random_complex_row_major(16, 8, 91);
        let r_full = wgpu_thin_svd(&m, 16, 8, 1024, 0.0).unwrap();
        let r_cut = wgpu_thin_svd(&m, 16, 8, 4, 0.0).unwrap();
        assert_eq!(r_cut.keep, 4);
        // The 4 kept SVs match the top 4 from full.
        for i in 0..4 {
            assert!(
                (r_cut.s[i] - r_full.s[i]).abs() < 1e-5,
                "top-{i} mismatch: cut={} full={}",
                r_cut.s[i],
                r_full.s[i]
            );
        }
        // trunc_error_sq matches sum of dropped squares from full.
        let dropped_sq_expected: f64 = (4..r_full.s.len())
            .map(|j| {
                let s = r_full.s[j] as f64;
                s * s
            })
            .sum();
        assert!(
            (r_cut.trunc_error_sq - dropped_sq_expected).abs() < 1e-4,
            "trunc_error_sq={} vs expected={}",
            r_cut.trunc_error_sq,
            dropped_sq_expected
        );
    }

    #[test]
    fn wgpu_thin_svd_truncate_eps_rank() {
        if !try_backend_available() {
            return;
        }
        // Rank-deficient M: outer product u*v^T gives rank 1.
        // Build M = a * b^T where a is 4×1 (random), b is 2×1.
        let mut m = vec![Complex::new(0.0_f32, 0.0); 4 * 2];
        let a = [
            Complex::new(1.0_f32, 0.0),
            Complex::new(2.0, 0.0),
            Complex::new(0.5, 0.0),
            Complex::new(-1.0, 0.0),
        ];
        let b = [Complex::new(1.0_f32, 0.0), Complex::new(3.0, 0.0)];
        for r in 0..4 {
            for c in 0..2 {
                m[r * 2 + c] = a[r] * b[c];
            }
        }
        // Full rank up to 2 but actual rank 1.  eps_rank=1 by tight cutoff.
        let r = wgpu_thin_svd(&m, 4, 2, 1024, 0.1).unwrap();
        assert_eq!(r.keep, 1, "rank-1 outer product should give keep=1");
        // Reconstruct should still be very close (the dropped SV ~0).
        let m_recon = reconstruct_row_major(&r.u_row_major, &r.s, &r.vt_row_major, 4, r.keep, 2);
        let diff = frobenius_row_major(&m, &m_recon);
        let norm = frobenius_row_major_single(&m);
        assert!(
            diff / norm.max(1e-30) < 5e-5,
            "rank-1 reconstruct rel ε = {}",
            diff / norm.max(1e-30)
        );
        assert!(
            r.trunc_error_sq < 1e-6,
            "rank-1 trunc_error_sq should be ~0, got {}",
            r.trunc_error_sq
        );
    }

    #[test]
    fn wgpu_thin_svd_keep_at_least_one() {
        if !try_backend_available() {
            return;
        }
        // Even max_keep=0 should clamp to keep=1 (avoid zero-rank bond).
        let m = random_complex_row_major(4, 4, 101);
        let r = wgpu_thin_svd(&m, 4, 4, 0, 0.0).unwrap();
        assert_eq!(r.keep, 1, "max_keep=0 must clamp to keep=1");
        // Even with absurdly large trunc_threshold (drops everything), keep=1.
        let r2 = wgpu_thin_svd(&m, 4, 4, 1024, 1e10).unwrap();
        assert_eq!(r2.keep, 1, "eps_rank=0 must clamp to keep=1");
    }

    #[test]
    fn wgpu_thin_svd_rejects_invalid_args() {
        if !try_backend_available() {
            return;
        }
        let m = vec![Complex::new(0.0_f32, 0.0); 8];
        assert!(matches!(
            wgpu_thin_svd(&m, 0, 4, 4, 0.0).unwrap_err(),
            WgpuMpsError::InvalidInput(_)
        ));
        // NaN trunc_threshold rejected.
        assert!(matches!(
            wgpu_thin_svd(&m, 4, 2, 4, f32::NAN).unwrap_err(),
            WgpuMpsError::InvalidInput(_)
        ));
        // Negative trunc_threshold rejected.
        assert!(matches!(
            wgpu_thin_svd(&m, 4, 2, 4, -1.0).unwrap_err(),
            WgpuMpsError::InvalidInput(_)
        ));
    }

    #[test]
    fn dispatch_jacobi_svd_singleton_col() {
        // cols = 1: no pairs, no rotation; just column norm.
        if !try_backend_available() {
            return;
        }
        let m = vec![Complex::new(3.0_f32, 0.0), Complex::new(0.0, 4.0)];
        let r = dispatch_jacobi_svd(&m, 2, 1).unwrap();
        // ||m||² = 9 + 16 = 25, σ = 5.
        assert!((r.s[0] - 5.0).abs() < 1e-5);
        // V is 1x1 identity.
        assert!((r.v_col_major[0].re - 1.0).abs() < 1e-6);
        assert!(r.v_col_major[0].im.abs() < 1e-6);
    }
}
