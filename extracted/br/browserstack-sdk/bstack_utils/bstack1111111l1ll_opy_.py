# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111ll11111_opy_
from browserstack_sdk.bstack1ll11l1ll_opy_ import bstack11l11llll1_opy_
def _1111111l11l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11111111l11_opy_:
    def __init__(self, handler):
        self._11111111ll1_opy_ = {}
        self._111111111l1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l11llll1_opy_.version()
        if bstack1111ll11111_opy_(pytest_version, bstack1111l_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤ↥")) >= 0:
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ↦")] = Module._register_setup_function_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭↧")] = Module._register_setup_module_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭↨")] = Class._register_setup_class_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ↩")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ↪"))
            Module._register_setup_module_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ↫"))
            Class._register_setup_class_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ↬"))
            Class._register_setup_method_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ↭"))
        else:
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ↮")] = Module._inject_setup_function_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ↯")] = Module._inject_setup_module_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ↰")] = Class._inject_setup_class_fixture
            self._11111111ll1_opy_[bstack1111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ↱")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ↲"))
            Module._inject_setup_module_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ↳"))
            Class._inject_setup_class_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ↴"))
            Class._inject_setup_method_fixture = self.bstack11111111l1l_opy_(bstack1111l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭↵"))
    def bstack111111l1111_opy_(self, bstack1111111ll1l_opy_, hook_type):
        bstack1111111111l_opy_ = id(bstack1111111ll1l_opy_.__class__)
        if (bstack1111111111l_opy_, hook_type) in self._111111111l1_opy_:
            return
        meth = getattr(bstack1111111ll1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111111111l1_opy_[(bstack1111111111l_opy_, hook_type)] = meth
            setattr(bstack1111111ll1l_opy_, hook_type, self.bstack11111111lll_opy_(hook_type, bstack1111111111l_opy_))
    def bstack1111111llll_opy_(self, instance, bstack111111111ll_opy_):
        if bstack111111111ll_opy_ == bstack1111l_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ↶"):
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣ↷"))
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ↸"))
        if bstack111111111ll_opy_ == bstack1111l_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ↹"):
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤ↺"))
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨ↻"))
        if bstack111111111ll_opy_ == bstack1111l_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧ↼"):
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦ↽"))
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣ↾"))
        if bstack111111111ll_opy_ == bstack1111l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ↿"):
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣ⇀"))
            self.bstack111111l1111_opy_(instance.obj, bstack1111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧ⇁"))
    @staticmethod
    def bstack1111111ll11_opy_(hook_type, func, args):
        if hook_type in [bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ⇂"), bstack1111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧ⇃")]:
            _1111111l11l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111111lll_opy_(self, hook_type, bstack1111111111l_opy_):
        def bstack1111111l1l1_opy_(arg=None):
            self.handler(hook_type, bstack1111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭⇄"))
            result = None
            try:
                bstack1ll1l1ll111_opy_ = self._111111111l1_opy_[(bstack1111111111l_opy_, hook_type)]
                self.bstack1111111ll11_opy_(hook_type, bstack1ll1l1ll111_opy_, (arg,))
                result = Result(result=bstack1111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ⇅"))
            except Exception as e:
                result = Result(result=bstack1111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⇆"), exception=e)
                self.handler(hook_type, bstack1111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ⇇"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ⇈"), result)
        def bstack1111111l111_opy_(this, arg=None):
            self.handler(hook_type, bstack1111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ⇉"))
            result = None
            exception = None
            try:
                self.bstack1111111ll11_opy_(hook_type, self._111111111l1_opy_[hook_type], (this, arg))
                result = Result(result=bstack1111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⇊"))
            except Exception as e:
                result = Result(result=bstack1111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭⇋"), exception=e)
                self.handler(hook_type, bstack1111l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭⇌"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1111l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ⇍"), result)
        if hook_type in [bstack1111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ⇎"), bstack1111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ⇏")]:
            return bstack1111111l111_opy_
        return bstack1111111l1l1_opy_
    def bstack11111111l1l_opy_(self, bstack111111111ll_opy_):
        def bstack1111111lll1_opy_(this, *args, **kwargs):
            self.bstack1111111llll_opy_(this, bstack111111111ll_opy_)
            self._11111111ll1_opy_[bstack111111111ll_opy_](this, *args, **kwargs)
        return bstack1111111lll1_opy_