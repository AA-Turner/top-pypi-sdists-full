//! Dense complex tensor with labeled indices + pairwise contraction.
//!
//! Tensor network contraction 의 기본 단위.  각 인덱스는 전역 고유 라벨
//! (`usize`) 을 가지며, 두 텐서의 contraction 은 공유 인덱스를 합(sum)으로
//! 소거한다.  contraction 은 permute(transpose) → reshape → matmul (tensordot)
//! 로 구현한다 — GPU 커널 (batched matmul) 로 자연스럽게 확장된다.

use num_complex::Complex64;
use rayon::prelude::*;

/// 라벨드 인덱스를 가진 dense 복소 텐서.
///
/// `data` 는 row-major (마지막 인덱스가 가장 빠르게 변함) 로 저장된다 —
/// 다중 인덱스 `(i_0, …, i_{r-1})` 의 flat 위치는 `Σ_k i_k · stride_k`,
/// `stride_{r-1} = 1`, `stride_k = stride_{k+1} · dims_{k+1}`.
#[derive(Debug, Clone)]
pub struct Tensor {
    /// 각 축의 전역 인덱스 라벨.
    pub indices: Vec<usize>,
    /// 각 축의 차원 (큐비트는 2).
    pub dims: Vec<usize>,
    /// row-major 복소 원소.
    pub data: Vec<Complex64>,
}

impl Tensor {
    /// 스칼라 (rank-0) 텐서.
    pub fn scalar(v: Complex64) -> Self {
        Tensor {
            indices: vec![],
            dims: vec![],
            data: vec![v],
        }
    }

    /// 인덱스/차원/데이터로 텐서를 만든다.  `data.len()` 은 `prod(dims)` 여야 한다.
    pub fn new(indices: Vec<usize>, dims: Vec<usize>, data: Vec<Complex64>) -> Self {
        debug_assert_eq!(indices.len(), dims.len());
        debug_assert_eq!(data.len(), dims.iter().product::<usize>().max(1));
        Tensor {
            indices,
            dims,
            data,
        }
    }

    /// 원소 개수 (`prod(dims)`).
    pub fn size(&self) -> usize {
        self.data.len()
    }

    pub fn rank(&self) -> usize {
        self.indices.len()
    }

    /// row-major stride 벡터.
    fn strides(dims: &[usize]) -> Vec<usize> {
        let n = dims.len();
        let mut s = vec![1usize; n];
        for k in (0..n.saturating_sub(1)).rev() {
            s[k] = s[k + 1] * dims[k + 1];
        }
        s
    }

    /// 축 순서를 `perm` (새 위치 → 기존 축 인덱스) 으로 재배열한 텐서를 반환.
    ///
    /// `perm[j] = i` 면 결과의 축 `j` 가 기존 축 `i` 다.
    pub fn permute(&self, perm: &[usize]) -> Tensor {
        let r = self.rank();
        debug_assert_eq!(perm.len(), r);
        if perm.iter().enumerate().all(|(j, &i)| j == i) {
            return self.clone();
        }
        let old_strides = Self::strides(&self.dims);
        let new_dims: Vec<usize> = perm.iter().map(|&i| self.dims[i]).collect();
        let new_indices: Vec<usize> = perm.iter().map(|&i| self.indices[i]).collect();
        let new_strides = Self::strides(&new_dims);
        let total = self.data.len();
        // 각 새 flat 위치 → 새 multi-index → 기존 flat 위치.
        let permuted: Vec<Complex64> = (0..total)
            .into_par_iter()
            .map(|new_flat| {
                let mut rem = new_flat;
                let mut old_flat = 0usize;
                for j in 0..r {
                    let coord = rem / new_strides[j];
                    rem %= new_strides[j];
                    old_flat += coord * old_strides[perm[j]];
                }
                self.data[old_flat]
            })
            .collect();
        Tensor {
            indices: new_indices,
            dims: new_dims,
            data: permuted,
        }
    }
}

/// matmul `C[m×n] = A[m×k]·B[k×n]` (row-major, complex) 제공자.  CPU 기본 구현
/// 외에 GPU (wgpu) 구현을 주입해 contraction 의 dominant FLOPs 를 offload 한다.
pub trait MatmulProvider: Sync {
    fn matmul(
        &self,
        m: usize,
        k: usize,
        n: usize,
        a: &[Complex64],
        b: &[Complex64],
    ) -> Vec<Complex64>;
}

/// CPU rayon matmul (기본).  복소 matmul 을 **SoA + Karatsuba 3-real-matmul**
/// 로 계산 — AoS `Complex` 곱은 LLVM auto-vectorization 이 약하므로 (이 프로젝트
/// v0.2.2 SIMD postmortem 참조) re/im 분리 실수 matmul 3 회 (`t1=Ar·Br`,
/// `t2=Ai·Bi`, `t3=(Ar+Ai)(Br+Bi)`; `Cr=t1−t2`, `Ci=t3−t1−t2`) 로 처리해 잘
/// 벡터화되는 실수 GEMM 3 개로 환원한다.
pub struct CpuMatmul;

