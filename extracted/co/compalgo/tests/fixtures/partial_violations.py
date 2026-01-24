"""
PyTeal contract with partial security violations (2-3 violations)
Used for testing that rule engine detects specific issues
"""
from pyteal import *


def partial_violations_contract():
    """
    Contract with some security checks but missing others
    
    Expected violations:
    - REKEY_NOT_ZERO (missing RekeyTo check)
    - MISSING_ARG_VALIDATION (args not validated)
    - Maybe STATE_MUTATION_UNGUARDED (depending on interpretation)
    """
    
    # Admin check is present ✅
    is_admin = Txn.sender() == Global.creator_address()
    
    # CloseRemainderTo check is present ✅
    safe_close = Txn.close_remainder_to() == Global.zero_address()
    
    # BUT: No RekeyTo check ❌
    # BUT: No arg validation ❌
    
    on_create = Seq([
        App.globalPut(Bytes("owner"), Txn.sender()),
        Approve()
    ])
    
    # Delete has admin check ✅
    on_delete = Seq([
        Assert(is_admin),  # ✅ GOOD
        Assert(safe_close),  # ✅ GOOD
        # ❌ MISSING: RekeyTo check
        Approve()
    ])
    
    # Update has admin check ✅
    on_update = Seq([
        Assert(is_admin),  # ✅ GOOD
        Assert(safe_close),  # ✅ GOOD
        # ❌ MISSING: RekeyTo check
        # ❌ MISSING: Arg validation
        App.globalPut(Bytes("version"), Txn.application_args[0]),
        Approve()
    ])
    
    # NoOp call - has some checks
    on_call = Seq([
        Assert(safe_close),  # ✅ GOOD
        # ❌ MISSING: RekeyTo check
        # ❌ MISSING: Arg validation (using raw args)
        App.globalPut(Bytes("data"), Txn.application_args[0]),
        Approve()
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
    )
    
    return program


if __name__ == "__main__":
    print(compileTeal(partial_violations_contract(), mode=Mode.Application, version=8))
