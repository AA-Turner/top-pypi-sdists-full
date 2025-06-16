from typing import overload
from enum import Enum
import abc
import typing

import System
import System.Runtime.Intrinsics
import System.Runtime.Intrinsics.Wasm


class PackedSimd(System.Object, metaclass=abc.ABCMeta):
    """Provides access to the WebAssembly packed SIMD instructions via intrinsics."""

    IS_SUPPORTED: bool
    """Gets a value that indicates whether the APIs in this class are supported."""

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.abs"""
        ...

    @staticmethod
    @overload
    def abs(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.abs"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.add"""
        ...

    @staticmethod
    @overload
    def add(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.add"""
        ...

    @staticmethod
    def add_pairwise_widening(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extadd_pairwise_i8x16_s"""
        ...

    @staticmethod
    def add_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.add.sat.s"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """i8x16.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def all_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        """i32x4.all_true"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def And(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.and"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def and_not(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.andnot"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[int]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[float]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    @overload
    def any_true(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> bool:
        """v128.any_true"""
        ...

    @staticmethod
    def average_rounded(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.avgr.u"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[int]) -> int:
        """i8x16.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitmask(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> int:
        """i32x4.bitmask"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int], select: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float], select: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr], select: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.bitselect"""
        ...

    @staticmethod
    @overload
    def bitwise_select(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr], select: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.bitselect"""
        ...

    @staticmethod
    def ceiling(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ceil"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.eq"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.gt"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.gt_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.gt_u"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ge"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.ge_s"""
        ...

    @staticmethod
    @overload
    def compare_greater_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.ge_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.lt"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.lt_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.lt_u"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.le"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.le_s"""
        ...

    @staticmethod
    @overload
    def compare_less_than_or_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.le_u"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.ne"""
        ...

    @staticmethod
    @overload
    def compare_not_equal(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.ne"""
        ...

    @staticmethod
    def convert_narrowing_saturate_signed(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.narrow_i16x8_s"""
        ...

    @staticmethod
    def convert_narrowing_saturate_unsigned(lower: System.Runtime.Intrinsics.Vector128[int], upper: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.narrow_i16x8_u"""
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.convert_low_i32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_double_lower(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f64x2.promote_low_f32x4"""
        ...

    @staticmethod
    def convert_to_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.convert_i32x4_s"""
        ...

    @staticmethod
    @overload
    def convert_to_single(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.demote_f64x2_zero"""
        ...

    @staticmethod
    def convert_to_u_int_32_saturate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.trunc_sat_f32x4_u"""
        ...

    @staticmethod
    def divide(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.div"""
        ...

    @staticmethod
    def dot(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i32x4.dot_i16x8_s"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[int], index: int) -> int:
        """i8x16.extract_lane_s"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[float], index: int) -> float:
        """f32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.IntPtr:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    @overload
    def extract_scalar(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.UIntPtr:
        """i32x4.extract_lane"""
        ...

    @staticmethod
    def floor(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.floor"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[int], index: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[float], index: int) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.load32_lane"""
        ...

    @staticmethod
    @overload
    def load_scalar_and_insert(address: typing.Any, vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.load32_lane"""
        ...

    @staticmethod
    def load_scalar_and_splat_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8_splat"""
        ...

    @staticmethod
    def load_scalar_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load32.zero"""
        ...

    @staticmethod
    def load_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load"""
        ...

    @staticmethod
    def load_widening_vector_128(address: typing.Any) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.load8x8_s"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.max.s"""
        ...

    @staticmethod
    @overload
    def max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.max"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.min.s"""
        ...

    @staticmethod
    @overload
    def min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.min"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.mul"""
        ...

    @staticmethod
    @overload
    def multiply(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.mul"""
        ...

    @staticmethod
    def multiply_rounded_saturate_q_15(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.q15mulr.sat.s"""
        ...

    @staticmethod
    def multiply_widening_lower(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_low_i8x16_s"""
        ...

    @staticmethod
    def multiply_widening_upper(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extmul_high_i8x16_s"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.neg"""
        ...

    @staticmethod
    @overload
    def negate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.neg"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Not(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.not"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.or"""
        ...

    @staticmethod
    @overload
    def Or(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.or"""
        ...

    @staticmethod
    def pop_count(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.popcnt"""
        ...

    @staticmethod
    def pseudo_max(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.pmax"""
        ...

    @staticmethod
    def pseudo_min(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.pmin"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[int], imm: int, value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[float], imm: int, value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.IntPtr], imm: int, value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    @overload
    def replace_scalar(vector: System.Runtime.Intrinsics.Vector128[System.UIntPtr], imm: int, value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.replace_lane"""
        ...

    @staticmethod
    def round_to_nearest(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.nearest"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_left(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shl"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_arithmetic(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shr_s"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[int], count: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.IntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    @overload
    def shift_right_logical(value: System.Runtime.Intrinsics.Vector128[System.UIntPtr], count: int) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.shr_u"""
        ...

    @staticmethod
    def sign_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_s"""
        ...

    @staticmethod
    def sign_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_s"""
        ...

    @staticmethod
    @overload
    def splat(value: int) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: float) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: System.IntPtr) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    @overload
    def splat(value: System.UIntPtr) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.splat or v128.const"""
        ...

    @staticmethod
    def sqrt(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.sqrt"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> None:
        """v128.store"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[int], index: int) -> None:
        """v128.store8_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[float], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.IntPtr], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def store_selected_scalar(address: typing.Any, source: System.Runtime.Intrinsics.Vector128[System.UIntPtr], index: int) -> None:
        """v128.store32_lane"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """i32x4.sub"""
        ...

    @staticmethod
    @overload
    def subtract(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.sub"""
        ...

    @staticmethod
    def subtract_saturate(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.sub.sat.s"""
        ...

    @staticmethod
    def swizzle(vector: System.Runtime.Intrinsics.Vector128[int], indices: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i8x16.swizzle"""
        ...

    @staticmethod
    def truncate(value: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """f32x4.trunc"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[int], right: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[float], right: System.Runtime.Intrinsics.Vector128[float]) -> System.Runtime.Intrinsics.Vector128[float]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.IntPtr], right: System.Runtime.Intrinsics.Vector128[System.IntPtr]) -> System.Runtime.Intrinsics.Vector128[System.IntPtr]:
        """v128.xor"""
        ...

    @staticmethod
    @overload
    def xor(left: System.Runtime.Intrinsics.Vector128[System.UIntPtr], right: System.Runtime.Intrinsics.Vector128[System.UIntPtr]) -> System.Runtime.Intrinsics.Vector128[System.UIntPtr]:
        """v128.xor"""
        ...

    @staticmethod
    def zero_extend_widening_lower(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_low_i8x16_u"""
        ...

    @staticmethod
    def zero_extend_widening_upper(value: System.Runtime.Intrinsics.Vector128[int]) -> System.Runtime.Intrinsics.Vector128[int]:
        """i16x8.extend_high_i8x16_u"""
        ...


