//! Quadratic-Form-Expansion (QFE) stabilizer 표현 — O(n²~n³) amplitude/gate.
//!
//! 상태:  `|ψ⟩ = ω · 2^{-k/2} Σ_{u∈F2^k} i^{φ(u)} |B u ⊕ b⟩`.
//! `B`: n×k (full column rank), `b∈F2ⁿ`, `φ`: ℤ₄ 2차형식, `ω` 전역위상, k≤n.
//!
//! C-type/Pauli 게이트는 (B,b,φ) 직접 갱신.  H 는 변수 추가 + kernel reduction
//! (자유변수 sum-out, Gauss 소거).  `PhaseStab` (Gauss-sum O(n³)/gate) 의 대안.
//! dense 레퍼런스로 전 게이트 검증.

#![allow(clippy::needless_range_loop)]

use num_complex::Complex64;
use std::f64::consts::FRAC_PI_2;

/// ℤ₄ 2차형식 `φ(u) = c0 + Σ lin_i u_i + 2 Σ_{i<j} quad_{ij} u_i u_j (mod 4)`.
#[derive(Clone)]
struct Z4Form {
    c0: u8,
    lin: Vec<u8>,
    quad: Vec<Vec<u8>>,
}

impl Z4Form {
    fn zero(k: usize) -> Self {
        Z4Form {
            c0: 0,
            lin: vec![0; k],
            quad: vec![vec![0; k]; k],
        }
    }
    fn k(&self) -> usize {
        self.lin.len()
    }
    fn eval(&self, u: &[bool]) -> u8 {
        let mut acc = self.c0 as u32;
        let k = self.k();
        for i in 0..k {
            if u[i] {
                acc += self.lin[i] as u32;
                for j in (i + 1)..k {
                    if u[j] && self.quad[i][j] == 1 {
                        acc += 2;
                    }
                }
            }
        }
        (acc % 4) as u8
    }
    /// φ += mult·(⊕_i a_i u_i)  (패리티; ℤ₄ XOR = Σ − 2Σpairs).
    fn add_parity(&mut self, a: &[bool], mult: u8) {
        let k = self.k();
        for i in 0..k {
            if a[i] {
                self.lin[i] = (self.lin[i] + mult) & 3;
            }
        }
        if mult & 1 == 1 {
            for i in 0..k {
                if a[i] {
                    for j in (i + 1)..k {
                        if a[j] {
                            self.quad[i][j] ^= 1;
                            self.quad[j][i] ^= 1;
                        }
                    }
                }
            }
        }
    }
    /// φ += 2·(a·u)(b·u).
    fn add_quad_outer(&mut self, a: &[bool], b: &[bool]) {
        let k = self.k();
        for i in 0..k {
            if a[i] && b[i] {
                self.lin[i] = (self.lin[i] + 2) & 3;
            }
        }
        for i in 0..k {
            for j in (i + 1)..k {
                let cross = ((a[i] && b[j]) as u8 + (a[j] && b[i]) as u8) & 1;
                if cross == 1 {
                    self.quad[i][j] ^= 1;
                    self.quad[j][i] ^= 1;
                }
            }
        }
    }
    fn push_var(&mut self) {
        let k = self.k();
        self.lin.push(0);
        for row in self.quad.iter_mut() {
            row.push(0);
        }
        self.quad.push(vec![0; k + 1]);
    }
    /// 선형 변수치환 v = A u 로 φ 재구성 (A: 각 행 amask[i] = v_i 의 입력 마스크).
    fn relabel(&self, amask: &[Vec<bool>]) -> Z4Form {
        let k = self.k();
        let mut new = Z4Form::zero(k);
        new.c0 = self.c0;
        for i in 0..k {
            if self.lin[i] != 0 {
                new.add_parity(&amask[i], self.lin[i]);
            }
        }
        for i in 0..k {
            for j in (i + 1)..k {
                if self.quad[i][j] == 1 {
                    new.add_quad_outer(&amask[i], &amask[j]);
                }
            }
        }
        new
    }
    fn drop_var(&mut self, c: usize) {
        self.lin.remove(c);
        self.quad.remove(c);
        for row in self.quad.iter_mut() {
            row.remove(c);
        }
    }
    /// 변수 p 를 `1 ⊕ u_p` 로 (NOT): lin_p·u_p, 2 quad·u_p u_j 의 u_p→1-u_p.
    fn flip_var(&mut self, p: usize) {
        let k = self.k();
        let lp = self.lin[p];
        self.c0 = (self.c0 + lp) & 3; // + lin_p·1
        self.lin[p] = (4 - lp) & 3; // -lin_p·u_p
        for j in 0..k {
            if j != p && self.quad[p][j] == 1 {
                // 2 u_p u_j → 2(1-u_p)u_j = 2u_j - 2u_p u_j.  quad bit (×2) 불변, +2u_j.
                self.lin[j] = (self.lin[j] + 2) & 3;
            }
        }
    }
}

