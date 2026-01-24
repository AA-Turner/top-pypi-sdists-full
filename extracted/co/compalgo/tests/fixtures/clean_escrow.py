"""
Clean PyTeal escrow contract with all P0 security checks
Should produce 0 violations when analyzed with algorand-baseline policy
"""
from pyteal import *


def clean_escrow():
    """
    Secure escrow contract demonstrating P0 compliance best practices
    
    Security features:
    - Admin sender verification on all privileged operations
    - RekeyTo == zero check
    - CloseRemainderTo == zero check
    - Transaction argument validation
    - Guarded state mutations
    - No unprotected inner transactions
    - Fee limits enforced
    """
    
    # Admin address check (example uses creator)
    is_admin = Txn.sender() == Global.creator_address()
    
    # Safe guards for account security
    safe_rekey = Txn.rekey_to() == Global.zero_address()
    safe_close = Txn.close_remainder_to() == Global.zero_address()
    safe_fee = Txn.fee() <= Int(2000)  # Max 2000 microALGO
    
    # Argument validation helper
    def validate_amount_arg():
        return And(
            Txn.application_args.length() > Int(0),
            Btoi(Txn.application_args[0]) > Int(0),
            Btoi(Txn.application_args[0]) <= Int(1000000),  # Max 1 ALGO
        )
    
    # On application creation
    on_create = Seq([
        App.globalPut(Bytes("owner"), Txn.sender()),
        App.globalPut(Bytes("balance"), Int(0)),
        Approve()
    ])
    
    # On application delete - SECURE: admin check
    on_delete = Seq([
        Assert(is_admin),  # ✅ Admin verification
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Approve()
    ])
    
    # On application update - SECURE: admin check
    on_update = Seq([
        Assert(is_admin),  # ✅ Admin verification
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Assert(validate_amount_arg()),  # ✅ Arg validation
        App.globalPut(Bytes("version"), Txn.application_args[0]),
        Approve()
    ])
    
    # NoOp call - deposit funds
    on_deposit = Seq([
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Assert(safe_fee),  # ✅ Fee limit
        Assert(validate_amount_arg()),  # ✅ Arg validation
        App.globalPut(
            Bytes("balance"),
            App.globalGet(Bytes("balance")) + Btoi(Txn.application_args[0])
        ),  # ✅ Guarded state mutation (validated args)
        Approve()
    ])
    
    # Admin-only withdrawal
    on_withdraw = Seq([
        Assert(is_admin),  # ✅ Admin verification
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Assert(validate_amount_arg()),  # ✅ Arg validation
        App.globalPut(
            Bytes("balance"),
            App.globalGet(Bytes("balance")) - Btoi(Txn.application_args[0])
        ),  # ✅ Guarded state mutation (admin only)
        Approve()
    ])
    
    # OptIn - allowed for all
    on_optin = Seq([
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Approve()
    ])
    
    # CloseOut - allowed for all
    on_closeout = Seq([
        Assert(safe_rekey),  # ✅ RekeyTo check
        Assert(safe_close),  # ✅ CloseRemainderTo check
        Approve()
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.DeleteApplication, on_delete],
        [Txn.on_completion() == OnComplete.UpdateApplication, on_update],
        [Txn.on_completion() == OnComplete.OptIn, on_optin],
        [Txn.on_completion() == OnComplete.CloseOut, on_closeout],
        # NoOp calls
        [And(
            Txn.on_completion() == OnComplete.NoOp,
            Txn.application_args[0] == Bytes("deposit")
        ), on_deposit],
        [And(
            Txn.on_completion() == OnComplete.NoOp,
            Txn.application_args[0] == Bytes("withdraw")
        ), on_withdraw],
    )
    
    return program


if __name__ == "__main__":
    print(compileTeal(clean_escrow(), mode=Mode.Application, version=8))
