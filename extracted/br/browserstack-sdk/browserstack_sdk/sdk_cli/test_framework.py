# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1l1l1_opy_ import bstack1111l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111l1111_opy_, bstack1111l11lll_opy_
class bstack1lll1l1l11l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l11lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᓯ").format(self.name)
class bstack1llll1111ll_opy_(Enum):
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
        return bstack1l11lll_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᓰ").format(self.name)
class bstack1lll1lllll1_opy_(bstack11111l1111_opy_):
    bstack1ll1l11ll11_opy_: List[str]
    bstack1l11llll111_opy_: Dict[str, str]
    state: bstack1llll1111ll_opy_
    bstack11111l111l_opy_: datetime
    bstack11111ll1l1_opy_: datetime
    def __init__(
        self,
        context: bstack1111l11lll_opy_,
        bstack1ll1l11ll11_opy_: List[str],
        bstack1l11llll111_opy_: Dict[str, str],
        state=bstack1llll1111ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l11ll11_opy_ = bstack1ll1l11ll11_opy_
        self.bstack1l11llll111_opy_ = bstack1l11llll111_opy_
        self.state = state
        self.bstack11111l111l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack11111ll1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1111l111ll_opy_(self, bstack1111l11l11_opy_: bstack1llll1111ll_opy_):
        bstack11111l11l1_opy_ = bstack1llll1111ll_opy_(bstack1111l11l11_opy_).name
        if not bstack11111l11l1_opy_:
            return False
        if bstack1111l11l11_opy_ == self.state:
            return False
        self.state = bstack1111l11l11_opy_
        self.bstack11111ll1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1l111l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lllllll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1ll1111111l_opy_: int = None
    bstack1ll11111111_opy_: str = None
    bstack11111l1_opy_: str = None
    bstack1l111l11ll_opy_: str = None
    bstack1ll11111l11_opy_: str = None
    bstack1l11l11ll11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1ll11lll_opy_ = bstack1l11lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᓱ")
    bstack1l11ll11111_opy_ = bstack1l11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᓲ")
    bstack1ll1ll111l1_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᓳ")
    bstack1l11l11l111_opy_ = bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᓴ")
    bstack1l11ll1l1l1_opy_ = bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᓵ")
    bstack1l1l1ll11ll_opy_ = bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᓶ")
    bstack1ll111l1l11_opy_ = bstack1l11lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᓷ")
    bstack1l1lllll1ll_opy_ = bstack1l11lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᓸ")
    bstack1ll111ll11l_opy_ = bstack1l11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᓹ")
    bstack1l111ll1ll1_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᓺ")
    bstack1ll1l1ll111_opy_ = bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᓻ")
    bstack1ll1111l1ll_opy_ = bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᓼ")
    bstack1l11lll1111_opy_ = bstack1l11lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᓽ")
    bstack1l1ll1l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᓾ")
    bstack1ll1l111lll_opy_ = bstack1l11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᓿ")
    bstack1l1l1lll1ll_opy_ = bstack1l11lll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᔀ")
    bstack1l111lll1l1_opy_ = bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᔁ")
    bstack1l111l1l11l_opy_ = bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᔂ")
    bstack1l111ll1111_opy_ = bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᔃ")
    bstack1l111l11l1l_opy_ = bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᔄ")
    bstack1l1l111l1l1_opy_ = bstack1l11lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᔅ")
    bstack1l11l1l1111_opy_ = bstack1l11lll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᔆ")
    bstack1l11l111ll1_opy_ = bstack1l11lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᔇ")
    bstack1l11ll11ll1_opy_ = bstack1l11lll_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᔈ")
    bstack1l11ll11l11_opy_ = bstack1l11lll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᔉ")
    bstack1l11lll11ll_opy_ = bstack1l11lll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᔊ")
    bstack1l11lll1lll_opy_ = bstack1l11lll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᔋ")
    bstack1l11l1llll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᔌ")
    bstack1l111l1lll1_opy_ = bstack1l11lll_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᔍ")
    bstack1l11lll111l_opy_ = bstack1l11lll_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᔎ")
    bstack1l11l1lll1l_opy_ = bstack1l11lll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᔏ")
    bstack1ll111l1ll1_opy_ = bstack1l11lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᔐ")
    bstack1l1lllllll1_opy_ = bstack1l11lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᔑ")
    bstack1l1lll1l111_opy_ = bstack1l11lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᔒ")
    bstack11111lllll_opy_: Dict[str, bstack1lll1lllll1_opy_] = dict()
    bstack1l1111lllll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l11ll11_opy_: List[str]
    bstack1l11llll111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l11ll11_opy_: List[str],
        bstack1l11llll111_opy_: Dict[str, str],
        bstack1111l1l1l1_opy_: bstack1111l1ll11_opy_
    ):
        self.bstack1ll1l11ll11_opy_ = bstack1ll1l11ll11_opy_
        self.bstack1l11llll111_opy_ = bstack1l11llll111_opy_
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
    def track_event(
        self,
        context: bstack1l11l1l111l_opy_,
        test_framework_state: bstack1llll1111ll_opy_,
        test_hook_state: bstack1lll1l1l11l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᔓ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111lll1ll_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llll1ll_opy_ = TestFramework.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        if not bstack1l11llll1ll_opy_ in TestFramework.bstack1l1111lllll_opy_:
            return
        self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᔔ").format(len(TestFramework.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_])))
        for callback in TestFramework.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_]:
            try:
                callback(self, instance, bstack11111l11ll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l11lll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᔕ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1ll111llll1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll111l1lll_opy_(self, instance, bstack11111l11ll_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll1ll1l_opy_(self, instance, bstack11111l11ll_opy_):
        return
    @staticmethod
    def bstack1111111l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack11111l1111_opy_.create_context(target)
        instance = TestFramework.bstack11111lllll_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1ll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llll1l11_opy_(reverse=True) -> List[bstack1lll1lllll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack11111lllll_opy_.values(),
            ),
            key=lambda t: t.bstack11111l111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111l1lll_opy_(ctx: bstack1111l11lll_opy_, reverse=True) -> List[bstack1lll1lllll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack11111lllll_opy_.values(),
            ),
            key=lambda t: t.bstack11111l111l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111ll11l_opy_(instance: bstack1lll1lllll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111111111_opy_(instance: bstack1lll1lllll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1111l111ll_opy_(instance: bstack1lll1lllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11lll_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔖ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11ll11l1l_opy_(instance: bstack1lll1lllll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l11lll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᔗ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111l1lll_opy_(instance: bstack1llll1111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11lll_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᔘ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1111111l1l_opy_(target, strict)
        return TestFramework.bstack1111111111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1111111l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l11lll1_opy_(instance: bstack1lll1lllll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l11l1111l1_opy_(instance: bstack1lll1lllll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11lllllll_opy_(bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_]):
        return bstack1l11lll_opy_ (u"ࠦ࠿ࠨᔙ").join((bstack1llll1111ll_opy_(bstack11111l11ll_opy_[0]).name, bstack1lll1l1l11l_opy_(bstack11111l11ll_opy_[1]).name))
    @staticmethod
    def bstack1ll1ll11l1l_opy_(bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_], callback: Callable):
        bstack1l11llll1ll_opy_ = TestFramework.bstack1l11lllllll_opy_(bstack11111l11ll_opy_)
        TestFramework.logger.debug(bstack1l11lll_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᔚ").format(bstack1l11llll1ll_opy_))
        if not bstack1l11llll1ll_opy_ in TestFramework.bstack1l1111lllll_opy_:
            TestFramework.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_] = []
        TestFramework.bstack1l1111lllll_opy_[bstack1l11llll1ll_opy_].append(callback)
    @staticmethod
    def bstack1l1llll1111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l11lll_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᔛ"):
            return klass.__qualname__
        return module + bstack1l11lll_opy_ (u"ࠢ࠯ࠤᔜ") + klass.__qualname__
    @staticmethod
    def bstack1ll11l11111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}