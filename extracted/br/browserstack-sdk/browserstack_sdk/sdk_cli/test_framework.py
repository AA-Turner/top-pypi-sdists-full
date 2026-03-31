# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll11llll11_opy_ import bstack1ll11llllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11ll11ll_opy_, bstack1ll11l11ll1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll11_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣ᧕").format(self.name)
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
        return bstack1ll11_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢ᧖").format(self.name)
class bstack1l1l1l111l1_opy_(bstack1ll11ll11ll_opy_):
    bstack1l1l111lll1_opy_: List[str]
    bstack11l11l1l1ll_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll11l1l1ll_opy_: datetime
    bstack1ll111ll11l_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11l11ll1_opy_,
        bstack1l1l111lll1_opy_: List[str],
        bstack11l11l1l1ll_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l111lll1_opy_ = bstack1l1l111lll1_opy_
        self.bstack11l11l1l1ll_opy_ = bstack11l11l1l1ll_opy_
        self.state = state
        self.bstack1ll11l1l1ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll111ll11l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1l11lllll_opy_(self, bstack1ll11lll11l_opy_: TestFrameworkState):
        bstack1ll11l1l1l1_opy_ = TestFrameworkState(bstack1ll11lll11l_opy_).name
        if not bstack1ll11l1l1l1_opy_:
            return False
        if bstack1ll11lll11l_opy_ == self.state:
            return False
        self.state = bstack1ll11lll11l_opy_
        self.bstack1ll111ll11l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1l11llll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1l1l1lll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack11llll1lll1_opy_: int = None
    bstack1l11111l111_opy_: str = None
    bstack1l11ll_opy_: str = None
    bstack1l11ll111l_opy_: str = None
    bstack1l111l1ll11_opy_: str = None
    bstack11l1l1lllll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11l1lll11_opy_ = bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ᧗")
    bstack11lll111111_opy_ = bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤ᧘")
    bstack1l11ll1ll1l_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧ᧙")
    bstack11l1lll1111_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦ᧚")
    bstack11l11l1llll_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢ᧛")
    bstack11lll11l111_opy_ = bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥ᧜")
    bstack1l111l1l1l1_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢ᧝")
    bstack1l111ll1111_opy_ = bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤ᧞")
    bstack11lllll1lll_opy_ = bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣ᧟")
    bstack11l1l11l1l1_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ᧠")
    bstack1l11l11llll_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤ᧡")
    bstack1l11111lll1_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ᧢")
    bstack11l1l1l1ll1_opy_ = bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣ᧣")
    bstack11lll1llll1_opy_ = bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣ᧤")
    bstack1l11llll11l_opy_ = bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣ᧥")
    bstack11ll1lll1ll_opy_ = bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢ᧦")
    bstack11l1l111l1l_opy_ = bstack1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨ᧧")
    bstack11l11l1ll1l_opy_ = bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨ᧨")
    bstack11l1l11l1ll_opy_ = bstack1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢ᧩")
    bstack11l11l1111l_opy_ = bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪ᧪")
    bstack11ll1111l1l_opy_ = bstack1ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢ᧫")
    bstack11l11l1ll11_opy_ = bstack1ll11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥ᧬")
    bstack11l1ll111l1_opy_ = bstack1ll11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤ᧭")
    bstack11l1l11ll1l_opy_ = bstack1ll11_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥ᧮")
    bstack11l1l11lll1_opy_ = bstack1ll11_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣ᧯")
    bstack11l1l111ll1_opy_ = bstack1ll11_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢ᧰")
    bstack11l1ll1111l_opy_ = bstack1ll11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣ᧱")
    bstack11l1ll111ll_opy_ = bstack1ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦ᧲")
    bstack11l1l1l1lll_opy_ = bstack1ll11_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤ᧳")
    bstack11l1lll1l1l_opy_ = bstack1ll11_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤ᧴")
    bstack11l11l1l1l1_opy_ = bstack1ll11_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ᧵")
    KIND_SCREENSHOT = bstack1ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧ᧶")
    bstack11lllllllll_opy_ = bstack1ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨ᧷")
    bstack11llll1llll_opy_ = bstack1ll11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ᧸")
    bstack1l1l111l_opy_: Dict[str, bstack1l1l1l111l1_opy_] = dict()
    bstack11l1111l1ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l111lll1_opy_: List[str]
    bstack11l11l1l1ll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l111lll1_opy_: List[str],
        bstack11l11l1l1ll_opy_: Dict[str, str],
        bstack1ll11llll11_opy_: bstack1ll11llllll_opy_
    ):
        self.bstack1l1l111lll1_opy_ = bstack1l1l111lll1_opy_
        self.bstack11l11l1l1ll_opy_ = bstack11l11l1l1ll_opy_
        self.bstack1ll11llll11_opy_ = bstack1ll11llll11_opy_
    def track_event(
        self,
        context: bstack1ll1l11llll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥ᧹").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l11llll1l_opy_(
        self,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l1llll111_opy_ = TestFramework.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        if not bstack11l1llll111_opy_ in TestFramework.bstack11l1111l1ll_opy_:
            return
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣ᧺").format(len(TestFramework.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_])))
        for callback in TestFramework.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_]:
            try:
                callback(self, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣ᧻").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l111l1l11l_opy_(self):
        return
    @abc.abstractmethod
    def bstack11lllllll1l_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111l1l1l_opy_(self, instance, bstack1ll11l11lll_opy_):
        return
    @abc.abstractmethod
    def bstack1l1111llll1_opy_(self, instance, bstack1ll11l11lll_opy_):
        return
    @staticmethod
    def bstack1ll111l1lll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll11ll11ll_opy_.create_context(target)
        instance = TestFramework.bstack1l1l111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll11ll1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1111l111l_opy_(reverse=True) -> List[bstack1l1l1l111l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1l1l111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11l1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll11lll1ll_opy_(ctx: bstack1ll11l11ll1_opy_, reverse=True) -> List[bstack1l1l1l111l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1l1l111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11l1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1ll11111_opy_(instance: bstack1l1l1l111l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1ll1l1l1_opy_(instance: bstack1l1l1l111l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1l11lllll_opy_(instance: bstack1l1l1l111l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll11_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨ᧼").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l1l1111_opy_(instance: bstack1l1l1l111l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥ᧽").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l11111lll_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll11_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦ᧾").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll111l1lll_opy_(target, strict)
        return TestFramework.bstack1ll1ll1l1l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll111l1lll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1l1lll1l_opy_(instance: bstack1l1l1l111l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1l1ll11l_opy_(instance: bstack1l1l1l111l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1ll11_opy_ (u"ࠧࡀࠢ᧿").join((TestFrameworkState(bstack1ll11l11lll_opy_[0]).name, TestHookState(bstack1ll11l11lll_opy_[1]).name))
    @staticmethod
    def bstack1l11lll1lll_opy_(bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11l1llll111_opy_ = TestFramework.bstack11l1lll1ll1_opy_(bstack1ll11l11lll_opy_)
        TestFramework.logger.debug(bstack1ll11_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᨀ").format(bstack11l1llll111_opy_))
        if not bstack11l1llll111_opy_ in TestFramework.bstack11l1111l1ll_opy_:
            TestFramework.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_] = []
        TestFramework.bstack11l1111l1ll_opy_[bstack11l1llll111_opy_].append(callback)
    @staticmethod
    def bstack1l111l11l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᨁ"):
            return klass.__qualname__
        return module + bstack1ll11_opy_ (u"ࠣ࠰ࠥᨂ") + klass.__qualname__
    @staticmethod
    def bstack1l111l11l1l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}