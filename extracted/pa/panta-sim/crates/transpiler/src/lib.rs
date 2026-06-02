//! 양자 회로 변환 (transpile) 패스 모음.
//!
//! - [`decompose`] : 임의 1큐비트 unitary → Rz(δ)·Ry(γ)·Rz(β) + global phase α
//!   (Nielsen-Chuang Thm 4.1)
//! - [`validate`] : 입력 행렬의 unitarity 검증 (`M·M† ≈ I`)
//! - [`peephole`] : 가벼운 회로 최적화 (회전 합성, 항등식)
//! - [`basis`] : 회로 레벨 CX-basis 타깃 transpile (모든 2/3q 게이트 → CX + 1q)

pub mod basis;
pub mod decompose;
pub mod peephole;
pub mod validate;

pub use basis::{is_cx_basis, transpile_to_cx_basis, TranspileError};
pub use decompose::{append_unitary, decompose_unitary_zyz, Matrix2, ZyzDecomposition};
pub use peephole::{peephole_optimize, PeepholeStats};
pub use validate::{is_unitary_2x2, UnitarityError};
