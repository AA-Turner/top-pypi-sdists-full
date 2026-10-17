from .generated.contract import CONTRACT

SDK_POLICY = CONTRACT.get('sdkPolicy')
if not isinstance(SDK_POLICY, dict):
    raise RuntimeError(
        'Generated SDK contract is missing sdkPolicy. Run generate:all before building or using SDK source.'
    )
