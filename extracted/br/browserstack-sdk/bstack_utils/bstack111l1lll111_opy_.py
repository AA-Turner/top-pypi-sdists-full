# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111lllll111_opy_
from browserstack_sdk.bstack11ll1l1l1l_opy_ import bstack1l11l11l1l_opy_
def _111l1ll1l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l1ll111l_opy_:
    def __init__(self, handler):
        self._111l1lllll1_opy_ = {}
        self._111l1llll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l11l11l1l_opy_.version()
        if bstack111lllll111_opy_(pytest_version, bstack1ll11ll_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣᵼ")) >= 0:
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵽ")] = Module._register_setup_function_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵾ")] = Module._register_setup_module_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵿ")] = Class._register_setup_class_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶀ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶁ"))
            Module._register_setup_module_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶂ"))
            Class._register_setup_class_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶃ"))
            Class._register_setup_method_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶄ"))
        else:
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶅ")] = Module._inject_setup_function_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶆ")] = Module._inject_setup_module_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶇ")] = Class._inject_setup_class_fixture
            self._111l1lllll1_opy_[bstack1ll11ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶈ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶉ"))
            Module._inject_setup_module_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶊ"))
            Class._inject_setup_class_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶋ"))
            Class._inject_setup_method_fixture = self.bstack111l1llllll_opy_(bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶌ"))
    def bstack111l1lll1l1_opy_(self, bstack111l1lll11l_opy_, hook_type):
        bstack111l1ll1l1l_opy_ = id(bstack111l1lll11l_opy_.__class__)
        if (bstack111l1ll1l1l_opy_, hook_type) in self._111l1llll11_opy_:
            return
        meth = getattr(bstack111l1lll11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l1llll11_opy_[(bstack111l1ll1l1l_opy_, hook_type)] = meth
            setattr(bstack111l1lll11l_opy_, hook_type, self.bstack111l1llll1l_opy_(hook_type, bstack111l1ll1l1l_opy_))
    def bstack111l1ll1ll1_opy_(self, instance, bstack111l1lll1ll_opy_):
        if bstack111l1lll1ll_opy_ == bstack1ll11ll_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᶍ"):
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᶎ"))
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᶏ"))
        if bstack111l1lll1ll_opy_ == bstack1ll11ll_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶐ"):
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣᶑ"))
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧᶒ"))
        if bstack111l1lll1ll_opy_ == bstack1ll11ll_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᶓ"):
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥᶔ"))
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢᶕ"))
        if bstack111l1lll1ll_opy_ == bstack1ll11ll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᶖ"):
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢᶗ"))
            self.bstack111l1lll1l1_opy_(instance.obj, bstack1ll11ll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦᶘ"))
    @staticmethod
    def bstack111ll111111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll11ll_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᶙ"), bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᶚ")]:
            _111l1ll1l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l1llll1l_opy_(self, hook_type, bstack111l1ll1l1l_opy_):
        def bstack111l1ll1lll_opy_(arg=None):
            self.handler(hook_type, bstack1ll11ll_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᶛ"))
            result = None
            try:
                bstack1lllll1l1l1_opy_ = self._111l1llll11_opy_[(bstack111l1ll1l1l_opy_, hook_type)]
                self.bstack111ll111111_opy_(hook_type, bstack1lllll1l1l1_opy_, (arg,))
                result = Result(result=bstack1ll11ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᶜ"))
            except Exception as e:
                result = Result(result=bstack1ll11ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᶝ"), exception=e)
                self.handler(hook_type, bstack1ll11ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᶞ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll11ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᶟ"), result)
        def bstack111l1ll11l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll11ll_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᶠ"))
            result = None
            exception = None
            try:
                self.bstack111ll111111_opy_(hook_type, self._111l1llll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll11ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᶡ"))
            except Exception as e:
                result = Result(result=bstack1ll11ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᶢ"), exception=e)
                self.handler(hook_type, bstack1ll11ll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᶣ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll11ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᶤ"), result)
        if hook_type in [bstack1ll11ll_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶥ"), bstack1ll11ll_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᶦ")]:
            return bstack111l1ll11l1_opy_
        return bstack111l1ll1lll_opy_
    def bstack111l1llllll_opy_(self, bstack111l1lll1ll_opy_):
        def bstack111l1ll11ll_opy_(this, *args, **kwargs):
            self.bstack111l1ll1ll1_opy_(this, bstack111l1lll1ll_opy_)
            self._111l1lllll1_opy_[bstack111l1lll1ll_opy_](this, *args, **kwargs)
        return bstack111l1ll11ll_opy_