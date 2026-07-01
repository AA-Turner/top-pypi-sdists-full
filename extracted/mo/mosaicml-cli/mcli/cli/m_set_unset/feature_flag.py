""" helper for set and unset """
import logging
from typing import Optional

from mcli import config
from mcli.utils.utils_interactive import choose_one
from mcli.utils.utils_logging import FAIL, OK

logger = logging.getLogger(__name__)


def use_feature_flag(feature: Optional[str], activate: bool = True, **kwargs) -> int:
    del kwargs
    conf = config.MCLIConfig.load_config()
    available_features = conf.mcli_mode.available_feature_flags()
    available_features_str = [x.value for x in available_features]
    feature_flag: Optional[config.FeatureFlag] = None
    if feature:
        feature = feature.upper()
        if feature not in available_features_str:
            if not available_features_str:
                logger.error(f'{FAIL} You currently do not have access to any feature flags')
            else:
                feature_list = "\n- ".join([""] + available_features_str)
                logger.error(f'{FAIL} Unable to find feature flag: {feature}\n'
                             f'Available feature flags are:{feature_list}')

            return 1
        else:
            feature_flag = config.FeatureFlag[feature]

    if not available_features:
        logger.error(f'{FAIL} No feature flags available')
        return 1

    if feature_flag is None:
        feature_flag = choose_one(
            f'What feature would you like to {"enable" if activate else "disable"}?',
            options=available_features,
            formatter=lambda x: x.value,
        )

    assert feature_flag is not None
    if activate:
        logger.info(f'{OK} Activating Feature: {feature_flag.value}')
    else:
        logger.info(f'{OK} Deactivating Feature: {feature_flag.value}')
    conf.feature_flags[feature_flag.value] = activate
    conf.save_config()

    return 0
