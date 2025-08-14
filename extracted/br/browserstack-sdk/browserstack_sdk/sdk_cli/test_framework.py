# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111l1l1_opy_ import bstack111111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1llll1ll11l_opy_, bstack1lllll11111_opy_
class bstack1lll1ll1ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1l1ll_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᖰ").format(self.name)
class bstack1lll111l111_opy_(Enum):
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
        return bstack1l1l1ll_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᖱ").format(self.name)
class bstack1ll1ll111ll_opy_(bstack1llll1ll11l_opy_):
    bstack1ll111l11l1_opy_: List[str]
    bstack1l111llll1l_opy_: Dict[str, str]
    state: bstack1lll111l111_opy_
    bstack1lllll1ll1l_opy_: datetime
    bstack1llllllll1l_opy_: datetime
    def __init__(
        self,
        context: bstack1lllll11111_opy_,
        bstack1ll111l11l1_opy_: List[str],
        bstack1l111llll1l_opy_: Dict[str, str],
        state=bstack1lll111l111_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll111l11l1_opy_ = bstack1ll111l11l1_opy_
        self.bstack1l111llll1l_opy_ = bstack1l111llll1l_opy_
        self.state = state
        self.bstack1lllll1ll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llllllll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllll111_opy_(self, bstack1lllll1111l_opy_: bstack1lll111l111_opy_):
        bstack1lllll111ll_opy_ = bstack1lll111l111_opy_(bstack1lllll1111l_opy_).name
        if not bstack1lllll111ll_opy_:
            return False
        if bstack1lllll1111l_opy_ == self.state:
            return False
        self.state = bstack1lllll1111l_opy_
        self.bstack1llllllll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l1111ll11l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1ll1l1ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1ll1lll11_opy_: int = None
    bstack1l1ll11l1ll_opy_: str = None
    bstack11l1l1_opy_: str = None
    bstack1llllllll1_opy_: str = None
    bstack1l1ll1ll1l1_opy_: str = None
    bstack1l1111l1l11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11ll1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᖲ")
    bstack1l111ll1l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᖳ")
    bstack1ll11l11111_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᖴ")
    bstack11lllll1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᖵ")
    bstack1l111l11lll_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᖶ")
    bstack1l11lllll11_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᖷ")
    bstack1l1ll11ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᖸ")
    bstack1l1l1lll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᖹ")
    bstack1l1ll111l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᖺ")
    bstack1l1111llll1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᖻ")
    bstack1ll11ll1ll1_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᖼ")
    bstack1l1ll1ll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᖽ")
    bstack1l111ll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᖾ")
    bstack1l1l1l111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᖿ")
    bstack1ll1l11l1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᗀ")
    bstack1l1l111111l_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᗁ")
    bstack1l111lll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᗂ")
    bstack1l11l11l111_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᗃ")
    bstack11llllllll1_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᗄ")
    bstack11lllll11ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᗅ")
    bstack1l11l1ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᗆ")
    bstack1l111llll11_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᗇ")
    bstack1l111l111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᗈ")
    bstack1l111lll111_opy_ = bstack1l1l1ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨᗉ")
    bstack11llllll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷࠦᗊ")
    bstack1l11111ll11_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵࠥᗋ")
    bstack11llllll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠦᗌ")
    bstack1l11111llll_opy_ = bstack1l1l1ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᗍ")
    bstack1l111ll1lll_opy_ = bstack1l1l1ll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᗎ")
    bstack1l111lll1ll_opy_ = bstack1l1l1ll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᗏ")
    bstack1l11l111111_opy_ = bstack1l1l1ll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᗐ")
    bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣᗑ")
    bstack1l1ll11111l_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤᗒ")
    bstack1l1l1ll1111_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᗓ")
    bstack1111111111_opy_: Dict[str, bstack1ll1ll111ll_opy_] = dict()
    bstack11lllll1111_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll111l11l1_opy_: List[str]
    bstack1l111llll1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll111l11l1_opy_: List[str],
        bstack1l111llll1l_opy_: Dict[str, str],
        bstack111111l1l1_opy_: bstack111111ll11_opy_
    ):
        self.bstack1ll111l11l1_opy_ = bstack1ll111l11l1_opy_
        self.bstack1l111llll1l_opy_ = bstack1l111llll1l_opy_
        self.bstack111111l1l1_opy_ = bstack111111l1l1_opy_
    def track_event(
        self,
        context: bstack1l1111ll11l_opy_,
        test_framework_state: bstack1lll111l111_opy_,
        test_hook_state: bstack1lll1ll1ll1_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨᗔ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l11111111l_opy_(
        self,
        instance: bstack1ll1ll111ll_opy_,
        bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l1l11l1_opy_ = TestFramework.bstack1l11l11l11l_opy_(bstack111111111l_opy_)
        if not bstack1l11l1l11l1_opy_ in TestFramework.bstack11lllll1111_opy_:
            return
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦᗕ").format(len(TestFramework.bstack11lllll1111_opy_[bstack1l11l1l11l1_opy_])))
        for callback in TestFramework.bstack11lllll1111_opy_[bstack1l11l1l11l1_opy_]:
            try:
                callback(self, instance, bstack111111111l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1l1ll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦᗖ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1ll11llll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1lll1111l_opy_(self, instance, bstack111111111l_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll11l1l_opy_(self, instance, bstack111111111l_opy_):
        return
    @staticmethod
    def bstack1lllllll11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1llll1ll11l_opy_.create_context(target)
        instance = TestFramework.bstack1111111111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llllll111l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1llll111l_opy_(reverse=True) -> List[bstack1ll1ll111ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1ll11_opy_(ctx: bstack1lllll11111_opy_, reverse=True) -> List[bstack1ll1ll111ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1111111111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1ll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll11ll_opy_(instance: bstack1ll1ll111ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll1llll1_opy_(instance: bstack1ll1ll111ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllll111_opy_(instance: bstack1ll1ll111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤᗗ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11lllllllll_opy_(instance: bstack1ll1ll111ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨᗘ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll11ll1_opy_(instance: bstack1lll111l111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᗙ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lllllll11l_opy_(target, strict)
        return TestFramework.bstack1llll1llll1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lllllll11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l111l1llll_opy_(instance: bstack1ll1ll111ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l1111111l1_opy_(instance: bstack1ll1ll111ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l11l11l_opy_(bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_]):
        return bstack1l1l1ll_opy_ (u"ࠣ࠼ࠥᗚ").join((bstack1lll111l111_opy_(bstack111111111l_opy_[0]).name, bstack1lll1ll1ll1_opy_(bstack111111111l_opy_[1]).name))
    @staticmethod
    def bstack1ll1l11lll1_opy_(bstack111111111l_opy_: Tuple[bstack1lll111l111_opy_, bstack1lll1ll1ll1_opy_], callback: Callable):
        bstack1l11l1l11l1_opy_ = TestFramework.bstack1l11l11l11l_opy_(bstack111111111l_opy_)
        TestFramework.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢᗛ").format(bstack1l11l1l11l1_opy_))
        if not bstack1l11l1l11l1_opy_ in TestFramework.bstack11lllll1111_opy_:
            TestFramework.bstack11lllll1111_opy_[bstack1l11l1l11l1_opy_] = []
        TestFramework.bstack11lllll1111_opy_[bstack1l11l1l11l1_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1111ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1l1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧᗜ"):
            return klass.__qualname__
        return module + bstack1l1l1ll_opy_ (u"ࠦ࠳ࠨᗝ") + klass.__qualname__
    @staticmethod
    def bstack1l1ll11l11l_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}