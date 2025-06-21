# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l111ll1_opy_
from browserstack_sdk.bstack11lll1111l_opy_ import bstack1l1l1l11_opy_
def _111lll11111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111lll111l1_opy_:
    def __init__(self, handler):
        self._111lll11l1l_opy_ = {}
        self._111lll111ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l1l11_opy_.version()
        if bstack11l1l111ll1_opy_(pytest_version, bstack1l1l1l1_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤ᳇")) >= 0:
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳈")] = Module._register_setup_function_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳉")] = Module._register_setup_module_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳊")] = Class._register_setup_class_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᳋")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᳌"))
            Module._register_setup_module_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᳍"))
            Class._register_setup_class_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᳎"))
            Class._register_setup_method_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᳏"))
        else:
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᳐")] = Module._inject_setup_function_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳑")] = Module._inject_setup_module_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳒")] = Class._inject_setup_class_fixture
            self._111lll11l1l_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳓")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩ᳔ࠬ"))
            Module._inject_setup_module_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨ᳕ࠫ"))
            Class._inject_setup_class_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨ᳖ࠫ"))
            Class._inject_setup_method_fixture = self.bstack111lll1ll11_opy_(bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ᳗࠭"))
    def bstack111lll11lll_opy_(self, bstack111lll1l11l_opy_, hook_type):
        bstack111lll1l1ll_opy_ = id(bstack111lll1l11l_opy_.__class__)
        if (bstack111lll1l1ll_opy_, hook_type) in self._111lll111ll_opy_:
            return
        meth = getattr(bstack111lll1l11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111lll111ll_opy_[(bstack111lll1l1ll_opy_, hook_type)] = meth
            setattr(bstack111lll1l11l_opy_, hook_type, self.bstack111lll11l11_opy_(hook_type, bstack111lll1l1ll_opy_))
    def bstack111lll1111l_opy_(self, instance, bstack111lll1lll1_opy_):
        if bstack111lll1lll1_opy_ == bstack1l1l1l1_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᳘"):
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮᳙ࠣ"))
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ᳚"))
        if bstack111lll1lll1_opy_ == bstack1l1l1l1_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ᳛"):
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤ᳜"))
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨ᳝"))
        if bstack111lll1lll1_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩ᳞ࠧ"):
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶ᳟ࠦ"))
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣ᳠"))
        if bstack111lll1lll1_opy_ == bstack1l1l1l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᳡"):
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤ᳢ࠣ"))
            self.bstack111lll11lll_opy_(instance.obj, bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨ᳣ࠧ"))
    @staticmethod
    def bstack111ll1lllll_opy_(hook_type, func, args):
        if hook_type in [bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦ᳤ࠪ"), bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪ᳥ࠧ")]:
            _111lll11111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111lll11l11_opy_(self, hook_type, bstack111lll1l1ll_opy_):
        def bstack111lll11ll1_opy_(arg=None):
            self.handler(hook_type, bstack1l1l1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ᳦࠭"))
            result = None
            try:
                bstack1llll1lllll_opy_ = self._111lll111ll_opy_[(bstack111lll1l1ll_opy_, hook_type)]
                self.bstack111ll1lllll_opy_(hook_type, bstack1llll1lllll_opy_, (arg,))
                result = Result(result=bstack1l1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪ᳧ࠧ"))
            except Exception as e:
                result = Result(result=bstack1l1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᳨"), exception=e)
                self.handler(hook_type, bstack1l1l1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᳩ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᳪ"), result)
        def bstack111lll1l111_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1l1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᳫ"))
            result = None
            exception = None
            try:
                self.bstack111ll1lllll_opy_(hook_type, self._111lll111ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᳬ"))
            except Exception as e:
                result = Result(result=bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ᳭࠭"), exception=e)
                self.handler(hook_type, bstack1l1l1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᳮ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᳯ"), result)
        if hook_type in [bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᳰ"), bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᳱ")]:
            return bstack111lll1l111_opy_
        return bstack111lll11ll1_opy_
    def bstack111lll1ll11_opy_(self, bstack111lll1lll1_opy_):
        def bstack111lll1ll1l_opy_(this, *args, **kwargs):
            self.bstack111lll1111l_opy_(this, bstack111lll1lll1_opy_)
            self._111lll11l1l_opy_[bstack111lll1lll1_opy_](this, *args, **kwargs)
        return bstack111lll1ll1l_opy_