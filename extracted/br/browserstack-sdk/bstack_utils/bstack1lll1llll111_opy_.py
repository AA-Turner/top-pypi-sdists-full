# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1llll11ll1l1_opy_
from browserstack_sdk.bstack11l1111lll_opy_ import bstack1l111l1ll_opy_
def _1lll1lllll11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lll1lll1ll1_opy_:
    def __init__(self, handler):
        self._1lll1lll1l11_opy_ = {}
        self._1lll1lll1lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l111l1ll_opy_.version()
        if bstack1llll11ll1l1_opy_(pytest_version, bstack1ll1l11_opy_ (u"ࠨ࠸࠯࠳࠱࠵ࠧ⏻")) >= 0:
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⏼")] = Module._register_setup_function_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⏽")] = Module._register_setup_module_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⏾")] = Class._register_setup_class_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⏿")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␀"))
            Module._register_setup_module_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭␁"))
            Class._register_setup_class_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭␂"))
            Class._register_setup_method_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␃"))
        else:
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ␄")] = Module._inject_setup_function_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␅")] = Module._inject_setup_module_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␆")] = Class._inject_setup_class_fixture
            self._1lll1lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ␇")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␈"))
            Module._inject_setup_module_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␉"))
            Class._inject_setup_class_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␊"))
            Class._inject_setup_method_fixture = self.bstack1lll1lll1l1l_opy_(bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␋"))
    def bstack1lll1llll1l1_opy_(self, bstack1lll1lllllll_opy_, hook_type):
        bstack1lll1llll1ll_opy_ = id(bstack1lll1lllllll_opy_.__class__)
        if (bstack1lll1llll1ll_opy_, hook_type) in self._1lll1lll1lll_opy_:
            return
        meth = getattr(bstack1lll1lllllll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lll1lll1lll_opy_[(bstack1lll1llll1ll_opy_, hook_type)] = meth
            setattr(bstack1lll1lllllll_opy_, hook_type, self.bstack1lll1llllll1_opy_(hook_type, bstack1lll1llll1ll_opy_))
    def bstack1llll11111l1_opy_(self, instance, bstack1llll111111l_opy_):
        if bstack1llll111111l_opy_ == bstack1ll1l11_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ␌"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦ␍"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣ␎"))
        if bstack1llll111111l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ␏"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧ␐"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤ␑"))
        if bstack1llll111111l_opy_ == bstack1ll1l11_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ␒"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢ␓"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦ␔"))
        if bstack1llll111111l_opy_ == bstack1ll1l11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ␕"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦ␖"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1ll1l11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣ␗"))
    @staticmethod
    def bstack1llll1111111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1l11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭␘"), bstack1ll1l11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ␙")]:
            _1lll1lllll11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lll1llllll1_opy_(self, hook_type, bstack1lll1llll1ll_opy_):
        def bstack1lll1lllll1l_opy_(arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ␚"))
            result = None
            try:
                bstack1l1lll111ll_opy_ = self._1lll1lll1lll_opy_[(bstack1lll1llll1ll_opy_, hook_type)]
                self.bstack1llll1111111_opy_(hook_type, bstack1l1lll111ll_opy_, (arg,))
                result = Result(result=bstack1ll1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ␛"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ␜"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ␝"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ␞"), result)
        def bstack1llll11111ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ␟"))
            result = None
            exception = None
            try:
                self.bstack1llll1111111_opy_(hook_type, self._1lll1lll1lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1l11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ␠"))
            except Exception as e:
                result = Result(result=bstack1ll1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ␡"), exception=e)
                self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ␢"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ␣"), result)
        if hook_type in [bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫ␤"), bstack1ll1l11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨ␥")]:
            return bstack1llll11111ll_opy_
        return bstack1lll1lllll1l_opy_
    def bstack1lll1lll1l1l_opy_(self, bstack1llll111111l_opy_):
        def bstack1lll1llll11l_opy_(this, *args, **kwargs):
            self.bstack1llll11111l1_opy_(this, bstack1llll111111l_opy_)
            self._1lll1lll1l11_opy_[bstack1llll111111l_opy_](this, *args, **kwargs)
        return bstack1lll1llll11l_opy_