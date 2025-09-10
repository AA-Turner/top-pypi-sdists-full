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
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1llllll11l1_opy_ import bstack1111111111_opy_, bstack1llllll111l_opy_
import os
import threading
class bstack1lllll111ll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll11ll_opy_ (u"ࠨࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧ႘").format(self.name)
class bstack1lllll1l111_opy_(Enum):
    NONE = 0
    bstack1llll1l1l11_opy_ = 1
    bstack1lllll1ll11_opy_ = 3
    bstack1llllllllll_opy_ = 4
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
        return bstack1ll11ll_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢ႙").format(self.name)
class bstack1llll1ll111_opy_(bstack1111111111_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lllll1l111_opy_
    previous_state: bstack1lllll1l111_opy_
    bstack1lllll11lll_opy_: datetime
    bstack1lllll1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1llllll111l_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lllll1l111_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lllll1l111_opy_.NONE
        self.bstack1lllll11lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lllll1111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llll1l1lll_opy_(self, bstack1llllll1l1l_opy_: bstack1lllll1l111_opy_):
        bstack1lllllll11l_opy_ = bstack1lllll1l111_opy_(bstack1llllll1l1l_opy_).name
        if not bstack1lllllll11l_opy_:
            return False
        if bstack1llllll1l1l_opy_ == self.state:
            return False
        if self.state == bstack1lllll1l111_opy_.bstack1lllll1ll11_opy_: # bstack1llll1lll11_opy_ bstack1llllll1ll1_opy_ for bstack1lllll11l1l_opy_ in bstack1lllll1llll_opy_, it bstack1lllll1lll1_opy_ bstack1lllll1ll1l_opy_ bstack1llllllll1l_opy_ times bstack1llll1l1l1l_opy_ a new state
            return True
        if (
            bstack1llllll1l1l_opy_ == bstack1lllll1l111_opy_.NONE
            or (self.state != bstack1lllll1l111_opy_.NONE and bstack1llllll1l1l_opy_ == bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_)
            or (self.state < bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_ and bstack1llllll1l1l_opy_ == bstack1lllll1l111_opy_.bstack1llllllllll_opy_)
            or (self.state < bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_ and bstack1llllll1l1l_opy_ == bstack1lllll1l111_opy_.QUIT)
        ):
            raise ValueError(bstack1ll11ll_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡸࡦࡺࡥࠡࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࠢႚ") + str(self.state) + bstack1ll11ll_opy_ (u"ࠤࠣࡁࡃࠦࠢႛ") + str(bstack1llllll1l1l_opy_))
        self.previous_state = self.state
        self.state = bstack1llllll1l1l_opy_
        self.bstack1lllll1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1llllll1111_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lllllll111_opy_: Dict[str, bstack1llll1ll111_opy_] = dict()
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
    def bstack1lllllll1ll_opy_(self, instance: bstack1llll1ll111_opy_, method_name: str, bstack1lllll11111_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lllll11ll1_opy_(
        self, method_name, previous_state: bstack1lllll1l111_opy_, *args, **kwargs
    ) -> bstack1lllll1l111_opy_:
        return
    @abc.abstractmethod
    def bstack1llll1ll11l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lllll11l11_opy_(self, bstack1llll1ll1ll_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1llll1ll1ll_opy_:
                bstack1lllll1l1l1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1lllll1l1l1_opy_):
                    self.logger.warning(bstack1ll11ll_opy_ (u"ࠥࡹࡳࡶࡡࡵࡥ࡫ࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣႜ") + str(method_name) + bstack1ll11ll_opy_ (u"ࠦࠧႝ"))
                    continue
                bstack1lllll111l1_opy_ = self.bstack1lllll11ll1_opy_(
                    method_name, previous_state=bstack1lllll1l111_opy_.NONE
                )
                bstack1llll1l11l1_opy_ = self.bstack1lllllll1l1_opy_(
                    method_name,
                    (bstack1lllll111l1_opy_ if bstack1lllll111l1_opy_ else bstack1lllll1l111_opy_.NONE),
                    bstack1lllll1l1l1_opy_,
                )
                if not callable(bstack1llll1l11l1_opy_):
                    self.logger.warning(bstack1ll11ll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠥࡴ࡯ࡵࠢࡳࡥࡹࡩࡨࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࠭ࢁࡳࡦ࡮ࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࡀࠠࠣ႞") + str(self.framework_version) + bstack1ll11ll_opy_ (u"ࠨࠩࠣ႟"))
                    continue
                setattr(clazz, method_name, bstack1llll1l11l1_opy_)
    def bstack1lllllll1l1_opy_(
        self,
        method_name: str,
        bstack1lllll111l1_opy_: bstack1lllll1l111_opy_,
        bstack1lllll1l1l1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1ll111l11_opy_ = datetime.now()
            (bstack1lllll111l1_opy_,) = wrapped.__vars__
            bstack1lllll111l1_opy_ = (
                bstack1lllll111l1_opy_
                if bstack1lllll111l1_opy_ and bstack1lllll111l1_opy_ != bstack1lllll1l111_opy_.NONE
                else self.bstack1lllll11ll1_opy_(method_name, previous_state=bstack1lllll111l1_opy_, *args, **kwargs)
            )
            if bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.bstack1llll1l1l11_opy_:
                ctx = bstack1111111111_opy_.create_context(self.bstack1lllll1l11l_opy_(target))
                if not self.bstack1llll1llll1_opy_() or ctx.id not in bstack1llllll1111_opy_.bstack1lllllll111_opy_:
                    bstack1llllll1111_opy_.bstack1lllllll111_opy_[ctx.id] = bstack1llll1ll111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lllll111l1_opy_
                    )
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣႠ") + str(bstack1llllll1111_opy_.bstack1lllllll111_opy_.keys()) + bstack1ll11ll_opy_ (u"ࠣࠤႡ"))
            else:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣ࡭ࡳࡼ࡯࡬ࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦႢ") + str(bstack1llllll1111_opy_.bstack1lllllll111_opy_.keys()) + bstack1ll11ll_opy_ (u"ࠥࠦႣ"))
            instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(self.bstack1lllll1l11l_opy_(target))
            if bstack1lllll111l1_opy_ == bstack1lllll1l111_opy_.NONE or not instance:
                ctx = bstack1111111111_opy_.create_context(self.bstack1lllll1l11l_opy_(target))
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡻ࡮ࡵࡴࡤࡧࡰ࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣႤ") + str(bstack1llllll1111_opy_.bstack1lllllll111_opy_.keys()) + bstack1ll11ll_opy_ (u"ࠧࠨႥ"))
                return bstack1lllll1l1l1_opy_(target, *args, **kwargs)
            bstack1llll1l1ll1_opy_ = self.bstack1llll1ll11l_opy_(
                target,
                (instance, method_name),
                (bstack1lllll111l1_opy_, bstack1lllll111ll_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1llll1l1lll_opy_(bstack1lllll111l1_opy_):
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠠࡴࡶࡤࡸࡪ࠳ࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡱࡴࡨࡺ࡮ࡵࡵࡴࡡࡶࡸࡦࡺࡥࡾࠢࡀࡂࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡵࡷࡥࡹ࡫ࡽࠡࠪࡾࡸࡾࡶࡥࠩࡶࡤࡶ࡬࡫ࡴࠪࡿ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡿࡦࡸࡧࡴࡿࠬࠤࡠࠨႦ") + str(instance.ref()) + bstack1ll11ll_opy_ (u"ࠢ࡞ࠤႧ"))
            result = (
                bstack1llll1l1ll1_opy_(target, bstack1lllll1l1l1_opy_, *args, **kwargs)
                if callable(bstack1llll1l1ll1_opy_)
                else bstack1lllll1l1l1_opy_(target, *args, **kwargs)
            )
            bstack1llll1lll1l_opy_ = self.bstack1llll1ll11l_opy_(
                target,
                (instance, method_name),
                (bstack1lllll111l1_opy_, bstack1lllll111ll_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1lllllll1ll_opy_(instance, method_name, datetime.now() - bstack1ll111l11_opy_, *args, **kwargs)
            return bstack1llll1lll1l_opy_ if bstack1llll1lll1l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lllll111l1_opy_,)
        return wrapped
    @staticmethod
    def bstack1llllllll11_opy_(target: object, strict=True):
        ctx = bstack1111111111_opy_.create_context(target)
        instance = bstack1llllll1111_opy_.bstack1lllllll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1llll1l11ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1llllll1l11_opy_(
        ctx: bstack1llllll111l_opy_, state: bstack1lllll1l111_opy_, reverse=True
    ) -> List[bstack1llll1ll111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1llllll1111_opy_.bstack1lllllll111_opy_.values(),
            ),
            key=lambda t: t.bstack1lllll11lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1llllll1lll_opy_(instance: bstack1llll1ll111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llll1lllll_opy_(instance: bstack1llll1ll111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llll1l1lll_opy_(instance: bstack1llll1ll111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1llllll1111_opy_.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣ࡯ࡪࡿ࠽ࡼ࡭ࡨࡽࢂࠦࡶࡢ࡮ࡸࡩࡂࠨႨ") + str(value) + bstack1ll11ll_opy_ (u"ࠤࠥႩ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(target, strict)
        return bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llll1llll1_opy_(self):
        return self.framework_name == bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧႪ")
    def bstack1lllll1l11l_opy_(self, target):
        return target if not self.bstack1llll1llll1_opy_() else self.bstack1llllll11ll_opy_()
    @staticmethod
    def bstack1llllll11ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())