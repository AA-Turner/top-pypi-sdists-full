# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
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
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1111111111_opy_, bstack1llllll111l_opy_
class bstack1ll1lllll11_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll11ll_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᖴ").format(self.name)
class bstack1lll1l1ll11_opy_(Enum):
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
        return bstack1ll11ll_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᖵ").format(self.name)
class bstack1lll11ll1l1_opy_(bstack1111111111_opy_):
    bstack1ll1l111l11_opy_: List[str]
    bstack1l111ll1lll_opy_: Dict[str, str]
    state: bstack1lll1l1ll11_opy_
    bstack1lllll11lll_opy_: datetime
    bstack1lllll1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1llllll111l_opy_,
        bstack1ll1l111l11_opy_: List[str],
        bstack1l111ll1lll_opy_: Dict[str, str],
        state=bstack1lll1l1ll11_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1l111l11_opy_ = bstack1ll1l111l11_opy_
        self.bstack1l111ll1lll_opy_ = bstack1l111ll1lll_opy_
        self.state = state
        self.bstack1lllll11lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll1111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll1l1lll_opy_(self, bstack1llllll1l1l_opy_: bstack1lll1l1ll11_opy_):
        bstack1lllllll11l_opy_ = bstack1lll1l1ll11_opy_(bstack1llllll1l1l_opy_).name
        if not bstack1lllllll11l_opy_:
            return False
        if bstack1llllll1l1l_opy_ == self.state:
            return False
        self.state = bstack1llllll1l1l_opy_
        self.bstack1lllll1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l111l11l1l_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1l1l1ll1_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1l1lll11l_opy_: int = None
    bstack1l1l1ll1ll1_opy_: str = None
    bstack11l111l_opy_: str = None
    bstack1lllllllll_opy_: str = None
    bstack1l1ll11l1ll_opy_: str = None
    bstack11lllll1l11_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll11l1111l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᖶ")
    bstack1l1111l1l11_opy_ = bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᖷ")
    bstack1ll11l111l1_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᖸ")
    bstack11lllllllll_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᖹ")
    bstack1l111llllll_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᖺ")
    bstack1l1l11111l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᖻ")
    bstack1l1ll11ll1l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᖼ")
    bstack1l1lll11111_opy_ = bstack1ll11ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᖽ")
    bstack1l1ll111lll_opy_ = bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᖾ")
    bstack1l1111lll1l_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᖿ")
    bstack1ll11ll111l_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤᗀ")
    bstack1l1ll1l1111_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᗁ")
    bstack1l1111111l1_opy_ = bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣᗂ")
    bstack1l1l1l11ll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣᗃ")
    bstack1ll1111lll1_opy_ = bstack1ll11ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᗄ")
    bstack1l1l111111l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢᗅ")
    bstack1l111llll1l_opy_ = bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨᗆ")
    bstack1l111l1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨᗇ")
    bstack1l1111ll111_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢᗈ")
    bstack11llll1l1ll_opy_ = bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪᗉ")
    bstack1l11l1l11l1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᗊ")
    bstack1l111ll1111_opy_ = bstack1ll11ll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᗋ")
    bstack1l111l11111_opy_ = bstack1ll11ll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᗌ")
    bstack1l111ll11l1_opy_ = bstack1ll11ll_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥᗍ")
    bstack1l11l111111_opy_ = bstack1ll11ll_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣᗎ")
    bstack11llllll111_opy_ = bstack1ll11ll_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢᗏ")
    bstack1l111111l1l_opy_ = bstack1ll11ll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣᗐ")
    bstack1l111111111_opy_ = bstack1ll11ll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᗑ")
    bstack1l111l1l11l_opy_ = bstack1ll11ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᗒ")
    bstack1l1111llll1_opy_ = bstack1ll11ll_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᗓ")
    bstack1l111lll1l1_opy_ = bstack1ll11ll_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᗔ")
    bstack1l1l1l1l111_opy_ = bstack1ll11ll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᗕ")
    bstack1l1ll1l1lll_opy_ = bstack1ll11ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᗖ")
    bstack1l1ll111111_opy_ = bstack1ll11ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᗗ")
    bstack1lllllll111_opy_: Dict[str, bstack1lll11ll1l1_opy_] = dict()
    bstack11llll11ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1l111l11_opy_: List[str]
    bstack1l111ll1lll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1l111l11_opy_: List[str],
        bstack1l111ll1lll_opy_: Dict[str, str],
        bstack1111111ll1_opy_: bstack11111111ll_opy_
    ):
        self.bstack1ll1l111l11_opy_ = bstack1ll1l111l11_opy_
        self.bstack1l111ll1lll_opy_ = bstack1l111ll1lll_opy_
        self.bstack1111111ll1_opy_ = bstack1111111ll1_opy_
    def track_event(
        self,
        context: bstack1l111l11l1l_opy_,
        test_framework_state: bstack1lll1l1ll11_opy_,
        test_hook_state: bstack1ll1lllll11_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᗘ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11llllll11l_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll11ll1_opy_:
            return
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᗙ").format(len(TestFramework.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_])))
        for callback in TestFramework.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_]:
            try:
                callback(self, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣᗚ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1ll1l11l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l1ll1ll11l_opy_(self, instance, bstack1llll1ll1l1_opy_):
        return
    @abc.abstractmethod
    def bstack1l1l1ll11l1_opy_(self, instance, bstack1llll1ll1l1_opy_):
        return
    @staticmethod
    def bstack1llllllll11_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1111111111_opy_.create_context(target)
        instance = TestFramework.bstack1lllllll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llll1l11ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1l1ll11ll_opy_(reverse=True) -> List[bstack1lll11ll1l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1l11_opy_(ctx: bstack1llllll111l_opy_, reverse=True) -> List[bstack1lll11ll1l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1lll_opy_(instance: bstack1lll11ll1l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll1lllll_opy_(instance: bstack1lll11ll1l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll1l1lll_opy_(instance: bstack1lll11ll1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨᗛ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111l1lll_opy_(instance: bstack1lll11ll1l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥᗜ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11llll11111_opy_(instance: bstack1lll1l1ll11_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᗝ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llllllll11_opy_(target, strict)
        return TestFramework.bstack1llll1lllll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llllllll11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l1111ll11l_opy_(instance: bstack1lll11ll1l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11lllllll11_opy_(instance: bstack1lll11ll1l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_]):
        return bstack1ll11ll_opy_ (u"ࠧࡀࠢᗞ").join((bstack1lll1l1ll11_opy_(bstack1llll1ll1l1_opy_[0]).name, bstack1ll1lllll11_opy_(bstack1llll1ll1l1_opy_[1]).name))
    @staticmethod
    def bstack1ll111l11ll_opy_(bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_], callback: Callable):
        bstack1l11l111l11_opy_ = TestFramework.bstack1l11l111l1l_opy_(bstack1llll1ll1l1_opy_)
        TestFramework.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᗟ").format(bstack1l11l111l11_opy_))
        if not bstack1l11l111l11_opy_ in TestFramework.bstack11llll11ll1_opy_:
            TestFramework.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_] = []
        TestFramework.bstack11llll11ll1_opy_[bstack1l11l111l11_opy_].append(callback)
    @staticmethod
    def bstack1l1ll1lllll_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1ll11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᗠ"):
            return klass.__qualname__
        return module + bstack1ll11ll_opy_ (u"ࠣ࠰ࠥᗡ") + klass.__qualname__
    @staticmethod
    def bstack1l1l1ll1111_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}