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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1lllllll1l1_opy_ import bstack1lllll11l11_opy_, bstack1lllll1l1l1_opy_
import os
import threading
class bstack1111111ll1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1ll1_opy_ (u"ࠣࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢၔ").format(self.name)
class bstack1lllll1lll1_opy_(Enum):
    NONE = 0
    bstack1lllll1l111_opy_ = 1
    bstack1111111111_opy_ = 3
    bstack1llllllll11_opy_ = 4
    bstack1lllll1ll11_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1ll1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤၕ").format(self.name)
class bstack1111111l1l_opy_(bstack1lllll11l11_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lllll1lll1_opy_
    previous_state: bstack1lllll1lll1_opy_
    bstack1llllllllll_opy_: datetime
    bstack1llll1lll11_opy_: datetime
    def __init__(
        self,
        context: bstack1lllll1l1l1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lllll1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lllll1lll1_opy_.NONE
        self.bstack1llllllllll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llll1lll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllllll1ll_opy_(self, bstack1llll1lllll_opy_: bstack1lllll1lll1_opy_):
        bstack11111111ll_opy_ = bstack1lllll1lll1_opy_(bstack1llll1lllll_opy_).name
        if not bstack11111111ll_opy_:
            return False
        if bstack1llll1lllll_opy_ == self.state:
            return False
        if self.state == bstack1lllll1lll1_opy_.bstack1111111111_opy_: # bstack1lllllll111_opy_ bstack1lllll1111l_opy_ for bstack1llllll1l11_opy_ in bstack1llllll11l1_opy_, it bstack1lllll111l1_opy_ bstack1llll1llll1_opy_ bstack1lllll11l1l_opy_ times bstack1lllll111ll_opy_ a new state
            return True
        if (
            bstack1llll1lllll_opy_ == bstack1lllll1lll1_opy_.NONE
            or (self.state != bstack1lllll1lll1_opy_.NONE and bstack1llll1lllll_opy_ == bstack1lllll1lll1_opy_.bstack1lllll1l111_opy_)
            or (self.state < bstack1lllll1lll1_opy_.bstack1lllll1l111_opy_ and bstack1llll1lllll_opy_ == bstack1lllll1lll1_opy_.bstack1llllllll11_opy_)
            or (self.state < bstack1lllll1lll1_opy_.bstack1lllll1l111_opy_ and bstack1llll1lllll_opy_ == bstack1lllll1lll1_opy_.QUIT)
        ):
            raise ValueError(bstack1l1ll1_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡺࡡࡵࡧࠣࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࠤၖ") + str(self.state) + bstack1l1ll1_opy_ (u"ࠦࠥࡃ࠾ࠡࠤၗ") + str(bstack1llll1lllll_opy_))
        self.previous_state = self.state
        self.state = bstack1llll1lllll_opy_
        self.bstack1llll1lll11_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack111111l1l1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1llllll1ll1_opy_: Dict[str, bstack1111111l1l_opy_] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack111111l11l_opy_(self, instance: bstack1111111l1l_opy_, method_name: str, bstack1111111lll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lllll11111_opy_(
        self, method_name, previous_state: bstack1lllll1lll1_opy_, *args, **kwargs
    ) -> bstack1lllll1lll1_opy_:
        return
    @abc.abstractmethod
    def bstack1llllll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1llll1lll1l_opy_(self, bstack1111111l11_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1111111l11_opy_:
                bstack111111111l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack111111111l_opy_):
                    self.logger.warning(bstack1l1ll1_opy_ (u"ࠧࡻ࡮ࡱࡣࡷࡧ࡭࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥၘ") + str(method_name) + bstack1l1ll1_opy_ (u"ࠨࠢၙ"))
                    continue
                bstack1lllllllll1_opy_ = self.bstack1lllll11111_opy_(
                    method_name, previous_state=bstack1lllll1lll1_opy_.NONE
                )
                bstack1lllll1l1ll_opy_ = self.bstack1lllll1l11l_opy_(
                    method_name,
                    (bstack1lllllllll1_opy_ if bstack1lllllllll1_opy_ else bstack1lllll1lll1_opy_.NONE),
                    bstack111111111l_opy_,
                )
                if not callable(bstack1lllll1l1ll_opy_):
                    self.logger.warning(bstack1l1ll1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠠ࡯ࡱࡷࠤࡵࡧࡴࡤࡪࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࠨࡼࡵࡨࡰ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥၚ") + str(self.framework_version) + bstack1l1ll1_opy_ (u"ࠣࠫࠥၛ"))
                    continue
                setattr(clazz, method_name, bstack1lllll1l1ll_opy_)
    def bstack1lllll1l11l_opy_(
        self,
        method_name: str,
        bstack1lllllllll1_opy_: bstack1lllll1lll1_opy_,
        bstack111111111l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l1lll1_opy_ = datetime.now()
            (bstack1lllllllll1_opy_,) = wrapped.__vars__
            bstack1lllllllll1_opy_ = (
                bstack1lllllllll1_opy_
                if bstack1lllllllll1_opy_ and bstack1lllllllll1_opy_ != bstack1lllll1lll1_opy_.NONE
                else self.bstack1lllll11111_opy_(method_name, previous_state=bstack1lllllllll1_opy_, *args, **kwargs)
            )
            if bstack1lllllllll1_opy_ == bstack1lllll1lll1_opy_.bstack1lllll1l111_opy_:
                ctx = bstack1lllll11l11_opy_.create_context(self.bstack1lllll11ll1_opy_(target))
                if not self.bstack1llllll1lll_opy_() or ctx.id not in bstack111111l1l1_opy_.bstack1llllll1ll1_opy_:
                    bstack111111l1l1_opy_.bstack1llllll1ll1_opy_[ctx.id] = bstack1111111l1l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lllllllll1_opy_
                    )
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥၜ") + str(bstack111111l1l1_opy_.bstack1llllll1ll1_opy_.keys()) + bstack1l1ll1_opy_ (u"ࠥࠦၝ"))
            else:
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥ࡯࡮ࡷࡱ࡮ࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨၞ") + str(bstack111111l1l1_opy_.bstack1llllll1ll1_opy_.keys()) + bstack1l1ll1_opy_ (u"ࠧࠨၟ"))
            instance = bstack111111l1l1_opy_.bstack1llllllll1l_opy_(self.bstack1lllll11ll1_opy_(target))
            if bstack1lllllllll1_opy_ == bstack1lllll1lll1_opy_.NONE or not instance:
                ctx = bstack1lllll11l11_opy_.create_context(self.bstack1lllll11ll1_opy_(target))
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡶࡰࡷࡶࡦࡩ࡫ࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥၠ") + str(bstack111111l1l1_opy_.bstack1llllll1ll1_opy_.keys()) + bstack1l1ll1_opy_ (u"ࠢࠣၡ"))
                return bstack111111111l_opy_(target, *args, **kwargs)
            bstack1lllll11lll_opy_ = self.bstack1llllll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lllllllll1_opy_, bstack1111111ll1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lllllll1ll_opy_(bstack1lllllllll1_opy_):
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡥࡥࠢࡶࡸࡦࡺࡥ࠮ࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡳࡶࡪࡼࡩࡰࡷࡶࡣࡸࡺࡡࡵࡧࢀࠤࡂࡄࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡷࡹࡧࡴࡦࡿࠣࠬࢀࡺࡹࡱࡧࠫࡸࡦࡸࡧࡦࡶࠬࢁ࠳ࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥࢁࡡࡳࡩࡶࢁ࠮࡛ࠦࠣၢ") + str(instance.ref()) + bstack1l1ll1_opy_ (u"ࠤࡠࠦၣ"))
            result = (
                bstack1lllll11lll_opy_(target, bstack111111111l_opy_, *args, **kwargs)
                if callable(bstack1lllll11lll_opy_)
                else bstack111111111l_opy_(target, *args, **kwargs)
            )
            bstack1llllll111l_opy_ = self.bstack1llllll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lllllllll1_opy_, bstack1111111ll1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack111111l11l_opy_(instance, method_name, datetime.now() - bstack1l1l1lll1_opy_, *args, **kwargs)
            return bstack1llllll111l_opy_ if bstack1llllll111l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lllllllll1_opy_,)
        return wrapped
    @staticmethod
    def bstack1llllllll1l_opy_(target: object, strict=True):
        ctx = bstack1lllll11l11_opy_.create_context(target)
        instance = bstack111111l1l1_opy_.bstack1llllll1ll1_opy_.get(ctx.id, None)
        if instance and instance.bstack11111111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llllll1l1l_opy_(
        ctx: bstack1lllll1l1l1_opy_, state: bstack1lllll1lll1_opy_, reverse=True
    ) -> List[bstack1111111l1l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack111111l1l1_opy_.bstack1llllll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1llllllllll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll1ll1l_opy_(instance: bstack1111111l1l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack111111l111_opy_(instance: bstack1111111l1l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllllll1ll_opy_(instance: bstack1111111l1l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack111111l1l1_opy_.logger.debug(bstack1l1ll1_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡸࡥࡧࠪࠬࢁࠥࡱࡥࡺ࠿ࡾ࡯ࡪࡿࡽࠡࡸࡤࡰࡺ࡫࠽ࠣၤ") + str(value) + bstack1l1ll1_opy_ (u"ࠦࠧၥ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack111111l1l1_opy_.bstack1llllllll1l_opy_(target, strict)
        return bstack111111l1l1_opy_.bstack111111l111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack111111l1l1_opy_.bstack1llllllll1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llllll1lll_opy_(self):
        return self.framework_name == bstack1l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩၦ")
    def bstack1lllll11ll1_opy_(self, target):
        return target if not self.bstack1llllll1lll_opy_() else self.bstack1lllll1llll_opy_()
    @staticmethod
    def bstack1lllll1llll_opy_():
        return str(os.getpid()) + str(threading.get_ident())