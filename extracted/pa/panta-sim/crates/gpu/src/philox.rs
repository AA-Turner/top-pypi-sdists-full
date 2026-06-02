//! Philox4x32-10 counter-based RNG (v0.6.10).
//!
//! Salmon, Moraes, Dror & Shaw, "Parallel Random Numbers: As Easy as 1, 2, 3"
//! (SC 2011, Random123).  Counter-based RNG 는 상태가 없어 GPU 의 각
//! invocation 이 (counter, key) 만으로 독립적이고 결정적인 난수를 생성할 수
//! 있다 — statevector / trajectory 의 GPU-side sampling 에 이상적.
//!
//! 이 모듈의 [`philox4x32_10`] CPU 레퍼런스는 동일 알고리즘의 WGSL 셰이더
//! (`shaders/philox_uniform.wgsl`) 와 bit-exact 해야 하며, Random123 의 공식
//! known-answer test (KAT) 벡터로 검증된다 (`tests` 모듈).  WGSL 셰이더는 GPU
//! device 가 필요해 sandbox 에서 직접 실행 검증은 불가하나, CPU 레퍼런스가
//! KAT 를 통과하면 알고리즘 정확성이 보장되고 셰이더는 그 1:1 이식이다.

/// Philox multiplier 상수 (M4x32).
const PHILOX_M0: u32 = 0xD251_1F53;
const PHILOX_M1: u32 = 0xCD9E_8D57;
/// Weyl sequence 상수 (key bump).
const PHILOX_W0: u32 = 0x9E37_79B9;
const PHILOX_W1: u32 = 0xBB67_AE85;

/// 32-bit 곱의 (high32, low32) 를 반환.
#[inline]
fn mulhilo(a: u32, b: u32) -> (u32, u32) {
    let prod = (a as u64) * (b as u64);
    ((prod >> 32) as u32, prod as u32)
}

/// 32×32 곱의 high 32비트를, 64비트 타입 없이 16비트 분해로 계산한다.
///
/// WGSL 에는 u64 가 없으므로 `philox_uniform.wgsl` 의 `mulhi` 가 이 알고리즘을
/// 그대로 사용한다.  이 Rust 사본은 셰이더가 쓰는 정확한 산술을 sandbox 에서
/// 검증하기 위한 것 — [`mulhilo`] (네이티브 u64) 와 모든 입력에서 일치해야
/// 한다 (`tests::mulhi_16bit_matches_native`).
#[cfg(test)]
#[inline]
fn mulhi_16bit(a: u32, b: u32) -> u32 {
    let a_lo = a & 0xFFFF;
    let a_hi = a >> 16;
    let b_lo = b & 0xFFFF;
    let b_hi = b >> 16;
    let ab_lo = a_lo.wrapping_mul(b_lo);
    let ab_mid = a_hi.wrapping_mul(b_lo);
    let ab_mid2 = a_lo.wrapping_mul(b_hi);
    let ab_hi = a_hi.wrapping_mul(b_hi);
    let carry = (ab_lo >> 16)
        .wrapping_add(ab_mid & 0xFFFF)
        .wrapping_add(ab_mid2 & 0xFFFF);
    ab_hi
        .wrapping_add(ab_mid >> 16)
        .wrapping_add(ab_mid2 >> 16)
        .wrapping_add(carry >> 16)
}

/// Philox4x32 single round.
#[inline]
fn round(ctr: [u32; 4], key: [u32; 2]) -> [u32; 4] {
    let (hi0, lo0) = mulhilo(PHILOX_M0, ctr[0]);
    let (hi1, lo1) = mulhilo(PHILOX_M1, ctr[2]);
    [hi1 ^ ctr[1] ^ key[0], lo1, hi0 ^ ctr[3] ^ key[1], lo0]
}

/// Philox4x32-10: 128-bit counter + 64-bit key → 128-bit 난수 (4×u32).
///
/// 결정적·무상태: 동일 `(ctr, key)` 는 항상 동일 출력.
pub fn philox4x32_10(mut ctr: [u32; 4], mut key: [u32; 2]) -> [u32; 4] {
    for i in 0..10 {
        if i > 0 {
            key[0] = key[0].wrapping_add(PHILOX_W0);
            key[1] = key[1].wrapping_add(PHILOX_W1);
        }
        ctr = round(ctr, key);
    }
    ctr
}

/// u32 난수 비트를 `[0, 1)` 의 f32 uniform 으로 변환.
///
/// 상위 24비트만 사용해 f32 mantissa 에 정확히 표현 가능한 격자
/// (`k / 2^24`, k ∈ [0, 2^24)) 위의 값을 만든다 (WGSL 셰이더와 동일).
#[inline]
pub fn u32_to_unit_f32(x: u32) -> f32 {
    (x >> 8) as f32 * (1.0 / 16_777_216.0)
}

