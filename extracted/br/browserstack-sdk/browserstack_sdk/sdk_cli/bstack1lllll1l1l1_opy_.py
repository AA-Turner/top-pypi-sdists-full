# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lllll11ll1_opy_, bstack1llllllll11_opy_
import os
import threading
class bstack1lllll1l11l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1ll_opy_ (u"ࠥࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤႎ").format(self.name)
class bstack1llllllll1l_opy_(Enum):
    NONE = 0
    bstack1lllll11l11_opy_ = 1
    bstack1lllllll111_opy_ = 3
    bstack1lllll11l1l_opy_ = 4
    bstack1lllllllll1_opy_ = 5
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
        return bstack1ll1ll_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦႏ").format(self.name)
class bstack111111l111_opy_(bstack1lllll11ll1_opy_):
    framework_name: str
    framework_version: str
    state: bstack1llllllll1l_opy_
    previous_state: bstack1llllllll1l_opy_
    bstack1lllll1lll1_opy_: datetime
    bstack1llllll1l11_opy_: datetime
    def __init__(
        self,
        context: bstack1llllllll11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1llllllll1l_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1llllllll1l_opy_.NONE
        self.bstack1lllll1lll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llllll1l11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lllll1ll1l_opy_(self, bstack1llllll111l_opy_: bstack1llllllll1l_opy_):
        bstack1llllll11l1_opy_ = bstack1llllllll1l_opy_(bstack1llllll111l_opy_).name
        if not bstack1llllll11l1_opy_:
            return False
        if bstack1llllll111l_opy_ == self.state:
            return False
        if self.state == bstack1llllllll1l_opy_.bstack1lllllll111_opy_: # bstack1llllll1l1l_opy_ bstack1lllllll11l_opy_ for bstack1lllll11111_opy_ in bstack1111111lll_opy_, it bstack1111111ll1_opy_ bstack1llllll1ll1_opy_ bstack1llll1lll11_opy_ times bstack11111111l1_opy_ a new state
            return True
        if (
            bstack1llllll111l_opy_ == bstack1llllllll1l_opy_.NONE
            or (self.state != bstack1llllllll1l_opy_.NONE and bstack1llllll111l_opy_ == bstack1llllllll1l_opy_.bstack1lllll11l11_opy_)
            or (self.state < bstack1llllllll1l_opy_.bstack1lllll11l11_opy_ and bstack1llllll111l_opy_ == bstack1llllllll1l_opy_.bstack1lllll11l1l_opy_)
            or (self.state < bstack1llllllll1l_opy_.bstack1lllll11l11_opy_ and bstack1llllll111l_opy_ == bstack1llllllll1l_opy_.QUIT)
        ):
            raise ValueError(bstack1ll1ll_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡵࡣࡷࡩࠥࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࠦ႐") + str(self.state) + bstack1ll1ll_opy_ (u"ࠨࠠ࠾ࡀࠣࠦ႑") + str(bstack1llllll111l_opy_))
        self.previous_state = self.state
        self.state = bstack1llllll111l_opy_
        self.bstack1llllll1l11_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lllllll1ll_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1111111l11_opy_: Dict[str, bstack111111l111_opy_] = dict()
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
    def bstack1lllll11lll_opy_(self, instance: bstack111111l111_opy_, method_name: str, bstack1llllllllll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1llll1lll1l_opy_(
        self, method_name, previous_state: bstack1llllllll1l_opy_, *args, **kwargs
    ) -> bstack1llllllll1l_opy_:
        return
    @abc.abstractmethod
    def bstack1llll1ll1ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack111111l111_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1llllllll1l_opy_, bstack1lllll1l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lllll1ll11_opy_(self, bstack1llll1llll1_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1llll1llll1_opy_:
                bstack1lllll1l111_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1lllll1l111_opy_):
                    self.logger.warning(bstack1ll1ll_opy_ (u"ࠢࡶࡰࡳࡥࡹࡩࡨࡦࡦࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧ႒") + str(method_name) + bstack1ll1ll_opy_ (u"ࠣࠤ႓"))
                    continue
                bstack1llllll11ll_opy_ = self.bstack1llll1lll1l_opy_(
                    method_name, previous_state=bstack1llllllll1l_opy_.NONE
                )
                bstack1lllllll1l1_opy_ = self.bstack1lllll1l1ll_opy_(
                    method_name,
                    (bstack1llllll11ll_opy_ if bstack1llllll11ll_opy_ else bstack1llllllll1l_opy_.NONE),
                    bstack1lllll1l111_opy_,
                )
                if not callable(bstack1lllllll1l1_opy_):
                    self.logger.warning(bstack1ll1ll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠢࡱࡳࡹࠦࡰࡢࡶࡦ࡬ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࠪࡾࡷࡪࡲࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧ႔") + str(self.framework_version) + bstack1ll1ll_opy_ (u"ࠥ࠭ࠧ႕"))
                    continue
                setattr(clazz, method_name, bstack1lllllll1l1_opy_)
    def bstack1lllll1l1ll_opy_(
        self,
        method_name: str,
        bstack1llllll11ll_opy_: bstack1llllllll1l_opy_,
        bstack1lllll1l111_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack111l1l111_opy_ = datetime.now()
            (bstack1llllll11ll_opy_,) = wrapped.__vars__
            bstack1llllll11ll_opy_ = (
                bstack1llllll11ll_opy_
                if bstack1llllll11ll_opy_ and bstack1llllll11ll_opy_ != bstack1llllllll1l_opy_.NONE
                else self.bstack1llll1lll1l_opy_(method_name, previous_state=bstack1llllll11ll_opy_, *args, **kwargs)
            )
            if bstack1llllll11ll_opy_ == bstack1llllllll1l_opy_.bstack1lllll11l11_opy_:
                ctx = bstack1lllll11ll1_opy_.create_context(self.bstack1lllll1111l_opy_(target))
                if not self.bstack111111111l_opy_() or ctx.id not in bstack1lllllll1ll_opy_.bstack1111111l11_opy_:
                    bstack1lllllll1ll_opy_.bstack1111111l11_opy_[ctx.id] = bstack111111l111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1llllll11ll_opy_
                    )
                self.logger.debug(bstack1ll1ll_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧ႖") + str(bstack1lllllll1ll_opy_.bstack1111111l11_opy_.keys()) + bstack1ll1ll_opy_ (u"ࠧࠨ႗"))
            else:
                self.logger.debug(bstack1ll1ll_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡪࡰࡹࡳࡰ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣ႘") + str(bstack1lllllll1ll_opy_.bstack1111111l11_opy_.keys()) + bstack1ll1ll_opy_ (u"ࠢࠣ႙"))
            instance = bstack1lllllll1ll_opy_.bstack1111111111_opy_(self.bstack1lllll1111l_opy_(target))
            if bstack1llllll11ll_opy_ == bstack1llllllll1l_opy_.NONE or not instance:
                ctx = bstack1lllll11ll1_opy_.create_context(self.bstack1lllll1111l_opy_(target))
                self.logger.warning(bstack1ll1ll_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡸࡲࡹࡸࡡࡤ࡭ࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧႚ") + str(bstack1lllllll1ll_opy_.bstack1111111l11_opy_.keys()) + bstack1ll1ll_opy_ (u"ࠤࠥႛ"))
                return bstack1lllll1l111_opy_(target, *args, **kwargs)
            bstack1lllll1llll_opy_ = self.bstack1llll1ll1ll_opy_(
                target,
                (instance, method_name),
                (bstack1llllll11ll_opy_, bstack1lllll1l11l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lllll1ll1l_opy_(bstack1llllll11ll_opy_):
                self.logger.debug(bstack1ll1ll_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠤࡸࡺࡡࡵࡧ࠰ࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡵࡸࡥࡷ࡫ࡲࡹࡸࡥࡳࡵࡣࡷࡩࢂࠦ࠽࠿ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡹࡴࡢࡶࡨࢁࠥ࠮ࡻࡵࡻࡳࡩ࠭ࡺࡡࡳࡩࡨࡸ࠮ࢃ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡼࡣࡵ࡫ࡸࢃࠩࠡ࡝ࠥႜ") + str(instance.ref()) + bstack1ll1ll_opy_ (u"ࠦࡢࠨႝ"))
            result = (
                bstack1lllll1llll_opy_(target, bstack1lllll1l111_opy_, *args, **kwargs)
                if callable(bstack1lllll1llll_opy_)
                else bstack1lllll1l111_opy_(target, *args, **kwargs)
            )
            bstack1lllll111l1_opy_ = self.bstack1llll1ll1ll_opy_(
                target,
                (instance, method_name),
                (bstack1llllll11ll_opy_, bstack1lllll1l11l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1lllll11lll_opy_(instance, method_name, datetime.now() - bstack111l1l111_opy_, *args, **kwargs)
            return bstack1lllll111l1_opy_ if bstack1lllll111l1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1llllll11ll_opy_,)
        return wrapped
    @staticmethod
    def bstack1111111111_opy_(target: object, strict=True):
        ctx = bstack1lllll11ll1_opy_.create_context(target)
        instance = bstack1lllllll1ll_opy_.bstack1111111l11_opy_.get(ctx.id, None)
        if instance and instance.bstack11111111ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llll1lllll_opy_(
        ctx: bstack1llllllll11_opy_, state: bstack1llllllll1l_opy_, reverse=True
    ) -> List[bstack111111l111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lllllll1ll_opy_.bstack1111111l11_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll1lll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll111ll_opy_(instance: bstack111111l111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1lll_opy_(instance: bstack111111l111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lllll1ll1l_opy_(instance: bstack111111l111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lllllll1ll_opy_.logger.debug(bstack1ll1ll_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠ࡬ࡧࡼࡁࢀࡱࡥࡺࡿࠣࡺࡦࡲࡵࡦ࠿ࠥ႞") + str(value) + bstack1ll1ll_opy_ (u"ࠨࠢ႟"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lllllll1ll_opy_.bstack1111111111_opy_(target, strict)
        return bstack1lllllll1ll_opy_.bstack1llllll1lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lllllll1ll_opy_.bstack1111111111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack111111111l_opy_(self):
        return self.framework_name == bstack1ll1ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫႠ")
    def bstack1lllll1111l_opy_(self, target):
        return target if not self.bstack111111111l_opy_() else self.bstack1111111l1l_opy_()
    @staticmethod
    def bstack1111111l1l_opy_():
        return str(os.getpid()) + str(threading.get_ident())