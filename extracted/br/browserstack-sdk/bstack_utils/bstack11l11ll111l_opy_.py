# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1llll1l1_opy_
from browserstack_sdk.bstack11l1111ll_opy_ import bstack1lll1111l_opy_
def _11l11ll1lll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11ll11ll_opy_:
    def __init__(self, handler):
        self._11l11ll1l1l_opy_ = {}
        self._11l11l1lll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1lll1111l_opy_.version()
        if bstack11l1llll1l1_opy_(pytest_version, bstack1llllll_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᯉ")) >= 0:
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯊ")] = Module._register_setup_function_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯋ")] = Module._register_setup_module_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯌ")] = Class._register_setup_class_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯍ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯎ"))
            Module._register_setup_module_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯏ"))
            Class._register_setup_class_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯐ"))
            Class._register_setup_method_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯑ"))
        else:
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯒ")] = Module._inject_setup_function_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯓ")] = Module._inject_setup_module_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯔ")] = Class._inject_setup_class_fixture
            self._11l11ll1l1l_opy_[bstack1llllll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯕ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯖ"))
            Module._inject_setup_module_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯗ"))
            Class._inject_setup_class_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯘ"))
            Class._inject_setup_method_fixture = self.bstack11l11l1ll1l_opy_(bstack1llllll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯙ"))
    def bstack11l11ll1l11_opy_(self, bstack11l11l1l111_opy_, hook_type):
        bstack11l11l1l1ll_opy_ = id(bstack11l11l1l111_opy_.__class__)
        if (bstack11l11l1l1ll_opy_, hook_type) in self._11l11l1lll1_opy_:
            return
        meth = getattr(bstack11l11l1l111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11l1lll1_opy_[(bstack11l11l1l1ll_opy_, hook_type)] = meth
            setattr(bstack11l11l1l111_opy_, hook_type, self.bstack11l11ll11l1_opy_(hook_type, bstack11l11l1l1ll_opy_))
    def bstack11l11l1llll_opy_(self, instance, bstack11l11ll1111_opy_):
        if bstack11l11ll1111_opy_ == bstack1llllll_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᯚ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᯛ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᯜ"))
        if bstack11l11ll1111_opy_ == bstack1llllll_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᯝ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᯞ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᯟ"))
        if bstack11l11ll1111_opy_ == bstack1llllll_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᯠ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᯡ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᯢ"))
        if bstack11l11ll1111_opy_ == bstack1llllll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᯣ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᯤ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1llllll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᯥ"))
    @staticmethod
    def bstack11l11ll1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack1llllll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᯦"), bstack1llllll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᯧ")]:
            _11l11ll1lll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11ll11l1_opy_(self, hook_type, bstack11l11l1l1ll_opy_):
        def bstack11l11l1l1l1_opy_(arg=None):
            self.handler(hook_type, bstack1llllll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᯨ"))
            result = None
            try:
                bstack1111l111ll_opy_ = self._11l11l1lll1_opy_[(bstack11l11l1l1ll_opy_, hook_type)]
                self.bstack11l11ll1ll1_opy_(hook_type, bstack1111l111ll_opy_, (arg,))
                result = Result(result=bstack1llllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᯩ"))
            except Exception as e:
                result = Result(result=bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᯪ"), exception=e)
                self.handler(hook_type, bstack1llllll_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᯫ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llllll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᯬ"), result)
        def bstack11l11l1ll11_opy_(this, arg=None):
            self.handler(hook_type, bstack1llllll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᯭ"))
            result = None
            exception = None
            try:
                self.bstack11l11ll1ll1_opy_(hook_type, self._11l11l1lll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1llllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᯮ"))
            except Exception as e:
                result = Result(result=bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᯯ"), exception=e)
                self.handler(hook_type, bstack1llllll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᯰ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llllll_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᯱ"), result)
        if hook_type in [bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ᯲࠭"), bstack1llllll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦ᯳ࠪ")]:
            return bstack11l11l1ll11_opy_
        return bstack11l11l1l1l1_opy_
    def bstack11l11l1ll1l_opy_(self, bstack11l11ll1111_opy_):
        def bstack11l11l1l11l_opy_(this, *args, **kwargs):
            self.bstack11l11l1llll_opy_(this, bstack11l11ll1111_opy_)
            self._11l11ll1l1l_opy_[bstack11l11ll1111_opy_](this, *args, **kwargs)
        return bstack11l11l1l11l_opy_