/// `count` 개의 `[0, 1)` uniform f32 를 생성한다 (CPU 레퍼런스).
///
/// `seed` 는 key 로, 블록 인덱스는 counter 의 하위 64비트로 사용한다 —
/// 블록 `b` 가 4개 (`b*4 .. b*4+4`) 의 uniform 을 담당.  GPU 셰이더가 각
/// invocation 에서 동일 매핑으로 4개씩 생성하므로 결과가 일치한다.
pub fn philox_uniforms_cpu(seed: u64, count: usize) -> Vec<f32> {
    let key = [seed as u32, (seed >> 32) as u32];
    let mut out = Vec::with_capacity(count);
    let n_blocks = count.div_ceil(4);
    for b in 0..n_blocks {
        let ctr = [b as u32, (b >> 32) as u32, 0, 0];
        let r = philox4x32_10(ctr, key);
        for &word in &r {
            if out.len() < count {
                out.push(u32_to_unit_f32(word));
            }
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Random123 공식 KAT (kat_vectors.txt) — philox4x32 10 rounds.
    /// ctr/key all-zero.
    #[test]
    fn kat_all_zero() {
        let out = philox4x32_10([0, 0, 0, 0], [0, 0]);
        assert_eq!(out, [0x6627_e8d5, 0xe169_c58d, 0xbc57_ac4c, 0x9b00_dbd8]);
    }

    /// KAT — ctr/key all-ones.
    #[test]
    fn kat_all_ones() {
        let out = philox4x32_10(
            [0xffff_ffff, 0xffff_ffff, 0xffff_ffff, 0xffff_ffff],
            [0xffff_ffff, 0xffff_ffff],
        );
        assert_eq!(out, [0x408f_276d, 0x41c8_3b0e, 0xa20b_c7c6, 0x6d54_51fd]);
    }

    /// KAT — digits of π / e (Random123 표준 3번째 벡터).
    #[test]
    fn kat_pi_digits() {
        let out = philox4x32_10(
            [0x243f_6a88, 0x85a3_08d3, 0x1319_8a2e, 0x0370_7344],
            [0xa409_3822, 0x299f_31d0],
        );
        assert_eq!(out, [0xd16c_fe09, 0x94fd_cceb, 0x5001_e420, 0x2412_6ea1]);
    }

    /// uniform 변환이 [0, 1) 범위.
    #[test]
    fn uniforms_in_range() {
        let us = philox_uniforms_cpu(0xdead_beef, 1000);
        assert_eq!(us.len(), 1000);
        for &u in &us {
            assert!((0.0..1.0).contains(&u), "u={u} out of [0,1)");
        }
    }

    /// 결정성: 동일 seed → 동일 sequence.
    #[test]
    fn deterministic() {
        let a = philox_uniforms_cpu(42, 64);
        let b = philox_uniforms_cpu(42, 64);
        assert_eq!(a, b);
        let c = philox_uniforms_cpu(43, 64);
        assert_ne!(a, c);
    }

    /// 16비트 분해 mulhi (WGSL 셰이더가 쓰는 산술) 가 네이티브 u64 mulhilo 의
    /// high 워드와 모든 테스트 입력에서 일치하는지 검증.
    #[test]
    fn mulhi_16bit_matches_native() {
        let samples = [
            0u32,
            1,
            0xFFFF_FFFF,
            0x8000_0000,
            0xDEAD_BEEF,
            0xCAFE_BABE,
            PHILOX_M0,
            PHILOX_M1,
            0x1234_5678,
            0x9ABC_DEF0,
            0x0000_FFFF,
            0xFFFF_0000,
        ];
        for &a in &samples {
            for &b in &samples {
                let (hi_native, _) = mulhilo(a, b);
                assert_eq!(
                    mulhi_16bit(a, b),
                    hi_native,
                    "mulhi mismatch a={a:#x} b={b:#x}"
                );
            }
        }
        // pseudo-random 광범위 입력.
        let mut x = 0x1234_5679u32;
        for _ in 0..5000 {
            x = x.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
            let mut y = x ^ 0x55AA_55AA;
            y = y.wrapping_mul(22_695_477).wrapping_add(1);
            let (hi_native, _) = mulhilo(x, y);
            assert_eq!(
                mulhi_16bit(x, y),
                hi_native,
                "mulhi mismatch x={x:#x} y={y:#x}"
            );
        }
    }

    /// 평균이 ~0.5 (간단 분포 sanity).
    #[test]
    fn mean_near_half() {
        let us = philox_uniforms_cpu(7, 100_000);
        let mean: f64 = us.iter().map(|&x| x as f64).sum::<f64>() / us.len() as f64;
        assert!((mean - 0.5).abs() < 0.01, "mean={mean}");
    }
}
