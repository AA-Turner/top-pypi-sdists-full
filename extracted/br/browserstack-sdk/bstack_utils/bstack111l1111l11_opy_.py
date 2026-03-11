# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1111l1l1_opy_
from browserstack_sdk.bstack1l1ll11ll_opy_ import bstack1l1ll11l1l_opy_
def _111l111l1ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l11111l1_opy_:
    def __init__(self, handler):
        self._111l1111ll1_opy_ = {}
        self._1111lllllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1ll11l1l_opy_.version()
        if bstack11l1111l1l1_opy_(pytest_version, bstack1ll111_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᰕ")) >= 0:
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰖ")] = Module._register_setup_function_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᰗ")] = Module._register_setup_module_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᰘ")] = Class._register_setup_class_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰙ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᰚ"))
            Module._register_setup_module_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰛ"))
            Class._register_setup_class_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᰜ"))
            Class._register_setup_method_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᰝ"))
        else:
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᰞ")] = Module._inject_setup_function_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰟ")] = Module._inject_setup_module_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᰠ")] = Class._inject_setup_class_fixture
            self._111l1111ll1_opy_[bstack1ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᰡ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᰢ"))
            Module._inject_setup_module_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᰣ"))
            Class._inject_setup_class_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᰤ"))
            Class._inject_setup_method_fixture = self.bstack111l111l11l_opy_(bstack1ll111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᰥ"))
    def bstack1111lllll1l_opy_(self, bstack111l111111l_opy_, hook_type):
        bstack111l111l111_opy_ = id(bstack111l111111l_opy_.__class__)
        if (bstack111l111l111_opy_, hook_type) in self._1111lllllll_opy_:
            return
        meth = getattr(bstack111l111111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1111lllllll_opy_[(bstack111l111l111_opy_, hook_type)] = meth
            setattr(bstack111l111111l_opy_, hook_type, self.bstack1111lllll11_opy_(hook_type, bstack111l111l111_opy_))
    def bstack1111llllll1_opy_(self, instance, bstack111l111l1l1_opy_):
        if bstack111l111l1l1_opy_ == bstack1ll111_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᰦ"):
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᰧ"))
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᰨ"))
        if bstack111l111l1l1_opy_ == bstack1ll111_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᰩ"):
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᰪ"))
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᰫ"))
        if bstack111l111l1l1_opy_ == bstack1ll111_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᰬ"):
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᰭ"))
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᰮ"))
        if bstack111l111l1l1_opy_ == bstack1ll111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᰯ"):
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᰰ"))
            self.bstack1111lllll1l_opy_(instance.obj, bstack1ll111_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᰱ"))
    @staticmethod
    def bstack111l11111ll_opy_(hook_type, func, args):
        if hook_type in [bstack1ll111_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᰲ"), bstack1ll111_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᰳ")]:
            _111l111l1ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1111lllll11_opy_(self, hook_type, bstack111l111l111_opy_):
        def bstack111l1111lll_opy_(arg=None):
            self.handler(hook_type, bstack1ll111_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᰴ"))
            result = None
            try:
                bstack1ll1ll11ll1_opy_ = self._1111lllllll_opy_[(bstack111l111l111_opy_, hook_type)]
                self.bstack111l11111ll_opy_(hook_type, bstack1ll1ll11ll1_opy_, (arg,))
                result = Result(result=bstack1ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᰵ"))
            except Exception as e:
                result = Result(result=bstack1ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᰶ"), exception=e)
                self.handler(hook_type, bstack1ll111_opy_ (u"࠭ࡡࡧࡶࡨࡶ᰷ࠬ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll111_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭᰸"), result)
        def bstack111l1111l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll111_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ᰹"))
            result = None
            exception = None
            try:
                self.bstack111l11111ll_opy_(hook_type, self._1111lllllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᰺"))
            except Exception as e:
                result = Result(result=bstack1ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᰻"), exception=e)
                self.handler(hook_type, bstack1ll111_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ᰼"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll111_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᰽"), result)
        if hook_type in [bstack1ll111_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ᰾"), bstack1ll111_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ᰿")]:
            return bstack111l1111l1l_opy_
        return bstack111l1111lll_opy_
    def bstack111l111l11l_opy_(self, bstack111l111l1l1_opy_):
        def bstack111l1111111_opy_(this, *args, **kwargs):
            self.bstack1111llllll1_opy_(this, bstack111l111l1l1_opy_)
            self._111l1111ll1_opy_[bstack111l111l1l1_opy_](this, *args, **kwargs)
        return bstack111l1111111_opy_