/// 실수 matmul `C[m×n] = A[m×k]·B[k×n]` (row-major, rayon ikj, 벡터화 친화).
fn real_matmul(m: usize, k: usize, n: usize, a: &[f64], b: &[f64]) -> Vec<f64> {
    (0..m)
        .into_par_iter()
        .flat_map(|i| {
            let a_row = &a[i * k..(i + 1) * k];
            let mut row = vec![0.0f64; n];
            for kk in 0..k {
                let a_ik = a_row[kk];
                if a_ik == 0.0 {
                    continue;
                }
                let b_row = &b[kk * n..(kk + 1) * n];
                for j in 0..n {
                    row[j] += a_ik * b_row[j];
                }
            }
            row
        })
        .collect()
}

impl MatmulProvider for CpuMatmul {
    fn matmul(
        &self,
        m: usize,
        k: usize,
        n: usize,
        a: &[Complex64],
        b: &[Complex64],
    ) -> Vec<Complex64> {
        // 작은 곱은 분리 오버헤드가 커 AoS 직접 계산.
        if (m * n).max(k) < 64 {
            return (0..m)
                .into_par_iter()
                .flat_map(|i| {
                    let a_row = &a[i * k..(i + 1) * k];
                    let mut row = vec![Complex64::new(0.0, 0.0); n];
                    for kk in 0..k {
                        let a_ik = a_row[kk];
                        if a_ik == Complex64::new(0.0, 0.0) {
                            continue;
                        }
                        let b_row = &b[kk * n..(kk + 1) * n];
                        for j in 0..n {
                            row[j] += a_ik * b_row[j];
                        }
                    }
                    row
                })
                .collect();
        }
        // SoA 분리.
        let ar: Vec<f64> = a.iter().map(|c| c.re).collect();
        let ai: Vec<f64> = a.iter().map(|c| c.im).collect();
        let br: Vec<f64> = b.iter().map(|c| c.re).collect();
        let bi: Vec<f64> = b.iter().map(|c| c.im).collect();
        // Karatsuba: 3 real GEMM.
        let asum: Vec<f64> = ar.iter().zip(&ai).map(|(x, y)| x + y).collect();
        let bsum: Vec<f64> = br.iter().zip(&bi).map(|(x, y)| x + y).collect();
        let (t1, (t2, t3)) = rayon::join(
            || real_matmul(m, k, n, &ar, &br),
            || {
                rayon::join(
                    || real_matmul(m, k, n, &ai, &bi),
                    || real_matmul(m, k, n, &asum, &bsum),
                )
            },
        );
        (0..m * n)
            .map(|idx| {
                let re = t1[idx] - t2[idx];
                let im = t3[idx] - t1[idx] - t2[idx];
                Complex64::new(re, im)
            })
            .collect()
    }
}

/// 두 텐서를 contraction 한다 (공유 인덱스 합 소거) — CPU matmul.
pub fn contract_pair(a: &Tensor, b: &Tensor) -> Tensor {
    contract_pair_with(a, b, &CpuMatmul)
}

