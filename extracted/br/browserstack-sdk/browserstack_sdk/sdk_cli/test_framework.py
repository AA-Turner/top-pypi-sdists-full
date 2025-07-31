# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack1111111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import bstack1llllll1ll1_opy_, bstack1llll1lllll_opy_
class bstack1lll1llll11_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l11l11_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᖩ").format(self.name)
class bstack1lll1l1lll1_opy_(Enum):
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
        return bstack1l11l11_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᖪ").format(self.name)
class bstack1lll11l1l11_opy_(bstack1llllll1ll1_opy_):
    bstack1ll111ll11l_opy_: List[str]
    bstack1l11l111111_opy_: Dict[str, str]
    state: bstack1lll1l1lll1_opy_
    bstack1lllll1ll1l_opy_: datetime
    bstack1llll1ll1l1_opy_: datetime
    def __init__(
        self,
        context: bstack1llll1lllll_opy_,
        bstack1ll111ll11l_opy_: List[str],
        bstack1l11l111111_opy_: Dict[str, str],
        state=bstack1lll1l1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll111ll11l_opy_ = bstack1ll111ll11l_opy_
        self.bstack1l11l111111_opy_ = bstack1l11l111111_opy_
        self.state = state
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llll1ll1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllll1l11l_opy_(self, bstack1lllllll1ll_opy_: bstack1lll1l1lll1_opy_):
        bstack1llll1lll11_opy_ = bstack1lll1l1lll1_opy_(bstack1lllllll1ll_opy_).name
        if not bstack1llll1lll11_opy_:
            return False
        if bstack1lllllll1ll_opy_ == self.state:
            return False
        self.state = bstack1lllllll1ll_opy_
        self.bstack1llll1ll1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11llllll1l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1l1ll111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1ll1l1_opy_: int = None
    bstack1l1l1l1llll_opy_: str = None
    bstack11ll111_opy_: str = None
    bstack11l1ll11l_opy_: str = None
    bstack1l1ll1l111l_opy_: str = None
    bstack1l111l1lll1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l1111l1_opy_ = bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᖫ")
    bstack1l11l1111ll_opy_ = bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᖬ")
    bstack1ll11lll1l1_opy_ = bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᖭ")
    bstack1l1111l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᖮ")
    bstack11llllll11l_opy_ = bstack1l11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᖯ")
    bstack1l11llll1l1_opy_ = bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᖰ")
    bstack1l1l1ll111l_opy_ = bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᖱ")
    bstack1l1l1lllll1_opy_ = bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᖲ")
    bstack1l1lll1lll1_opy_ = bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᖳ")
    bstack1l1111111ll_opy_ = bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᖴ")
    bstack1ll11l11ll1_opy_ = bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᖵ")
    bstack1l1ll1ll1ll_opy_ = bstack1l11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᖶ")
    bstack1l111l1l11l_opy_ = bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᖷ")
    bstack1l1l1l11ll1_opy_ = bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᖸ")
    bstack1ll11l1l11l_opy_ = bstack1l11l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᖹ")
    bstack1l1l11111ll_opy_ = bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᖺ")
    bstack1l1111l111l_opy_ = bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᖻ")
    bstack1l111llll1l_opy_ = bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᖼ")
    bstack1l111l1ll1l_opy_ = bstack1l11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᖽ")
    bstack11lllll11ll_opy_ = bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᖾ")
    bstack1l11l1lll11_opy_ = bstack1l11l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᖿ")
    bstack1l111ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᗀ")
    bstack1l11111l111_opy_ = bstack1l11l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᗁ")
    bstack1l111lllll1_opy_ = bstack1l11l11_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨᗂ")
    bstack1l11111l1l1_opy_ = bstack1l11l11_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦᗃ")
    bstack11llllll1ll_opy_ = bstack1l11l11_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥᗄ")
    bstack1l111l1111l_opy_ = bstack1l11l11_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦᗅ")
    bstack1l1111llll1_opy_ = bstack1l11l11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᗆ")
    bstack1l111111ll1_opy_ = bstack1l11l11_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᗇ")
    bstack1l1111111l1_opy_ = bstack1l11l11_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᗈ")
    bstack1l111llll11_opy_ = bstack1l11l11_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᗉ")
    bstack1l1l1lll11l_opy_ = bstack1l11l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᗊ")
    bstack1l1ll11l111_opy_ = bstack1l11l11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᗋ")
    bstack1l1ll1lll11_opy_ = bstack1l11l11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᗌ")
    bstack1llll1ll1ll_opy_: Dict[str, bstack1lll11l1l11_opy_] = dict()
    bstack11llll1l11l_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll111ll11l_opy_: List[str]
    bstack1l11l111111_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll111ll11l_opy_: List[str],
        bstack1l11l111111_opy_: Dict[str, str],
        bstack111111l1l1_opy_: bstack1111111lll_opy_
    ):
        self.bstack1ll111ll11l_opy_ = bstack1ll111ll11l_opy_
        self.bstack1l11l111111_opy_ = bstack1l11l111111_opy_
        self.bstack111111l1l1_opy_ = bstack111111l1l1_opy_
    def track_event(
        self,
        context: bstack11llllll1l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1lll1llll11_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᗍ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111l11111_opy_(
        self,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l11l111_opy_ = TestFramework.bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_)
        if not bstack1l11l11l111_opy_ in TestFramework.bstack11llll1l11l_opy_:
            return
        self.logger.debug(bstack1l11l11_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᗎ").format(len(TestFramework.bstack11llll1l11l_opy_[bstack1l11l11l111_opy_])))
        for callback in TestFramework.bstack11llll1l11l_opy_[bstack1l11l11l111_opy_]:
            try:
                callback(self, instance, bstack1llllll11l1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l11l11_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦᗏ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll1l1ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1l1ll11ll_opy_(self, instance, bstack1llllll11l1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1ll11ll11_opy_(self, instance, bstack1llllll11l1_opy_):
        return
    @staticmethod
    def bstack1lllll11l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llllll1ll1_opy_.create_context(target)
        instance = TestFramework.bstack1llll1ll1ll_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllll11ll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l1llll1l_opy_(reverse=True) -> List[bstack1lll11l1l11_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llll1ll1ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll11l11_opy_(ctx: bstack1llll1lllll_opy_, reverse=True) -> List[bstack1lll11l1l11_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llll1ll1ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1llll_opy_(instance: bstack1lll11l1l11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllllll11l_opy_(instance: bstack1lll11l1l11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllll1l11l_opy_(instance: bstack1lll11l1l11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᗐ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111lll11l_opy_(instance: bstack1lll11l1l11_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l11l11_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᗑ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll111ll_opy_(instance: bstack1lll1l1lll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11l11_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᗒ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        return TestFramework.bstack1lllllll11l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l11lll_opy_(instance: bstack1lll11l1l11_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l1111ll111_opy_(instance: bstack1lll11l1l11_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_]):
        return bstack1l11l11_opy_ (u"ࠣ࠼ࠥᗓ").join((bstack1lll1l1lll1_opy_(bstack1llllll11l1_opy_[0]).name, bstack1lll1llll11_opy_(bstack1llllll11l1_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111l11_opy_(bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_], callback: Callable):
        bstack1l11l11l111_opy_ = TestFramework.bstack1l11l11lll1_opy_(bstack1llllll11l1_opy_)
        TestFramework.logger.debug(bstack1l11l11_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᗔ").format(bstack1l11l11l111_opy_))
        if not bstack1l11l11l111_opy_ in TestFramework.bstack11llll1l11l_opy_:
            TestFramework.bstack11llll1l11l_opy_[bstack1l11l11l111_opy_] = []
        TestFramework.bstack11llll1l11l_opy_[bstack1l11l11l111_opy_].append(callback)
    @staticmethod
    def bstack1l1ll111111_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l11l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᗕ"):
            return klass.__qualname__
        return module + bstack1l11l11_opy_ (u"ࠦ࠳ࠨᗖ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll1ll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}