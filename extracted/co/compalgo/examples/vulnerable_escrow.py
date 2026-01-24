"""
Example PyTeal escrow contract with P0 violations for testing
"""
from pyteal import *


def escrow_contract():
    # P0 Violations:
    # 1. DELETE_WITHOUT_ADMIN_CHECK - App.globalDel without Txn.sender() == admin
    # 2. REKEY_WITHOUT_ZERO_CHECK - No check for RekeyTo
    # 3. MISSING_ARG_VALIDATION - Txn.application_args not validated
    # 4. STATE_MUTATION_UNGUARDED - App.globalPut without authorization
    
    on_delete = Seq([
        App.globalDel(Bytes("owner")),  # VIOLATION: no admin check
        Approve()
    ])
    
    on_update = Seq([
        App.globalPut(Bytes("version"), Txn.application_args[0]),  # VIOLATION: no validation
        Approve()
    ])
    
    on_call = Seq([
        App.globalPut(Bytes("balance"), Btoi(Txn.application_args[0])),  # VIOLATION: unguarded state mutation
        Approve()
    ])
    
    # No RekeyTo check - VIOLATION
    
    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.NoOp, on_call],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
    )
    
    return program


if __name__ == "__main__":
    print(compileTeal(escrow_contract(), mode=Mode.Application, version=6))
