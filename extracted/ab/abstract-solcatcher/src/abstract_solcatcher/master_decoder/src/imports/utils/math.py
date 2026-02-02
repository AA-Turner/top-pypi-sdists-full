from .imports import *
from .bignumber import *
def derive_token_decimals_from_reserves(
    virtual_sol_reserves: int,
    virtual_token_reserves: int,
) -> int:
    """
    Derive token decimals by comparing reserve ratios.
    
    TypeScript equivalent: deriveTokenDecimals()
    
    Note: Pump.fun always uses 6 decimals, so this is mainly for
    verification or non-pump.fun tokens.
    """
    if virtual_sol_reserves <= 0 or virtual_token_reserves <= 0:
        return PUMPFUN_TOKEN_DECIMALS
    
    ratio = virtual_token_reserves / virtual_sol_reserves
    magnitude_diff = math.log10(ratio) - math.log10(SOL_LAMPORTS)
    derived_decimals = round(magnitude_diff + SOL_DECIMALS)
    
    # For pump.fun, always return 6 (their standard)
    # Derivation is approximate due to virtual reserve constants
    return PUMPFUN_TOKEN_DECIMALS


def derive_token_decimals(
    token_amount: BN,
    virtual_token_reserves: BN,
    price: BN,
    sol_decimals: int = 9,
) -> int:
    """
    Derives token decimals given token amount, virtual reserves, and price.
    
    TypeScript equivalent: derive_token_decimals()
    """
    if token_amount.lte(0) or virtual_token_reserves.lte(0) or price.lte(0):
        raise ValueError("All inputs must be positive.")
    
    derived_token_amount = virtual_token_reserves.divided_by(price)
    ratio = derived_token_amount.divided_by(token_amount)
    
    decimals = 0
    epsilon = BN(1e-9)
    
    while ratio.minus(ratio.integer_value()).abs().gt(epsilon) and decimals < 18:
        ratio = ratio.multiplied_by(10)
        decimals += 1
    
    return decimals


def derive_price(sol_reserves: BN, token_reserves: BN) -> BN:
    """
    Derives price given SOL and token reserves.
    
    TypeScript equivalent: derive_price()
    """
    if token_reserves.is_zero():
        raise ValueError("Invalid reserves for price calculation.")
    
    return sol_reserves.divided_by(token_reserves)


def get_ui_price(amount: BN, decimals: int) -> Optional[BN]:
    """
    Calculates the UI price based on amount and decimals.
    
    TypeScript equivalent: getUiPrice()
    """
    decimals = -int(decimals)
    try:
        return amount.multiplied_by(BN(10).pow(decimals))
    except Exception as e:
        print(f"Error in get_ui_price: {e}")
        return None
