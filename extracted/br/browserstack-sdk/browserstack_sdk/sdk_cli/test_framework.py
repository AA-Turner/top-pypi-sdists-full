# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack111111ll11_opy_ import bstack111111llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1lllll11l11_opy_, bstack1lllll1l1l1_opy_
class bstack1ll1lllll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1ll1_opy_ (u"ࠤࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᕫ").format(self.name)
class bstack1ll1llll111_opy_(Enum):
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
        return bstack1l1ll1_opy_ (u"ࠥࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᕬ").format(self.name)
class bstack1ll1llllll1_opy_(bstack1lllll11l11_opy_):
    bstack1ll1l11l11l_opy_: List[str]
    bstack1l11l111lll_opy_: Dict[str, str]
    state: bstack1ll1llll111_opy_
    bstack1llllllllll_opy_: datetime
    bstack1llll1lll11_opy_: datetime
    def __init__(
        self,
        context: bstack1lllll1l1l1_opy_,
        bstack1ll1l11l11l_opy_: List[str],
        bstack1l11l111lll_opy_: Dict[str, str],
        state=bstack1ll1llll111_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l11l11l_opy_ = bstack1ll1l11l11l_opy_
        self.bstack1l11l111lll_opy_ = bstack1l11l111lll_opy_
        self.state = state
        self.bstack1llllllllll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llll1lll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllll1ll_opy_(self, bstack1llll1lllll_opy_: bstack1ll1llll111_opy_):
        bstack11111111ll_opy_ = bstack1ll1llll111_opy_(bstack1llll1lllll_opy_).name
        if not bstack11111111ll_opy_:
            return False
        if bstack1llll1lllll_opy_ == self.state:
            return False
        self.state = bstack1llll1lllll_opy_
        self.bstack1llll1lll11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111lll1ll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1lll11ll111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l1ll1l1l_opy_: int = None
    bstack1l1l1ll1lll_opy_: str = None
    bstack1llllll1_opy_: str = None
    bstack1l11l11l1_opy_: str = None
    bstack1l1ll1l1lll_opy_: str = None
    bstack1l1111ll11l_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11l1l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠢᕭ")
    bstack1l1111lllll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡭ࡩࠨᕮ")
    bstack1ll11llllll_opy_ = bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠤᕯ")
    bstack1l1111l1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠣᕰ")
    bstack1l11111ll1l_opy_ = bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡴࡢࡩࡶࠦᕱ")
    bstack1l1l111l11l_opy_ = bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᕲ")
    bstack1l1ll1ll111_opy_ = bstack1l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡷࡺࡲࡴࡠࡣࡷࠦᕳ")
    bstack1l1ll111lll_opy_ = bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᕴ")
    bstack1l1ll1111ll_opy_ = bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧᕵ")
    bstack1l111lll111_opy_ = bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡣࡢࡶ࡬ࡳࡳࠨᕶ")
    bstack1ll1l11l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࠨᕷ")
    bstack1l1ll1ll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠥᕸ")
    bstack1l11l11111l_opy_ = bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡤࡱࡧࡩࠧᕹ")
    bstack1l1l1l1ll1l_opy_ = bstack1l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠧᕺ")
    bstack1ll11l1l111_opy_ = bstack1l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࠧᕻ")
    bstack1l1l11l1111_opy_ = bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࠦᕼ")
    bstack1l111ll1ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠥᕽ")
    bstack1l1111ll1l1_opy_ = bstack1l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡲ࡯ࡨࡵࠥᕾ")
    bstack1l111l111l1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡭ࡦࡶࡤࠦᕿ")
    bstack11lllllll11_opy_ = bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡴࡥࡲࡴࡪࡹࠧᖀ")
    bstack1l11l1lll1l_opy_ = bstack1l1ll1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦᖁ")
    bstack1l11l11l111_opy_ = bstack1l1ll1_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᖂ")
    bstack1l1111l11ll_opy_ = bstack1l1ll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡪࡴࡤࡦࡦࡢࡥࡹࠨᖃ")
    bstack1l111ll1l11_opy_ = bstack1l1ll1_opy_ (u"ࠨࡨࡰࡱ࡮ࡣ࡮ࡪࠢᖄ")
    bstack1l1111l1111_opy_ = bstack1l1ll1_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡸࡥࡴࡷ࡯ࡸࠧᖅ")
    bstack1l1111lll11_opy_ = bstack1l1ll1_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡬ࡰࡩࡶࠦᖆ")
    bstack1l1111ll111_opy_ = bstack1l1ll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠧᖇ")
    bstack1l11l111l11_opy_ = bstack1l1ll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᖈ")
    bstack1l11l11l11l_opy_ = bstack1l1ll1_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᖉ")
    bstack11llllllll1_opy_ = bstack1l1ll1_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨᖊ")
    bstack1l111l11l1l_opy_ = bstack1l1ll1_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢᖋ")
    bstack1l1ll1ll11l_opy_ = bstack1l1ll1_opy_ (u"ࠢࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠤᖌ")
    bstack1l1lll111l1_opy_ = bstack1l1ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡌࡐࡉࠥᖍ")
    bstack1l1ll1llll1_opy_ = bstack1l1ll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᖎ")
    bstack1llllll1ll1_opy_: Dict[str, bstack1ll1llllll1_opy_] = dict()
    bstack11llll1lll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l11l11l_opy_: List[str]
    bstack1l11l111lll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l11l11l_opy_: List[str],
        bstack1l11l111lll_opy_: Dict[str, str],
        bstack111111ll11_opy_: bstack111111llll_opy_
    ):
        self.bstack1ll1l11l11l_opy_ = bstack1ll1l11l11l_opy_
        self.bstack1l11l111lll_opy_ = bstack1l11l111lll_opy_
        self.bstack111111ll11_opy_ = bstack111111ll11_opy_
    def track_event(
        self,
        context: bstack1l111lll1ll_opy_,
        test_framework_state: bstack1ll1llll111_opy_,
        test_hook_state: bstack1ll1lllll1l_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࢁࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡥࡷ࡭ࡳ࠾ࡽࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࢃࠢᖏ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111ll11ll_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l1l1l1l_opy_ = TestFramework.bstack1l11l11llll_opy_(bstack1llllll1111_opy_)
        if not bstack1l11l1l1l1l_opy_ in TestFramework.bstack11llll1lll1_opy_:
            return
        self.logger.debug(bstack1l1ll1_opy_ (u"ࠦ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡻࡾࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࡷࠧᖐ").format(len(TestFramework.bstack11llll1lll1_opy_[bstack1l11l1l1l1l_opy_])))
        for callback in TestFramework.bstack11llll1lll1_opy_[bstack1l11l1l1l1l_opy_]:
            try:
                callback(self, instance, bstack1llllll1111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1ll1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡾࢁࠧᖑ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lll1l111_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1llll11l1_opy_(self, instance, bstack1llllll1111_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll11ll1_opy_(self, instance, bstack1llllll1111_opy_):
        return
    @staticmethod
    def bstack1llllllll1l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lllll11l11_opy_.create_context(target)
        instance = TestFramework.bstack1llllll1ll1_opy_.get(ctx.id, None)
        if instance and instance.bstack11111111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll1l11ll_opy_(reverse=True) -> List[bstack1ll1llllll1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1llllll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1llllllllll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1l1l_opy_(ctx: bstack1lllll1l1l1_opy_, reverse=True) -> List[bstack1ll1llllll1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1llllll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1llllllllll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1ll1l_opy_(instance: bstack1ll1llllll1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111l111_opy_(instance: bstack1ll1llllll1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllll1ll_opy_(instance: bstack1ll1llllll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1ll1_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡ࡭ࡨࡽࡂࢁࡽࠡࡸࡤࡰࡺ࡫࠽ࡼࡿࠥᖒ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11111ll11_opy_(instance: bstack1ll1llllll1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1ll1_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧࡢࡩࡳࡺࡲࡪࡧࡶ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣࡩࡳࡺࡲࡪࡧࡶࡁࢀࢃࠢᖓ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll1ll11_opy_(instance: bstack1ll1llll111_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡷࡳࡨࡦࡺࡥࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᖔ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llllllll1l_opy_(target, strict)
        return TestFramework.bstack111111l111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llllllll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111l1l_opy_(instance: bstack1ll1llllll1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111lll1l1_opy_(instance: bstack1ll1llllll1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l11llll_opy_(bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_]):
        return bstack1l1ll1_opy_ (u"ࠤ࠽ࠦᖕ").join((bstack1ll1llll111_opy_(bstack1llllll1111_opy_[0]).name, bstack1ll1lllll1l_opy_(bstack1llllll1111_opy_[1]).name))
    @staticmethod
    def bstack1ll11llll11_opy_(bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_], callback: Callable):
        bstack1l11l1l1l1l_opy_ = TestFramework.bstack1l11l11llll_opy_(bstack1llllll1111_opy_)
        TestFramework.logger.debug(bstack1l1ll1_opy_ (u"ࠥࡷࡪࡺ࡟ࡩࡱࡲ࡯ࡤࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡪࡲࡳࡰࡥࡲࡦࡩ࡬ࡷࡹࡸࡹࡠ࡭ࡨࡽࡂࢁࡽࠣᖖ").format(bstack1l11l1l1l1l_opy_))
        if not bstack1l11l1l1l1l_opy_ in TestFramework.bstack11llll1lll1_opy_:
            TestFramework.bstack11llll1lll1_opy_[bstack1l11l1l1l1l_opy_] = []
        TestFramework.bstack11llll1lll1_opy_[bstack1l11l1l1l1l_opy_].append(callback)
    @staticmethod
    def bstack1l1l1lll1ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡶ࡬ࡲࡸࠨᖗ"):
            return klass.__qualname__
        return module + bstack1l1ll1_opy_ (u"ࠧ࠴ࠢᖘ") + klass.__qualname__
    @staticmethod
    def bstack1l1lll1l1l1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}