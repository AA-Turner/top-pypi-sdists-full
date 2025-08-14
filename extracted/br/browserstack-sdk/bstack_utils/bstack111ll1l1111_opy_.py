# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11ll1111_opy_
from browserstack_sdk.bstack1111l11ll_opy_ import bstack11111ll1l_opy_
def _111ll1l1l11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll111l1l_opy_:
    def __init__(self, handler):
        self._111ll11lll1_opy_ = {}
        self._111ll11l1l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11111ll1l_opy_.version()
        if bstack11l11ll1111_opy_(pytest_version, bstack1l1l1ll_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᶋ")) >= 0:
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶌ")] = Module._register_setup_function_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶍ")] = Module._register_setup_module_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶎ")] = Class._register_setup_class_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶏ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶐ"))
            Module._register_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶑ"))
            Class._register_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᶒ"))
            Class._register_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶓ"))
        else:
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᶔ")] = Module._inject_setup_function_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶕ")] = Module._inject_setup_module_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᶖ")] = Class._inject_setup_class_fixture
            self._111ll11lll1_opy_[bstack1l1l1ll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᶗ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᶘ"))
            Module._inject_setup_module_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶙ"))
            Class._inject_setup_class_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᶚ"))
            Class._inject_setup_method_fixture = self.bstack111ll111lll_opy_(bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᶛ"))
    def bstack111ll1l11ll_opy_(self, bstack111ll11l111_opy_, hook_type):
        bstack111ll1l11l1_opy_ = id(bstack111ll11l111_opy_.__class__)
        if (bstack111ll1l11l1_opy_, hook_type) in self._111ll11l1l1_opy_:
            return
        meth = getattr(bstack111ll11l111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11l1l1_opy_[(bstack111ll1l11l1_opy_, hook_type)] = meth
            setattr(bstack111ll11l111_opy_, hook_type, self.bstack111ll11llll_opy_(hook_type, bstack111ll1l11l1_opy_))
    def bstack111ll11l11l_opy_(self, instance, bstack111ll11ll1l_opy_):
        if bstack111ll11ll1l_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶜ"):
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᶝ"))
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᶞ"))
        if bstack111ll11ll1l_opy_ == bstack1l1l1ll_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᶟ"):
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᶠ"))
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᶡ"))
        if bstack111ll11ll1l_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᶢ"):
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᶣ"))
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᶤ"))
        if bstack111ll11ll1l_opy_ == bstack1l1l1ll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᶥ"):
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᶦ"))
            self.bstack111ll1l11ll_opy_(instance.obj, bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᶧ"))
    @staticmethod
    def bstack111ll11l1ll_opy_(hook_type, func, args):
        if hook_type in [bstack1l1l1ll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᶨ"), bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᶩ")]:
            _111ll1l1l11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll11llll_opy_(self, hook_type, bstack111ll1l11l1_opy_):
        def bstack111ll11ll11_opy_(arg=None):
            self.handler(hook_type, bstack1l1l1ll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᶪ"))
            result = None
            try:
                bstack1lllll1l1ll_opy_ = self._111ll11l1l1_opy_[(bstack111ll1l11l1_opy_, hook_type)]
                self.bstack111ll11l1ll_opy_(hook_type, bstack1lllll1l1ll_opy_, (arg,))
                result = Result(result=bstack1l1l1ll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᶫ"))
            except Exception as e:
                result = Result(result=bstack1l1l1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶬ"), exception=e)
                self.handler(hook_type, bstack1l1l1ll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᶭ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1ll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᶮ"), result)
        def bstack111ll111ll1_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1l1ll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᶯ"))
            result = None
            exception = None
            try:
                self.bstack111ll11l1ll_opy_(hook_type, self._111ll11l1l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1l1ll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᶰ"))
            except Exception as e:
                result = Result(result=bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᶱ"), exception=e)
                self.handler(hook_type, bstack1l1l1ll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᶲ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1l1ll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᶳ"), result)
        if hook_type in [bstack1l1l1ll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᶴ"), bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᶵ")]:
            return bstack111ll111ll1_opy_
        return bstack111ll11ll11_opy_
    def bstack111ll111lll_opy_(self, bstack111ll11ll1l_opy_):
        def bstack111ll1l111l_opy_(this, *args, **kwargs):
            self.bstack111ll11l11l_opy_(this, bstack111ll11ll1l_opy_)
            self._111ll11lll1_opy_[bstack111ll11ll1l_opy_](this, *args, **kwargs)
        return bstack111ll1l111l_opy_