# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack11111111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll111l_opy_ import bstack1llll1lll11_opy_, bstack1llll1lllll_opy_
class bstack1lll111l1l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l11ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᖳ").format(self.name)
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
        return bstack1l11ll1_opy_ (u"࡚ࠧࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᖴ").format(self.name)
class bstack1lll11l1111_opy_(bstack1llll1lll11_opy_):
    bstack1ll111ll1l1_opy_: List[str]
    bstack11lllll111l_opy_: Dict[str, str]
    state: bstack1ll1ll11l1l_opy_
    bstack1lllll1l1ll_opy_: datetime
    bstack1lllll11lll_opy_: datetime
    def __init__(
        self,
        context: bstack1llll1lllll_opy_,
        bstack1ll111ll1l1_opy_: List[str],
        bstack11lllll111l_opy_: Dict[str, str],
        state=bstack1ll1ll11l1l_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll111ll1l1_opy_ = bstack1ll111ll1l1_opy_
        self.bstack11lllll111l_opy_ = bstack11lllll111l_opy_
        self.state = state
        self.bstack1lllll1l1ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll11lll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llllll1ll1_opy_(self, bstack1lllllllll1_opy_: bstack1ll1ll11l1l_opy_):
        bstack1llll1l1lll_opy_ = bstack1ll1ll11l1l_opy_(bstack1lllllllll1_opy_).name
        if not bstack1llll1l1lll_opy_:
            return False
        if bstack1lllllllll1_opy_ == self.state:
            return False
        self.state = bstack1lllllllll1_opy_
        self.bstack1lllll11lll_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l1l11l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lll1l11_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1l111l_opy_: int = None
    bstack1l1ll1l1l11_opy_: str = None
    bstack111l111_opy_: str = None
    bstack111ll11l_opy_: str = None
    bstack1l1l1ll1l1l_opy_: str = None
    bstack1l1111111ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll111ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤᖵ")
    bstack1l11l11111l_opy_ = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡯ࡤࠣᖶ")
    bstack1ll11llll1l_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠦᖷ")
    bstack1l111111l11_opy_ = bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠥᖸ")
    bstack1l111ll111l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡶࡤ࡫ࡸࠨᖹ")
    bstack1l1l1111ll1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡩࡸࡻ࡬ࡵࠤᖺ")
    bstack1l1ll1ll111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࡢࡥࡹࠨᖻ")
    bstack1l1l1lll11l_opy_ = bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᖼ")
    bstack1l1ll1lll11_opy_ = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᖽ")
    bstack11lllll11l1_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᖾ")
    bstack1ll1l111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠣᖿ")
    bstack1l1l1l1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᗀ")
    bstack11lllll1ll1_opy_ = bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡦࡳࡩ࡫ࠢᗁ")
    bstack1l1l1l111l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠢᗂ")
    bstack1ll1111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᗃ")
    bstack1l1l1111l11_opy_ = bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡡࡪ࡮ࡸࡶࡪࠨᗄ")
    bstack1l11111l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠧᗅ")
    bstack1l111llll1l_opy_ = bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡪࡷࠧᗆ")
    bstack1l111l1ll1l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡯ࡨࡸࡦࠨᗇ")
    bstack11llll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡶࡧࡴࡶࡥࡴࠩᗈ")
    bstack1l11l1l11l1_opy_ = bstack1l11ll1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡰࡤࡱࡪࠨᗉ")
    bstack1l111l111ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᗊ")
    bstack11lllllll11_opy_ = bstack1l11ll1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᗋ")
    bstack1l11111ll11_opy_ = bstack1l11ll1_opy_ (u"ࠣࡪࡲࡳࡰࡥࡩࡥࠤᗌ")
    bstack1l111ll1111_opy_ = bstack1l11ll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡳࡧࡶࡹࡱࡺࠢᗍ")
    bstack1l1111ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡮ࡲ࡫ࡸࠨᗎ")
    bstack1l11111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠢᗏ")
    bstack1l111111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᗐ")
    bstack11lllll11ll_opy_ = bstack1l11ll1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᗑ")
    bstack1l111111lll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣᗒ")
    bstack1l111l1ll11_opy_ = bstack1l11ll1_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᗓ")
    bstack1l1ll1ll1ll_opy_ = bstack1l11ll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠦᗔ")
    bstack1l1ll1l1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡎࡒࡋࠧᗕ")
    bstack1l1ll11lll1_opy_ = bstack1l11ll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᗖ")
    bstack1llllll1lll_opy_: Dict[str, bstack1lll11l1111_opy_] = dict()
    bstack11llll1l111_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll111ll1l1_opy_: List[str]
    bstack11lllll111l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll111ll1l1_opy_: List[str],
        bstack11lllll111l_opy_: Dict[str, str],
        bstack1111111ll1_opy_: bstack11111111ll_opy_
    ):
        self.bstack1ll111ll1l1_opy_ = bstack1ll111ll1l1_opy_
        self.bstack11lllll111l_opy_ = bstack11lllll111l_opy_
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
    def track_event(
        self,
        context: bstack1l111l1l11l_opy_,
        test_framework_state: bstack1ll1ll11l1l_opy_,
        test_hook_state: bstack1lll111l1l1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡧࡲࡨࡵࡀࡿࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻࡾࠤᗗ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111ll1l11_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll1l111_opy_:
            return
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡽࢀࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡹࠢᗘ").format(len(TestFramework.bstack11llll1l111_opy_[bstack1l11l111l11_opy_])))
        for callback in TestFramework.bstack11llll1l111_opy_[bstack1l11l111l11_opy_]:
            try:
                callback(self, instance, bstack1lllll1llll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᗙ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll11111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1l1ll11ll_opy_(self, instance, bstack1lllll1llll_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l1ll111l_opy_(self, instance, bstack1lllll1llll_opy_):
        return
    @staticmethod
    def bstack1lllll11l1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llll1lll11_opy_.create_context(target)
        instance = TestFramework.bstack1llllll1lll_opy_.get(ctx.id, None)
        if instance and instance.bstack1111111111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1lll1ll11_opy_(reverse=True) -> List[bstack1lll11l1111_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllll1lll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllllll1l1_opy_(ctx: bstack1llll1lllll_opy_, reverse=True) -> List[bstack1lll11l1111_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllll1lll_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll11l11_opy_(instance: bstack1lll11l1111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllllllll_opy_(instance: bstack1lll11l1111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llllll1ll1_opy_(instance: bstack1lll11l1111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᗚ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l111l1_opy_(instance: bstack1lll11l1111_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥ࡫࡮ࡵࡴ࡬ࡩࡸࡃࡻࡾࠤᗛ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll11111_opy_(instance: bstack1ll1ll11l1l_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡹࡵࡪࡡࡵࡧࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᗜ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        return TestFramework.bstack1llllllllll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllll11l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111lllll1_opy_(instance: bstack1lll11l1111_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111lll111_opy_(instance: bstack1lll11l1111_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_]):
        return bstack1l11ll1_opy_ (u"ࠦ࠿ࠨᗝ").join((bstack1ll1ll11l1l_opy_(bstack1lllll1llll_opy_[0]).name, bstack1lll111l1l1_opy_(bstack1lllll1llll_opy_[1]).name))
    @staticmethod
    def bstack1ll11ll111l_opy_(bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l11l11l_opy_(bstack1lllll1llll_opy_)
        TestFramework.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡥࡵࡡ࡫ࡳࡴࡱ࡟ࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣ࡬ࡴࡵ࡫ࡠࡴࡨ࡫࡮ࡹࡴࡳࡻࡢ࡯ࡪࡿ࠽ࡼࡿࠥᗞ").format(bstack1l11l111l11_opy_))
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll1l111_opy_:
            TestFramework.bstack11llll1l111_opy_[bstack1l11l111l11_opy_] = []
        TestFramework.bstack11llll1l111_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1l1ll111ll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡸ࡮ࡴࡳࠣᗟ"):
            return klass.__qualname__
        return module + bstack1l11ll1_opy_ (u"ࠢ࠯ࠤᗠ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll111111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}