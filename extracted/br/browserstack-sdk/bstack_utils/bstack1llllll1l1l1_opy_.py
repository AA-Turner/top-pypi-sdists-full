# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111111llll1_opy_
from browserstack_sdk.bstack1111ll111_opy_ import bstack1l11111l_opy_
def _1llllll111l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lllll1lll1l_opy_:
    def __init__(self, handler):
        self._1lllll1lllll_opy_ = {}
        self._1lllll1llll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l11111l_opy_.version()
        if bstack111111llll1_opy_(pytest_version, bstack1ll1lll_opy_ (u"ࠧ࠾࠮࠲࠰࠴ࠦ∗")) >= 0:
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∘")] = Module._register_setup_function_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ∙")] = Module._register_setup_module_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ√")] = Class._register_setup_class_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ∛")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∜"))
            Module._register_setup_module_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∝"))
            Class._register_setup_class_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ∞"))
            Class._register_setup_method_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ∟"))
        else:
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ∠")] = Module._inject_setup_function_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∡")] = Module._inject_setup_module_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ∢")] = Class._inject_setup_class_fixture
            self._1lllll1lllll_opy_[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ∣")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ∤"))
            Module._inject_setup_module_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∥"))
            Class._inject_setup_class_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭∦"))
            Class._inject_setup_method_fixture = self.bstack1llllll11l1l_opy_(bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ∧"))
    def bstack1llllll1l111_opy_(self, bstack1llllll1111l_opy_, hook_type):
        bstack1llllll11l11_opy_ = id(bstack1llllll1111l_opy_.__class__)
        if (bstack1llllll11l11_opy_, hook_type) in self._1lllll1llll1_opy_:
            return
        meth = getattr(bstack1llllll1111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lllll1llll1_opy_[(bstack1llllll11l11_opy_, hook_type)] = meth
            setattr(bstack1llllll1111l_opy_, hook_type, self.bstack1llllll1l1ll_opy_(hook_type, bstack1llllll11l11_opy_))
    def bstack1llllll1l11l_opy_(self, instance, bstack1llllll11ll1_opy_):
        if bstack1llllll11ll1_opy_ == bstack1ll1lll_opy_ (u"ࠣࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ∨"):
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ∩"))
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢ∪"))
        if bstack1llllll11ll1_opy_ == bstack1ll1lll_opy_ (u"ࠦࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ∫"):
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠦ∬"))
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠣ∭"))
        if bstack1llllll11ll1_opy_ == bstack1ll1lll_opy_ (u"ࠢࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ∮"):
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸࠨ∯"))
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠥ∰"))
        if bstack1llllll11ll1_opy_ == bstack1ll1lll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠦ∱"):
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠥ∲"))
            self.bstack1llllll1l111_opy_(instance.obj, bstack1ll1lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠢ∳"))
    @staticmethod
    def bstack1llllll11111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1lll_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ∴"), bstack1ll1lll_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ∵")]:
            _1llllll111l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1llllll1l1ll_opy_(self, hook_type, bstack1llllll11l11_opy_):
        def bstack1lllll1lll11_opy_(arg=None):
            self.handler(hook_type, bstack1ll1lll_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ∶"))
            result = None
            try:
                bstack1ll11ll111l_opy_ = self._1lllll1llll1_opy_[(bstack1llllll11l11_opy_, hook_type)]
                self.bstack1llllll11111_opy_(hook_type, bstack1ll11ll111l_opy_, (arg,))
                result = Result(result=bstack1ll1lll_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ∷"))
            except Exception as e:
                result = Result(result=bstack1ll1lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ∸"), exception=e)
                self.handler(hook_type, bstack1ll1lll_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ∹"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1lll_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ∺"), result)
        def bstack1llllll11lll_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1lll_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭∻"))
            result = None
            exception = None
            try:
                self.bstack1llllll11111_opy_(hook_type, self._1lllll1llll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1lll_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ∼"))
            except Exception as e:
                result = Result(result=bstack1ll1lll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ∽"), exception=e)
                self.handler(hook_type, bstack1ll1lll_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ∾"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1lll_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ∿"), result)
        if hook_type in [bstack1ll1lll_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ≀"), bstack1ll1lll_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ≁")]:
            return bstack1llllll11lll_opy_
        return bstack1lllll1lll11_opy_
    def bstack1llllll11l1l_opy_(self, bstack1llllll11ll1_opy_):
        def bstack1llllll111ll_opy_(this, *args, **kwargs):
            self.bstack1llllll1l11l_opy_(this, bstack1llllll11ll1_opy_)
            self._1lllll1lllll_opy_[bstack1llllll11ll1_opy_](this, *args, **kwargs)
        return bstack1llllll111ll_opy_