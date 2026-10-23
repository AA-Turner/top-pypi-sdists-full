from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

class reg_value_base_t:
    ADD: int  # 0
    AND: int  # 3
    AND_NOT: int  # 5
    CONTAINED: int  # 2
    CONTAINS: int  # 1
    EQUAL: int  # 0
    MOVT: int  # 9
    NEG: int  # 10
    NOT: int  # 11
    NOT_COMPARABLE: int  # 3
    OR: int  # 2
    SAR: int  # 8
    SLL: int  # 6
    SLR: int  # 7
    SUB: int  # 1
    XOR: int  # 4
    def __getitem__(self, i: int) -> reg_value_def_t:
        ...
    def __init__(self) -> Any:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> Any:
        ...
    def __str__(self) -> str:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def aborted(self) -> bool:
        r"""Return 'true' if the tracking process was aborted.
        
        """
        ...
    def add(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""The methods below save INSN as a defining instruction. Add R to the value. 
                
        """
        ...
    @overload
    def add_num(self, r: int, insn: insn_t) -> None:
        r"""Add R to the value."""
        ...
    @overload
    def add_num(self, r: int) -> None:
        r"""The methods below do not change the defining instructions. Add R to the value."""
        ...
    def band(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise AND of R to the value. 
                
        """
        ...
    def bandnot(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise AND of the inverse of R to the value. 
                
        """
        ...
    def bnot(self, insn: insn_t) -> None:
        r"""Make bitwise inverse of the value.
        
        """
        ...
    def bor(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise OR of R to the value. 
                
        """
        ...
    def bxor(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise eXclusive OR of R to the value. 
                
        """
        ...
    def clear(self) -> None:
        r"""Undefine the value.
        
        """
        ...
    def empty(self) -> bool:
        r"""Return 'true' if we know nothing about a value.
        
        """
        ...
    def extend(self, width: int, is_signed: bool) -> None:
        r"""Zero-, or sign-extend the value from WIDTH bytes to uint64. 
                
        """
        ...
    def get_aborting_depth(self) -> int:
        r"""Return the aborting depth if the value is ABORTED.
        
        """
        ...
    def get_def_ea(self) -> ida_idaapi.ea_t:
        r"""Return the defining address.
        
        """
        ...
    def get_def_itype(self) -> int:
        r"""Return the defining instruction code (processor specific).
        
        """
        ...
    def get_stride(self) -> int:
        r"""Return the loop stride of a NUMLOOP value. 
                
        """
        ...
    def has_any_vals_flag(self, val_flags: int) -> bool:
        ...
    def have_all_vals_flag(self, val_flags: int) -> bool:
        r"""Check the given flag for each value.
        
        """
        ...
    def is_all_vals_like_got(self) -> bool:
        ...
    def is_all_vals_pc_based(self) -> bool:
        ...
    def is_any_vals_had_delta(self) -> bool:
        ...
    def is_any_vals_like_got(self) -> bool:
        ...
    def is_any_vals_pc_based(self) -> bool:
        ...
    def is_badinsn(self) -> bool:
        r"""Return 'true' if the value is unknown because of a bad insn.
        
        """
        ...
    def is_dead_end(self) -> bool:
        r"""Return 'true' if the value is undefined because of a dead end.
        
        """
        ...
    def is_known(self) -> bool:
        r"""Return 'true' if the value is known (i.e. it is a number or SP delta).
        
        """
        ...
    def is_num(self) -> bool:
        r"""Return 'true' if the value is a constant.
        
        """
        ...
    def is_numloop(self) -> bool:
        r"""Return 'true' if the value is a number changed in a loop by adding a constant stride each iteration. 
                
        """
        ...
    def is_spd(self) -> bool:
        r"""Return 'true' if the value depends on the stack pointer.
        
        """
        ...
    def is_special(self) -> bool:
        r"""Return 'true' if the value requires special handling.
        
        """
        ...
    def is_unkfunc(self) -> bool:
        r"""Return 'true' if the value is unknown from the function start.
        
        """
        ...
    def is_unkinsn(self) -> bool:
        r"""Return 'true' if the value is unknown after executing the insn.
        
        """
        ...
    def is_unkloop(self) -> bool:
        r"""Return 'true' if the value is unknown because it changes in a loop.
        
        """
        ...
    def is_unkmult(self) -> bool:
        r"""Return 'true' if the value is unknown because the register has incompatible values (a number and SP delta). 
                
        """
        ...
    def is_unknown(self) -> bool:
        r"""Return 'true' if the value is unknown.
        
        """
        ...
    def is_unkvals(self) -> bool:
        r"""Return 'true' if the value is unknown because the register has too many values. 
                
        """
        ...
    def is_unkxref(self) -> bool:
        r"""Return 'true' if the value is unknown because there are too many xrefs.
        
        """
        ...
    def is_value_unique(self) -> bool:
        r"""Check that the value is unique.
        
        """
        ...
    @staticmethod
    def make_aborted(bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> reg_value_base_t:
        r"""Return the value after aborting. 
                
        """
        ...
    @staticmethod
    def make_badinsn(insn_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value after a bad insn. 
                
        """
        ...
    @staticmethod
    def make_dead_end(dead_end_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the undefined value because of a dead end. 
                
        """
        ...
    @staticmethod
    def make_initial_sp(func_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the value that is the initial stack pointer. 
                
        """
        ...
    @overload
    @staticmethod
    def make_num(rval: int, insn: insn_t, val_flags: int = 0) -> reg_value_base_t:
        r"""Return the value that is the RVAL number."""
        ...
    @overload
    @staticmethod
    def make_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: int = 0) -> reg_value_base_t:
        r"""Return the value that is the RVAL number."""
        ...
    @staticmethod
    def make_unkfunc(func_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value from the function start. 
                
        """
        ...
    @staticmethod
    def make_unkinsn(insn: insn_t) -> reg_value_base_t:
        r"""Return the unknown value after executing the insn. 
                
        """
        ...
    @staticmethod
    def make_unkloop(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if it changes in a loop. 
                
        """
        ...
    @staticmethod
    def make_unkmult(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if the register has incompatible values. 
                
        """
        ...
    @staticmethod
    def make_unkvals(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if the register has too many values. 
                
        """
        ...
    @staticmethod
    def make_unkxref(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if there are too many xrefs. 
                
        """
        ...
    def movt(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Replace the top 16 bits with bottom 16 bits of R, leaving the bottom 16 bits untouched. 
                
        """
        ...
    def neg(self, insn: insn_t) -> None:
        r"""Negate the value.
        
        """
        ...
    def sar(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift arithmetically the value right by R. 
                
        """
        ...
    def set_aborted(self, bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> None:
        r"""Set the value after aborting. 
                
        """
        ...
    def set_all_vals_flag(self, val_flags: int) -> None:
        r"""Set the given flag for each value.
        
        """
        ...
    def set_all_vals_got_based(self) -> None:
        ...
    def set_all_vals_had_delta(self) -> None:
        ...
    def set_all_vals_pc_based(self) -> None:
        ...
    def set_badinsn(self, insn_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown after a bad insn. 
                
        """
        ...
    def set_dead_end(self, dead_end_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be undefined because of a dead end. 
                
        """
        ...
    def set_def_itype_for_mov(self, insn: insn_t) -> bool:
        r"""Set the defining instruction The value of the destination register after the mov instruction is equal to the value of the source register before it. Therefore, we can consider this instruction as defining that value. 
                
        """
        ...
    @overload
    def set_num(self, rval: int, insn: insn_t, val_flags: int = 0) -> None:
        r"""Set the value to be a number after executing an insn."""
        ...
    @overload
    def set_num(self, rvals: uvalvec_t, insn: insn_t) -> None:
        r"""Set the value to be numbers after executing an insn."""
        ...
    @overload
    def set_num(self, rval: int, val_ea: ida_idaapi.ea_t, val_flags: int = 0) -> None:
        r"""Set the value to be a number before an address."""
        ...
    def set_numloop(self, loop_stride: int) -> None:
        r"""Turn a number into the NUMLOOP value: the register is changed in a loop by adding LOOP_STRIDE each iteration, VALS keeps the initial value(s). 
                
        """
        ...
    def set_unkfunc(self, func_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown from the function start. 
                
        """
        ...
    def set_unkinsn(self, insn: insn_t) -> None:
        r"""Set the value to be unknown after executing the insn. 
                
        """
        ...
    def set_unkloop(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because it changes in a loop. 
                
        """
        ...
    def set_unkmult(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because the register has incompatible values. 
                
        """
        ...
    def set_unkvals(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because the register has too many values. 
                
        """
        ...
    def set_unkxref(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because there are too many xrefs. 
                
        """
        ...
    def shift_left(self, r: int) -> None:
        r"""Shift the value left by R. 
                
        """
        ...
    def shift_right(self, r: int, nbytes: int = 0) -> None:
        r"""Shift the value right by R. If NBYTES is non-zero, perform an arithmetic (signed) shift assuming the value is NBYTES bytes wide. 
                
        """
        ...
    def sll(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift the value left by R. 
                
        """
        ...
    def slr(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift logically the value right by R. 
                
        """
        ...
    def sub(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Subtract R from the value. 
                
        """
        ...
    def swap(self, r: reg_value_base_t) -> None:
        ...
    def vals_union(self, r: reg_value_base_t) -> set_compare_res_t:
        r"""Add values from R into THIS ignoring duplicates. 
                
        :returns: EQUAL: THIS is not changed
        :returns: CONTAINS: THIS is not changed
        :returns: CONTAINED: THIS is a copy of R
        :returns: NOT_COMPARABLE: values from R are added to THIS
        """
        ...

class reg_value_def_t:
    ABORTED: int  # 3
    NOVAL: int  # 0
    SPVAL: int  # 2
    UVAL: int  # 1
    @property
    def HAD_DELTA(self) -> Any: ...
    @property
    def LIKE_GOT(self) -> Any: ...
    @property
    def PC_BASED(self) -> Any: ...
    @property
    def SHORT_INSN(self) -> Any: ...
    @property
    def def_ea(self) -> ida_idaapi.ea_t: ...
    @def_ea.setter
    def def_ea(self, value: ida_idaapi.ea_t) -> None: ...
    @property
    def def_itype(self) -> int: ...
    @def_itype.setter
    def def_itype(self, value: int) -> None: ...
    @property
    def flags(self) -> int: ...
    @flags.setter
    def flags(self, value: int) -> None: ...
    @property
    def val(self) -> int: ...
    @val.setter
    def val(self, value: int) -> None: ...
    def __eq__(self, r: reg_value_def_t) -> bool:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __lt__(self, r: reg_value_def_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def dstr(self, how: dstr_val_t, pm: procmod_t = None) -> str:
        r"""Return the string representation.
        
        """
        ...
    def had_delta(self) -> bool:
        ...
    def is_like_got(self) -> bool:
        ...
    def is_pc_based(self) -> bool:
        ...
    @overload
    def is_short_insn(self) -> bool: ...
    @overload
    def is_short_insn(self, insn: insn_t) -> bool: ...

class reg_value_info_t(reg_value_base_t):
    ADD: int  # 0
    AND: int  # 3
    AND_NOT: int  # 5
    CONTAINED: int  # 2
    CONTAINS: int  # 1
    EQUAL: int  # 0
    MOVT: int  # 9
    NEG: int  # 10
    NOT: int  # 11
    NOT_COMPARABLE: int  # 3
    OR: int  # 2
    SAR: int  # 8
    SLL: int  # 6
    SLR: int  # 7
    SUB: int  # 1
    XOR: int  # 4
    def __getitem__(self, i: int) -> reg_value_def_t:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> Any:
        ...
    def __str__(self) -> str:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def aborted(self) -> bool:
        r"""Return 'true' if the tracking process was aborted.
        
        """
        ...
    def add(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""The methods below save INSN as a defining instruction. Add R to the value. 
                
        """
        ...
    @overload
    def add_num(self, r: int, insn: insn_t) -> None:
        r"""Add R to the value."""
        ...
    @overload
    def add_num(self, r: int) -> None:
        r"""The methods below do not change the defining instructions. Add R to the value."""
        ...
    def band(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise AND of R to the value. 
                
        """
        ...
    def bandnot(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise AND of the inverse of R to the value. 
                
        """
        ...
    def bnot(self, insn: insn_t) -> None:
        r"""Make bitwise inverse of the value.
        
        """
        ...
    def bor(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise OR of R to the value. 
                
        """
        ...
    def bxor(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Make bitwise eXclusive OR of R to the value. 
                
        """
        ...
    def clear(self) -> None:
        r"""Undefine the value.
        
        """
        ...
    def empty(self) -> bool:
        r"""Return 'true' if we know nothing about a value.
        
        """
        ...
    def extend(self, width: int, is_signed: bool) -> None:
        r"""Zero-, or sign-extend the value from WIDTH bytes to uint64. 
                
        """
        ...
    def get_aborting_depth(self) -> int:
        r"""Return the aborting depth if the value is ABORTED.
        
        """
        ...
    def get_addr(self) -> bool:
        r"""Return the address if the value is a constant (truncated to ADDRSIZE). 
                
        """
        ...
    def get_def_ea(self) -> ida_idaapi.ea_t:
        r"""Return the defining address.
        
        """
        ...
    def get_def_itype(self) -> int:
        r"""Return the defining instruction code (processor specific).
        
        """
        ...
    def get_num(self) -> bool:
        r"""Return the number if the value is a constant (truncated to SLOTSIZE). 
                
        """
        ...
    def get_spd(self) -> bool:
        r"""Return the SP delta if the value depends on the stack pointer (sign-extended to ADDRSIZE). 
                
        """
        ...
    def get_stride(self) -> int:
        r"""Return the loop stride of a NUMLOOP value. 
                
        """
        ...
    def has_any_vals_flag(self, val_flags: int) -> bool:
        ...
    def have_all_vals_flag(self, val_flags: int) -> bool:
        r"""Check the given flag for each value.
        
        """
        ...
    def is_all_vals_like_got(self) -> bool:
        ...
    def is_all_vals_pc_based(self) -> bool:
        ...
    def is_any_vals_had_delta(self) -> bool:
        ...
    def is_any_vals_like_got(self) -> bool:
        ...
    def is_any_vals_pc_based(self) -> bool:
        ...
    def is_badinsn(self) -> bool:
        r"""Return 'true' if the value is unknown because of a bad insn.
        
        """
        ...
    def is_dead_end(self) -> bool:
        r"""Return 'true' if the value is undefined because of a dead end.
        
        """
        ...
    def is_known(self) -> bool:
        r"""Return 'true' if the value is known (i.e. it is a number or SP delta).
        
        """
        ...
    def is_num(self) -> bool:
        r"""Return 'true' if the value is a constant.
        
        """
        ...
    def is_numloop(self) -> bool:
        r"""Return 'true' if the value is a number changed in a loop by adding a constant stride each iteration. 
                
        """
        ...
    def is_spd(self) -> bool:
        r"""Return 'true' if the value depends on the stack pointer.
        
        """
        ...
    def is_special(self) -> bool:
        r"""Return 'true' if the value requires special handling.
        
        """
        ...
    def is_unkfunc(self) -> bool:
        r"""Return 'true' if the value is unknown from the function start.
        
        """
        ...
    def is_unkinsn(self) -> bool:
        r"""Return 'true' if the value is unknown after executing the insn.
        
        """
        ...
    def is_unkloop(self) -> bool:
        r"""Return 'true' if the value is unknown because it changes in a loop.
        
        """
        ...
    def is_unkmult(self) -> bool:
        r"""Return 'true' if the value is unknown because the register has incompatible values (a number and SP delta). 
                
        """
        ...
    def is_unknown(self) -> bool:
        r"""Return 'true' if the value is unknown.
        
        """
        ...
    def is_unkvals(self) -> bool:
        r"""Return 'true' if the value is unknown because the register has too many values. 
                
        """
        ...
    def is_unkxref(self) -> bool:
        r"""Return 'true' if the value is unknown because there are too many xrefs.
        
        """
        ...
    def is_value_unique(self) -> bool:
        r"""Check that the value is unique.
        
        """
        ...
    @staticmethod
    def make_aborted(bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> reg_value_base_t:
        r"""Return the value after aborting. 
                
        """
        ...
    @staticmethod
    def make_badinsn(insn_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value after a bad insn. 
                
        """
        ...
    @staticmethod
    def make_dead_end(dead_end_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the undefined value because of a dead end. 
                
        """
        ...
    @staticmethod
    def make_initial_sp(func_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the value that is the initial stack pointer. 
                
        """
        ...
    @overload
    @staticmethod
    def make_num(rval: int, insn: insn_t, val_flags: int = 0) -> reg_value_base_t:
        r"""Return the value that is the RVAL number."""
        ...
    @overload
    @staticmethod
    def make_num(rval: int, val_ea: ida_idaapi.ea_t, val_flags: int = 0) -> reg_value_base_t:
        r"""Return the value that is the RVAL number."""
        ...
    @staticmethod
    def make_unkfunc(func_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value from the function start. 
                
        """
        ...
    @staticmethod
    def make_unkinsn(insn: insn_t) -> reg_value_base_t:
        r"""Return the unknown value after executing the insn. 
                
        """
        ...
    @staticmethod
    def make_unkloop(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if it changes in a loop. 
                
        """
        ...
    @staticmethod
    def make_unkmult(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if the register has incompatible values. 
                
        """
        ...
    @staticmethod
    def make_unkvals(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if the register has too many values. 
                
        """
        ...
    @staticmethod
    def make_unkxref(bblk_ea: ida_idaapi.ea_t) -> reg_value_base_t:
        r"""Return the unknown value if there are too many xrefs. 
                
        """
        ...
    def movt(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Replace the top 16 bits with bottom 16 bits of R, leaving the bottom 16 bits untouched. 
                
        """
        ...
    def neg(self, insn: insn_t) -> None:
        r"""Negate the value.
        
        """
        ...
    def sar(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift arithmetically the value right by R. 
                
        """
        ...
    def set_aborted(self, bblk_ea: ida_idaapi.ea_t, aborting_depth: int = -1) -> None:
        r"""Set the value after aborting. 
                
        """
        ...
    def set_all_vals_flag(self, val_flags: int) -> None:
        r"""Set the given flag for each value.
        
        """
        ...
    def set_all_vals_got_based(self) -> None:
        ...
    def set_all_vals_had_delta(self) -> None:
        ...
    def set_all_vals_pc_based(self) -> None:
        ...
    def set_badinsn(self, insn_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown after a bad insn. 
                
        """
        ...
    def set_context(self, _slotsize: int, _addrsize: int) -> None:
        r"""Set the context. 
                
        """
        ...
    def set_dead_end(self, dead_end_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be undefined because of a dead end. 
                
        """
        ...
    def set_def_itype_for_mov(self, insn: insn_t) -> bool:
        r"""Set the defining instruction The value of the destination register after the mov instruction is equal to the value of the source register before it. Therefore, we can consider this instruction as defining that value. 
                
        """
        ...
    @overload
    def set_num(self, rval: int, insn: insn_t, val_flags: int = 0) -> None:
        r"""Set the value to be a number after executing an insn."""
        ...
    @overload
    def set_num(self, rvals: uvalvec_t, insn: insn_t) -> None:
        r"""Set the value to be numbers after executing an insn."""
        ...
    @overload
    def set_num(self, rval: int, val_ea: ida_idaapi.ea_t, val_flags: int = 0) -> None:
        r"""Set the value to be a number before an address."""
        ...
    def set_numloop(self, loop_stride: int) -> None:
        r"""Turn a number into the NUMLOOP value: the register is changed in a loop by adding LOOP_STRIDE each iteration, VALS keeps the initial value(s). 
                
        """
        ...
    def set_unkfunc(self, func_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown from the function start. 
                
        """
        ...
    def set_unkinsn(self, insn: insn_t) -> None:
        r"""Set the value to be unknown after executing the insn. 
                
        """
        ...
    def set_unkloop(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because it changes in a loop. 
                
        """
        ...
    def set_unkmult(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because the register has incompatible values. 
                
        """
        ...
    def set_unkvals(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because the register has too many values. 
                
        """
        ...
    def set_unkxref(self, bblk_ea: ida_idaapi.ea_t) -> None:
        r"""Set the value to be unknown because there are too many xrefs. 
                
        """
        ...
    def shift_left(self, r: int) -> None:
        r"""Shift the value left by R. 
                
        """
        ...
    def shift_right(self, r: int, nbytes: int = 0) -> None:
        r"""Shift the value right by R. If NBYTES is non-zero, perform an arithmetic (signed) shift assuming the value is NBYTES bytes wide. 
                
        """
        ...
    def sll(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift the value left by R. 
                
        """
        ...
    def slr(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Shift logically the value right by R. 
                
        """
        ...
    def sub(self, r: reg_value_base_t, insn: insn_t) -> None:
        r"""Subtract R from the value. 
                
        """
        ...
    def swap(self, r: reg_value_base_t) -> None:
        ...
    def trunc_uval(self, pm: procmod_t) -> None:
        ...
    def truncate(self, width: int = 0) -> None:
        r"""Truncate the value to WIDTH (in bytes). For numbers: zero-truncate to WIDTH. For SP deltas: sign-extend to WIDTH. If WIDTH = 0, defaults to SLOTSIZE for numbers and ADDRSIZE for SP deltas. 
                
        """
        ...
    def vals_union(self, r: reg_value_base_t) -> set_compare_res_t:
        r"""Add values from R into THIS ignoring duplicates. 
                
        :returns: EQUAL: THIS is not changed
        :returns: CONTAINS: THIS is not changed
        :returns: CONTAINED: THIS is a copy of R
        :returns: NOT_COMPARABLE: values from R are added to THIS
        """
        ...

def find_nearest_rvi(rvi: reg_value_info_t, ea: ida_idaapi.ea_t, reg: Any) -> int:
    r"""Find the value of any of the two registers using the register tracker. First, this function tries to find the registers in the basic block of EA, and if it could not do this, then it tries to find in the entire function. 
            
    :param rvi: the found value with additional attributes
    :param ea: the address to find a value at
    :param reg: the registers to find
    :returns: the index of the found register or -1
    """
    ...

def find_op_value_info(rvi: reg_value_info_t, insn: insn_t, op: op_t, max_depth: int = 0) -> bool:
    r"""Find the value of an instruction operand using the register tracker. Works for register and stack-variable operands; returns 'false' for operands the tracker cannot turn into a tracked object. 
            
    :param rvi: the found value with additional attributes
    :param insn: the instruction owning the operand
    :param op: the operand to find a value of
    :param max_depth: as in find_regname_value_info()
    :returns: 'false': the processor module does not support a register tracker, or the operand cannot be tracked
    :returns: 'true': the found value is in RVI
    """
    ...

def find_reg_value(ea: ida_idaapi.ea_t, reg: int) -> int:
    r"""Find register value using the register tracker. 
            
    :param ea: the address to find a value at
    :param reg: the register to find
    :returns: 0: no value (the value is varying or the find depth is not enough to find a value)
    :returns: 1: the found value is in VAL
    :returns: -1: the processor module does not support a register tracker
    """
    ...

def find_reg_value_info(rvi: reg_value_info_t, ea: ida_idaapi.ea_t, reg: int, max_depth: int = 0) -> bool:
    r"""Find register value using the register tracker. 
            
    :param rvi: the found value with additional attributes
    :param ea: the address to find a value at
    :param reg: the register to find
    :param max_depth: the number of basic blocks to look before aborting the search and returning the unknown value. 0 means the value of REGTRACK_MAX_DEPTH from ida.cfg for ordinal registers or REGTRACK_FUNC_MAX_DEPTH for the function-wide registers, -1 means the value of REGTRACK_FUNC_MAX_DEPTH from ida.cfg.
    :returns: 'false': the processor module does not support a register tracker
    :returns: 'true': the found value is in RVI
    """
    ...

def find_regname_value_info(rvi: reg_value_info_t, ea: ida_idaapi.ea_t, regname: str, max_depth: int = 0) -> bool:
    r"""Find register value using the register tracker. 
            
    :param rvi: the found value with additional attributes
    :param ea: the address to find a value at
    :param regname: the name of the register to find
    :param max_depth: the number of basic blocks to look before aborting the search and returning the unknown value. 0 means the value of REGTRACK_MAX_DEPTH from ida.cfg for ordinal registers or REGTRACK_FUNC_MAX_DEPTH for the function-wide registers, -1 means the value of REGTRACK_FUNC_MAX_DEPTH from ida.cfg.
    :returns: 'false': the processor module does not support a register tracker
    :returns: 'true': the found value is in RVI
    """
    ...

def find_sp_value(ea: ida_idaapi.ea_t, reg: int = -1) -> sval_t:
    r"""Find a value of the SP based register using the register tracker. 
            
    :param ea: the address to find a value at
    :param reg: the register to find. by default the SP register is used.
    :returns: 0: no value (the value is varying or the find depth is not enough to find a value)
    :returns: 1: the found value is in VAL
    :returns: -1: the processor module does not support a register tracker
    """
    ...

def invalidate_regfinder_cache(*args: Any) -> None:
    r"""The control flow from FROM to TO has removed (CREF==fl_U) or added (CREF!=fl_U). Try to update the register tracker cache after this change. If TO == BADADDR then clear the entire cache. 
            
    """
    ...

def invalidate_regfinder_xrefs_cache(*args: Any) -> None:
    r"""The data reference to TO has added (DREF!=dr_O) or removed (DREF==dr_O). Update the regtracker xrefs cache after this change. If TO == BADADDR then clear the entire xrefs cache. 
            
    """
    ...

SWIG_PYTHON_LEGACY_BOOL: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
cvar: swigvarlink
ida_idaapi: module
weakref: module