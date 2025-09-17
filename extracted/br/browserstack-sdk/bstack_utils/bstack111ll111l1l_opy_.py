# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11l11l11_opy_
from browserstack_sdk.bstack1111l11l1_opy_ import bstack1ll11l1l11_opy_
def _111l1llll1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll11l1ll_opy_:
    def __init__(self, handler):
        self._111ll11l11l_opy_ = {}
        self._111ll111111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll11l1l11_opy_.version()
        if bstack11l11l11l11_opy_(pytest_version, bstack1l11ll1_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᵶ")) >= 0:
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵷ")] = Module._register_setup_function_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵸ")] = Module._register_setup_module_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵹ")] = Class._register_setup_class_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵺ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵻ"))
            Module._register_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵼ"))
            Class._register_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵽ"))
            Class._register_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵾ"))
        else:
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵿ")] = Module._inject_setup_function_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶀ")] = Module._inject_setup_module_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶁ")] = Class._inject_setup_class_fixture
            self._111ll11l11l_opy_[bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶂ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶃ"))
            Module._inject_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶄ"))
            Class._inject_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶅ"))
            Class._inject_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1l11ll1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶆ"))
    def bstack111ll1111ll_opy_(self, bstack111l1llllll_opy_, hook_type):
        bstack111ll11l111_opy_ = id(bstack111l1llllll_opy_.__class__)
        if (bstack111ll11l111_opy_, hook_type) in self._111ll111111_opy_:
            return
        meth = getattr(bstack111l1llllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll111111_opy_[(bstack111ll11l111_opy_, hook_type)] = meth
            setattr(bstack111l1llllll_opy_, hook_type, self.bstack111ll111l11_opy_(hook_type, bstack111ll11l111_opy_))
    def bstack111ll11l1l1_opy_(self, instance, bstack111l1llll11_opy_):
        if bstack111l1llll11_opy_ == bstack1l11ll1_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶇ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᶈ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᶉ"))
        if bstack111l1llll11_opy_ == bstack1l11ll1_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᶊ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᶋ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᶌ"))
        if bstack111l1llll11_opy_ == bstack1l11ll1_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᶍ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᶎ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᶏ"))
        if bstack111l1llll11_opy_ == bstack1l11ll1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶐ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᶑ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1l11ll1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᶒ"))
    @staticmethod
    def bstack111ll1111l1_opy_(hook_type, func, args):
        if hook_type in [bstack1l11ll1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᶓ"), bstack1l11ll1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶔ")]:
            _111l1llll1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll111l11_opy_(self, hook_type, bstack111ll11l111_opy_):
        def bstack111l1lllll1_opy_(arg=None):
            self.handler(hook_type, bstack1l11ll1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᶕ"))
            result = None
            try:
                bstack1lllll11111_opy_ = self._111ll111111_opy_[(bstack111ll11l111_opy_, hook_type)]
                self.bstack111ll1111l1_opy_(hook_type, bstack1lllll11111_opy_, (arg,))
                result = Result(result=bstack1l11ll1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᶖ"))
            except Exception as e:
                result = Result(result=bstack1l11ll1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶗ"), exception=e)
                self.handler(hook_type, bstack1l11ll1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᶘ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11ll1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᶙ"), result)
        def bstack111ll111ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack1l11ll1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᶚ"))
            result = None
            exception = None
            try:
                self.bstack111ll1111l1_opy_(hook_type, self._111ll111111_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᶛ"))
            except Exception as e:
                result = Result(result=bstack1l11ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶜ"), exception=e)
                self.handler(hook_type, bstack1l11ll1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᶝ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11ll1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᶞ"), result)
        if hook_type in [bstack1l11ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᶟ"), bstack1l11ll1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᶠ")]:
            return bstack111ll111ll1_opy_
        return bstack111l1lllll1_opy_
    def bstack111ll111lll_opy_(self, bstack111l1llll11_opy_):
        def bstack111ll11111l_opy_(this, *args, **kwargs):
            self.bstack111ll11l1l1_opy_(this, bstack111l1llll11_opy_)
            self._111ll11l11l_opy_[bstack111l1llll11_opy_](this, *args, **kwargs)
        return bstack111ll11111l_opy_