# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lll11lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1ll1lllllll_opy_, bstack1ll1lll11l1_opy_
class bstack1l1llll1l1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢព").format(self.name)
class bstack1ll1ll11l1l_opy_(Enum):
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
        return bstack11ll111_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨភ").format(self.name)
class bstack1ll1l111111_opy_(bstack1ll1lllllll_opy_):
    bstack1l1l1ll1l1l_opy_: List[str]
    bstack11ll1l1111l_opy_: Dict[str, str]
    state: bstack1ll1ll11l1l_opy_
    bstack1ll1lll1l1l_opy_: datetime
    bstack1lll11l11ll_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1lll11l1_opy_,
        bstack1l1l1ll1l1l_opy_: List[str],
        bstack11ll1l1111l_opy_: Dict[str, str],
        state=bstack1ll1ll11l1l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll1l1l_opy_
        self.bstack11ll1l1111l_opy_ = bstack11ll1l1111l_opy_
        self.state = state
        self.bstack1ll1lll1l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll11l11ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll11l1111_opy_(self, bstack1lll11ll11l_opy_: bstack1ll1ll11l1l_opy_):
        bstack1ll1lll1l11_opy_ = bstack1ll1ll11l1l_opy_(bstack1lll11ll11l_opy_).name
        if not bstack1ll1lll1l11_opy_:
            return False
        if bstack1lll11ll11l_opy_ == self.state:
            return False
        self.state = bstack1lll11ll11l_opy_
        self.bstack1lll11l11ll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11l1llllll1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1l1l11ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11ll1l1ll_opy_: int = None
    bstack1l11l11ll11_opy_: str = None
    bstack1_opy_: str = None
    bstack11ll11l1ll_opy_: str = None
    bstack1l11lll1lll_opy_: str = None
    bstack11lll1111l1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1l11ll1ll_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤម")
    bstack11ll1l1llll_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣយ")
    bstack1l1l1l1111l_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦរ")
    bstack11ll1l1l111_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥល")
    bstack11ll1l1l1l1_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨវ")
    bstack1l11111l1l1_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤឝ")
    bstack1l11ll1ll1l_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨឞ")
    bstack1l11l1lll11_opy_ = bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣស")
    bstack1l11l11llll_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢហ")
    bstack11ll1111l11_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣឡ")
    bstack1l1ll1ll1l1_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣអ")
    bstack1l11l1l11l1_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧឣ")
    bstack11ll1l11111_opy_ = bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢឤ")
    bstack1l111ll111l_opy_ = bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢឥ")
    bstack1l1ll1lll11_opy_ = bstack11ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢឦ")
    bstack1l1111l1l1l_opy_ = bstack11ll111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨឧ")
    bstack11ll111lll1_opy_ = bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧឨ")
    bstack11ll11ll11l_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧឩ")
    bstack11ll1llll11_opy_ = bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨឪ")
    bstack11l1lll1111_opy_ = bstack11ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩឫ")
    bstack11lll1lllll_opy_ = bstack11ll111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨឬ")
    bstack11ll1lll1ll_opy_ = bstack11ll111_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤឭ")
    bstack11ll1lll11l_opy_ = bstack11ll111_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣឮ")
    bstack11ll1llllll_opy_ = bstack11ll111_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤឯ")
    bstack11ll11ll111_opy_ = bstack11ll111_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢឰ")
    bstack11ll11ll1ll_opy_ = bstack11ll111_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨឱ")
    bstack11ll1ll11l1_opy_ = bstack11ll111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢឲ")
    bstack11ll1l1ll1l_opy_ = bstack11ll111_opy_ (u"ࠧࡲ࡯ࡨࡵࠥឳ")
    bstack11ll1ll111l_opy_ = bstack11ll111_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣ឴")
    bstack11ll1111lll_opy_ = bstack11ll111_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ឵")
    bstack11ll1lllll1_opy_ = bstack11ll111_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤា")
    bstack1l11llll1ll_opy_ = bstack11ll111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦិ")
    bstack1l111lll111_opy_ = bstack11ll111_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧី")
    bstack1l11lll1l1l_opy_ = bstack11ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨឹ")
    bstack1ll1lll1ll1_opy_: Dict[str, bstack1ll1l111111_opy_] = dict()
    bstack11l1ll111ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1ll1l1l_opy_: List[str]
    bstack11ll1l1111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1ll1l1l_opy_: List[str],
        bstack11ll1l1111l_opy_: Dict[str, str],
        bstack1lll11llll1_opy_: bstack1lll11lll11_opy_
    ):
        self.bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll1l1l_opy_
        self.bstack11ll1l1111l_opy_ = bstack11ll1l1111l_opy_
        self.bstack1lll11llll1_opy_ = bstack1lll11llll1_opy_
    def track_event(
        self,
        context: bstack11l1llllll1_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1l1llll1l1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11ll111_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤឺ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11lll111l1l_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        bstack11lll11l1ll_opy_ = TestFramework.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        if not bstack11lll11l1ll_opy_ in TestFramework.bstack11l1ll111ll_opy_:
            return
        self.logger.debug(bstack11ll111_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢុ").format(len(TestFramework.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_])))
        for callback in TestFramework.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_]:
            try:
                callback(self, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢូ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11l111lll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l111lll11l_opy_(self, instance, bstack1ll1ll1llll_opy_):
        return
    @abc.abstractmethod
    def bstack1l111llllll_opy_(self, instance, bstack1ll1ll1llll_opy_):
        return
    @staticmethod
    def bstack1lll1111111_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1ll1lllllll_opy_.create_context(target)
        instance = TestFramework.bstack1ll1lll1ll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll111l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11lllll11_opy_(reverse=True) -> List[bstack1ll1l111111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll1lll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll11l11l1_opy_(ctx: bstack1ll1lll11l1_opy_, reverse=True) -> List[bstack1ll1l111111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll1lll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1lll111l_opy_(instance: bstack1ll1l111111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lllll11_opy_(instance: bstack1ll1l111111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll11l1111_opy_(instance: bstack1ll1l111111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧួ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll11111ll_opy_(instance: bstack1ll1l111111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤើ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11l1ll111l1_opy_(instance: bstack1ll1ll11l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥឿ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lll1111111_opy_(target, strict)
        return TestFramework.bstack1ll1lllll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lll1111111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1111l1l_opy_(instance: bstack1ll1l111111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll11l1lll_opy_(instance: bstack1ll1l111111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_]):
        return bstack11ll111_opy_ (u"ࠦ࠿ࠨៀ").join((bstack1ll1ll11l1l_opy_(bstack1ll1ll1llll_opy_[0]).name, bstack1l1llll1l1l_opy_(bstack1ll1ll1llll_opy_[1]).name))
    @staticmethod
    def bstack1l1l1lll11l_opy_(bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_], callback: Callable):
        bstack11lll11l1ll_opy_ = TestFramework.bstack11lll1l111l_opy_(bstack1ll1ll1llll_opy_)
        TestFramework.logger.debug(bstack11ll111_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥេ").format(bstack11lll11l1ll_opy_))
        if not bstack11lll11l1ll_opy_ in TestFramework.bstack11l1ll111ll_opy_:
            TestFramework.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_] = []
        TestFramework.bstack11l1ll111ll_opy_[bstack11lll11l1ll_opy_].append(callback)
    @staticmethod
    def bstack1l111ll1lll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣែ"):
            return klass.__qualname__
        return module + bstack11ll111_opy_ (u"ࠢ࠯ࠤៃ") + klass.__qualname__
    @staticmethod
    def bstack1l11ll111l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}