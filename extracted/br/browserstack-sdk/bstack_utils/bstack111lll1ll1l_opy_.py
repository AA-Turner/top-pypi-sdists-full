# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1111111l_opy_
from browserstack_sdk.bstack1l1ll11ll1_opy_ import bstack1l111l1l_opy_
def _111ll1lllll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111lll11l11_opy_:
    def __init__(self, handler):
        self._111lll1111l_opy_ = {}
        self._111lll1ll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l111l1l_opy_.version()
        if bstack11l1111111l_opy_(pytest_version, bstack11ll11_opy_ (u"ࠤ࠻࠲࠶࠴࠱ࠣ᳆")) >= 0:
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳇")] = Module._register_setup_function_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᳈")] = Module._register_setup_module_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᳉")] = Class._register_setup_class_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳊")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᳋"))
            Module._register_setup_module_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳌"))
            Class._register_setup_class_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳍"))
            Class._register_setup_method_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᳎"))
        else:
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳏")] = Module._inject_setup_function_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳐")] = Module._inject_setup_module_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳑")] = Class._inject_setup_class_fixture
            self._111lll1111l_opy_[bstack11ll11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᳒")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᳓"))
            Module._inject_setup_module_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧ᳔ࠪ"))
            Class._inject_setup_class_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧ᳕ࠪ"))
            Class._inject_setup_method_fixture = self.bstack111lll111ll_opy_(bstack11ll11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ᳖ࠬ"))
    def bstack111lll11lll_opy_(self, bstack111lll1lll1_opy_, hook_type):
        bstack111lll11111_opy_ = id(bstack111lll1lll1_opy_.__class__)
        if (bstack111lll11111_opy_, hook_type) in self._111lll1ll11_opy_:
            return
        meth = getattr(bstack111lll1lll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111lll1ll11_opy_[(bstack111lll11111_opy_, hook_type)] = meth
            setattr(bstack111lll1lll1_opy_, hook_type, self.bstack111lll1l1l1_opy_(hook_type, bstack111lll11111_opy_))
    def bstack111lll11ll1_opy_(self, instance, bstack111lll1l111_opy_):
        if bstack111lll1l111_opy_ == bstack11ll11_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥ᳗ࠣ"):
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ᳘ࠢ"))
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱ᳙ࠦ"))
        if bstack111lll1l111_opy_ == bstack11ll11_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ᳚"):
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣ᳛"))
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩ᳜ࠧ"))
        if bstack111lll1l111_opy_ == bstack11ll11_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨ᳝ࠦ"):
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵ᳞ࠥ"))
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹ᳟ࠢ"))
        if bstack111lll1l111_opy_ == bstack11ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ᳠"):
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢ᳡"))
            self.bstack111lll11lll_opy_(instance.obj, bstack11ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧ᳢ࠦ"))
    @staticmethod
    def bstack111lll11l1l_opy_(hook_type, func, args):
        if hook_type in [bstack11ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥ᳣ࠩ"), bstack11ll11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ᳤࠭")]:
            _111ll1lllll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111lll1l1l1_opy_(self, hook_type, bstack111lll11111_opy_):
        def bstack111lll1l1ll_opy_(arg=None):
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩ᳥ࠬ"))
            result = None
            try:
                bstack1lllll11111_opy_ = self._111lll1ll11_opy_[(bstack111lll11111_opy_, hook_type)]
                self.bstack111lll11l1l_opy_(hook_type, bstack1lllll11111_opy_, (arg,))
                result = Result(result=bstack11ll11_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ᳦࠭"))
            except Exception as e:
                result = Result(result=bstack11ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ᳧ࠧ"), exception=e)
                self.handler(hook_type, bstack11ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸ᳨ࠧ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᳩ"), result)
        def bstack111lll1l11l_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᳪ"))
            result = None
            exception = None
            try:
                self.bstack111lll11l1l_opy_(hook_type, self._111lll1ll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᳫ"))
            except Exception as e:
                result = Result(result=bstack11ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᳬ"), exception=e)
                self.handler(hook_type, bstack11ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶ᳭ࠬ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᳮ"), result)
        if hook_type in [bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᳯ"), bstack11ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᳰ")]:
            return bstack111lll1l11l_opy_
        return bstack111lll1l1ll_opy_
    def bstack111lll111ll_opy_(self, bstack111lll1l111_opy_):
        def bstack111lll111l1_opy_(this, *args, **kwargs):
            self.bstack111lll11ll1_opy_(this, bstack111lll1l111_opy_)
            self._111lll1111l_opy_[bstack111lll1l111_opy_](this, *args, **kwargs)
        return bstack111lll111l1_opy_