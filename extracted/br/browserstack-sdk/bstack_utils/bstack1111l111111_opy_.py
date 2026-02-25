# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l1111ll1_opy_
from browserstack_sdk.bstack1ll1lll11_opy_ import bstack11111111_opy_
def _11111lllll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11111llll11_opy_:
    def __init__(self, handler):
        self._11111lll11l_opy_ = {}
        self._1111l111lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11111111_opy_.version()
        if bstack111l1111ll1_opy_(pytest_version, bstack11l1l11_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧι")) >= 0:
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᾿")] = Module._register_setup_function_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ῀")] = Module._register_setup_module_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ῁")] = Class._register_setup_class_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫῂ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧῃ"))
            Module._register_setup_module_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ῄ"))
            Class._register_setup_class_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭῅"))
            Class._register_setup_method_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨῆ"))
        else:
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫῇ")] = Module._inject_setup_function_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪῈ")] = Module._inject_setup_module_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪΈ")] = Class._inject_setup_class_fixture
            self._11111lll11l_opy_[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬῊ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨΉ"))
            Module._inject_setup_module_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧῌ"))
            Class._inject_setup_class_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ῍"))
            Class._inject_setup_method_fixture = self.bstack1111l1111ll_opy_(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ῎"))
    def bstack11111llll1l_opy_(self, bstack1111l111l11_opy_, hook_type):
        bstack11111lll1ll_opy_ = id(bstack1111l111l11_opy_.__class__)
        if (bstack11111lll1ll_opy_, hook_type) in self._1111l111lll_opy_:
            return
        meth = getattr(bstack1111l111l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111l111lll_opy_[(bstack11111lll1ll_opy_, hook_type)] = meth
            setattr(bstack1111l111l11_opy_, hook_type, self.bstack1111l11111l_opy_(hook_type, bstack11111lll1ll_opy_))
    def bstack1111l111l1l_opy_(self, instance, bstack1111l111ll1_opy_):
        if bstack1111l111ll1_opy_ == bstack11l1l11_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ῏"):
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦῐ"))
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣῑ"))
        if bstack1111l111ll1_opy_ == bstack11l1l11_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨῒ"):
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧΐ"))
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤ῔"))
        if bstack1111l111ll1_opy_ == bstack11l1l11_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ῕"):
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢῖ"))
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦῗ"))
        if bstack1111l111ll1_opy_ == bstack11l1l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧῘ"):
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦῙ"))
            self.bstack11111llll1l_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣῚ"))
    @staticmethod
    def bstack11111lll1l1_opy_(hook_type, func, args):
        if hook_type in [bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ί"), bstack11l1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ῜")]:
            _11111lllll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111l11111l_opy_(self, hook_type, bstack11111lll1ll_opy_):
        def bstack11111llllll_opy_(arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ῝"))
            result = None
            try:
                bstack1ll1ll1l1ll_opy_ = self._1111l111lll_opy_[(bstack11111lll1ll_opy_, hook_type)]
                self.bstack11111lll1l1_opy_(hook_type, bstack1ll1ll1l1ll_opy_, (arg,))
                result = Result(result=bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ῞"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ῟"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫῠ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬῡ"), result)
        def bstack11111lll111_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧῢ"))
            result = None
            exception = None
            try:
                self.bstack11111lll1l1_opy_(hook_type, self._1111l111lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨΰ"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩῤ"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩῥ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪῦ"), result)
        if hook_type in [bstack11l1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫῧ"), bstack11l1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨῨ")]:
            return bstack11111lll111_opy_
        return bstack11111llllll_opy_
    def bstack1111l1111ll_opy_(self, bstack1111l111ll1_opy_):
        def bstack1111l1111l1_opy_(this, *args, **kwargs):
            self.bstack1111l111l1l_opy_(this, bstack1111l111ll1_opy_)
            self._11111lll11l_opy_[bstack1111l111ll1_opy_](this, *args, **kwargs)
        return bstack1111l1111l1_opy_