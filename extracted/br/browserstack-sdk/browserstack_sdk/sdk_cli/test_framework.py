# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1llll1l1l1l_opy_ import bstack1ll1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1lll_opy_ import bstack1l1lll111ll_opy_, bstack1ll1ll1l11l_opy_
class bstack1lll1lll1ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1111_opy_ (u"ࠢࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᐒ").format(self.name)
class bstack1lllll11l11_opy_(Enum):
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
        return bstack11l1111_opy_ (u"ࠣࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᐓ").format(self.name)
class bstack1lllll111ll_opy_(bstack1l1lll111ll_opy_):
    bstack1l1l1lll111_opy_: List[str]
    bstack1l1lll1l11l_opy_: Dict[str, str]
    state: bstack1lllll11l11_opy_
    bstack1ll1lll1l11_opy_: datetime
    bstack1l1l111ll11_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll1l11l_opy_,
        bstack1l1l1lll111_opy_: List[str],
        bstack1l1lll1l11l_opy_: Dict[str, str],
        state=bstack1lllll11l11_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1l1lll111_opy_ = bstack1l1l1lll111_opy_
        self.bstack1l1lll1l11l_opy_ = bstack1l1lll1l11l_opy_
        self.state = state
        self.bstack1ll1lll1l11_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1l111ll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll111l11_opy_(self, bstack1l1l111l1l1_opy_: bstack1lllll11l11_opy_):
        bstack1l1l111ll1l_opy_ = bstack1lllll11l11_opy_(bstack1l1l111l1l1_opy_).name
        if not bstack1l1l111ll1l_opy_:
            return False
        if bstack1l1l111l1l1_opy_ == self.state:
            return False
        self.state = bstack1l1l111l1l1_opy_
        self.bstack1l1l111ll11_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l1l1l1l1l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1llll11ll1l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack111111l1l1_opy_: int = None
    bstack1llll1l1111_opy_: str = None
    bstack1ll1l_opy_: str = None
    bstack1l1111111_opy_: str = None
    bstack1llll111111_opy_: str = None
    bstack1l1ll11l1l1_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll1l1ll1l_opy_ = bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧᐔ")
    bstack1l1ll11l111_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡫ࡧࠦᐕ")
    bstack1lll11lllll_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠢᐖ")
    bstack1l1l1l1l11l_opy_ = bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭ࠨᐗ")
    bstack1l1lll1ll1l_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡹࡧࡧࡴࠤᐘ")
    bstack1ll1l11l111_opy_ = bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࠧᐙ")
    bstack11111111l1_opy_ = bstack11l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࡥࡡࡵࠤᐚ")
    bstack1lllll1ll1l_opy_ = bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᐛ")
    bstack1lll1lll111_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᐜ")
    bstack1l1l1ll1l1l_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᐝ")
    bstack1lll1ll1l11_opy_ = bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠦᐞ")
    bstack1lll1l11ll1_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣᐟ")
    bstack1l1ll1l1l1l_opy_ = bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡩ࡯ࡥࡧࠥᐠ")
    bstack1lll11l1l1l_opy_ = bstack11l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠥᐡ")
    bstack1llllll1lll_opy_ = bstack11l1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࠥᐢ")
    bstack1ll1l111l11_opy_ = bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࠤᐣ")
    bstack1l1ll1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠣᐤ")
    bstack1l1l1l111l1_opy_ = bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴ࡭ࡳࠣᐥ")
    bstack1l1ll111lll_opy_ = bstack11l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡲ࡫ࡴࡢࠤᐦ")
    bstack1l1l11lll1l_opy_ = bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡹࡣࡰࡲࡨࡷࠬᐧ")
    bstack1ll1111lll1_opy_ = bstack11l1111_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࡢࡷࡪࡹࡳࡪࡱࡱࡣࡳࡧ࡭ࡦࠤᐨ")
    bstack1l1l1l1ll11_opy_ = bstack11l1111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᐩ")
    bstack1l1lll11l1l_opy_ = bstack11l1111_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᐪ")
    bstack1l1l1l11lll_opy_ = bstack11l1111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡬ࡨࠧᐫ")
    bstack1l1lll1lll1_opy_ = bstack11l1111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡶࡪࡹࡵ࡭ࡶࠥᐬ")
    bstack1l1l1ll1ll1_opy_ = bstack11l1111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡱࡵࡧࡴࠤᐭ")
    bstack1l1lll111l1_opy_ = bstack11l1111_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠥᐮ")
    bstack1l1ll11ll11_opy_ = bstack11l1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᐯ")
    bstack1l1llll1111_opy_ = bstack11l1111_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᐰ")
    bstack1l1lll11ll1_opy_ = bstack11l1111_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᐱ")
    bstack1l1ll111111_opy_ = bstack11l1111_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧᐲ")
    bstack1llll1l1lll_opy_ = bstack11l1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠢᐳ")
    bstack1lllllll11l_opy_ = bstack11l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡑࡕࡇࠣᐴ")
    bstack1llll1l1l11_opy_ = bstack11l1111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᐵ")
    bstack1ll11llllll_opy_: Dict[str, bstack1lllll111ll_opy_] = dict()
    bstack1l1l11l11ll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l1lll111_opy_: List[str]
    bstack1l1lll1l11l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1l1lll111_opy_: List[str],
        bstack1l1lll1l11l_opy_: Dict[str, str],
        bstack1llll1l1l1l_opy_: bstack1ll1llllll1_opy_
    ):
        self.bstack1l1l1lll111_opy_ = bstack1l1l1lll111_opy_
        self.bstack1l1lll1l11l_opy_ = bstack1l1lll1l11l_opy_
        self.bstack1llll1l1l1l_opy_ = bstack1llll1l1l1l_opy_
    def track_event(
        self,
        context: bstack1l1l1l1l1l1_opy_,
        test_framework_state: bstack1lllll11l11_opy_,
        test_hook_state: bstack1lll1lll1ll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1111_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡣࡵ࡫ࡸࡃࡻࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾࢁࠧᐶ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l1l1l1ll1l_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11111111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        if not bstack1ll11111111_opy_ in TestFramework.bstack1l1l11l11ll_opy_:
            return
        self.logger.debug(bstack11l1111_opy_ (u"ࠤ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࢀࢃࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠥᐷ").format(len(TestFramework.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_])))
        for callback in TestFramework.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_]:
            try:
                callback(self, instance, bstack1llll11l111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢ࡬ࡲࡻࡵ࡫ࡪࡰࡪࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡼࡿࠥᐸ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1lllllll1ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1llll11ll11_opy_(self, instance, bstack1llll11l111_opy_):
        return
    @abc.abstractmethod
    def bstack1llll111ll1_opy_(self, instance, bstack1llll11l111_opy_):
        return
    @staticmethod
    def bstack1l1l1lllll1_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1l1lll111ll_opy_.create_context(target)
        instance = TestFramework.bstack1ll11llllll_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1l111l11l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1111111l1l_opy_(reverse=True) -> List[bstack1lllll111ll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1ll11llllll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1111l_opy_(ctx: bstack1ll1ll1l11l_opy_, reverse=True) -> List[bstack1lllll111ll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1ll11llllll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l11_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1ll1_opy_(instance: bstack1lllll111ll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lllll1l11l_opy_(instance: bstack1lllll111ll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll111l11_opy_(instance: bstack1lllll111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1111_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦ࡫ࡦࡻࡀࡿࢂࠦࡶࡢ࡮ࡸࡩࡂࢁࡽࠣᐹ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1ll1111ll_opy_(instance: bstack1lllll111ll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1111_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡽࠡࡧࡱࡸࡷ࡯ࡥࡴ࠿ࡾࢁࠧᐺ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1l111l1ll_opy_(instance: bstack1lllll11l11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1111_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᐻ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1l1l1lllll1_opy_(target, strict)
        return TestFramework.bstack1lllll1l11l_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1l1l1lllll1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1ll1lll11_opy_(instance: bstack1lllll111ll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l1l1ll11ll_opy_(instance: bstack1lllll111ll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_]):
        return bstack11l1111_opy_ (u"ࠢ࠻ࠤᐼ").join((bstack1lllll11l11_opy_(bstack1llll11l111_opy_[0]).name, bstack1lll1lll1ll_opy_(bstack1llll11l111_opy_[1]).name))
    @staticmethod
    def bstack1lllll1llll_opy_(bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_], callback: Callable):
        bstack1ll11111111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(bstack1llll11l111_opy_)
        TestFramework.logger.debug(bstack11l1111_opy_ (u"ࠣࡵࡨࡸࡤ࡮࡯ࡰ࡭ࡢࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡨࡰࡱ࡮ࡣࡷ࡫ࡧࡪࡵࡷࡶࡾࡥ࡫ࡦࡻࡀࡿࢂࠨᐽ").format(bstack1ll11111111_opy_))
        if not bstack1ll11111111_opy_ in TestFramework.bstack1l1l11l11ll_opy_:
            TestFramework.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_] = []
        TestFramework.bstack1l1l11l11ll_opy_[bstack1ll11111111_opy_].append(callback)
    @staticmethod
    def bstack1lll1l11l11_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡴࡪࡰࡶࠦᐾ"):
            return klass.__qualname__
        return module + bstack11l1111_opy_ (u"ࠥ࠲ࠧᐿ") + klass.__qualname__
    @staticmethod
    def bstack1lll1ll11ll_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}