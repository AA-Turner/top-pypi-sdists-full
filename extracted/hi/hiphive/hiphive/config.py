from hiphive.input_output.logging_tools import logger


logger = logger.getChild(__name__)

default_config = {
    'acoustic_sum_rules': True,
    'symprec': 1e-5,
    'length_scale': 0.1,
    'intprec': 1e-12,
    'standardize_prototype': True,
    'shell_tolerance': 1e-5,
    'max_number_constraint_elements': 1e8
    }


class Config(dict):
    def __init__(self, **kwargs):
        super().__init__(**default_config)
        if 'sum_rules' in kwargs:
            logger.warning('kw sum_rules deprecated.'
                           ' Use acoustic_sum_rules instead')
            kwargs['acoustic_sum_rules'] = kwargs['sum_rules']
            del kwargs['sum_rules']
        for k, v in kwargs.items():
            if k not in default_config:
                raise ValueError('{} is not a valid setting'.format(k))
            if not isinstance(v, type(default_config[k])):
                raise TypeError('Value {} of kw {} is not a valid type'
                                .format(v, k))
        super().update(kwargs)
