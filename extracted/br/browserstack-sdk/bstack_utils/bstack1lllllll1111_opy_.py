# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11111l1llll_opy_
from browserstack_sdk.bstack11l111ll11_opy_ import bstack111l1lll1l_opy_
def _1lllllll11ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lllllll11l1_opy_:
    def __init__(self, handler):
        self._1llllll1l111_opy_ = {}
        self._1llllll1ll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack111l1lll1l_opy_.version()
        if bstack11111l1llll_opy_(pytest_version, bstack1l1_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦ⇻")) >= 0:
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⇼")] = Module._register_setup_function_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⇽")] = Module._register_setup_module_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⇾")] = Class._register_setup_class_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⇿")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∀"))
            Module._register_setup_module_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∁"))
            Class._register_setup_class_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∂"))
            Class._register_setup_method_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ∃"))
        else:
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ∄")] = Module._inject_setup_function_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∅")] = Module._inject_setup_module_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∆")] = Class._inject_setup_class_fixture
            self._1llllll1l111_opy_[bstack1l1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ∇")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ∈"))
            Module._inject_setup_module_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∉"))
            Class._inject_setup_class_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∊"))
            Class._inject_setup_method_fixture = self.bstack1llllll11l1l_opy_(bstack1l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ∋"))
    def bstack1llllll1lll1_opy_(self, bstack1llllll1l11l_opy_, hook_type):
        bstack1llllll11ll1_opy_ = id(bstack1llllll1l11l_opy_.__class__)
        if (bstack1llllll11ll1_opy_, hook_type) in self._1llllll1ll11_opy_:
            return
        meth = getattr(bstack1llllll1l11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llllll1ll11_opy_[(bstack1llllll11ll1_opy_, hook_type)] = meth
            setattr(bstack1llllll1l11l_opy_, hook_type, self.bstack1llllll11l11_opy_(hook_type, bstack1llllll11ll1_opy_))
    def bstack1llllll1l1l1_opy_(self, instance, bstack1llllll11lll_opy_):
        if bstack1llllll11lll_opy_ == bstack1l1_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ∌"):
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ∍"))
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢ∎"))
        if bstack1llllll11lll_opy_ == bstack1l1_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ∏"):
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦ∐"))
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣ∑"))
        if bstack1llllll11lll_opy_ == bstack1l1_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ−"):
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨ∓"))
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥ∔"))
        if bstack1llllll11lll_opy_ == bstack1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ∕"):
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥ∖"))
            self.bstack1llllll1lll1_opy_(instance.obj, bstack1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢ∗"))
    @staticmethod
    def bstack1llllll1l1ll_opy_(hook_type, func, args):
        if hook_type in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ∘"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ∙")]:
            _1lllllll11ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1llllll11l11_opy_(self, hook_type, bstack1llllll11ll1_opy_):
        def bstack1llllll1ll1l_opy_(arg=None):
            self.handler(hook_type, bstack1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ√"))
            result = None
            try:
                bstack1ll1l111111_opy_ = self._1llllll1ll11_opy_[(bstack1llllll11ll1_opy_, hook_type)]
                self.bstack1llllll1l1ll_opy_(hook_type, bstack1ll1l111111_opy_, (arg,))
                result = Result(result=bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ∛"))
            except Exception as e:
                result = Result(result=bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ∜"), exception=e)
                self.handler(hook_type, bstack1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ∝"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ∞"), result)
        def bstack1llllll1llll_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭∟"))
            result = None
            exception = None
            try:
                self.bstack1llllll1l1ll_opy_(hook_type, self._1llllll1ll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ∠"))
            except Exception as e:
                result = Result(result=bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ∡"), exception=e)
                self.handler(hook_type, bstack1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ∢"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ∣"), result)
        if hook_type in [bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ∤"), bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ∥")]:
            return bstack1llllll1llll_opy_
        return bstack1llllll1ll1l_opy_
    def bstack1llllll11l1l_opy_(self, bstack1llllll11lll_opy_):
        def bstack1lllllll111l_opy_(this, *args, **kwargs):
            self.bstack1llllll1l1l1_opy_(this, bstack1llllll11lll_opy_)
            self._1llllll1l111_opy_[bstack1llllll11lll_opy_](this, *args, **kwargs)
        return bstack1lllllll111l_opy_