# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111llllllll_opy_
from browserstack_sdk.bstack1l111llll1_opy_ import bstack11l1ll1ll1_opy_
def _111ll11l1l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll11l1ll_opy_:
    def __init__(self, handler):
        self._111ll111lll_opy_ = {}
        self._111ll11l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l1ll1ll1_opy_.version()
        if bstack111llllllll_opy_(pytest_version, bstack1111l1l_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦᵸ")) >= 0:
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵹ")] = Module._register_setup_function_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵺ")] = Module._register_setup_module_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵻ")] = Class._register_setup_class_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵼ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᵽ"))
            Module._register_setup_module_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵾ"))
            Class._register_setup_class_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵿ"))
            Class._register_setup_method_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶀ"))
        else:
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶁ")] = Module._inject_setup_function_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶂ")] = Module._inject_setup_module_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶃ")] = Class._inject_setup_class_fixture
            self._111ll111lll_opy_[bstack1111l1l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶄ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶅ"))
            Module._inject_setup_module_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶆ"))
            Class._inject_setup_class_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶇ"))
            Class._inject_setup_method_fixture = self.bstack111l1llll1l_opy_(bstack1111l1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶈ"))
    def bstack111ll111l1l_opy_(self, bstack111l1llllll_opy_, hook_type):
        bstack111ll11ll11_opy_ = id(bstack111l1llllll_opy_.__class__)
        if (bstack111ll11ll11_opy_, hook_type) in self._111ll11l11l_opy_:
            return
        meth = getattr(bstack111l1llllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11l11l_opy_[(bstack111ll11ll11_opy_, hook_type)] = meth
            setattr(bstack111l1llllll_opy_, hook_type, self.bstack111l1lllll1_opy_(hook_type, bstack111ll11ll11_opy_))
    def bstack111ll111111_opy_(self, instance, bstack111ll1111l1_opy_):
        if bstack111ll1111l1_opy_ == bstack1111l1l_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᶉ"):
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᶊ"))
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢᶋ"))
        if bstack111ll1111l1_opy_ == bstack1111l1l_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᶌ"):
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦᶍ"))
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣᶎ"))
        if bstack111ll1111l1_opy_ == bstack1111l1l_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᶏ"):
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨᶐ"))
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥᶑ"))
        if bstack111ll1111l1_opy_ == bstack1111l1l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦᶒ"):
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥᶓ"))
            self.bstack111ll111l1l_opy_(instance.obj, bstack1111l1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢᶔ"))
    @staticmethod
    def bstack111ll11111l_opy_(hook_type, func, args):
        if hook_type in [bstack1111l1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᶕ"), bstack1111l1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᶖ")]:
            _111ll11l1l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l1lllll1_opy_(self, hook_type, bstack111ll11ll11_opy_):
        def bstack111ll11l111_opy_(arg=None):
            self.handler(hook_type, bstack1111l1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᶗ"))
            result = None
            try:
                bstack1lllll1llll_opy_ = self._111ll11l11l_opy_[(bstack111ll11ll11_opy_, hook_type)]
                self.bstack111ll11111l_opy_(hook_type, bstack1lllll1llll_opy_, (arg,))
                result = Result(result=bstack1111l1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᶘ"))
            except Exception as e:
                result = Result(result=bstack1111l1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᶙ"), exception=e)
                self.handler(hook_type, bstack1111l1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᶚ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111l1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᶛ"), result)
        def bstack111ll111ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack1111l1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᶜ"))
            result = None
            exception = None
            try:
                self.bstack111ll11111l_opy_(hook_type, self._111ll11l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111l1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᶝ"))
            except Exception as e:
                result = Result(result=bstack1111l1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶞ"), exception=e)
                self.handler(hook_type, bstack1111l1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᶟ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111l1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᶠ"), result)
        if hook_type in [bstack1111l1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᶡ"), bstack1111l1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶢ")]:
            return bstack111ll111ll1_opy_
        return bstack111ll11l111_opy_
    def bstack111l1llll1l_opy_(self, bstack111ll1111l1_opy_):
        def bstack111ll111l11_opy_(this, *args, **kwargs):
            self.bstack111ll111111_opy_(this, bstack111ll1111l1_opy_)
            self._111ll111lll_opy_[bstack111ll1111l1_opy_](this, *args, **kwargs)
        return bstack111ll111l11_opy_