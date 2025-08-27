# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l111ll111_opy_
from browserstack_sdk.bstack11l11l1ll_opy_ import bstack1ll1ll1l11_opy_
def _111ll1l1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll111l1l_opy_:
    def __init__(self, handler):
        self._111ll11lll1_opy_ = {}
        self._111ll11l1ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll1ll1l11_opy_.version()
        if bstack11l111ll111_opy_(pytest_version, bstack1111lll_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᵳ")) >= 0:
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵴ")] = Module._register_setup_function_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵵ")] = Module._register_setup_module_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵶ")] = Class._register_setup_class_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵷ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵸ"))
            Module._register_setup_module_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵹ"))
            Class._register_setup_class_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵺ"))
            Class._register_setup_method_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵻ"))
        else:
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵼ")] = Module._inject_setup_function_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵽ")] = Module._inject_setup_module_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᵾ")] = Class._inject_setup_class_fixture
            self._111ll11lll1_opy_[bstack1111lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵿ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶀ"))
            Module._inject_setup_module_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶁ"))
            Class._inject_setup_class_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶂ"))
            Class._inject_setup_method_fixture = self.bstack111ll11ll1l_opy_(bstack1111lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶃ"))
    def bstack111ll1111ll_opy_(self, bstack111ll1l111l_opy_, hook_type):
        bstack111ll111ll1_opy_ = id(bstack111ll1l111l_opy_.__class__)
        if (bstack111ll111ll1_opy_, hook_type) in self._111ll11l1ll_opy_:
            return
        meth = getattr(bstack111ll1l111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11l1ll_opy_[(bstack111ll111ll1_opy_, hook_type)] = meth
            setattr(bstack111ll1l111l_opy_, hook_type, self.bstack111ll11l1l1_opy_(hook_type, bstack111ll111ll1_opy_))
    def bstack111ll111l11_opy_(self, instance, bstack111ll11l11l_opy_):
        if bstack111ll11l11l_opy_ == bstack1111lll_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᶄ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᶅ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᶆ"))
        if bstack111ll11l11l_opy_ == bstack1111lll_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᶇ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᶈ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᶉ"))
        if bstack111ll11l11l_opy_ == bstack1111lll_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶊ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᶋ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᶌ"))
        if bstack111ll11l11l_opy_ == bstack1111lll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᶍ"):
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᶎ"))
            self.bstack111ll1111ll_opy_(instance.obj, bstack1111lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᶏ"))
    @staticmethod
    def bstack111ll11ll11_opy_(hook_type, func, args):
        if hook_type in [bstack1111lll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶐ"), bstack1111lll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᶑ")]:
            _111ll1l1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll11l1l1_opy_(self, hook_type, bstack111ll111ll1_opy_):
        def bstack111ll1111l1_opy_(arg=None):
            self.handler(hook_type, bstack1111lll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᶒ"))
            result = None
            try:
                bstack1llllll1ll1_opy_ = self._111ll11l1ll_opy_[(bstack111ll111ll1_opy_, hook_type)]
                self.bstack111ll11ll11_opy_(hook_type, bstack1llllll1ll1_opy_, (arg,))
                result = Result(result=bstack1111lll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᶓ"))
            except Exception as e:
                result = Result(result=bstack1111lll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᶔ"), exception=e)
                self.handler(hook_type, bstack1111lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᶕ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111lll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᶖ"), result)
        def bstack111ll11llll_opy_(this, arg=None):
            self.handler(hook_type, bstack1111lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᶗ"))
            result = None
            exception = None
            try:
                self.bstack111ll11ll11_opy_(hook_type, self._111ll11l1ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᶘ"))
            except Exception as e:
                result = Result(result=bstack1111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶙ"), exception=e)
                self.handler(hook_type, bstack1111lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᶚ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᶛ"), result)
        if hook_type in [bstack1111lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᶜ"), bstack1111lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᶝ")]:
            return bstack111ll11llll_opy_
        return bstack111ll1111l1_opy_
    def bstack111ll11ll1l_opy_(self, bstack111ll11l11l_opy_):
        def bstack111ll11l111_opy_(this, *args, **kwargs):
            self.bstack111ll111l11_opy_(this, bstack111ll11l11l_opy_)
            self._111ll11lll1_opy_[bstack111ll11l11l_opy_](this, *args, **kwargs)
        return bstack111ll11l111_opy_