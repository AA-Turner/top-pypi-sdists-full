from enum import Enum

class ThresholdType(Enum):
    ANOMALY = "ANOMALY"
    RELATIVE = "RELATIVE"
    TIME_BASED = "TIME_BASED"
    ABSOLUTE = "ABSOLUTE"

    def display_name(self):
        return self.name


class RuleThresholdConfiguration:
    @property
    def type(self) -> ThresholdType:
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class AbsoluteThresholdConfig(RuleThresholdConfiguration):
    def __init__(self, config):
        self.config = config

    @property
    def type(self):
        return ThresholdType.ABSOLUTE


class AnomalyThresholdConfig(RuleThresholdConfiguration):
    def __init__(self, config):
        self.config = config

    @property
    def type(self):
        return ThresholdType.ANOMALY


class RelativeThresholdConfig(RuleThresholdConfiguration):
    def __init__(self, config, operational_config):
        self.config = config
        self.operational_config = operational_config

    @property
    def type(self):
        return ThresholdType.RELATIVE


class TimeBasedThresholdConfig(RuleThresholdConfiguration):
    def __init__(self, config):
        self.config = config

    @property
    def type(self):
        return ThresholdType.TIME_BASED


RuleLevelThresholdConfiguration = RuleThresholdConfiguration

def parse_rule_threshold_configuration(data: dict) -> RuleThresholdConfiguration:
    if not data:
        return None

    threshold_type = data.get("type")

    if threshold_type == "ABSOLUTE":
        return AbsoluteThresholdConfig(config=data.get("config"))

    if threshold_type == "ANOMALY":
        return AnomalyThresholdConfig(config=data.get("config"))

    if threshold_type == "RELATIVE":
        return RelativeThresholdConfig(
            config=data.get("config"),
            operational_config=data.get("operationalConfig"),
        )

    if threshold_type == "TIME_BASED":
        return TimeBasedThresholdConfig(config=data.get("config"))

    raise ValueError(f"Unsupported ThresholdType: {threshold_type}")

