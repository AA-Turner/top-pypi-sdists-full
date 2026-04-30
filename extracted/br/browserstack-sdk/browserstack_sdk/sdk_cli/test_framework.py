# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1ll11lll1_opy_, bstack1l1ll1ll11l_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1111l_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᬦ").format(self.name)
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
        return bstack1l1111l_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᬧ").format(self.name)
class bstack1l11l1ll111_opy_(bstack1l1ll11lll1_opy_):
    bstack1l1l1lll111_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1l1lll11111_opy_: datetime
    bstack1l1ll1l1l1l_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll1ll11l_opy_,
        bstack1l1l1lll111_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1lll111_opy_ = bstack1l1l1lll111_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.state = state
        self.bstack1l1lll11111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1l1l1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack111l1llll1_opy_(self, bstack1l1ll1l1lll_opy_: TestFrameworkState):
        bstack1l1ll111lll_opy_ = TestFrameworkState(bstack1l1ll1l1lll_opy_).name
        if not bstack1l1ll111lll_opy_:
            return False
        if bstack1l1ll1l1lll_opy_ == self.state:
            return False
        self.state = bstack1l1ll1l1lll_opy_
        self.bstack1l1ll1l1l1l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1lll111l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack11lll1ll1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11ll11l1111_opy_: int = None
    bstack11ll11ll1ll_opy_: str = None
    bstack111111_opy_: str = None
    bstack11l1l111ll_opy_: str = None
    bstack11ll111l111_opy_: str = None
    bstack111ll1l1l1l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11llllll111_opy_ = bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᬨ")
    bstack11l1ll11111_opy_ = bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᬩ")
    bstack1l111l11l1l_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᬪ")
    bstack11l1111ll11_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᬫ")
    bstack11l11111ll1_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᬬ")
    bstack11l1ll1111l_opy_ = bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᬭ")
    bstack11ll111l11l_opy_ = bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᬮ")
    bstack11lll1111ll_opy_ = bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᬯ")
    bstack11ll1ll1l11_opy_ = bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᬰ")
    bstack11l1111lll1_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᬱ")
    bstack1l11111l11l_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᬲ")
    bstack11ll11l1lll_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᬳ")
    bstack11l1111111l_opy_ = bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤ᬴")
    bstack11ll11111l1_opy_ = bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᬵ")
    bstack1l111l1l111_opy_ = bstack1l1111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᬶ")
    bstack11l1l1ll11l_opy_ = bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᬷ")
    bstack111ll11l1ll_opy_ = bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᬸ")
    bstack111lll1lll1_opy_ = bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᬹ")
    bstack111ll11l11l_opy_ = bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᬺ")
    bstack111ll11111l_opy_ = bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᬻ")
    bstack11l11l11l1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᬼ")
    bstack111ll11lll1_opy_ = bstack1l1111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᬽ")
    bstack11l111111ll_opy_ = bstack1l1111l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᬾ")
    bstack11l1111l111_opy_ = bstack1l1111l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᬿ")
    bstack111lll111ll_opy_ = bstack1l1111l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᭀ")
    bstack111ll111lll_opy_ = bstack1l1111l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᭁ")
    bstack11l1111ll1l_opy_ = bstack1l1111l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᭂ")
    bstack111llll1l1l_opy_ = bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᭃ")
    bstack111lll1llll_opy_ = bstack1l1111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣ᭄ࠥ")
    bstack111lll1l1ll_opy_ = bstack1l1111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᭅ")
    bstack111ll1lll11_opy_ = bstack1l1111l_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᭆ")
    KIND_SCREENSHOT = bstack1l1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᭇ")
    bstack11lll11llll_opy_ = bstack1l1111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᭈ")
    bstack11ll1ll1ll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᭉ")
    bstack1lllll1ll1_opy_: Dict[str, bstack1l11l1ll111_opy_] = dict()
    bstack111l1l11lll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1lll111_opy_: List[str]
    bstack1l111lllll1_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1lll111_opy_: List[str],
        bstack1l111lllll1_opy_: Dict[str, str],
        bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_
    ):
        self.bstack1l1l1lll111_opy_ = bstack1l1l1lll111_opy_
        self.bstack1l111lllll1_opy_ = bstack1l111lllll1_opy_
        self.bstack1l1lll11l1l_opy_ = bstack1l1lll11l1l_opy_
    def track_event(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᭊ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack111lllll11l_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l111ll111_opy_ = TestFramework.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        if not bstack11l111ll111_opy_ in TestFramework.bstack111l1l11lll_opy_:
            return
        self.logger.debug(bstack1l1111l_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᭋ").format(len(TestFramework.bstack111l1l11lll_opy_[bstack11l111ll111_opy_])))
        for callback in TestFramework.bstack111l1l11lll_opy_[bstack11l111ll111_opy_]:
            try:
                callback(self, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᭌ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack11ll11l111l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11ll1l11l1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11lll1l111l_opy_(self, instance, bstack1l1ll1ll111_opy_):
        return
    @abc.abstractmethod
    def bstack11ll1llll1l_opy_(self, instance, bstack1l1ll1ll111_opy_):
        return
    @staticmethod
    def bstack1l1ll1ll1ll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1ll11lll1_opy_.create_context(target)
        instance = TestFramework.bstack1lllll1ll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll11l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack11ll1ll111l_opy_(reverse=True) -> List[bstack1l11l1ll111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1l1lll11111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1ll111111_opy_(ctx: bstack1l1ll1ll11l_opy_, reverse=True) -> List[bstack1l11l1ll111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1l1lll11111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1lll1l111_opy_(instance: bstack1l11l1ll111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1111l1l1_opy_(instance: bstack1l11l1ll111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack111l1llll1_opy_(instance: bstack1l11l1ll111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢ᭍").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111ll1lllll_opy_(instance: bstack1l11l1ll111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1111l_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦ᭎").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l1l11ll1_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1111l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧ᭏").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(target, strict)
        return TestFramework.bstack1ll1111l1l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111lll11ll1_opy_(instance: bstack1l11l1ll111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111ll1l1l11_opy_(instance: bstack1l11l1ll111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1l1111l_opy_ (u"ࠨ࠺ࠣ᭐").join((TestFrameworkState(bstack1l1ll1ll111_opy_[0]).name, TestHookState(bstack1l1ll1ll111_opy_[1]).name))
    @staticmethod
    def bstack1l1111lllll_opy_(bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l111ll111_opy_ = TestFramework.bstack11l111llll1_opy_(bstack1l1ll1ll111_opy_)
        TestFramework.logger.debug(bstack1l1111l_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧ᭑").format(bstack11l111ll111_opy_))
        if not bstack11l111ll111_opy_ in TestFramework.bstack111l1l11lll_opy_:
            TestFramework.bstack111l1l11lll_opy_[bstack11l111ll111_opy_] = []
        TestFramework.bstack111l1l11lll_opy_[bstack11l111ll111_opy_].append(callback)
    @staticmethod
    def bstack11lll11ll11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥ᭒"):
            return klass.__qualname__
        return module + bstack1l1111l_opy_ (u"ࠤ࠱ࠦ᭓") + klass.__qualname__
    @staticmethod
    def bstack11ll1lll1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}