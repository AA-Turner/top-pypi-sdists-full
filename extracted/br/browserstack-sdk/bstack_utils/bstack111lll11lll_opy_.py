# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1111ll11_opy_
from browserstack_sdk.bstack1lll1l11l1_opy_ import bstack1l1lllllll_opy_
def _111lll11ll1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111ll1lll11_opy_:
    def __init__(self, handler):
        self._111ll1lll1l_opy_ = {}
        self._111ll1llll1_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1lllllll_opy_.version()
        if bstack11l1111ll11_opy_(pytest_version, bstack11ll1l1_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨ᳧")) >= 0:
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨ᳨ࠫ")] = Module._register_setup_function_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᳩ")] = Module._register_setup_module_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᳪ")] = Class._register_setup_class_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᳫ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᳬ"))
            Module._register_setup_module_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫᳭ࠧ"))
            Class._register_setup_class_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᳮ"))
            Class._register_setup_method_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᳯ"))
        else:
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᳰ")] = Module._inject_setup_function_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᳱ")] = Module._inject_setup_module_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᳲ")] = Class._inject_setup_class_fixture
            self._111ll1lll1l_opy_[bstack11ll1l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᳳ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳴"))
            Module._inject_setup_module_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᳵ"))
            Class._inject_setup_class_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᳶ"))
            Class._inject_setup_method_fixture = self.bstack111lll11l1l_opy_(bstack11ll1l1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᳷"))
    def bstack111ll1ll1l1_opy_(self, bstack111ll1ll11l_opy_, hook_type):
        bstack111ll1ll111_opy_ = id(bstack111ll1ll11l_opy_.__class__)
        if (bstack111ll1ll111_opy_, hook_type) in self._111ll1llll1_opy_:
            return
        meth = getattr(bstack111ll1ll11l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll1llll1_opy_[(bstack111ll1ll111_opy_, hook_type)] = meth
            setattr(bstack111ll1ll11l_opy_, hook_type, self.bstack111ll1lllll_opy_(hook_type, bstack111ll1ll111_opy_))
    def bstack111lll111l1_opy_(self, instance, bstack111ll1ll1ll_opy_):
        if bstack111ll1ll1ll_opy_ == bstack11ll1l1_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ᳸"):
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ᳹"))
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᳺ"))
        if bstack111ll1ll1ll_opy_ == bstack11ll1l1_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᳻"):
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨ᳼"))
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥ᳽"))
        if bstack111ll1ll1ll_opy_ == bstack11ll1l1_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᳾"):
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣ᳿"))
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᴀ"))
        if bstack111ll1ll1ll_opy_ == bstack11ll1l1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᴁ"):
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᴂ"))
            self.bstack111ll1ll1l1_opy_(instance.obj, bstack11ll1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᴃ"))
    @staticmethod
    def bstack111lll11l11_opy_(hook_type, func, args):
        if hook_type in [bstack11ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᴄ"), bstack11ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᴅ")]:
            _111lll11ll1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll1lllll_opy_(self, hook_type, bstack111ll1ll111_opy_):
        def bstack111lll11111_opy_(arg=None):
            self.handler(hook_type, bstack11ll1l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᴆ"))
            result = None
            try:
                bstack1llllll111l_opy_ = self._111ll1llll1_opy_[(bstack111ll1ll111_opy_, hook_type)]
                self.bstack111lll11l11_opy_(hook_type, bstack1llllll111l_opy_, (arg,))
                result = Result(result=bstack11ll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᴇ"))
            except Exception as e:
                result = Result(result=bstack11ll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᴈ"), exception=e)
                self.handler(hook_type, bstack11ll1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᴉ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᴊ"), result)
        def bstack111lll1111l_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᴋ"))
            result = None
            exception = None
            try:
                self.bstack111lll11l11_opy_(hook_type, self._111ll1llll1_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᴌ"))
            except Exception as e:
                result = Result(result=bstack11ll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᴍ"), exception=e)
                self.handler(hook_type, bstack11ll1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᴎ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᴏ"), result)
        if hook_type in [bstack11ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᴐ"), bstack11ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᴑ")]:
            return bstack111lll1111l_opy_
        return bstack111lll11111_opy_
    def bstack111lll11l1l_opy_(self, bstack111ll1ll1ll_opy_):
        def bstack111lll111ll_opy_(this, *args, **kwargs):
            self.bstack111lll111l1_opy_(this, bstack111ll1ll1ll_opy_)
            self._111ll1lll1l_opy_[bstack111ll1ll1ll_opy_](this, *args, **kwargs)
        return bstack111lll111ll_opy_