/// QFE stabilizer 상태.
#[derive(Clone)]
pub struct ChForm {
    n: usize,
    k: usize,
    bmat: Vec<Vec<bool>>, // n×k
    b: Vec<bool>,
    phi: Z4Form,
    omega: Complex64,
}

impl ChForm {
    pub fn new(n: usize) -> Self {
        ChForm {
            n,
            k: 0,
            bmat: vec![vec![]; n],
            b: vec![false; n],
            phi: Z4Form::zero(0),
            omega: Complex64::new(1.0, 0.0),
        }
    }

    fn row(&self, q: usize) -> Vec<bool> {
        self.bmat[q].clone()
    }
    /// B 의 열 j (length n).
    fn col(&self, j: usize) -> Vec<bool> {
        (0..self.n).map(|i| self.bmat[i][j]).collect()
    }

    /// 지지집합(support)의 아핀 방향 벡터들 — `B` 의 열들 (각 length n).
    ///
    /// `supp(|φ⟩) = { b ⊕ Σ_j u_j·B[:,j] }` 이므로 이 열들의 span 이 아핀
    /// 부분공간의 방향이다.  MCMC 제안이 지지집합 내부에서 이동하도록 하는 데
    /// 쓰인다 (단일 비트플립은 아핀 지지집합을 연결하지 못함).
    pub fn support_directions(&self) -> Vec<Vec<bool>> {
        (0..self.k).map(|j| self.col(j)).collect()
    }

    /// `B u = z` 풀이 (유일 또는 None).
    fn solve(&self, z: &[bool]) -> Option<Vec<bool>> {
        let n = self.n;
        let k = self.k;
        if k == 0 {
            return if z.iter().all(|&x| !x) {
                Some(vec![])
            } else {
                None
            };
        }
        let mut a: Vec<Vec<bool>> = (0..n)
            .map(|i| {
                let mut r = self.bmat[i].clone();
                r.push(z[i]);
                r
            })
            .collect();
        let mut piv = vec![usize::MAX; k];
        let mut r = 0;
        for col in 0..k {
            let mut sel = None;
            for row in r..n {
                if a[row][col] {
                    sel = Some(row);
                    break;
                }
            }
            let Some(sel) = sel else { continue };
            a.swap(r, sel);
            for row in 0..n {
                if row != r && a[row][col] {
                    for c2 in 0..=k {
                        let t = a[r][c2];
                        a[row][c2] ^= t;
                    }
                }
            }
            piv[col] = r;
            r += 1;
        }
        for row in 0..n {
            if (0..k).all(|c| !a[row][c]) && a[row][k] {
                return None;
            }
        }
        let mut u = vec![false; k];
        for col in 0..k {
            if piv[col] != usize::MAX {
                u[col] = a[piv[col]][k];
            }
        }
        Some(u)
    }

    pub fn amplitude(&self, x: &[u8]) -> Complex64 {
        let z: Vec<bool> = (0..self.n).map(|i| (x[i] == 1) ^ self.b[i]).collect();
        let Some(u) = self.solve(&z) else {
            return Complex64::new(0.0, 0.0);
        };
        let qv = self.phi.eval(&u);
        let phase = Complex64::from_polar(1.0, (qv as f64) * FRAC_PI_2);
        let scale = 2.0_f64.powf(-(self.k as f64) / 2.0);
        self.omega * phase * Complex64::new(scale, 0.0)
    }

