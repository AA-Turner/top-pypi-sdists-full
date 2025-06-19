# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l11llll11_opy_
from browserstack_sdk.bstack1l1l1lllll_opy_ import bstack1llll1l111_opy_
def _111llllll11_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111llll11l1_opy_:
    def __init__(self, handler):
        self._111llll1l11_opy_ = {}
        self._111lll1llll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1llll1l111_opy_.version()
        if bstack11l11llll11_opy_(pytest_version, bstack111lll_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᲷ")) >= 0:
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᲸ")] = Module._register_setup_function_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᲹ")] = Module._register_setup_module_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᲺ")] = Class._register_setup_class_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᲻")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᲼"))
            Module._register_setup_module_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᲽ"))
            Class._register_setup_class_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᲾ"))
            Class._register_setup_method_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᲿ"))
        else:
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᳀")] = Module._inject_setup_function_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᳁")] = Module._inject_setup_module_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᳂")] = Class._inject_setup_class_fixture
            self._111llll1l11_opy_[bstack111lll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᳃")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᳄"))
            Module._inject_setup_module_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳅"))
            Class._inject_setup_class_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᳆"))
            Class._inject_setup_method_fixture = self.bstack111lllll1ll_opy_(bstack111lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᳇"))
    def bstack111llll111l_opy_(self, bstack111llll1l1l_opy_, hook_type):
        bstack111lllll11l_opy_ = id(bstack111llll1l1l_opy_.__class__)
        if (bstack111lllll11l_opy_, hook_type) in self._111lll1llll_opy_:
            return
        meth = getattr(bstack111llll1l1l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111lll1llll_opy_[(bstack111lllll11l_opy_, hook_type)] = meth
            setattr(bstack111llll1l1l_opy_, hook_type, self.bstack111lllll111_opy_(hook_type, bstack111lllll11l_opy_))
    def bstack111llll11ll_opy_(self, instance, bstack111llll1lll_opy_):
        if bstack111llll1lll_opy_ == bstack111lll_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᳈"):
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨ᳉"))
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥ᳊"))
        if bstack111llll1lll_opy_ == bstack111lll_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣ᳋"):
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢ᳌"))
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦ᳍"))
        if bstack111llll1lll_opy_ == bstack111lll_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ᳎"):
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ᳏"))
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ᳐"))
        if bstack111llll1lll_opy_ == bstack111lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᳑"):
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨ᳒"))
            self.bstack111llll111l_opy_(instance.obj, bstack111lll_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥ᳓"))
    @staticmethod
    def bstack111llll1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack111lll_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᳔"), bstack111lll_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨ᳕ࠬ")]:
            _111llllll11_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111lllll111_opy_(self, hook_type, bstack111lllll11l_opy_):
        def bstack111lllllll1_opy_(arg=None):
            self.handler(hook_type, bstack111lll_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨ᳖ࠫ"))
            result = None
            try:
                bstack1lllllllll1_opy_ = self._111lll1llll_opy_[(bstack111lllll11l_opy_, hook_type)]
                self.bstack111llll1ll1_opy_(hook_type, bstack1lllllllll1_opy_, (arg,))
                result = Result(result=bstack111lll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨ᳗ࠬ"))
            except Exception as e:
                result = Result(result=bstack111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ᳘࠭"), exception=e)
                self.handler(hook_type, bstack111lll_opy_ (u"ࠧࡢࡨࡷࡩࡷ᳙࠭"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111lll_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ᳚"), result)
        def bstack111lllll1l1_opy_(this, arg=None):
            self.handler(hook_type, bstack111lll_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ᳛"))
            result = None
            exception = None
            try:
                self.bstack111llll1ll1_opy_(hook_type, self._111lll1llll_opy_[hook_type], (this, arg))
                result = Result(result=bstack111lll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦ᳜ࠪ"))
            except Exception as e:
                result = Result(result=bstack111lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ᳝ࠫ"), exception=e)
                self.handler(hook_type, bstack111lll_opy_ (u"ࠬࡧࡦࡵࡧࡵ᳞ࠫ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111lll_opy_ (u"࠭ࡡࡧࡶࡨࡶ᳟ࠬ"), result)
        if hook_type in [bstack111lll_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᳠"), bstack111lll_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ᳡")]:
            return bstack111lllll1l1_opy_
        return bstack111lllllll1_opy_
    def bstack111lllll1ll_opy_(self, bstack111llll1lll_opy_):
        def bstack111llll1111_opy_(this, *args, **kwargs):
            self.bstack111llll11ll_opy_(this, bstack111llll1lll_opy_)
            self._111llll1l11_opy_[bstack111llll1lll_opy_](this, *args, **kwargs)
        return bstack111llll1111_opy_