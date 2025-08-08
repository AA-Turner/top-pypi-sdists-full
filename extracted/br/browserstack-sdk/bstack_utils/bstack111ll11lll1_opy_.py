# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111lll1ll11_opy_
from browserstack_sdk.bstack11lllll11_opy_ import bstack1l1lll1l11_opy_
def _111ll1l1ll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1l11ll_opy_:
    def __init__(self, handler):
        self._111ll11ll1l_opy_ = {}
        self._111ll11l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1lll1l11_opy_.version()
        if bstack111lll1ll11_opy_(pytest_version, bstack1ll1ll_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᵽ")) >= 0:
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵾ")] = Module._register_setup_function_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵿ")] = Module._register_setup_module_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶀ")] = Class._register_setup_class_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶁ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶂ"))
            Module._register_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶃ"))
            Class._register_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶄ"))
            Class._register_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶅ"))
        else:
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶆ")] = Module._inject_setup_function_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶇ")] = Module._inject_setup_module_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶈ")] = Class._inject_setup_class_fixture
            self._111ll11ll1l_opy_[bstack1ll1ll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶉ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶊ"))
            Module._inject_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶋ"))
            Class._inject_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶌ"))
            Class._inject_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1ll1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶍ"))
    def bstack111ll11l111_opy_(self, bstack111ll1l1111_opy_, hook_type):
        bstack111ll1l11l1_opy_ = id(bstack111ll1l1111_opy_.__class__)
        if (bstack111ll1l11l1_opy_, hook_type) in self._111ll11l11l_opy_:
            return
        meth = getattr(bstack111ll1l1111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11l11l_opy_[(bstack111ll1l11l1_opy_, hook_type)] = meth
            setattr(bstack111ll1l1111_opy_, hook_type, self.bstack111ll1l1l11_opy_(hook_type, bstack111ll1l11l1_opy_))
    def bstack111ll11l1l1_opy_(self, instance, bstack111ll11llll_opy_):
        if bstack111ll11llll_opy_ == bstack1ll1ll_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶎ"):
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᶏ"))
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᶐ"))
        if bstack111ll11llll_opy_ == bstack1ll1ll_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᶑ"):
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᶒ"))
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᶓ"))
        if bstack111ll11llll_opy_ == bstack1ll1ll_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᶔ"):
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᶕ"))
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᶖ"))
        if bstack111ll11llll_opy_ == bstack1ll1ll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶗ"):
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᶘ"))
            self.bstack111ll11l111_opy_(instance.obj, bstack1ll1ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᶙ"))
    @staticmethod
    def bstack111ll11l1ll_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᶚ"), bstack1ll1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶛ")]:
            _111ll1l1ll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll1l1l11_opy_(self, hook_type, bstack111ll1l11l1_opy_):
        def bstack111ll1l1l1l_opy_(arg=None):
            self.handler(hook_type, bstack1ll1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᶜ"))
            result = None
            try:
                bstack1lllll1l111_opy_ = self._111ll11l11l_opy_[(bstack111ll1l11l1_opy_, hook_type)]
                self.bstack111ll11l1ll_opy_(hook_type, bstack1lllll1l111_opy_, (arg,))
                result = Result(result=bstack1ll1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᶝ"))
            except Exception as e:
                result = Result(result=bstack1ll1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶞ"), exception=e)
                self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᶟ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᶠ"), result)
        def bstack111ll1l111l_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᶡ"))
            result = None
            exception = None
            try:
                self.bstack111ll11l1ll_opy_(hook_type, self._111ll11l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᶢ"))
            except Exception as e:
                result = Result(result=bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶣ"), exception=e)
                self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᶤ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᶥ"), result)
        if hook_type in [bstack1ll1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᶦ"), bstack1ll1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᶧ")]:
            return bstack111ll1l111l_opy_
        return bstack111ll1l1l1l_opy_
    def bstack111ll111lll_opy_(self, bstack111ll11llll_opy_):
        def bstack111ll11ll11_opy_(this, *args, **kwargs):
            self.bstack111ll11l1l1_opy_(this, bstack111ll11llll_opy_)
            self._111ll11ll1l_opy_[bstack111ll11llll_opy_](this, *args, **kwargs)
        return bstack111ll11ll11_opy_