    /// 같은 상태에 대해 **여러 비트열의 amplitude 를 평가** 할 때 (MCMC 샘플링)
    /// 쓰는 미리계산 평가기를 만든다.  [`amplitude`] 는 호출마다 `B` 를 Gaussian
    /// elimination (O(n·k²)) 하지만, 샘플링 중 `B` 는 불변이므로 `B` 의 행축약
    /// 변환 `T` (`T·B = R`, RREF) 를 **1회** 계산해 두면 각 solve 가 단일 행렬·
    /// 벡터곱 O(n²) 으로 줄어든다.
    ///
    /// [`amplitude`]: ChForm::amplitude
    pub fn amp_eval(&self) -> ChAmpEval {
        let n = self.n;
        let k = self.k;
        // 증강행렬 [B | I_n] → 가우스 소거 → [R | T] (T·B = R).
        let mut a: Vec<Vec<bool>> = (0..n)
            .map(|i| {
                let mut r = self.bmat[i].clone(); // length k
                r.extend((0..n).map(|j| j == i)); // identity 부분
                r
            })
            .collect();
        let width = k + n;
        let mut piv = vec![usize::MAX; k];
        let mut r = 0;
        for col in 0..k {
            let mut sel = None;
            for row in r..n {
                if a[row][col] {
                    sel = Some(row);
                    break;
                }
            }
            let Some(sel) = sel else { continue };
            a.swap(r, sel);
            for row in 0..n {
                if row != r && a[row][col] {
                    for c2 in 0..width {
                        let t = a[r][c2];
                        a[row][c2] ^= t;
                    }
                }
            }
            piv[col] = r;
            r += 1;
        }
        // 행 i 가 pivot 행인지 / 어떤 col 의 pivot 인지.
        let mut is_pivot_row = vec![false; n];
        let mut pivot_col_for_row = vec![0usize; n];
        for (col, &row) in piv.iter().enumerate() {
            if row != usize::MAX {
                is_pivot_row[row] = true;
                pivot_col_for_row[row] = col;
            }
        }
        // T = a[.][k..k+n].
        let tmat: Vec<Vec<bool>> = a.iter().map(|row| row[k..width].to_vec()).collect();
        ChAmpEval {
            n,
            k,
            b: self.b.clone(),
            omega: self.omega,
            phi: self.phi.clone(),
            tmat,
            is_pivot_row,
            pivot_col_for_row,
        }
    }

    // ---- C-type / Pauli ----
    pub fn x_gate(&mut self, q: usize) {
        self.b[q] ^= true;
    }
    pub fn z_gate(&mut self, q: usize) {
        let r = self.row(q);
        self.phi.add_parity(&r, 2);
        if self.b[q] {
            self.phi.c0 = (self.phi.c0 + 2) & 3;
        }
    }
    pub fn s_gate(&mut self, q: usize) {
        let r = self.row(q);
        if !self.b[q] {
            self.phi.add_parity(&r, 1);
        } else {
            self.phi.c0 = (self.phi.c0 + 1) & 3;
            self.phi.add_parity(&r, 3);
        }
    }
    pub fn sdg_gate(&mut self, q: usize) {
        self.s_gate(q);
        self.s_gate(q);
        self.s_gate(q);
    }
    pub fn y_gate(&mut self, q: usize) {
        self.z_gate(q);
        self.x_gate(q);
        self.phi.c0 = (self.phi.c0 + 1) & 3;
    }
    pub fn cz_gate(&mut self, q: usize, r: usize) {
        let rq = self.row(q);
        let rr = self.row(r);
        let cq = self.b[q];
        let cr = self.b[r];
        if !cq && !cr {
            self.phi.add_quad_outer(&rq, &rr);
        } else if cq && cr {
            self.phi.c0 = (self.phi.c0 + 2) & 3;
            self.phi.add_parity(&rq, 2);
            self.phi.add_parity(&rr, 2);
            self.phi.add_quad_outer(&rq, &rr);
        } else if cq && !cr {
            self.phi.add_parity(&rr, 2);
            self.phi.add_quad_outer(&rq, &rr);
        } else {
            self.phi.add_parity(&rq, 2);
            self.phi.add_quad_outer(&rq, &rr);
        }
    }
    pub fn cx_gate(&mut self, q: usize, t: usize) {
        for j in 0..self.k {
            let v = self.bmat[q][j];
            self.bmat[t][j] ^= v;
        }
        let v = self.b[q];
        self.b[t] ^= v;
    }
    pub fn sx_gate(&mut self, q: usize) {
        self.h_gate(q);
        self.s_gate(q);
        self.h_gate(q);
    }
    pub fn sxdg_gate(&mut self, q: usize) {
        self.h_gate(q);
        self.sdg_gate(q);
        self.h_gate(q);
    }

