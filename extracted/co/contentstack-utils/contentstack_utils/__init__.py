# pip install -r requirements.txt
# pytest --html=tests/report/test-report.html
# coverage report -m
# coverage html -d coveragereport
"""
__author__, __status__, __version__, __endpoint__ and __email__

`Your code has been rated at 10.00/10`
"""

from contentstack_utils.embedded.item_type import ItemType
from contentstack_utils.embedded.styletype import StyleType
from contentstack_utils.helper.metadata import Metadata
from contentstack_utils.helper.node_to_html import NodeToHtml
from contentstack_utils.render.options import Options
from contentstack_utils.utils import Utils
from contentstack_utils.gql import GQL
from contentstack_utils.automate import Automate
from contentstack_utils.entry_editable import addEditableTags, addTags, getTag

__all__ = (
"Utils",
"Options",
"Metadata",
"GQL",
"Automate",
"StyleType",
"ItemType",
"NodeToHtml",
"addEditableTags",
"addTags",
"getTag",
)

__title__ = 'contentstack_utils'
__author__ = 'contentstack'
__status__ = 'debug'
__version__ = '1.4.0'
__endpoint__ = 'cdn.contentstack.io'
__contact__ = 'support@contentstack.com'
