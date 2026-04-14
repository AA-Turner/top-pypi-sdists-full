# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1llll1l11111_opy_
from browserstack_sdk.bstack11l1llll1l_opy_ import bstack1ll11l1lll_opy_
def _1lll1lll11l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lll1ll1ll1l_opy_:
    def __init__(self, handler):
        self._1lll1ll1lll1_opy_ = {}
        self._1lll1lll111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1ll11l1lll_opy_.version()
        if bstack1llll1l11111_opy_(pytest_version, bstack1l111l_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨ␘")) >= 0:
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ␙")] = Module._register_setup_function_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␚")] = Module._register_setup_module_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␛")] = Class._register_setup_class_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ␜")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␝"))
            Module._register_setup_module_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␞"))
            Class._register_setup_class_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ␟"))
            Class._register_setup_method_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␠"))
        else:
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ␡")] = Module._inject_setup_function_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ␢")] = Module._inject_setup_module_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ␣")] = Class._inject_setup_class_fixture
            self._1lll1ll1lll1_opy_[bstack1l111l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭␤")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ␥"))
            Module._inject_setup_module_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␦"))
            Class._inject_setup_class_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ␧"))
            Class._inject_setup_method_fixture = self.bstack1lll1lll1lll_opy_(bstack1l111l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ␨"))
    def bstack1lll1llll1l1_opy_(self, bstack1lll1ll1ll11_opy_, hook_type):
        bstack1lll1llll111_opy_ = id(bstack1lll1ll1ll11_opy_.__class__)
        if (bstack1lll1llll111_opy_, hook_type) in self._1lll1lll111l_opy_:
            return
        meth = getattr(bstack1lll1ll1ll11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1lll1lll111l_opy_[(bstack1lll1llll111_opy_, hook_type)] = meth
            setattr(bstack1lll1ll1ll11_opy_, hook_type, self.bstack1lll1lll1l1l_opy_(hook_type, bstack1lll1llll111_opy_))
    def bstack1lll1lll1l11_opy_(self, instance, bstack1lll1lll1ll1_opy_):
        if bstack1lll1lll1ll1_opy_ == bstack1l111l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ␩"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧ␪"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤ␫"))
        if bstack1lll1lll1ll1_opy_ == bstack1l111l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ␬"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨ␭"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥ␮"))
        if bstack1lll1lll1ll1_opy_ == bstack1l111l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤ␯"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣ␰"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧ␱"))
        if bstack1lll1lll1ll1_opy_ == bstack1l111l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨ␲"):
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧ␳"))
            self.bstack1lll1llll1l1_opy_(instance.obj, bstack1l111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤ␴"))
    @staticmethod
    def bstack1lll1llll1ll_opy_(hook_type, func, args):
        if hook_type in [bstack1l111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧ␵"), bstack1l111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ␶")]:
            _1lll1lll11l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lll1lll1l1l_opy_(self, hook_type, bstack1lll1llll111_opy_):
        def bstack1lll1llll11l_opy_(arg=None):
            self.handler(hook_type, bstack1l111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ␷"))
            result = None
            try:
                bstack1l1ll111ll1_opy_ = self._1lll1lll111l_opy_[(bstack1lll1llll111_opy_, hook_type)]
                self.bstack1lll1llll1ll_opy_(hook_type, bstack1l1ll111ll1_opy_, (arg,))
                result = Result(result=bstack1l111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ␸"))
            except Exception as e:
                result = Result(result=bstack1l111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ␹"), exception=e)
                self.handler(hook_type, bstack1l111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ␺"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l111l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭␻"), result)
        def bstack1lll1lll11ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1l111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ␼"))
            result = None
            exception = None
            try:
                self.bstack1lll1llll1ll_opy_(hook_type, self._1lll1lll111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ␽"))
            except Exception as e:
                result = Result(result=bstack1l111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ␾"), exception=e)
                self.handler(hook_type, bstack1l111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ␿"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ⑀"), result)
        if hook_type in [bstack1l111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ⑁"), bstack1l111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩ⑂")]:
            return bstack1lll1lll11ll_opy_
        return bstack1lll1llll11l_opy_
    def bstack1lll1lll1lll_opy_(self, bstack1lll1lll1ll1_opy_):
        def bstack1lll1lll1111_opy_(this, *args, **kwargs):
            self.bstack1lll1lll1l11_opy_(this, bstack1lll1lll1ll1_opy_)
            self._1lll1ll1lll1_opy_[bstack1lll1lll1ll1_opy_](this, *args, **kwargs)
        return bstack1lll1lll1111_opy_