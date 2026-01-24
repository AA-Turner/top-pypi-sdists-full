from skillcorner.config.method_config_list import method_config_list
from skillcorner.pagination import paginated
from skillcorner.params_list import params_list

class_config = {
    'class_name': 'SkillcornerClient',
    'client_name': 'skillcorner',
    'base_url': 'https://skillcorner.com',
    'auth': {
        'username': {'env_name': 'SKILLCORNER_USERNAME'},
        'password': {'env_name': 'SKILLCORNER_PASSWORD'},
    },
    'method_decorators': [paginated, params_list],
    'method_docstring': (
        'Retrieve response from {endpoint} GET request.\n'
        'To learn more about it go to: https://skillcorner.com/api/docs/#{anchor}.'
    ),
    'family_name_templates': {'save': 'save_{base_name}'},
    'method_config_list': method_config_list,
}
