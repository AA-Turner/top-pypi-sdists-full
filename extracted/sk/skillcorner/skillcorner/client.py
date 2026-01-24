from fitrequest.fit_config import FitConfig

from skillcorner.config.class_config import class_config


class SkillcornerClient(FitConfig.from_dict(**class_config)): ...