    /// 단일 변수 치환 `u_l → u_l ⊕ u_c` (φ 재구성 + B 열 갱신).
    fn subst_xor(&mut self, l: usize, c: usize) {
        // φ relabel: v_l = u_l ⊕ u_c, 나머지 v_i=u_i.
        let mut amask: Vec<Vec<bool>> = (0..self.k)
            .map(|i| {
                let mut row = vec![false; self.k];
                row[i] = true;
                row
            })
            .collect();
        amask[l][c] = true; // v_l = u_l ⊕ u_c
        self.phi = self.phi.relabel(&amask);
        // B' col c ^= col l.
        for i in 0..self.n {
            let v = self.bmat[i][l];
            self.bmat[i][c] ^= v;
        }
    }

    /// 자유변수 `c` (col c = 0) 를 sum-out — Gauss 소거.
    fn sum_out_free(&mut self, c: usize) {
        // φ = φ\c + L u_c + 2 u_c Σ_j d_j u_j,  L=lin[c], d_j=quad[c][j].
        let l = self.phi.lin[c];
        let d: Vec<bool> = (0..self.k)
            .map(|j| j != c && self.phi.quad[c][j] == 1)
            .collect();
        let dnz = d.iter().any(|&x| x);
        if l & 1 == 1 {
            // L 홀수: factor √2 e^{±iπ/4} i^{∓p}.  √2 는 k→k-1 로 2^{-k/2} 가 √2
            // 커지며 자동 흡수 → ω 에는 위상 e^{±iπ/4} 만.
            let sign = if l == 1 { 1.0 } else { -1.0 };
            self.omega *= Complex64::from_polar(1.0, sign * std::f64::consts::FRAC_PI_4);
            // i^{∓(parity d·u')}: l=1 → i^{-(d·u)} → add_parity(d, -1=3); l=3 → +1.
            let mult = if l == 1 { 3 } else { 1 };
            self.phi.add_parity(&d, mult);
            self.drop_var(c);
        } else if !dnz {
            // L 짝수, d=0.  L=0 → factor 2 (정규화 over-count, 정상상태선 미발생);
            //               L=2 → factor 0 (상태 0).
            if l == 0 {
                // 정상 입력에선 발생 안 함 — 안전하게 ω *= √2.
                self.omega *= Complex64::new(2.0_f64.sqrt(), 0.0);
            } else {
                self.omega = Complex64::new(0.0, 0.0);
            }
            self.drop_var(c);
        } else {
            // L 짝수, d≠0: 제약 d·u' = cval (cval=L/2).  pivot p 제거.
            let cval = (l >> 1) & 1; // L=0→0, L=2→1
            let p = d.iter().position(|&x| x).unwrap();
            // u_p = cval ⊕ ⊕_{j∈d\p} u_j.  B'/φ 에서 u_p 치환·제거.
            // mask = d\{p}.
            let mut mask = d.clone();
            mask[p] = false;
            // B': col j (j∈mask) ^= col p ; b ^= col p · cval.
            let colp = self.col(p);
            for i in 0..self.n {
                if colp[i] {
                    for (j, &mj) in mask.iter().enumerate() {
                        if mj {
                            self.bmat[i][j] ^= true;
                        }
                    }
                    if cval == 1 {
                        self.b[i] ^= true;
                    }
                }
            }
            // φ: u_p → (mask·u) ⊕ cval.  relabel + 상수.
            // v_p = mask·u ⊕ cval 을 선형치환 + cval 상수로.
            self.substitute_const(p, &mask, cval == 1);
            // 두 자유변수 (c, p) 제거.  factor 2 = 2^{-k/2}·2 = 2^{-(k-2)/2} (정규화 정확).
            // c 와 p 모두 drop (c 는 이미 col 0; p 는 치환됨).
            let (hi, lo) = if c > p { (c, p) } else { (p, c) };
            self.drop_var(hi);
            self.drop_var(lo);
            for i in 0..self.n {
                self.bmat[i].remove(hi);
                self.bmat[i].remove(lo);
            }
            self.k -= 2;
            return;
        }
        // c 만 제거된 경우 B 열 제거.
        for i in 0..self.n {
            self.bmat[i].remove(c);
        }
        self.k -= 1;
    }

