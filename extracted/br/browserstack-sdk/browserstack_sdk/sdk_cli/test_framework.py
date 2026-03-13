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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1ll1ll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll1l1ll1l1_opy_, bstack1ll11lll1l1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1111l_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᥬ").format(self.name)
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
        return bstack1111l_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᥭ").format(self.name)
class bstack1ll111lllll_opy_(bstack1ll1l1ll1l1_opy_):
    bstack1l11lll111l_opy_: List[str]
    bstack11l1l11llll_opy_: Dict[str, str]
    state: TestFrameworkState
    bstack1ll11llllll_opy_: datetime
    bstack1ll1l1111ll_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11lll1l1_opy_,
        bstack1l11lll111l_opy_: List[str],
        bstack11l1l11llll_opy_: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.bstack1l11lll111l_opy_ = bstack1l11lll111l_opy_
        self.bstack11l1l11llll_opy_ = bstack11l1l11llll_opy_
        self.state = state
        self.bstack1ll11llllll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1111ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll1lllll11_opy_(self, bstack1ll1l1111l1_opy_: TestFrameworkState):
        bstack1ll1l1llll1_opy_ = TestFrameworkState(bstack1ll1l1111l1_opy_).name
        if not bstack1ll1l1llll1_opy_:
            return False
        if bstack1ll1l1111l1_opy_ == self.state:
            return False
        self.state = bstack1ll1l1111l1_opy_
        self.bstack1ll1l1111ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1ll1lll11l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1l1lllllll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11l11l1l1_opy_: int = None
    bstack1l111l11ll1_opy_: str = None
    bstack1llll1l_opy_: str = None
    bstack111lll1111_opy_: str = None
    bstack1l111ll11ll_opy_: str = None
    bstack11ll11l1111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l11ll1ll1l_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥ᥮")
    bstack11llll1l1l1_opy_ = bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤ᥯")
    bstack1l1l111llll_opy_ = bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᥰ")
    bstack11l1ll111l1_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᥱ")
    bstack11l1lll111l_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᥲ")
    bstack11lll1ll1l1_opy_ = bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᥳ")
    bstack1l111ll1l11_opy_ = bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᥴ")
    bstack1l11l111l11_opy_ = bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤ᥵")
    bstack1l11l1l11ll_opy_ = bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣ᥶")
    bstack11l1ll111ll_opy_ = bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤ᥷")
    bstack1l1l1l1ll1l_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤ᥸")
    bstack1l11l11ll1l_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨ᥹")
    bstack11l1ll11l11_opy_ = bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣ᥺")
    bstack1l11111l111_opy_ = bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣ᥻")
    bstack1l1l1l111ll_opy_ = bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣ᥼")
    bstack11llll11l11_opy_ = bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢ᥽")
    bstack11l1l1l11ll_opy_ = bstack1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨ᥾")
    bstack11l1l1ll1l1_opy_ = bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨ᥿")
    bstack11l1l1lllll_opy_ = bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢᦀ")
    bstack11l1l11l1l1_opy_ = bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪᦁ")
    bstack11ll1l1ll11_opy_ = bstack1111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᦂ")
    bstack11ll111l1l1_opy_ = bstack1111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᦃ")
    bstack11l1ll1llll_opy_ = bstack1111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᦄ")
    bstack11l1ll1l1ll_opy_ = bstack1111l_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥᦅ")
    bstack11ll111ll11_opy_ = bstack1111l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣᦆ")
    bstack11l1ll11111_opy_ = bstack1111l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢᦇ")
    bstack11l1l1l1l11_opy_ = bstack1111l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣᦈ")
    bstack11l1ll1ll11_opy_ = bstack1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᦉ")
    bstack11l1l1l1lll_opy_ = bstack1111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᦊ")
    bstack11ll1111l11_opy_ = bstack1111l_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᦋ")
    bstack11ll1111111_opy_ = bstack1111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᦌ")
    KIND_SCREENSHOT = bstack1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᦍ")
    bstack1l1111l1111_opy_ = bstack1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᦎ")
    bstack1l1111l111l_opy_ = bstack1111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᦏ")
    bstack1ll1lll111l_opy_: Dict[str, bstack1ll111lllll_opy_] = dict()
    bstack11l11lll111_opy_: Dict[str, List[Callable]] = dict()
    bstack1l11lll111l_opy_: List[str]
    bstack11l1l11llll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l11lll111l_opy_: List[str],
        bstack11l1l11llll_opy_: Dict[str, str],
        bstack1ll1ll11lll_opy_: bstack1ll1ll11l11_opy_
    ):
        self.bstack1l11lll111l_opy_ = bstack1l11lll111l_opy_
        self.bstack11l1l11llll_opy_ = bstack11l1l11llll_opy_
        self.bstack1ll1ll11lll_opy_ = bstack1ll1ll11lll_opy_
    def track_event(
        self,
        context: bstack1ll1lll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᦐ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11l1lll1ll1_opy_(
        self,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11ll11lllll_opy_ = TestFramework.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        if not bstack11ll11lllll_opy_ in TestFramework.bstack11l11lll111_opy_:
            return
        self.logger.debug(bstack1111l_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᦑ").format(len(TestFramework.bstack11l11lll111_opy_[bstack11ll11lllll_opy_])))
        for callback in TestFramework.bstack11l11lll111_opy_[bstack11ll11lllll_opy_]:
            try:
                callback(self, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1111l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣᦒ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11111llll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1111l11l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l111llllll_opy_(self, instance, bstack1ll1l111l11_opy_):
        return
    @abc.abstractmethod
    def bstack1l111lll111_opy_(self, instance, bstack1ll1l111l11_opy_):
        return
    @staticmethod
    def bstack1ll1l11l111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1l1ll1l1_opy_.create_context(target)
        instance = TestFramework.bstack1ll1lll111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1l1ll11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11l111ll1_opy_(reverse=True) -> List[bstack1ll111lllll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll1lll111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11llllll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l111ll1_opy_(ctx: bstack1ll11lll1l1_opy_, reverse=True) -> List[bstack1ll111lllll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll1lll111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11llllll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l11ll_opy_(instance: bstack1ll111lllll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lll1l11_opy_(instance: bstack1ll111lllll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll1lllll11_opy_(instance: bstack1ll111lllll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1111l_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᦓ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1111lll_opy_(instance: bstack1ll111lllll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥᦔ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l11l1ll1l_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1111l_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᦕ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1ll1l11l111_opy_(target, strict)
        return TestFramework.bstack1ll1lll1l11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1ll1l11l111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11l1ll1l11l_opy_(instance: bstack1ll111lllll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11l1lllllll_opy_(instance: bstack1ll111lllll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState]):
        return bstack1111l_opy_ (u"ࠧࡀࠢᦖ").join((TestFrameworkState(bstack1ll1l111l11_opy_[0]).name, TestHookState(bstack1ll1l111l11_opy_[1]).name))
    @staticmethod
    def bstack1l1l11llll1_opy_(bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        bstack11ll11lllll_opy_ = TestFramework.bstack11ll1l11l1l_opy_(bstack1ll1l111l11_opy_)
        TestFramework.logger.debug(bstack1111l_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᦗ").format(bstack11ll11lllll_opy_))
        if not bstack11ll11lllll_opy_ in TestFramework.bstack11l11lll111_opy_:
            TestFramework.bstack11l11lll111_opy_[bstack11ll11lllll_opy_] = []
        TestFramework.bstack11l11lll111_opy_[bstack11ll11lllll_opy_].append(callback)
    @staticmethod
    def bstack1l1111l11ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᦘ"):
            return klass.__qualname__
        return module + bstack1111l_opy_ (u"ࠣ࠰ࠥᦙ") + klass.__qualname__
    @staticmethod
    def bstack1l11111l1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}