# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll111lll11_opy_ import bstack1ll11llll1l_opy_, bstack1ll11l1l1l1_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1l11l11l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1lll_opy_ (u"ࠢࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨጲ").format(self.name)
class bstack11lll111_opy_(Enum):
    NONE = 0
    bstack1l111ll1l1_opy_ = 1
    bstack1ll11l11ll1_opy_ = 3
    bstack1ll1l1lllll_opy_ = 4
    bstack1ll11l11111_opy_ = 5
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
        return bstack1ll1lll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣጳ").format(self.name)
class bstack1ll11ll1l11_opy_(bstack1ll11llll1l_opy_):
    framework_name: str
    framework_version: str
    state: bstack11lll111_opy_
    previous_state: bstack11lll111_opy_
    bstack1ll11lll1l1_opy_: datetime
    bstack1ll11ll1ll1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11l1l1l1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack11lll111_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack11lll111_opy_.NONE
        self.bstack1ll11lll1l1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll11ll1ll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1111ll_opy_(self, bstack1ll11lll11l_opy_: bstack11lll111_opy_):
        bstack1ll11l111l1_opy_ = bstack11lll111_opy_(bstack1ll11lll11l_opy_).name
        if not bstack1ll11l111l1_opy_:
            return False
        if bstack1ll11lll11l_opy_ == self.state:
            return False
        if self.state == bstack11lll111_opy_.bstack1ll11l11ll1_opy_: # bstack1ll11ll1lll_opy_ bstack1ll11ll1111_opy_ for bstack1ll11lll1ll_opy_ in Playwright, it bstack1ll111llll1_opy_ bstack1ll11l1ll1l_opy_ bstack1ll11l1llll_opy_ times bstack1ll11l1l11l_opy_ a new state
            return True
        if (
            bstack1ll11lll11l_opy_ == bstack11lll111_opy_.NONE
            or (self.state != bstack11lll111_opy_.NONE and bstack1ll11lll11l_opy_ == bstack11lll111_opy_.bstack1l111ll1l1_opy_)
            or (self.state < bstack11lll111_opy_.bstack1l111ll1l1_opy_ and bstack1ll11lll11l_opy_ == bstack11lll111_opy_.bstack1ll1l1lllll_opy_)
            or (self.state < bstack11lll111_opy_.bstack1l111ll1l1_opy_ and bstack1ll11lll11l_opy_ == bstack11lll111_opy_.QUIT)
        ):
            raise ValueError(bstack1ll1lll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡹࡧࡴࡦࠢࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࠣጴ") + str(self.state) + bstack1ll1lll_opy_ (u"ࠥࠤࡂࡄࠠࠣጵ") + str(bstack1ll11lll11l_opy_))
        self.previous_state = self.state
        self.state = bstack1ll11lll11l_opy_
        self.bstack1ll11ll1ll1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11ll11l1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1111l1ll1l_opy_: Dict[str, bstack1ll11ll1l11_opy_] = dict()
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
    def bstack1ll11l11l11_opy_(self, instance: bstack1ll11ll1l11_opy_, method_name: str, bstack1ll111ll1l1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll11llll11_opy_(
        self, method_name, previous_state: bstack11lll111_opy_, *args, **kwargs
    ) -> bstack11lll111_opy_:
        return
    @abc.abstractmethod
    def bstack1l1lll1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll111lll1l_opy_(self, bstack1ll111lllll_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1ll111lllll_opy_:
                bstack1ll11ll111l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll11ll111l_opy_):
                    self.logger.warning(bstack1ll1lll_opy_ (u"ࠦࡺࡴࡰࡢࡶࡦ࡬ࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤጶ") + str(method_name) + bstack1ll1lll_opy_ (u"ࠧࠨጷ"))
                    continue
                bstack1ll11l1lll1_opy_ = self.bstack1ll11llll11_opy_(
                    method_name, previous_state=bstack11lll111_opy_.NONE
                )
                bstack1ll11l1l1ll_opy_ = self.bstack1ll111ll11l_opy_(
                    method_name,
                    (bstack1ll11l1lll1_opy_ if bstack1ll11l1lll1_opy_ else bstack11lll111_opy_.NONE),
                    bstack1ll11ll111l_opy_,
                )
                if not callable(bstack1ll11l1l1ll_opy_):
                    self.logger.warning(bstack1ll1lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠦ࡮ࡰࡶࠣࡴࡦࡺࡣࡩࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࠮ࡻࡴࡧ࡯ࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃ࠺ࠡࠤጸ") + str(self.framework_version) + bstack1ll1lll_opy_ (u"ࠢࠪࠤጹ"))
                    continue
                setattr(clazz, method_name, bstack1ll11l1l1ll_opy_)
    def bstack1ll111ll11l_opy_(
        self,
        method_name: str,
        bstack1ll11l1lll1_opy_: bstack11lll111_opy_,
        bstack1ll11ll111l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11lllll111_opy_ = datetime.now()
            (bstack1ll11l1lll1_opy_,) = wrapped.__vars__
            bstack1ll11l1lll1_opy_ = (
                bstack1ll11l1lll1_opy_
                if bstack1ll11l1lll1_opy_ and bstack1ll11l1lll1_opy_ != bstack11lll111_opy_.NONE
                else self.bstack1ll11llll11_opy_(method_name, previous_state=bstack1ll11l1lll1_opy_, *args, **kwargs)
            )
            if bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.bstack1l111ll1l1_opy_:
                ctx = bstack1ll11llll1l_opy_.create_context(self.bstack1ll11ll1l1l_opy_(target))
                if not self.bstack1ll11l1111l_opy_() or ctx.id not in bstack11ll11l1_opy_.bstack1111l1ll1l_opy_:
                    bstack11ll11l1_opy_.bstack1111l1ll1l_opy_[ctx.id] = bstack1ll11ll1l11_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1ll11l1lll1_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1ll11ll11ll_opy_ = None
                    if label:
                        if bstack1ll1lll_opy_ (u"ࠣࠥࠥጺ") in label:
                            suffix = label.rsplit(bstack1ll1lll_opy_ (u"ࠤࠦࠦጻ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1ll11ll11ll_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1ll11l1ll11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣጼ")
                                )
                        else:
                            self.logger.debug(
                                bstack1ll11l1ll11_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧጽ")
                            )
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡸࡷࡧࡣ࡬ࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡴࡤࡲࡰࡃࡻࡳࡣࡱ࡯ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥጾ") + str(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠨࠢጿ"))
                    bstack1ll11l11l1l_opy_ = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(self.bstack1ll11ll1l1l_opy_(target))
                    bstack1ll11l11l1l_opy_.data[bstack1ll1lll_opy_ (u"ࠧࡳࡣࡱ࡯ࠬፀ")] = bstack1ll11ll11ll_opy_
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤፁ") + str(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠤࠥፂ"))
            else:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤ࡮ࡴࡶࡰ࡭ࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧፃ") + str(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠦࠧፄ"))
            instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(self.bstack1ll11ll1l1l_opy_(target))
            if bstack1ll11l1lll1_opy_ == bstack11lll111_opy_.NONE or not instance:
                ctx = bstack1ll11llll1l_opy_.create_context(self.bstack1ll11ll1l1l_opy_(target))
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡵ࡯ࡶࡵࡥࡨࡱࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤፅ") + str(bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.keys()) + bstack1ll1lll_opy_ (u"ࠨࠢፆ"))
                return bstack1ll11ll111l_opy_(target, *args, **kwargs)
            bstack1ll11l11lll_opy_ = self.bstack1l1lll1l1_opy_(
                target,
                (instance, method_name),
                (bstack1ll11l1lll1_opy_, bstack1l11l11l1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll1111ll_opy_(bstack1ll11l1lll1_opy_):
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠡࡵࡷࡥࡹ࡫࠭ࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡲࡵࡩࡻ࡯࡯ࡶࡵࡢࡷࡹࡧࡴࡦࡿࠣࡁࡃࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡶࡸࡦࡺࡥࡾࠢࠫࡿࡹࡿࡰࡦࠪࡷࡥࡷ࡭ࡥࡵࠫࢀ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࢀࡧࡲࡨࡵࢀ࠭ࠥࡡࠢፇ") + str(instance.ref()) + bstack1ll1lll_opy_ (u"ࠣ࡟ࠥፈ"))
            result = (
                bstack1ll11l11lll_opy_(target, bstack1ll11ll111l_opy_, *args, **kwargs)
                if callable(bstack1ll11l11lll_opy_)
                else bstack1ll11ll111l_opy_(target, *args, **kwargs)
            )
            bstack1ll11lll111_opy_ = self.bstack1l1lll1l1_opy_(
                target,
                (instance, method_name),
                (bstack1ll11l1lll1_opy_, bstack1l11l11l1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll11l11l11_opy_(instance, method_name, datetime.now() - bstack11lllll111_opy_, *args, **kwargs)
            return bstack1ll11lll111_opy_ if bstack1ll11lll111_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll11l1lll1_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll11ll11l1_opy_(target: object, strict=True):
        ctx = bstack1ll11llll1l_opy_.create_context(target)
        instance = bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll111ll111_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll111ll1ll_opy_(
        ctx: bstack1ll11l1l1l1_opy_, state: bstack11lll111_opy_, reverse=True
    ) -> List[bstack1ll11ll1l11_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11ll11l1_opy_.bstack1111l1ll1l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll11lll1l1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1lll1l_opy_(instance: bstack1ll11ll1l11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1l11llll_opy_(instance: bstack1ll11ll1l11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1111ll_opy_(instance: bstack1ll11ll1l11_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11ll11l1_opy_.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡰ࡫ࡹ࠾ࡽ࡮ࡩࡾࢃࠠࡷࡣ࡯ࡹࡪࡃࠢፉ") + str(value) + bstack1ll1lll_opy_ (u"ࠥࠦፊ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(target, strict)
        return bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1ll11l1111l_opy_(self):
        return self.framework_name == bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨፋ")
    def bstack1ll11ll1l1l_opy_(self, target):
        return target if not self.bstack1ll11l1111l_opy_() else self.bstack1ll11l111ll_opy_()
    @staticmethod
    def bstack1ll11l111ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())