    /// φ 에서 변수 `p` 를 `(mask·u) ⊕ cst` 로 치환 (p 는 mask 에 없음).  변수는
    /// 제거하지 않음 (호출자가 drop).
    fn substitute_const(&mut self, p: usize, mask: &[bool], cst: bool) {
        // u_p → (mask·u) ⊕ cst = flip(if cst) ∘ relabel(u_p→mask·u).
        if cst {
            self.phi.flip_var(p); // u_p → 1 ⊕ u_p
        }
        let mut amask: Vec<Vec<bool>> = (0..self.k)
            .map(|i| {
                let mut row = vec![false; self.k];
                row[i] = true;
                row
            })
            .collect();
        amask[p] = mask.to_vec(); // 그 후 u_p → mask·u  → 합성: (mask·u)⊕cst
        self.phi = self.phi.relabel(&amask);
    }

    fn drop_var(&mut self, c: usize) {
        self.phi.drop_var(c);
    }

    /// kernel 기반 reduction — B' 를 full column rank 로.
    fn reduce(&mut self) {
        while let Some(mu) = self.kernel_vector() {
            // c = support(mu) 의 최대 인덱스.
            let c = (0..self.k).rev().find(|&i| mu[i]).unwrap();
            // l ∈ support(mu)\{c}: subst u_l → u_l ⊕ u_c → col c = 0.
            for l in 0..self.k {
                if l != c && mu[l] {
                    self.subst_xor(l, c);
                }
            }
            // 이제 col c = 0.  sum-out.
            self.sum_out_free(c);
        }
    }

    /// B' 의 kernel 벡터 (열 의존) 하나 — 없으면 None.
    fn kernel_vector(&self) -> Option<Vec<bool>> {
        let n = self.n;
        let k = self.k;
        if k == 0 {
            return None;
        }
        // 열을 변수로 행 소거 → free 열 발견 시 kernel 구성.
        let mut a: Vec<Vec<bool>> = self.bmat.clone();
        let mut piv_col_of_row = vec![usize::MAX; n];
        let mut where_piv = vec![usize::MAX; k]; // col → pivot row
        let mut r = 0;
        for col in 0..k {
            let mut sel = None;
            for row in r..n {
                if a[row][col] {
                    sel = Some(row);
                    break;
                }
            }
            let Some(sel) = sel else { continue };
            a.swap(r, sel);
            for row in 0..n {
                if row != r && a[row][col] {
                    for c2 in 0..k {
                        let t = a[r][c2];
                        a[row][c2] ^= t;
                    }
                }
            }
            piv_col_of_row[r] = col;
            where_piv[col] = r;
            r += 1;
        }
        // free 열 = pivot 없는 열 → kernel 벡터.
        for free in 0..k {
            if where_piv[free] == usize::MAX {
                let mut mu = vec![false; k];
                mu[free] = true;
                for col in 0..k {
                    if where_piv[col] != usize::MAX && a[where_piv[col]][free] {
                        mu[col] = true;
                    }
                }
                return Some(mu);
            }
        }
        None
    }

    /// H_q.
    pub fn h_gate(&mut self, q: usize) {
        let r = self.row(q);
        let bq = self.b[q];
        // 변수 w 추가, 비트 q = w.
        self.phi.push_var();
        let w = self.k;
        self.k += 1;
        for i in 0..self.n {
            self.bmat[i].push(false);
        }
        // φ += 2 w (r·u ⊕ b_q) = 2 w (r·u) + 2 b_q w.
        for (j, &rj) in r.iter().enumerate() {
            if rj {
                self.phi.quad[w][j] ^= 1;
                self.phi.quad[j][w] ^= 1;
            }
        }
        if bq {
            self.phi.lin[w] = (self.phi.lin[w] + 2) & 3;
        }
        // 비트 q 행 = e_w.
        self.bmat[q] = vec![false; self.k];
        self.bmat[q][w] = true;
        self.b[q] = false;
        // full column rank 회복.
        self.reduce();
    }
}

