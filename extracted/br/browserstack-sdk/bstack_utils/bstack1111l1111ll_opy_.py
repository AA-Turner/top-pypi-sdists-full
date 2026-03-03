# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l1l11l1l_opy_
from browserstack_sdk.bstack1ll111lll1_opy_ import bstack1l1l111l11_opy_
def _1111l111ll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111l1111l1_opy_:
    def __init__(self, handler):
        self._11111lll11l_opy_ = {}
        self._11111ll1lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l111l11_opy_.version()
        if bstack111l1l11l1l_opy_(pytest_version, bstack11ll111_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤΆ")) >= 0:
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᾼ")] = Module._register_setup_function_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᾽")] = Module._register_setup_module_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ι")] = Class._register_setup_class_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᾿")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ῀"))
            Module._register_setup_module_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ῁"))
            Class._register_setup_class_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪῂ"))
            Class._register_setup_method_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬῃ"))
        else:
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨῄ")] = Module._inject_setup_function_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ῅")] = Module._inject_setup_module_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧῆ")] = Class._inject_setup_class_fixture
            self._11111lll11l_opy_[bstack11ll111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩῇ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬῈ"))
            Module._inject_setup_module_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫΈ"))
            Class._inject_setup_class_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫῊ"))
            Class._inject_setup_method_fixture = self.bstack1111l111l1l_opy_(bstack11ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭Ή"))
    def bstack1111l11111l_opy_(self, bstack11111llllll_opy_, hook_type):
        bstack11111lll111_opy_ = id(bstack11111llllll_opy_.__class__)
        if (bstack11111lll111_opy_, hook_type) in self._11111ll1lll_opy_:
            return
        meth = getattr(bstack11111llllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11111ll1lll_opy_[(bstack11111lll111_opy_, hook_type)] = meth
            setattr(bstack11111llllll_opy_, hook_type, self.bstack11111lll1l1_opy_(hook_type, bstack11111lll111_opy_))
    def bstack11111lll1ll_opy_(self, instance, bstack1111l111l11_opy_):
        if bstack1111l111l11_opy_ == bstack11ll111_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤῌ"):
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣ῍"))
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ῎"))
        if bstack1111l111l11_opy_ == bstack11ll111_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ῏"):
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤῐ"))
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨῑ"))
        if bstack1111l111l11_opy_ == bstack11ll111_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧῒ"):
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦΐ"))
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣ῔"))
        if bstack1111l111l11_opy_ == bstack11ll111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ῕"):
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣῖ"))
            self.bstack1111l11111l_opy_(instance.obj, bstack11ll111_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧῗ"))
    @staticmethod
    def bstack1111l111111_opy_(hook_type, func, args):
        if hook_type in [bstack11ll111_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪῘ"), bstack11ll111_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧῙ")]:
            _1111l111ll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111lll1l1_opy_(self, hook_type, bstack11111lll111_opy_):
        def bstack11111llll11_opy_(arg=None):
            self.handler(hook_type, bstack11ll111_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭Ὶ"))
            result = None
            try:
                bstack1lll111ll11_opy_ = self._11111ll1lll_opy_[(bstack11111lll111_opy_, hook_type)]
                self.bstack1111l111111_opy_(hook_type, bstack1lll111ll11_opy_, (arg,))
                result = Result(result=bstack11ll111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧΊ"))
            except Exception as e:
                result = Result(result=bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ῜"), exception=e)
                self.handler(hook_type, bstack11ll111_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ῝"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ῞"), result)
        def bstack11111lllll1_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ῟"))
            result = None
            exception = None
            try:
                self.bstack1111l111111_opy_(hook_type, self._11111ll1lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll111_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬῠ"))
            except Exception as e:
                result = Result(result=bstack11ll111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ῡ"), exception=e)
                self.handler(hook_type, bstack11ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ῢ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll111_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧΰ"), result)
        if hook_type in [bstack11ll111_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨῤ"), bstack11ll111_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬῥ")]:
            return bstack11111lllll1_opy_
        return bstack11111llll11_opy_
    def bstack1111l111l1l_opy_(self, bstack1111l111l11_opy_):
        def bstack11111llll1l_opy_(this, *args, **kwargs):
            self.bstack11111lll1ll_opy_(this, bstack1111l111l11_opy_)
            self._11111lll11l_opy_[bstack1111l111l11_opy_](this, *args, **kwargs)
        return bstack11111llll1l_opy_