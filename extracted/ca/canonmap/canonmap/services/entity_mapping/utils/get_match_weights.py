# canonmap/services/entity_mapper/get_match_weights.py

from typing import Dict, Optional
from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

def get_match_weights(
    user_weights: Optional[Dict[str, float]],
    use_semantic_search: bool
) -> Dict[str, float]:
    """
    Merge default matching weights with any user overrides, enforce that
    they sum to 1.0, and drop the semantic weight if use_semantic_search=False.

    Args:
        user_weights: partial dict of weights the user wants to override (values in [0,1])
        use_semantic_search: if False, semantic weight is forced to 0 and redistributed

    Returns:
        A dict with keys ['semantic','fuzzy','initial','keyword','phonetic'], values summing to 1.0.

    Raises:
        ValueError: if sum(user_weights) > 1.0
    """
    # 1) Defaults
    default_weights = {
        'semantic': 0.40,
        'fuzzy':    0.40,
        'initial':  0.10,
        'keyword':  0.05,
        'phonetic': 0.05,
    }

    # 2) Coerce missing user_weights → {}
    uw = dict(user_weights or {})

    # 3) Validate user's total
    total_user = sum(uw.values())
    if total_user > 1.0:
        logger.error("User-provided weights sum to %.2f, which exceeds the maximum allowed total of 1.0.")     
        raise ValueError(f"User-provided weights sum to {total_user:.2f}, which exceeds the maximum allowed total of 1.0. Please adjust user-provided weights so they sum to 1.0 or less.")

    # 4) Determine which defaults to use
    if not use_semantic_search:
        # warn and drop any user semantic weight
        if uw.get('semantic', 0.0) > 0:
            logger.warning(
                "use_semantic_search=False, dropping user semantic weight %.2f",
                uw['semantic']
            )
        uw.pop('semantic', None)
        effective_defaults = {k: v for k, v in default_weights.items() if k != 'semantic'}
    else:
        effective_defaults = default_weights.copy()

    # 5) Build final weight dict
    #   a) preserve any user‐provided keys exactly
    weights: Dict[str, float] = {k: v for k, v in uw.items()}

    #   b) compute remaining mass
    remaining = 1.0 - sum(weights.values())

    #   c) distribute remaining across the unset keys proportionally
    #      to their default share
    rest_keys = [k for k in effective_defaults if k not in weights]
    sum_rest_defaults = sum(effective_defaults[k] for k in rest_keys) or 1.0
    for k in rest_keys:
        weights[k] = effective_defaults[k] / sum_rest_defaults * remaining

    #   d) if semantic disabled, force it to 0.0
    if not use_semantic_search:
        weights['semantic'] = 0.0

    # 6) Final sanity check & logging
    total_final = sum(weights.values())
    if not abs(total_final - 1.0) < 1e-6:
        logger.warning("Final weights sum to %.4f (adjusting rounding)", total_final)
        # renormalize as a last resort
        for k in weights:
            weights[k] = weights[k] / total_final

    logger.info("Final merged weights (sum≈1.0): %s", weights)
    return weights