/// [`ChForm::amp_eval`] 가 반환하는 미리계산 amplitude 평가기.
///
/// `B` 의 행축약 변환 `T` (`T·B = R`, RREF) 를 보관해, `B u = z` 풀이를
/// 단일 행렬·벡터곱 `y = T·z` (O(n²)) + pivot 읽기 (O(n)) 로 처리한다.
/// 같은 상태에서 다수 비트열을 평가하는 MCMC 샘플링에 쓰인다 — 결과는
/// [`ChForm::amplitude`] 와 bit-exact.
pub struct ChAmpEval {
    n: usize,
    k: usize,
    b: Vec<bool>,
    omega: Complex64,
    phi: Z4Form,
    /// `T`: n×n, `T·B = R` (RREF).  행 i = `tmat[i]` (length n).
    tmat: Vec<Vec<bool>>,
    is_pivot_row: Vec<bool>,
    pivot_col_for_row: Vec<usize>,
}

impl ChAmpEval {
    /// `⟨x|ψ⟩` — [`ChForm::amplitude`] 와 동일하지만 미리계산된 `T` 를 사용.
    pub fn amplitude(&self, x: &[u8]) -> Complex64 {
        let n = self.n;
        // z = x ⊕ b ;  y = T·z 를 계산하며 pivot 행에서 u 를 읽고 free 행은
        // 일관성 (y=0) 을 검사한다.
        let z: Vec<bool> = (0..n).map(|i| (x[i] == 1) ^ self.b[i]).collect();
        let mut u = vec![false; self.k];
        for i in 0..n {
            let row = &self.tmat[i];
            let mut yi = false;
            for j in 0..n {
                yi ^= row[j] & z[j];
            }
            if self.is_pivot_row[i] {
                u[self.pivot_col_for_row[i]] = yi;
            } else if yi {
                return Complex64::new(0.0, 0.0); // 해 없음 (지지집합 밖).
            }
        }
        let qv = self.phi.eval(&u);
        let phase = Complex64::from_polar(1.0, (qv as f64) * FRAC_PI_2);
        let scale = 2.0_f64.powf(-(self.k as f64) / 2.0);
        self.omega * phase * Complex64::new(scale, 0.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_complex::Complex64;
    use rand::rngs::StdRng;
    use rand::{Rng, SeedableRng};

    struct Dense {
        n: usize,
        amp: Vec<Complex64>,
    }
    impl Dense {
        fn new(n: usize) -> Self {
            let mut amp = vec![Complex64::new(0.0, 0.0); 1 << n];
            amp[0] = Complex64::new(1.0, 0.0);
            Dense { n, amp }
        }
        fn one(&mut self, q: usize, m: [[Complex64; 2]; 2]) {
            let st = 1 << q;
            for base in 0..(1 << self.n) {
                if base & st == 0 {
                    let a = self.amp[base];
                    let b = self.amp[base | st];
                    self.amp[base] = m[0][0] * a + m[0][1] * b;
                    self.amp[base | st] = m[1][0] * a + m[1][1] * b;
                }
            }
        }
        fn h(&mut self, q: usize) {
            let s = Complex64::new(1.0 / 2.0_f64.sqrt(), 0.0);
            self.one(q, [[s, s], [s, -s]]);
        }
        fn s(&mut self, q: usize) {
            self.one(
                q,
                [
                    [Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                    [Complex64::new(0.0, 0.0), Complex64::new(0.0, 1.0)],
                ],
            );
        }
        fn z(&mut self, q: usize) {
            self.one(
                q,
                [
                    [Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                    [Complex64::new(0.0, 0.0), Complex64::new(-1.0, 0.0)],
                ],
            );
        }
        fn x(&mut self, q: usize) {
            let o = Complex64::new(1.0, 0.0);
            let z = Complex64::new(0.0, 0.0);
            self.one(q, [[z, o], [o, z]]);
        }
        fn y(&mut self, q: usize) {
            let i = Complex64::new(0.0, 1.0);
            let z = Complex64::new(0.0, 0.0);
            self.one(q, [[z, -i], [i, z]]);
        }
        fn cz(&mut self, q: usize, r: usize) {
            for base in 0..(1 << self.n) {
                if base & (1 << q) != 0 && base & (1 << r) != 0 {
                    self.amp[base] = -self.amp[base];
                }
            }
        }
        fn cx(&mut self, q: usize, r: usize) {
            for base in 0..(1 << self.n) {
                if base & (1 << q) != 0 && base & (1 << r) == 0 {
                    self.amp.swap(base, base | (1 << r));
                }
            }
        }
    }

    #[test]
    fn qfe_matches_dense_full_clifford() {
        let mut rng = StdRng::seed_from_u64(7);
        for _ in 0..500 {
            let n = rng.gen_range(1..6);
            let mut ch = ChForm::new(n);
            let mut d = Dense::new(n);
            for _ in 0..rng.gen_range(0..10 * n) {
                match rng.gen_range(0..7) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        ch.h_gate(q);
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        ch.s_gate(q);
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        ch.z_gate(q);
                        d.z(q);
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        ch.x_gate(q);
                        d.x(q);
                    }
                    4 => {
                        let q = rng.gen_range(0..n);
                        ch.y_gate(q);
                        d.y(q);
                    }
                    5 => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            ch.cz_gate(a, b);
                            d.cz(a, b);
                        }
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            ch.cx_gate(a, b);
                            d.cx(a, b);
                        }
                    }
                }
            }
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let got = ch.amplitude(&bits);
                assert!(
                    (got - d.amp[i]).norm() < 1e-9,
                    "n={n} i={i} got={got} want={}",
                    d.amp[i]
                );
            }
        }
    }

    /// 미리계산 평가기 [`ChAmpEval`] 가 [`ChForm::amplitude`] 와 bit-exact 인지
    /// (전 비트열) 확인한다 — 같은 RREF 이론, 분할상환 경로만 다름.
    #[test]
    fn amp_eval_matches_amplitude() {
        let mut rng = StdRng::seed_from_u64(31);
        for _ in 0..400 {
            let n = rng.gen_range(1..7);
            let mut ch = ChForm::new(n);
            for _ in 0..rng.gen_range(0..10 * n) {
                match rng.gen_range(0..7) {
                    0 => ch.h_gate(rng.gen_range(0..n)),
                    1 => ch.s_gate(rng.gen_range(0..n)),
                    2 => ch.z_gate(rng.gen_range(0..n)),
                    3 => ch.x_gate(rng.gen_range(0..n)),
                    4 => ch.y_gate(rng.gen_range(0..n)),
                    5 if n >= 2 => {
                        let a = rng.gen_range(0..n);
                        let mut b = rng.gen_range(0..n);
                        while b == a {
                            b = rng.gen_range(0..n);
                        }
                        ch.cz_gate(a, b);
                    }
                    _ if n >= 2 => {
                        let a = rng.gen_range(0..n);
                        let mut b = rng.gen_range(0..n);
                        while b == a {
                            b = rng.gen_range(0..n);
                        }
                        ch.cx_gate(a, b);
                    }
                    _ => {}
                }
            }
            let eval = ch.amp_eval();
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let a = ch.amplitude(&bits);
                let e = eval.amplitude(&bits);
                assert!(
                    (a - e).norm() < 1e-12,
                    "n={n} i={i} amplitude={a} amp_eval={e}"
                );
            }
        }
    }

    /// `cargo test -p qsim-stabilizer amp_eval_speedup -- --ignored --nocapture`
    /// 로 ChForm::amplitude (매번 Gauss 소거) vs ChAmpEval (RREF 1회) 비교.
    #[test]
    #[ignore]
    fn amp_eval_speedup() {
        let mut rng = StdRng::seed_from_u64(1);
        let n = 60;
        let mut ch = ChForm::new(n);
        for _ in 0..(3 * n) {
            match rng.gen_range(0..3) {
                0 => ch.h_gate(rng.gen_range(0..n)),
                1 => ch.cx_gate(rng.gen_range(0..n), rng.gen_range(0..n)),
                _ => ch.s_gate(rng.gen_range(0..n)),
            }
        }
        let queries: Vec<Vec<u8>> = (0..20000)
            .map(|_| (0..n).map(|_| rng.gen::<bool>() as u8).collect())
            .collect();
        let t0 = std::time::Instant::now();
        let mut s1 = Complex64::new(0.0, 0.0);
        for q in &queries {
            s1 += ch.amplitude(q);
        }
        let slow = t0.elapsed();
        let eval = ch.amp_eval();
        let t1 = std::time::Instant::now();
        let mut s2 = Complex64::new(0.0, 0.0);
        for q in &queries {
            s2 += eval.amplitude(q);
        }
        let fast = t1.elapsed();
        eprintln!(
            "n={n} k={} queries={}: amplitude={slow:?} amp_eval={fast:?} (×{:.1})",
            eval.k,
            queries.len(),
            slow.as_secs_f64() / fast.as_secs_f64().max(1e-9)
        );
        assert!((s1 - s2).norm() < 1e-9);
    }
}
