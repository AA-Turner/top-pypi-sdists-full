import pytest

from fitrequest.templating import jinja_env


@pytest.mark.parametrize(
    ('template', 'env', 'expected'),
    [
        ('hello {name}', {'name': 'toto'}, 'hello toto'),
        ('hello {name}', {}, 'hello {name}'),
        (
            'hello {name}, do you want to {action}?',
            {'name': 'toto', 'action': 'play'},
            'hello toto, do you want to play?',
        ),
        ('hello {name}, do you want to {action}?', {'name': 'toto'}, 'hello toto, do you want to {action}?'),
        ('hello {name}, do you want to {action}?', {'action': 'play'}, 'hello {name}, do you want to play?'),
        ('hello {name}, do you want to {action}?', {}, 'hello {name}, do you want to {action}?'),
        ('hello {name}, do you want to {action}?', {'day': 'monday'}, 'hello {name}, do you want to {action}?'),
    ],
)
def test_render(template, env, expected):
    assert jinja_env.from_string(template).render(**env) == expected
