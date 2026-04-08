# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_, bstack1l1lll111ll_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack111l_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᮜ").format(self.name)
class TestFrameworkState(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack111l_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᮝ").format(self.name)
class bstack1l1l11ll11l_opy_(bstack1l1l1ll1l1l_opy_):
    bstack1l1ll1ll11l_opy_: List[str]
    bstack1l1lll1l111_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l11lll1l1l_opy_: datetime
    bstack1l1l11l11l1_opy_: datetime
    def __init__(
        self,
        context: bstack1l1lll111ll_opy_,
        bstack1l1ll1ll11l_opy_: List[str],
        bstack1l1lll1l111_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1ll1ll11l_opy_ = bstack1l1ll1ll11l_opy_
        self.bstack1l1lll1l111_opy_ = bstack1l1lll1l111_opy_
        self.state = state
        self.bstack1l11lll1l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1l11l11l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l11l1ll11_opy_(self, bstack1l1l111l11l_opy_: TestFrameworkState):
        bstack1l11lll1lll_opy_ = TestFrameworkState(bstack1l1l111l11l_opy_).name
        if not bstack1l11lll1lll_opy_:
            return False
        if bstack1l1l111l11l_opy_ == self.state:
            return False
        self.state = bstack1l1l111l11l_opy_
        self.bstack1l1l11l11l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1lll1l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack11lllllll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l11ll1l1_opy_: int = None
    bstack1l1l1l1l111_opy_: str = None
    bstack1lllllll_opy_: str = None
    bstack1ll1l1l11l_opy_: str = None
    bstack11ll1111111_opy_: str = None
    bstack111ll1ll1ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l1lll11l_opy_ = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᮞ")
    bstack1l1ll111l1l_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᮟ")
    bstack1l1ll1lll1l_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᮠ")
    bstack1l1ll111lll_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᮡ")
    bstack1l1ll1ll1l1_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᮢ")
    bstack1l1ll1lll11_opy_ = bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᮣ")
    bstack1l1l1ll1111_opy_ = bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᮤ")
    bstack1l1l1ll1ll1_opy_ = bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᮥ")
    bstack1l1l1ll1l11_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᮦ")
    bstack111ll1l11l1_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᮧ")
    bstack1l1ll1l1l11_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤᮨ")
    bstack1l1l1lll1l1_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᮩ")
    bstack1l1ll111l11_opy_ = bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥ᮪ࠣ")
    bstack1l1ll11ll11_opy_ = bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥ᮫ࠣ")
    bstack1l1l1l11ll1_opy_ = bstack111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᮬ")
    bstack1l1ll1111l1_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢᮭ")
    bstack1l1l1lll111_opy_ = bstack111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨᮮ")
    bstack1l1l11lllll_opy_ = bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨᮯ")
    bstack1l1lll11ll1_opy_ = bstack111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢ᮰")
    bstack1l1l1l1ll1l_opy_ = bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪ᮱")
    bstack1l1l1lll1ll_opy_ = bstack111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢ᮲")
    bstack1l1l11llll1_opy_ = bstack111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥ᮳")
    bstack1l1ll1ll1ll_opy_ = bstack111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤ᮴")
    bstack1l1ll11llll_opy_ = bstack111l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥ᮵")
    bstack1l1ll11ll1l_opy_ = bstack111l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣ᮶")
    bstack1l1ll11l111_opy_ = bstack111l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢ᮷")
    bstack1l1ll11l1ll_opy_ = bstack111l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣ᮸")
    bstack111ll1l1l1l_opy_ = bstack111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦ᮹")
    bstack111lll1l111_opy_ = bstack111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᮺ")
    bstack1l1lll11l11_opy_ = bstack111l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᮻ")
    bstack1l1ll11lll1_opy_ = bstack111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᮼ")
    KIND_SCREENSHOT = bstack111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᮽ")
    bstack11l1lllll11_opy_ = bstack111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᮾ")
    bstack11l1ll1l1ll_opy_ = bstack111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᮿ")
    bstack1l111l111_opy_: Dict[str, bstack1l1l11ll11l_opy_] = dict()
    bstack111l1l11ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll1ll11l_opy_: List[str]
    bstack1l1lll1l111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1ll1ll11l_opy_: List[str],
        bstack1l1lll1l111_opy_: Dict[str, str],
        bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_
    ):
        self.bstack1l1ll1ll11l_opy_ = bstack1l1ll1ll11l_opy_
        self.bstack1l1lll1l111_opy_ = bstack1l1lll1l111_opy_
        self.bstack1l1l1ll11l1_opy_ = bstack1l1l1ll11l1_opy_
    def track_event(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᯀ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l1l1l11lll_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack111llllll11_opy_ = TestFramework.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        if not bstack111llllll11_opy_ in TestFramework.bstack111l1l11ll1_opy_:
            return
        self.logger.debug(bstack111l_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᯁ").format(len(TestFramework.bstack111l1l11ll1_opy_[bstack111llllll11_opy_])))
        for callback in TestFramework.bstack111l1l11ll1_opy_[bstack111llllll11_opy_]:
            try:
                callback(self, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣᯂ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l1llll1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll11111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1111l_opy_(self, instance, bstack1l1l1lllll1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l1l11111_opy_(self, instance, bstack1l1l1lllll1_opy_):
        return
    @staticmethod
    def bstack1l1l1l1l11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1l1ll1l1l_opy_.create_context(target)
        instance = TestFramework.bstack1l111l111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1l111l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll111ll11_opy_(reverse=True) -> List[bstack1l1l11ll11l_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1l111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l11lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1l111111l_opy_(ctx: bstack1l1lll111ll_opy_, reverse=True) -> List[bstack1l1l11ll11l_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1l111l111_opy_.values(),
            ),
            key=lambda t: t.bstack1l11lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1111ll1l_opy_(instance: bstack1l1l11ll11l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll111111ll_opy_(instance: bstack1l1l11ll11l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l11l1ll11_opy_(instance: bstack1l1l11ll11l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack111l_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᯃ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1l1l1111l_opy_(instance: bstack1l1l11ll11l_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥᯄ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l11lll1l_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack111l_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᯅ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1l1l1l11l_opy_(target, strict)
        return TestFramework.bstack1ll111111ll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1l1l1l11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111ll1llll1_opy_(instance: bstack1l1l11ll11l_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111ll1l1lll_opy_(instance: bstack1l1l11ll11l_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack111l_opy_ (u"ࠧࡀࠢᯆ").join((TestFrameworkState(bstack1l1l1lllll1_opy_[0]).name, TestHookState(bstack1l1l1lllll1_opy_[1]).name))
    @staticmethod
    def bstack11llll1l1l1_opy_(bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack111llllll11_opy_ = TestFramework.bstack111llll1l1l_opy_(bstack1l1l1lllll1_opy_)
        TestFramework.logger.debug(bstack111l_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᯇ").format(bstack111llllll11_opy_))
        if not bstack111llllll11_opy_ in TestFramework.bstack111l1l11ll1_opy_:
            TestFramework.bstack111l1l11ll1_opy_[bstack111llllll11_opy_] = []
        TestFramework.bstack111l1l11ll1_opy_[bstack111llllll11_opy_].append(callback)
    @staticmethod
    def bstack11l1lll1l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᯈ"):
            return klass.__qualname__
        return module + bstack111l_opy_ (u"ࠣ࠰ࠥᯉ") + klass.__qualname__
    @staticmethod
    def bstack11l1ll1ll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}