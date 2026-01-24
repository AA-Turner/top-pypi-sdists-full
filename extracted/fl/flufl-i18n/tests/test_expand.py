from types import SimpleNamespace
from unittest.mock import patch

import pytest

from flufl.i18n._expand import expand
from flufl.i18n._substitute import Template


class FailingTemplateClass:
    def __init__(self, template):
        self.template = template

    def safe_substitute(self, *args, **kws):
        raise TypeError


def test_exception():
    with patch('flufl.i18n._expand.log.exception') as log:
        with pytest.raises(TypeError):
            expand('my-template', {}, FailingTemplateClass)
    log.assert_called_once_with('broken template: %s', 'my-template')


def test_trailing_dot_is_not_a_placeholder():
    # GL#12 - $foo.bar.baz. interpreted the trailing dot as part of the
    # placeholder, but it shouldn't be.
    expanded = expand('Me and $you.', dict(you='You'), Template)
    assert expanded == 'Me and You.'
