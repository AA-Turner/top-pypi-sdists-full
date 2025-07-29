# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11llllll_opy_
from browserstack_sdk.bstack11l11l111_opy_ import bstack11lll111l_opy_
def _111ll1lll1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1l11ll_opy_:
    def __init__(self, handler):
        self._111ll1ll1l1_opy_ = {}
        self._111ll1l1ll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11lll111l_opy_.version()
        if bstack11l11llllll_opy_(pytest_version, bstackl_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᴮ")) >= 0:
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴯ")] = Module._register_setup_function_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴰ")] = Module._register_setup_module_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴱ")] = Class._register_setup_class_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴲ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴳ"))
            Module._register_setup_module_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴴ"))
            Class._register_setup_class_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴵ"))
            Class._register_setup_method_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴶ"))
        else:
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴷ")] = Module._inject_setup_function_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴸ")] = Module._inject_setup_module_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴹ")] = Class._inject_setup_class_fixture
            self._111ll1ll1l1_opy_[bstackl_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴺ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴻ"))
            Module._inject_setup_module_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴼ"))
            Class._inject_setup_class_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴽ"))
            Class._inject_setup_method_fixture = self.bstack111ll1l1l1l_opy_(bstackl_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴾ"))
    def bstack111ll1lll11_opy_(self, bstack111ll1ll1ll_opy_, hook_type):
        bstack111ll1llll1_opy_ = id(bstack111ll1ll1ll_opy_.__class__)
        if (bstack111ll1llll1_opy_, hook_type) in self._111ll1l1ll1_opy_:
            return
        meth = getattr(bstack111ll1ll1ll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll1l1ll1_opy_[(bstack111ll1llll1_opy_, hook_type)] = meth
            setattr(bstack111ll1ll1ll_opy_, hook_type, self.bstack111ll1l1lll_opy_(hook_type, bstack111ll1llll1_opy_))
    def bstack111ll1lllll_opy_(self, instance, bstack111ll1ll11l_opy_):
        if bstack111ll1ll11l_opy_ == bstackl_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᴿ"):
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᵀ"))
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᵁ"))
        if bstack111ll1ll11l_opy_ == bstackl_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᵂ"):
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᵃ"))
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᵄ"))
        if bstack111ll1ll11l_opy_ == bstackl_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᵅ"):
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᵆ"))
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᵇ"))
        if bstack111ll1ll11l_opy_ == bstackl_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᵈ"):
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᵉ"))
            self.bstack111ll1lll11_opy_(instance.obj, bstackl_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᵊ"))
    @staticmethod
    def bstack111lll11111_opy_(hook_type, func, args):
        if hook_type in [bstackl_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᵋ"), bstackl_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᵌ")]:
            _111ll1lll1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll1l1lll_opy_(self, hook_type, bstack111ll1llll1_opy_):
        def bstack111ll1l1l11_opy_(arg=None):
            self.handler(hook_type, bstackl_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᵍ"))
            result = None
            try:
                bstack1llll1ll1ll_opy_ = self._111ll1l1ll1_opy_[(bstack111ll1llll1_opy_, hook_type)]
                self.bstack111lll11111_opy_(hook_type, bstack1llll1ll1ll_opy_, (arg,))
                result = Result(result=bstackl_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᵎ"))
            except Exception as e:
                result = Result(result=bstackl_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᵏ"), exception=e)
                self.handler(hook_type, bstackl_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᵐ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstackl_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᵑ"), result)
        def bstack111ll1ll111_opy_(this, arg=None):
            self.handler(hook_type, bstackl_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᵒ"))
            result = None
            exception = None
            try:
                self.bstack111lll11111_opy_(hook_type, self._111ll1l1ll1_opy_[hook_type], (this, arg))
                result = Result(result=bstackl_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵓ"))
            except Exception as e:
                result = Result(result=bstackl_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᵔ"), exception=e)
                self.handler(hook_type, bstackl_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᵕ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstackl_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᵖ"), result)
        if hook_type in [bstackl_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᵗ"), bstackl_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᵘ")]:
            return bstack111ll1ll111_opy_
        return bstack111ll1l1l11_opy_
    def bstack111ll1l1l1l_opy_(self, bstack111ll1ll11l_opy_):
        def bstack111ll1l111l_opy_(this, *args, **kwargs):
            self.bstack111ll1lllll_opy_(this, bstack111ll1ll11l_opy_)
            self._111ll1ll1l1_opy_[bstack111ll1ll11l_opy_](this, *args, **kwargs)
        return bstack111ll1l111l_opy_