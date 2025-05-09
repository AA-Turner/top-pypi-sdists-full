# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l111l11_opy_
from browserstack_sdk.bstack1l1l1ll1ll_opy_ import bstack1ll11l11_opy_
def _11l11l1l111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11ll1l11_opy_:
    def __init__(self, handler):
        self._11l11l1l1ll_opy_ = {}
        self._11l11ll11ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll11l11_opy_.version()
        if bstack11l1l111l11_opy_(pytest_version, bstack11lll_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᯒ")) >= 0:
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯓ")] = Module._register_setup_function_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯔ")] = Module._register_setup_module_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯕ")] = Class._register_setup_class_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯖ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯗ"))
            Module._register_setup_module_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯘ"))
            Class._register_setup_class_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯙ"))
            Class._register_setup_method_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯚ"))
        else:
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯛ")] = Module._inject_setup_function_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯜ")] = Module._inject_setup_module_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯝ")] = Class._inject_setup_class_fixture
            self._11l11l1l1ll_opy_[bstack11lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯞ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯟ"))
            Module._inject_setup_module_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯠ"))
            Class._inject_setup_class_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯡ"))
            Class._inject_setup_method_fixture = self.bstack11l11l1ll1l_opy_(bstack11lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯢ"))
    def bstack11l11l1l11l_opy_(self, bstack11l11l11lll_opy_, hook_type):
        bstack11l11ll11l1_opy_ = id(bstack11l11l11lll_opy_.__class__)
        if (bstack11l11ll11l1_opy_, hook_type) in self._11l11ll11ll_opy_:
            return
        meth = getattr(bstack11l11l11lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll11ll_opy_[(bstack11l11ll11l1_opy_, hook_type)] = meth
            setattr(bstack11l11l11lll_opy_, hook_type, self.bstack11l11l1ll11_opy_(hook_type, bstack11l11ll11l1_opy_))
    def bstack11l11ll111l_opy_(self, instance, bstack11l11l11ll1_opy_):
        if bstack11l11l11ll1_opy_ == bstack11lll_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯣ"):
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᯤ"))
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᯥ"))
        if bstack11l11l11ll1_opy_ == bstack11lll_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧ᯦ࠥ"):
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᯧ"))
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᯨ"))
        if bstack11l11l11ll1_opy_ == bstack11lll_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᯩ"):
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᯪ"))
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᯫ"))
        if bstack11l11l11ll1_opy_ == bstack11lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯬ"):
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᯭ"))
            self.bstack11l11l1l11l_opy_(instance.obj, bstack11lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᯮ"))
    @staticmethod
    def bstack11l11ll1l1l_opy_(hook_type, func, args):
        if hook_type in [bstack11lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᯯ"), bstack11lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᯰ")]:
            _11l11l1l111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1ll11_opy_(self, hook_type, bstack11l11ll11l1_opy_):
        def bstack11l11l1llll_opy_(arg=None):
            self.handler(hook_type, bstack11lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᯱ"))
            result = None
            try:
                bstack111111l11l_opy_ = self._11l11ll11ll_opy_[(bstack11l11ll11l1_opy_, hook_type)]
                self.bstack11l11ll1l1l_opy_(hook_type, bstack111111l11l_opy_, (arg,))
                result = Result(result=bstack11lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪ᯲ࠧ"))
            except Exception as e:
                result = Result(result=bstack11lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᯳"), exception=e)
                self.handler(hook_type, bstack11lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ᯴"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ᯵"), result)
        def bstack11l11l1l1l1_opy_(this, arg=None):
            self.handler(hook_type, bstack11lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ᯶"))
            result = None
            exception = None
            try:
                self.bstack11l11ll1l1l_opy_(hook_type, self._11l11ll11ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᯷"))
            except Exception as e:
                result = Result(result=bstack11lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᯸"), exception=e)
                self.handler(hook_type, bstack11lll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭᯹"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ᯺"), result)
        if hook_type in [bstack11lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᯻"), bstack11lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ᯼")]:
            return bstack11l11l1l1l1_opy_
        return bstack11l11l1llll_opy_
    def bstack11l11l1ll1l_opy_(self, bstack11l11l11ll1_opy_):
        def bstack11l11ll1111_opy_(this, *args, **kwargs):
            self.bstack11l11ll111l_opy_(this, bstack11l11l11ll1_opy_)
            self._11l11l1l1ll_opy_[bstack11l11l11ll1_opy_](this, *args, **kwargs)
        return bstack11l11ll1111_opy_