/// 두 텐서를 contraction 한다 (공유 인덱스 합 소거), `provider` 의 matmul 사용.
///
/// 결과 인덱스 = `a` 고유 인덱스 ++ `b` 고유 인덱스.  공유 인덱스는 소거된다.
/// permute → reshape (M×K, K×N) → matmul.
pub fn contract_pair_with<M: MatmulProvider>(a: &Tensor, b: &Tensor, provider: &M) -> Tensor {
    // 공유 인덱스 (a, b 둘 다) 와 각 고유 인덱스 파악.
    let shared: Vec<usize> = a
        .indices
        .iter()
        .copied()
        .filter(|i| b.indices.contains(i))
        .collect();

    // 공유 인덱스가 없으면 외적 (outer product).
    let a_free_pos: Vec<usize> = (0..a.rank())
        .filter(|&p| !shared.contains(&a.indices[p]))
        .collect();
    let b_free_pos: Vec<usize> = (0..b.rank())
        .filter(|&p| !shared.contains(&b.indices[p]))
        .collect();

    // a 를 [a_free, shared] 순서로 permute.
    let a_shared_pos: Vec<usize> = shared
        .iter()
        .map(|s| a.indices.iter().position(|x| x == s).unwrap())
        .collect();
    let mut a_perm = a_free_pos.clone();
    a_perm.extend_from_slice(&a_shared_pos);
    let a_p = a.permute(&a_perm);

    // b 를 [shared, b_free] 순서로 permute.
    let b_shared_pos: Vec<usize> = shared
        .iter()
        .map(|s| b.indices.iter().position(|x| x == s).unwrap())
        .collect();
    let mut b_perm = b_shared_pos.clone();
    b_perm.extend_from_slice(&b_free_pos);
    let b_p = b.permute(&b_perm);

    let m: usize = a_free_pos
        .iter()
        .map(|&p| a.dims[p])
        .product::<usize>()
        .max(1);
    let k: usize = shared
        .iter()
        .map(|s| {
            let p = a.indices.iter().position(|x| x == s).unwrap();
            a.dims[p]
        })
        .product::<usize>()
        .max(1);
    let n: usize = b_free_pos
        .iter()
        .map(|&p| b.dims[p])
        .product::<usize>()
        .max(1);

    // C = A(m×k) · B(k×n), row-major.
    let c_data = provider.matmul(m, k, n, &a_p.data, &b_p.data);

    let mut out_indices: Vec<usize> = a_free_pos.iter().map(|&p| a.indices[p]).collect();
    out_indices.extend(b_free_pos.iter().map(|&p| b.indices[p]));
    let mut out_dims: Vec<usize> = a_free_pos.iter().map(|&p| a.dims[p]).collect();
    out_dims.extend(b_free_pos.iter().map(|&p| b.dims[p]));

    Tensor {
        indices: out_indices,
        dims: out_dims,
        data: c_data,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn c(re: f64, im: f64) -> Complex64 {
        Complex64::new(re, im)
    }

    #[test]
    fn permute_2x2_transpose() {
        // T[i,j] = 2*i + j  (i,j ∈ {0,1}); indices [0,1].
        let t = Tensor::new(
            vec![0, 1],
            vec![2, 2],
            vec![c(0., 0.), c(1., 0.), c(2., 0.), c(3., 0.)],
        );
        let tp = t.permute(&[1, 0]); // swap axes
        assert_eq!(tp.indices, vec![1, 0]);
        // tp[j,i] = t[i,j] → flat order (j,i): (0,0)=0,(0,1)=2,(1,0)=1,(1,1)=3
        assert_eq!(tp.data, vec![c(0., 0.), c(2., 0.), c(1., 0.), c(3., 0.)]);
    }

    #[test]
    fn contract_matrix_vector() {
        // A[i,k] (2x2) · v[k] → result[i].  shared index = 1 (k).
        let a = Tensor::new(
            vec![0, 1],
            vec![2, 2],
            vec![c(1., 0.), c(2., 0.), c(3., 0.), c(4., 0.)],
        );
        let v = Tensor::new(vec![1], vec![2], vec![c(1., 0.), c(1., 0.)]);
        let r = contract_pair(&a, &v);
        assert_eq!(r.indices, vec![0]);
        // [1+2, 3+4] = [3, 7]
        assert_eq!(r.data, vec![c(3., 0.), c(7., 0.)]);
    }

    #[test]
    fn contract_full_to_scalar() {
        // <v|v> with v = [1, i].  shared all → scalar.
        let v1 = Tensor::new(vec![0], vec![2], vec![c(1., 0.), c(0., 1.)]);
        let v2 = Tensor::new(vec![0], vec![2], vec![c(1., 0.), c(0., 1.)]);
        let r = contract_pair(&v1, &v2);
        assert_eq!(r.rank(), 0);
        // 1*1 + i*i = 1 - 1 = 0
        assert_eq!(r.data[0], c(0., 0.));
    }

    #[test]
    fn contract_outer_product() {
        // no shared indices → outer product.
        let a = Tensor::new(vec![0], vec![2], vec![c(1., 0.), c(2., 0.)]);
        let b = Tensor::new(vec![1], vec![2], vec![c(3., 0.), c(4., 0.)]);
        let r = contract_pair(&a, &b);
        assert_eq!(r.indices, vec![0, 1]);
        assert_eq!(r.data, vec![c(3., 0.), c(4., 0.), c(6., 0.), c(8., 0.)]);
    }
}

#[cfg(test)]
mod bench_tests {
    use super::*;
    use num_complex::Complex64 as C;
    use std::time::Instant;

    fn naive(m: usize, k: usize, n: usize, a: &[C], b: &[C]) -> Vec<C> {
        let mut c = vec![C::new(0.0, 0.0); m * n];
        for i in 0..m {
            for kk in 0..k {
                let av = a[i * k + kk];
                for j in 0..n {
                    c[i * n + j] += av * b[kk * n + j];
                }
            }
        }
        c
    }

    #[test]
    #[ignore] // timing only: cargo test -p qsim-tensornet -- --ignored --nocapture
    fn matmul_speedup() {
        let (m, k, n) = (300, 300, 300);
        let mut s = 1u64;
        let mut f = || {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            C::new(
                (s >> 33) as f64 / u32::MAX as f64 - 0.5,
                (s >> 11 & 0xffff) as f64 / 65535.0 - 0.5,
            )
        };
        let a: Vec<C> = (0..m * k).map(|_| f()).collect();
        let b: Vec<C> = (0..k * n).map(|_| f()).collect();
        let t = Instant::now();
        let r1 = CpuMatmul.matmul(m, k, n, &a, &b);
        let karatsuba = t.elapsed();
        let t = Instant::now();
        let r2 = naive(m, k, n, &a, &b);
        let naive_t = t.elapsed();
        let maxerr = r1
            .iter()
            .zip(&r2)
            .map(|(x, y)| (x - y).norm())
            .fold(0.0, f64::max);
        eprintln!(
            "matmul {m}x{k}x{n}: Karatsuba(SoA,rayon)={karatsuba:?} naive(serial)={naive_t:?} maxerr={maxerr:.2e}"
        );
        assert!(maxerr < 1e-9);
    }
}
