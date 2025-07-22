# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111llll1111_opy_
from browserstack_sdk.bstack1l1ll11ll_opy_ import bstack1l1l11l111_opy_
def _111ll1lllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1ll1ll_opy_:
    def __init__(self, handler):
        self._111lll11111_opy_ = {}
        self._111ll1l11ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l11l111_opy_.version()
        if bstack111llll1111_opy_(pytest_version, bstack111l111_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᴭ")) >= 0:
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴮ")] = Module._register_setup_function_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴯ")] = Module._register_setup_module_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴰ")] = Class._register_setup_class_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴱ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴲ"))
            Module._register_setup_module_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴳ"))
            Class._register_setup_class_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴴ"))
            Class._register_setup_method_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴵ"))
        else:
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴶ")] = Module._inject_setup_function_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴷ")] = Module._inject_setup_module_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴸ")] = Class._inject_setup_class_fixture
            self._111lll11111_opy_[bstack111l111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴹ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴺ"))
            Module._inject_setup_module_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴻ"))
            Class._inject_setup_class_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴼ"))
            Class._inject_setup_method_fixture = self.bstack111ll1ll111_opy_(bstack111l111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴽ"))
    def bstack111ll1l1l11_opy_(self, bstack111ll1l1l1l_opy_, hook_type):
        bstack111ll1lll11_opy_ = id(bstack111ll1l1l1l_opy_.__class__)
        if (bstack111ll1lll11_opy_, hook_type) in self._111ll1l11ll_opy_:
            return
        meth = getattr(bstack111ll1l1l1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll1l11ll_opy_[(bstack111ll1lll11_opy_, hook_type)] = meth
            setattr(bstack111ll1l1l1l_opy_, hook_type, self.bstack111ll1llll1_opy_(hook_type, bstack111ll1lll11_opy_))
    def bstack111ll1l1lll_opy_(self, instance, bstack111ll1l11l1_opy_):
        if bstack111ll1l11l1_opy_ == bstack111l111_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᴾ"):
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᴿ"))
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᵀ"))
        if bstack111ll1l11l1_opy_ == bstack111l111_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᵁ"):
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᵂ"))
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᵃ"))
        if bstack111ll1l11l1_opy_ == bstack111l111_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᵄ"):
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᵅ"))
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᵆ"))
        if bstack111ll1l11l1_opy_ == bstack111l111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᵇ"):
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᵈ"))
            self.bstack111ll1l1l11_opy_(instance.obj, bstack111l111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᵉ"))
    @staticmethod
    def bstack111ll1ll11l_opy_(hook_type, func, args):
        if hook_type in [bstack111l111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᵊ"), bstack111l111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᵋ")]:
            _111ll1lllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll1llll1_opy_(self, hook_type, bstack111ll1lll11_opy_):
        def bstack111ll1lll1l_opy_(arg=None):
            self.handler(hook_type, bstack111l111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᵌ"))
            result = None
            try:
                bstack1llll1lllll_opy_ = self._111ll1l11ll_opy_[(bstack111ll1lll11_opy_, hook_type)]
                self.bstack111ll1ll11l_opy_(hook_type, bstack1llll1lllll_opy_, (arg,))
                result = Result(result=bstack111l111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᵍ"))
            except Exception as e:
                result = Result(result=bstack111l111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᵎ"), exception=e)
                self.handler(hook_type, bstack111l111_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᵏ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᵐ"), result)
        def bstack111lll1111l_opy_(this, arg=None):
            self.handler(hook_type, bstack111l111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᵑ"))
            result = None
            exception = None
            try:
                self.bstack111ll1ll11l_opy_(hook_type, self._111ll1l11ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack111l111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᵒ"))
            except Exception as e:
                result = Result(result=bstack111l111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᵓ"), exception=e)
                self.handler(hook_type, bstack111l111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᵔ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᵕ"), result)
        if hook_type in [bstack111l111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᵖ"), bstack111l111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᵗ")]:
            return bstack111lll1111l_opy_
        return bstack111ll1lll1l_opy_
    def bstack111ll1ll111_opy_(self, bstack111ll1l11l1_opy_):
        def bstack111ll1l1ll1_opy_(this, *args, **kwargs):
            self.bstack111ll1l1lll_opy_(this, bstack111ll1l11l1_opy_)
            self._111lll11111_opy_[bstack111ll1l11l1_opy_](this, *args, **kwargs)
        return bstack111ll1l1ll1_opy_