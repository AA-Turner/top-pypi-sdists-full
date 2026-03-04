# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l11ll111_opy_
from browserstack_sdk.bstack1l11l11l11_opy_ import bstack11lllll1l_opy_
def _11111l111l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11111l111ll_opy_:
    def __init__(self, handler):
        self._111111lll1l_opy_ = {}
        self._111111lllll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11lllll1l_opy_.version()
        if bstack111l11ll111_opy_(pytest_version, bstack1lll1l_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨ⃥")) >= 0:
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨ⃦ࠫ")] = Module._register_setup_function_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⃧")] = Module._register_setup_module_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧ⃨ࠪ")] = Class._register_setup_class_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ⃩")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃪"))
            Module._register_setup_module_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫⃫ࠧ"))
            Class._register_setup_class_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫⃬ࠧ"))
            Class._register_setup_method_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ⃭ࠩ"))
        else:
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩ⃮ࠬ")] = Module._inject_setup_function_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨ⃯ࠫ")] = Module._inject_setup_module_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ⃰")] = Class._inject_setup_class_fixture
            self._111111lll1l_opy_[bstack1lll1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭⃱")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ⃲"))
            Module._inject_setup_module_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃳"))
            Class._inject_setup_class_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ⃴"))
            Class._inject_setup_method_fixture = self.bstack111111llll1_opy_(bstack1lll1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ⃵"))
    def bstack111111lll11_opy_(self, bstack11111l11111_opy_, hook_type):
        bstack11111l11lll_opy_ = id(bstack11111l11111_opy_.__class__)
        if (bstack11111l11lll_opy_, hook_type) in self._111111lllll_opy_:
            return
        meth = getattr(bstack11111l11111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111111lllll_opy_[(bstack11111l11lll_opy_, hook_type)] = meth
            setattr(bstack11111l11111_opy_, hook_type, self.bstack11111l1111l_opy_(hook_type, bstack11111l11lll_opy_))
    def bstack111111ll1ll_opy_(self, instance, bstack11111l11ll1_opy_):
        if bstack11111l11ll1_opy_ == bstack1lll1l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ⃶"):
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ⃷"))
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤ⃸"))
        if bstack11111l11ll1_opy_ == bstack1lll1l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ⃹"):
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨ⃺"))
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥ⃻"))
        if bstack11111l11ll1_opy_ == bstack1lll1l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ⃼"):
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣ⃽"))
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧ⃾"))
        if bstack11111l11ll1_opy_ == bstack1lll1l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ⃿"):
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧ℀"))
            self.bstack111111lll11_opy_(instance.obj, bstack1lll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤ℁"))
    @staticmethod
    def bstack11111l11l11_opy_(hook_type, func, args):
        if hook_type in [bstack1lll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧℂ"), bstack1lll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ℃")]:
            _11111l111l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111l1111l_opy_(self, hook_type, bstack11111l11lll_opy_):
        def bstack111111ll111_opy_(arg=None):
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ℄"))
            result = None
            try:
                bstack1ll1ll1l111_opy_ = self._111111lllll_opy_[(bstack11111l11lll_opy_, hook_type)]
                self.bstack11111l11l11_opy_(hook_type, bstack1ll1ll1l111_opy_, (arg,))
                result = Result(result=bstack1lll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ℅"))
            except Exception as e:
                result = Result(result=bstack1lll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ℆"), exception=e)
                self.handler(hook_type, bstack1lll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬℇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭℈"), result)
        def bstack111111ll11l_opy_(this, arg=None):
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ℉"))
            result = None
            exception = None
            try:
                self.bstack11111l11l11_opy_(hook_type, self._111111lllll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1lll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩℊ"))
            except Exception as e:
                result = Result(result=bstack1lll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪℋ"), exception=e)
                self.handler(hook_type, bstack1lll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪℌ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1lll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫℍ"), result)
        if hook_type in [bstack1lll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬℎ"), bstack1lll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩℏ")]:
            return bstack111111ll11l_opy_
        return bstack111111ll111_opy_
    def bstack111111llll1_opy_(self, bstack11111l11ll1_opy_):
        def bstack11111l11l1l_opy_(this, *args, **kwargs):
            self.bstack111111ll1ll_opy_(this, bstack11111l11ll1_opy_)
            self._111111lll1l_opy_[bstack11111l11ll1_opy_](this, *args, **kwargs)
        return bstack11111l11l1l_opy_