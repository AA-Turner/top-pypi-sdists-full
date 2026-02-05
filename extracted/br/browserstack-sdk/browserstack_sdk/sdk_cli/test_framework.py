# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1lll1llll11_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1l1l111_opy_, bstack1lll1lll11l_opy_
class bstack1ll1111llll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11l1ll1_opy_ (u"࡚ࠧࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᛅ").format(self.name)
class bstack1ll11l1l1l1_opy_(Enum):
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
        return bstack11l1ll1_opy_ (u"ࠨࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢᛆ").format(self.name)
class bstack1ll1ll111l1_opy_(bstack1lll1l1l111_opy_):
    bstack1l1lll1l1ll_opy_: List[str]
    bstack11ll1l11lll_opy_: Dict[str, str]
    state: bstack1ll11l1l1l1_opy_
    bstack1lll1l1l1ll_opy_: datetime
    bstack1lll11ll1l1_opy_: datetime
    def __init__(
        self,
        context: bstack1lll1lll11l_opy_,
        bstack1l1lll1l1ll_opy_: List[str],
        bstack11ll1l11lll_opy_: Dict[str, str],
        state=bstack1ll11l1l1l1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1l1lll1l1ll_opy_ = bstack1l1lll1l1ll_opy_
        self.bstack11ll1l11lll_opy_ = bstack11ll1l11lll_opy_
        self.state = state
        self.bstack1lll1l1l1ll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll11ll1l1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1l1111l_opy_(self, bstack1lll111ll11_opy_: bstack1ll11l1l1l1_opy_):
        bstack1lll11l11l1_opy_ = bstack1ll11l1l1l1_opy_(bstack1lll111ll11_opy_).name
        if not bstack1lll11l11l1_opy_:
            return False
        if bstack1lll111ll11_opy_ == self.state:
            return False
        self.state = bstack1lll111ll11_opy_
        self.bstack1lll11ll1l1_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack11lll11llll_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1lll11ll_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l11ll1l1l1_opy_: int = None
    bstack1l11lll111l_opy_: str = None
    bstack1ll1lll_opy_: str = None
    bstack111lllll1l_opy_: str = None
    bstack1l1l11l1l11_opy_: str = None
    bstack11ll1llllll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1l1llll1l11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡻࡵࡪࡦࠥᛇ")
    bstack11ll1ll1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡩࡥࠤᛈ")
    bstack1l1l1lll11l_opy_ = bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠧᛉ")
    bstack11lll111111_opy_ = bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠦᛊ")
    bstack11lll11l11l_opy_ = bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡷࡥ࡬ࡹࠢᛋ")
    bstack1l111l1ll11_opy_ = bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡪࡹࡵ࡭ࡶࠥᛌ")
    bstack1l11ll11l1l_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࡣࡦࡺࠢᛍ")
    bstack1l11ll1ll11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᛎ")
    bstack1l1l11lll11_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᛏ")
    bstack11lll1l1lll_opy_ = bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᛐ")
    bstack1l1llllll11_opy_ = bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠤᛑ")
    bstack1l1l111llll_opy_ = bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᛒ")
    bstack11llll111l1_opy_ = bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡧࡴࡪࡥࠣᛓ")
    bstack1l11l1l1l11_opy_ = bstack11l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠣᛔ")
    bstack1l1l1lll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᛕ")
    bstack1l111ll111l_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡢ࡫࡯ࡹࡷ࡫ࠢᛖ")
    bstack11llll1ll11_opy_ = bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪࠨᛗ")
    bstack11ll1l1l1ll_opy_ = bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲ࡫ࡸࠨᛘ")
    bstack11lll111lll_opy_ = bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡰࡩࡹࡧࠢᛙ")
    bstack11ll11lllll_opy_ = bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡷࡨࡵࡰࡦࡵࠪᛚ")
    bstack1l111111111_opy_ = bstack11l1ll1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡱࡥࡲ࡫ࠢᛛ")
    bstack11ll1ll1lll_opy_ = bstack11l1ll1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᛜ")
    bstack11llll1l111_opy_ = bstack11l1ll1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᛝ")
    bstack11llll1lll1_opy_ = bstack11l1ll1_opy_ (u"ࠤ࡫ࡳࡴࡱ࡟ࡪࡦࠥᛞ")
    bstack11ll1llll1l_opy_ = bstack11l1ll1_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠࡴࡨࡷࡺࡲࡴࠣᛟ")
    bstack11lll1l1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡ࡯ࡳ࡬ࡹࠢᛠ")
    bstack11lll1llll1_opy_ = bstack11l1ll1_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠣᛡ")
    bstack11lll11ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᛢ")
    bstack11ll1lll111_opy_ = bstack11l1ll1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᛣ")
    bstack11ll1l1l111_opy_ = bstack11l1ll1_opy_ (u"ࠣࡲࡨࡲࡩ࡯࡮ࡨࠤᛤ")
    bstack11llll1ll1l_opy_ = bstack11l1ll1_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᛥ")
    bstack1l1l11ll11l_opy_ = bstack11l1ll1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠧᛦ")
    bstack1l1l11l1l1l_opy_ = bstack11l1ll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡏࡓࡌࠨᛧ")
    bstack1l11l1lllll_opy_ = bstack11l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᛨ")
    bstack1lll1ll11ll_opy_: Dict[str, bstack1ll1ll111l1_opy_] = dict()
    bstack11ll11l1ll1_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1lll1l1ll_opy_: List[str]
    bstack11ll1l11lll_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1l1lll1l1ll_opy_: List[str],
        bstack11ll1l11lll_opy_: Dict[str, str],
        bstack1lll1llll11_opy_: bstack1lll1llll1l_opy_
    ):
        self.bstack1l1lll1l1ll_opy_ = bstack1l1lll1l1ll_opy_
        self.bstack11ll1l11lll_opy_ = bstack11ll1l11lll_opy_
        self.bstack1lll1llll11_opy_ = bstack1lll1llll11_opy_
    def track_event(
        self,
        context: bstack11lll11llll_opy_,
        test_framework_state: bstack1ll11l1l1l1_opy_,
        test_hook_state: bstack1ll1111llll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡽࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࡀࡿࢂࠦࡡࡳࡩࡶࡁࢀࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼࡿࠥᛩ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack11lll1ll111_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        bstack11lllll1lll_opy_ = TestFramework.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        if not bstack11lllll1lll_opy_ in TestFramework.bstack11ll11l1ll1_opy_:
            return
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡾࢁࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠣᛪ").format(len(TestFramework.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_])))
        for callback in TestFramework.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_]:
            try:
                callback(self, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡪࡰࡹࡳࡰ࡯࡮ࡨࠢࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥࢁࡽࠣ᛫").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1l11l11l1_opy_(self):
        return
    @abc.abstractmethod
    def bstack1l11llll1ll_opy_(self, instance, bstack1lll1l1ll11_opy_):
        return
    @abc.abstractmethod
    def bstack1l11lll11ll_opy_(self, instance, bstack1lll1l1ll11_opy_):
        return
    @staticmethod
    def bstack1lll11ll11l_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack1lll1l1l111_opy_.create_context(target)
        instance = TestFramework.bstack1lll1ll11ll_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll11l111l_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l11l1ll1ll_opy_(reverse=True) -> List[bstack1ll1ll111l1_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lll1ll11ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lll1l1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll11l11ll_opy_(ctx: bstack1lll1lll11l_opy_, reverse=True) -> List[bstack1ll1ll111l1_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lll1ll11ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lll1l1l1ll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll11l1111_opy_(instance: bstack1ll1ll111l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1ll11l1_opy_(instance: bstack1ll1ll111l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1l1111l_opy_(instance: bstack1ll1ll111l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡰ࡫ࡹ࠾ࡽࢀࠤࡻࡧ࡬ࡶࡧࡀࡿࢂࠨ᛬").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11lll1111l1_opy_(instance: bstack1ll1ll111l1_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡥࡥ࡯ࡶࡵ࡭ࡪࡹ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿࢂࠦࡥ࡯ࡶࡵ࡭ࡪࡹ࠽ࡼࡿࠥ᛭").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack11ll111ll1l_opy_(instance: bstack1ll11l1l1l1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡺࡶࡤࡢࡶࡨࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢ࡮ࡩࡾࡃࡻࡾࠢࡹࡥࡱࡻࡥ࠾ࡽࢀࠦᛮ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1lll11ll11l_opy_(target, strict)
        return TestFramework.bstack1lll1ll11l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1lll11ll11l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack11ll1l1l1l1_opy_(instance: bstack1ll1ll111l1_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack11lllll11ll_opy_(instance: bstack1ll1ll111l1_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_]):
        return bstack11l1ll1_opy_ (u"ࠧࡀࠢᛯ").join((bstack1ll11l1l1l1_opy_(bstack1lll1l1ll11_opy_[0]).name, bstack1ll1111llll_opy_(bstack1lll1l1ll11_opy_[1]).name))
    @staticmethod
    def bstack1l1ll11llll_opy_(bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_], callback: Callable):
        bstack11lllll1lll_opy_ = TestFramework.bstack11llllll1ll_opy_(bstack1lll1l1ll11_opy_)
        TestFramework.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡳࡦࡶࡢ࡬ࡴࡵ࡫ࡠࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤ࡭ࡵ࡯࡬ࡡࡵࡩ࡬࡯ࡳࡵࡴࡼࡣࡰ࡫ࡹ࠾ࡽࢀࠦᛰ").format(bstack11lllll1lll_opy_))
        if not bstack11lllll1lll_opy_ in TestFramework.bstack11ll11l1ll1_opy_:
            TestFramework.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_] = []
        TestFramework.bstack11ll11l1ll1_opy_[bstack11lllll1lll_opy_].append(callback)
    @staticmethod
    def bstack1l1l11l1ll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡹ࡯࡮ࡴࠤᛱ"):
            return klass.__qualname__
        return module + bstack11l1ll1_opy_ (u"ࠣ࠰ࠥᛲ") + klass.__qualname__
    @staticmethod
    def bstack1l11l1lll11_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}