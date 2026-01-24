from collections.abc import Callable

from fitrequest.decorators import hybrid_syntax


@hybrid_syntax
def greetings(name: str = 'toto') -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> str:
            return f'Hi {name}! {func(*args, **kwargs)}'

        return wrapper

    return decorator


@greetings
def ca_va() -> str:
    return 'How are you ?'


@greetings()
def age() -> str:
    return 'How old are you ?'


@greetings(name='Peter')
def hungry() -> str:
    return 'Are you hungry ?'


def test_hybrid_syntax():
    assert ca_va() == 'Hi toto! How are you ?'
    assert age() == 'Hi toto! How old are you ?'
    assert hungry() == 'Hi Peter! Are you hungry ?'
