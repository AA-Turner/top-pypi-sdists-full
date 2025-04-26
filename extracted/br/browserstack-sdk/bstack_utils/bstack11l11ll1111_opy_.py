# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1lll11ll_opy_
from browserstack_sdk.bstack1ll1lll11l_opy_ import bstack1ll11l11ll_opy_
def _11l11l1ll11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11l1lll1_opy_:
    def __init__(self, handler):
        self._11l11ll1l11_opy_ = {}
        self._11l11ll11ll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll11l11ll_opy_.version()
        if bstack11l1lll11ll_opy_(pytest_version, bstack1l11lll_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧᯇ")) >= 0:
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯈ")] = Module._register_setup_function_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯉ")] = Module._register_setup_module_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯊ")] = Class._register_setup_class_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯋ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯌ"))
            Module._register_setup_module_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯍ"))
            Class._register_setup_class_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯎ"))
            Class._register_setup_method_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯏ"))
        else:
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯐ")] = Module._inject_setup_function_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯑ")] = Module._inject_setup_module_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯒ")] = Class._inject_setup_class_fixture
            self._11l11ll1l11_opy_[bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯓ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯔ"))
            Module._inject_setup_module_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯕ"))
            Class._inject_setup_class_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯖ"))
            Class._inject_setup_method_fixture = self.bstack11l11l1l11l_opy_(bstack1l11lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯗ"))
    def bstack11l11l1l1ll_opy_(self, bstack11l11ll1ll1_opy_, hook_type):
        bstack11l11l1llll_opy_ = id(bstack11l11ll1ll1_opy_.__class__)
        if (bstack11l11l1llll_opy_, hook_type) in self._11l11ll11ll_opy_:
            return
        meth = getattr(bstack11l11ll1ll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll11ll_opy_[(bstack11l11l1llll_opy_, hook_type)] = meth
            setattr(bstack11l11ll1ll1_opy_, hook_type, self.bstack11l11l1ll1l_opy_(hook_type, bstack11l11l1llll_opy_))
    def bstack11l11l1l1l1_opy_(self, instance, bstack11l11ll1lll_opy_):
        if bstack11l11ll1lll_opy_ == bstack1l11lll_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᯘ"):
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦᯙ"))
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᯚ"))
        if bstack11l11ll1lll_opy_ == bstack1l11lll_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᯛ"):
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧᯜ"))
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤᯝ"))
        if bstack11l11ll1lll_opy_ == bstack1l11lll_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᯞ"):
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢᯟ"))
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦᯠ"))
        if bstack11l11ll1lll_opy_ == bstack1l11lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᯡ"):
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦᯢ"))
            self.bstack11l11l1l1ll_opy_(instance.obj, bstack1l11lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣᯣ"))
    @staticmethod
    def bstack11l11ll1l1l_opy_(hook_type, func, args):
        if hook_type in [bstack1l11lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᯤ"), bstack1l11lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᯥ")]:
            _11l11l1ll11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11l1ll1l_opy_(self, hook_type, bstack11l11l1llll_opy_):
        def bstack11l11ll111l_opy_(arg=None):
            self.handler(hook_type, bstack1l11lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦ᯦ࠩ"))
            result = None
            try:
                bstack1lllllll1ll_opy_ = self._11l11ll11ll_opy_[(bstack11l11l1llll_opy_, hook_type)]
                self.bstack11l11ll1l1l_opy_(hook_type, bstack1lllllll1ll_opy_, (arg,))
                result = Result(result=bstack1l11lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᯧ"))
            except Exception as e:
                result = Result(result=bstack1l11lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᯨ"), exception=e)
                self.handler(hook_type, bstack1l11lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᯩ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11lll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᯪ"), result)
        def bstack11l11l1l111_opy_(this, arg=None):
            self.handler(hook_type, bstack1l11lll_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᯫ"))
            result = None
            exception = None
            try:
                self.bstack11l11ll1l1l_opy_(hook_type, self._11l11ll11ll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l11lll_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᯬ"))
            except Exception as e:
                result = Result(result=bstack1l11lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᯭ"), exception=e)
                self.handler(hook_type, bstack1l11lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᯮ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l11lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᯯ"), result)
        if hook_type in [bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᯰ"), bstack1l11lll_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᯱ")]:
            return bstack11l11l1l111_opy_
        return bstack11l11ll111l_opy_
    def bstack11l11l1l11l_opy_(self, bstack11l11ll1lll_opy_):
        def bstack11l11ll11l1_opy_(this, *args, **kwargs):
            self.bstack11l11l1l1l1_opy_(this, bstack11l11ll1lll_opy_)
            self._11l11ll1l11_opy_[bstack11l11ll1lll_opy_](this, *args, **kwargs)
        return bstack11l11ll11l1_opy_