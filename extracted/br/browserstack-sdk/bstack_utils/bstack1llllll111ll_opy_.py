# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111l1l111l_opy_
from browserstack_sdk.bstack11llll11ll_opy_ import bstack1lll1l111l_opy_
def _1llllll11111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lllll1lll1l_opy_:
    def __init__(self, handler):
        self._1llllll1111l_opy_ = {}
        self._1llllll11lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1lll1l111l_opy_.version()
        if bstack1111l1l111l_opy_(pytest_version, bstack1ll11_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢ∨")) >= 0:
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∩")] = Module._register_setup_function_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ∪")] = Module._register_setup_module_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ∫")] = Class._register_setup_class_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∬")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∭"))
            Module._register_setup_module_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ∮"))
            Class._register_setup_class_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ∯"))
            Class._register_setup_method_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ∰"))
        else:
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∱")] = Module._inject_setup_function_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∲")] = Module._inject_setup_module_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∳")] = Class._inject_setup_class_fixture
            self._1llllll1111l_opy_[bstack1ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ∴")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ∵"))
            Module._inject_setup_module_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∶"))
            Class._inject_setup_class_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∷"))
            Class._inject_setup_method_fixture = self.bstack1llllll1l11l_opy_(bstack1ll11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ∸"))
    def bstack1llllll111l1_opy_(self, bstack1llllll11l1l_opy_, hook_type):
        bstack1llllll11l11_opy_ = id(bstack1llllll11l1l_opy_.__class__)
        if (bstack1llllll11l11_opy_, hook_type) in self._1llllll11lll_opy_:
            return
        meth = getattr(bstack1llllll11l1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llllll11lll_opy_[(bstack1llllll11l11_opy_, hook_type)] = meth
            setattr(bstack1llllll11l1l_opy_, hook_type, self.bstack1lllll1lllll_opy_(hook_type, bstack1llllll11l11_opy_))
    def bstack1lllll1ll1ll_opy_(self, instance, bstack1lllll1llll1_opy_):
        if bstack1lllll1llll1_opy_ == bstack1ll11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ∹"):
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ∺"))
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ∻"))
        if bstack1lllll1llll1_opy_ == bstack1ll11_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ∼"):
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢ∽"))
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦ∾"))
        if bstack1lllll1llll1_opy_ == bstack1ll11_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ∿"):
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ≀"))
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ≁"))
        if bstack1lllll1llll1_opy_ == bstack1ll11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ≂"):
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨ≃"))
            self.bstack1llllll111l1_opy_(instance.obj, bstack1ll11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥ≄"))
    @staticmethod
    def bstack1lllll1ll1l1_opy_(hook_type, func, args):
        if hook_type in [bstack1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ≅"), bstack1ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ≆")]:
            _1llllll11111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lllll1lllll_opy_(self, hook_type, bstack1llllll11l11_opy_):
        def bstack1lllll1lll11_opy_(arg=None):
            self.handler(hook_type, bstack1ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ≇"))
            result = None
            try:
                bstack1ll111llll1_opy_ = self._1llllll11lll_opy_[(bstack1llllll11l11_opy_, hook_type)]
                self.bstack1lllll1ll1l1_opy_(hook_type, bstack1ll111llll1_opy_, (arg,))
                result = Result(result=bstack1ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ≈"))
            except Exception as e:
                result = Result(result=bstack1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭≉"), exception=e)
                self.handler(hook_type, bstack1ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭≊"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ≋"), result)
        def bstack1llllll1l111_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ≌"))
            result = None
            exception = None
            try:
                self.bstack1lllll1ll1l1_opy_(hook_type, self._1llllll11lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ≍"))
            except Exception as e:
                result = Result(result=bstack1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ≎"), exception=e)
                self.handler(hook_type, bstack1ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ≏"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ≐"), result)
        if hook_type in [bstack1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭≑"), bstack1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ≒")]:
            return bstack1llllll1l111_opy_
        return bstack1lllll1lll11_opy_
    def bstack1llllll1l11l_opy_(self, bstack1lllll1llll1_opy_):
        def bstack1llllll11ll1_opy_(this, *args, **kwargs):
            self.bstack1lllll1ll1ll_opy_(this, bstack1lllll1llll1_opy_)
            self._1llllll1111l_opy_[bstack1lllll1llll1_opy_](this, *args, **kwargs)
        return bstack1llllll11ll1_opy_