# pytest --html=tests/report/test-report.html 
# above command runs tests and test reports generates in tests/report location.
# nosetests --with-coverage --cover-html
# clean all the .pyc files
# find . -name \*.pyc -delete
# nosetests --with-coverage --cover-html
# pytest --cov=contentstack_utils
# pytest -v --cov=contentstack_utils --cov-report=html
# pytest --html=tests/report/test-report.html
from unittest import TestLoader, TestSuite

from .convert_style import TestConvertStyle
from .test_default_opt_others import TestDefaultOptOther
from .test_helper_node_to_html import TestHelperNodeToHtml
from .test_item_types import TestItemType
from .test_metadata import TestMetadata
from .test_option_render_mark import TestOptionRenderMark
from .test_render_default_options import TestRenderDefaultOption
from .test_render_options import TestRenderOption
from .test_style_type import TestStyleType
from .test_util_srte import TestSuperchargedUtils
from .test_utils import TestUtility


def all_tests():
    test_module_itemtype = TestLoader().loadTestsFromTestCase(TestItemType)
    test_module_metadata = TestLoader().loadTestsFromTestCase(TestMetadata)
    test_module_style_type = TestLoader().loadTestsFromTestCase(TestStyleType)
    test_module_utility = TestLoader().loadTestsFromTestCase(TestUtility)

    test_module_default_option = TestLoader().loadTestsFromTestCase(TestDefaultOptOther)
    test_module_node_to_html = TestLoader().loadTestsFromTestCase(TestHelperNodeToHtml)
    test_module_render_mark = TestLoader().loadTestsFromTestCase(TestOptionRenderMark)
    test_module_render_default_option = TestLoader().loadTestsFromTestCase(TestRenderDefaultOption)
    test_module_render_option = TestLoader().loadTestsFromTestCase(TestRenderOption)
    test_module_utils_srte = TestLoader().loadTestsFromTestCase(TestSuperchargedUtils)
    test_module_convert_style = TestLoader().loadTestsFromTestCase(TestConvertStyle)

    suite = TestSuite([
        test_module_itemtype,
        test_module_metadata,
        test_module_style_type,
        test_module_utility,
        test_module_default_option,
        test_module_node_to_html,
        test_module_render_mark,
        test_module_render_default_option,
        test_module_render_option,
        test_module_utils_srte,
        test_module_convert_style

    ])
