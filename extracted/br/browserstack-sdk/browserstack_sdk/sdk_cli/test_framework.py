# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1llll_opy_, bstack1lll11lll11_opy_
class bstack1ll1l111111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1111_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᚿ").format(self.name)
class bstack1ll1ll111ll_opy_(Enum):
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
        return bstack1l1111_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᛀ").format(self.name)
class bstack1ll111l1lll_opy_(bstack1lll1l1llll_opy_):
    bstack1l1ll1l1l1l_opy_: List[str]
    bstack11ll1l1l11l_opy_: Dict[str, str]
    state: bstack1ll1ll111ll_opy_
    bstack1lll1lll111_opy_: datetime
    bstack1lll11l1111_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11lll11_opy_,
        bstack1l1ll1l1l1l_opy_: List[str],
        bstack11ll1l1l11l_opy_: Dict[str, str],
        state=bstack1ll1ll111ll_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1ll1l1l1l_opy_ = bstack1l1ll1l1l1l_opy_
        self.bstack11ll1l1l11l_opy_ = bstack11ll1l1l11l_opy_
        self.state = state
        self.bstack1lll1lll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll11l1111_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll11l1ll1_opy_(self, bstack1lll11l111l_opy_: bstack1ll1ll111ll_opy_):
        bstack1lll1l1l111_opy_ = bstack1ll1ll111ll_opy_(bstack1lll11l111l_opy_).name
        if not bstack1lll1l1l111_opy_:
            return False
        if bstack1lll11l111l_opy_ == self.state:
            return False
        self.state = bstack1lll11l111l_opy_
        self.bstack1lll11l1111_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11lllll1l11_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll11l1l11l_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11ll1l11l_opy_: int = None
    bstack1l11ll1l1ll_opy_: str = None
    bstack1llllll1_opy_: str = None
    bstack1l1l11l11l_opy_: str = None
    bstack1l1l11lllll_opy_: str = None
    bstack11lll111111_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1lll111ll_opy_ = bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᛁ")
    bstack11lllll111l_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᛂ")
    bstack1l1ll11111l_opy_ = bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᛃ")
    bstack11llll1l11l_opy_ = bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᛄ")
    bstack11lll11l1l1_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᛅ")
    bstack1l111l1l1l1_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᛆ")
    bstack1l1l1111lll_opy_ = bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᛇ")
    bstack1l11lll1l11_opy_ = bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᛈ")
    bstack1l1l11l1l11_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᛉ")
    bstack11lll1l1l11_opy_ = bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᛊ")
    bstack1l1lll1ll1l_opy_ = bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᛋ")
    bstack1l1l1l1111l_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᛌ")
    bstack11ll1l1ll11_opy_ = bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᛍ")
    bstack1l11l1l1111_opy_ = bstack1l1111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᛎ")
    bstack1l1ll1l11ll_opy_ = bstack1l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᛏ")
    bstack1l111l1ll11_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᛐ")
    bstack11lll11lll1_opy_ = bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᛑ")
    bstack11lll111ll1_opy_ = bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᛒ")
    bstack11llll1111l_opy_ = bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᛓ")
    bstack11ll1l111l1_opy_ = bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᛔ")
    bstack1l111111lll_opy_ = bstack1l1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᛕ")
    bstack11lllll1l1l_opy_ = bstack1l1111_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᛖ")
    bstack11ll1ll1ll1_opy_ = bstack1l1111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᛗ")
    bstack11lll1l1lll_opy_ = bstack1l1111_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᛘ")
    bstack11llll11111_opy_ = bstack1l1111_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᛙ")
    bstack11lll1ll11l_opy_ = bstack1l1111_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᛚ")
    bstack11lll111l1l_opy_ = bstack1l1111_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᛛ")
    bstack11lll11ll11_opy_ = bstack1l1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᛜ")
    bstack11llll111l1_opy_ = bstack1l1111_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᛝ")
    bstack11lll1l111l_opy_ = bstack1l1111_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᛞ")
    bstack11lll11l111_opy_ = bstack1l1111_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᛟ")
    bstack1l11ll1lll1_opy_ = bstack1l1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᛠ")
    bstack1l1l11ll11l_opy_ = bstack1l1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᛡ")
    bstack1l1l111l11l_opy_ = bstack1l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᛢ")
    bstack1lll11ll1ll_opy_: Dict[str, bstack1ll111l1lll_opy_] = dict()
    bstack11ll11l111l_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1ll1l1l1l_opy_: List[str]
    bstack11ll1l1l11l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1ll1l1l1l_opy_: List[str],
        bstack11ll1l1l11l_opy_: Dict[str, str],
        bstack1lll1llll1l_opy_: bstack1lll1lllll1_opy_
    ):
        self.bstack1l1ll1l1l1l_opy_ = bstack1l1ll1l1l1l_opy_
        self.bstack11ll1l1l11l_opy_ = bstack11ll1l1l11l_opy_
        self.bstack1lll1llll1l_opy_ = bstack1lll1llll1l_opy_
    def track_event(
        self,
        context: bstack11lllll1l11_opy_,
        test_framework_state: bstack1ll1ll111ll_opy_,
        test_hook_state: bstack1ll1l111111_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1111_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᛣ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11lllll11ll_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        bstack11llllllll1_opy_ = TestFramework.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        if not bstack11llllllll1_opy_ in TestFramework.bstack11ll11l111l_opy_:
            return
        self.logger.debug(bstack1l1111_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᛤ").format(len(TestFramework.bstack11ll11l111l_opy_[bstack11llllllll1_opy_])))
        for callback in TestFramework.bstack11ll11l111l_opy_[bstack11llllllll1_opy_]:
            try:
                callback(self, instance, bstack1lll111llll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᛥ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l11lll11ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11ll11lll_opy_(self, instance, bstack1lll111llll_opy_):
        return
    @abc.abstractmethod
    def bstack1l11lllll11_opy_(self, instance, bstack1lll111llll_opy_):
        return
    @staticmethod
    def bstack1lll11l1lll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lll1l1llll_opy_.create_context(target)
        instance = TestFramework.bstack1lll11ll1ll_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll1l1l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l11ll111_opy_(reverse=True) -> List[bstack1ll111l1lll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll11ll1ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lll1lll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll11l1l11_opy_(ctx: bstack1lll11lll11_opy_, reverse=True) -> List[bstack1ll111l1lll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll11ll1ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lll1lll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll1l11111_opy_(instance: bstack1ll111l1lll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1l11lll_opy_(instance: bstack1ll111l1lll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll11l1ll1_opy_(instance: bstack1ll111l1lll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1111_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᛦ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11llll1llll_opy_(instance: bstack1ll111l1lll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1111_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦᛧ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11ll11l1111_opy_(instance: bstack1ll1ll111ll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1111_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᛨ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lll11l1lll_opy_(target, strict)
        return TestFramework.bstack1lll1l11lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lll11l1lll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11lll1ll111_opy_(instance: bstack1ll111l1lll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11ll1llllll_opy_(instance: bstack1ll111l1lll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11lllllllll_opy_(bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_]):
        return bstack1l1111_opy_ (u"ࠨ࠺ࠣᛩ").join((bstack1ll1ll111ll_opy_(bstack1lll111llll_opy_[0]).name, bstack1ll1l111111_opy_(bstack1lll111llll_opy_[1]).name))
    @staticmethod
    def bstack1l1lll1ll11_opy_(bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_], callback: Callable):
        bstack11llllllll1_opy_ = TestFramework.bstack11lllllllll_opy_(bstack1lll111llll_opy_)
        TestFramework.logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧᛪ").format(bstack11llllllll1_opy_))
        if not bstack11llllllll1_opy_ in TestFramework.bstack11ll11l111l_opy_:
            TestFramework.bstack11ll11l111l_opy_[bstack11llllllll1_opy_] = []
        TestFramework.bstack11ll11l111l_opy_[bstack11llllllll1_opy_].append(callback)
    @staticmethod
    def bstack1l1l11l11ll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥ᛫"):
            return klass.__qualname__
        return module + bstack1l1111_opy_ (u"ࠤ࠱ࠦ᛬") + klass.__qualname__
    @staticmethod
    def bstack1l1l1111111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}