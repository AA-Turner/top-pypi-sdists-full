from typing import List, Optional, Union

from deepteam.vulnerabilities import BaseVulnerability
from deepteam.attacks import BaseAttack
from deepteam.attacks.multi_turn.types import CallbackType
from deepteam.red_teamer import RedTeamer
from deepteam.frameworks import get_combined_framework_config, FrameworkType


def red_team(
    model_callback: CallbackType,
    vulnerabilities: Optional[List[BaseVulnerability]] = None,
    attacks: Optional[List[BaseAttack]] = None,
    frameworks: Optional[List[Union[str, FrameworkType]]] = None,
    attacks_per_vulnerability_type: int = 1,
    ignore_errors: bool = False,
    run_async: bool = True,
    max_concurrent: int = 10,
    target_purpose: Optional[str] = None,
):

    if frameworks:
        framework_config = get_combined_framework_config(frameworks)
        final_vulnerabilities = framework_config.vulnerabilities
        final_attacks = framework_config.attacks
    else:
        if not vulnerabilities or not attacks:
            raise ValueError(
                "Either 'frameworks' must be provided, or both 'vulnerabilities' and 'attacks' must be provided."
            )

        final_vulnerabilities = vulnerabilities
        final_attacks = attacks

    red_teamer = RedTeamer(
        async_mode=run_async,
        max_concurrent=max_concurrent,
        target_purpose=target_purpose,
    )
    risk_assessment = red_teamer.red_team(
        model_callback=model_callback,
        vulnerabilities=final_vulnerabilities,
        attacks=final_attacks,
        attacks_per_vulnerability_type=attacks_per_vulnerability_type,
        ignore_errors=ignore_errors,
    )
    return risk_assessment
