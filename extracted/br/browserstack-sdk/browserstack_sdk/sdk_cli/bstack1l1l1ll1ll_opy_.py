# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1l1ll11ll1l_opy_ import bstack1l1ll11l1l1_opy_, bstack1l1ll11lll1_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1ll111111l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1ll1l11_opy_ (u"ࠥࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᑛ").format(self.name)
class bstack1l1111l1l1_opy_(Enum):
    NONE = 0
    bstack1l111l11ll_opy_ = 1
    bstack1l1l1lllll1_opy_ = 3
    bstack1l1llllll11_opy_ = 4
    bstack1l1ll111111_opy_ = 5
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
        return bstack1ll1l11_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᑜ").format(self.name)
class bstack1l1ll1111l1_opy_(bstack1l1ll11l1l1_opy_):
    framework_name: str
    framework_version: str
    state: bstack1l1111l1l1_opy_
    previous_state: bstack1l1111l1l1_opy_
    bstack1l1ll1l1lll_opy_: datetime
    bstack1l1ll1l111l_opy_: datetime
    def __init__(
        self,
        context: bstack1l1ll11lll1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1l1111l1l1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1l1111l1l1_opy_.NONE
        self.bstack1l1ll1l1lll_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l1ll1l111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll11l1ll_opy_(self, bstack1l1ll111l1l_opy_: bstack1l1111l1l1_opy_):
        bstack1l1ll1ll111_opy_ = bstack1l1111l1l1_opy_(bstack1l1ll111l1l_opy_).name
        if not bstack1l1ll1ll111_opy_:
            return False
        if bstack1l1ll111l1l_opy_ == self.state:
            return False
        if self.state == bstack1l1111l1l1_opy_.bstack1l1l1lllll1_opy_: # bstack1l1ll1ll1l1_opy_ bstack1l1l1llllll_opy_ for bstack1l1ll1l1111_opy_ in Playwright, it bstack1l1ll1lll1l_opy_ bstack1l1ll111ll1_opy_ bstack1l1ll1l1ll1_opy_ times bstack1l1ll11111l_opy_ a new state
            return True
        if (
            bstack1l1ll111l1l_opy_ == bstack1l1111l1l1_opy_.NONE
            or (self.state != bstack1l1111l1l1_opy_.NONE and bstack1l1ll111l1l_opy_ == bstack1l1111l1l1_opy_.bstack1l111l11ll_opy_)
            or (self.state < bstack1l1111l1l1_opy_.bstack1l111l11ll_opy_ and bstack1l1ll111l1l_opy_ == bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_)
            or (self.state < bstack1l1111l1l1_opy_.bstack1l111l11ll_opy_ and bstack1l1ll111l1l_opy_ == bstack1l1111l1l1_opy_.QUIT)
        ):
            raise ValueError(bstack1ll1l11_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡵࡣࡷࡩࠥࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࠦᑝ") + str(self.state) + bstack1ll1l11_opy_ (u"ࠨࠠ࠾ࡀࠣࠦᑞ") + str(bstack1l1ll111l1l_opy_))
        self.previous_state = self.state
        self.state = bstack1l1ll111l1l_opy_
        self.bstack1l1ll1l111l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1111lll1ll_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11l111111_opy_: Dict[str, bstack1l1ll1111l1_opy_] = dict()
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
    def bstack1l1ll11l111_opy_(self, instance: bstack1l1ll1111l1_opy_, method_name: str, bstack1l1lll1111l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1l1ll111l11_opy_(
        self, method_name, previous_state: bstack1l1111l1l1_opy_, *args, **kwargs
    ) -> bstack1l1111l1l1_opy_:
        return
    @abc.abstractmethod
    def bstack11lll1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1l1ll111lll_opy_(self, bstack1l1ll1l1l11_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1l1ll1l1l11_opy_:
                bstack1l1lll111ll_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1l1lll111ll_opy_):
                    self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡶࡰࡳࡥࡹࡩࡨࡦࡦࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᑟ") + str(method_name) + bstack1ll1l11_opy_ (u"ࠣࠤᑠ"))
                    continue
                bstack1l1ll11ll11_opy_ = self.bstack1l1ll111l11_opy_(
                    method_name, previous_state=bstack1l1111l1l1_opy_.NONE
                )
                bstack1l1lll111l1_opy_ = self.bstack1l1ll1111ll_opy_(
                    method_name,
                    (bstack1l1ll11ll11_opy_ if bstack1l1ll11ll11_opy_ else bstack1l1111l1l1_opy_.NONE),
                    bstack1l1lll111ll_opy_,
                )
                if not callable(bstack1l1lll111l1_opy_):
                    self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠢࡱࡳࡹࠦࡰࡢࡶࡦ࡬ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࠪࡾࡷࡪࡲࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᑡ") + str(self.framework_version) + bstack1ll1l11_opy_ (u"ࠥ࠭ࠧᑢ"))
                    continue
                setattr(clazz, method_name, bstack1l1lll111l1_opy_)
    def bstack1l1ll1111ll_opy_(
        self,
        method_name: str,
        bstack1l1ll11ll11_opy_: bstack1l1111l1l1_opy_,
        bstack1l1lll111ll_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l11llll_opy_ = datetime.now()
            (bstack1l1ll11ll11_opy_,) = wrapped.__vars__
            bstack1l1ll11ll11_opy_ = (
                bstack1l1ll11ll11_opy_
                if bstack1l1ll11ll11_opy_ and bstack1l1ll11ll11_opy_ != bstack1l1111l1l1_opy_.NONE
                else self.bstack1l1ll111l11_opy_(method_name, previous_state=bstack1l1ll11ll11_opy_, *args, **kwargs)
            )
            if bstack1l1ll11ll11_opy_ == bstack1l1111l1l1_opy_.bstack1l111l11ll_opy_:
                ctx = bstack1l1ll11l1l1_opy_.create_context(self.bstack1l1ll11llll_opy_(target))
                if not self.bstack1l1ll1l11ll_opy_() or ctx.id not in bstack1111lll1ll_opy_.bstack11l111111_opy_:
                    bstack1111lll1ll_opy_.bstack11l111111_opy_[ctx.id] = bstack1l1ll1111l1_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1l1ll11ll11_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1l1ll11l11l_opy_ = None
                    if label:
                        if bstack1ll1l11_opy_ (u"ࠦࠨࠨᑣ") in label:
                            suffix = label.rsplit(bstack1ll1l11_opy_ (u"ࠧࠩࠢᑤ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1l1ll11l11l_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1l1ll1ll11l_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᑥ")
                                )
                        else:
                            self.logger.debug(
                                bstack1l1ll1ll11l_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᑦ")
                            )
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡴࡳࡣࡦ࡯ࡪࡪࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤࡷࡧ࡮࡬࠿ࡾࡶࡦࡴ࡫ࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᑧ") + str(bstack1111lll1ll_opy_.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠤࠥᑨ"))
                    bstack1l1ll1lllll_opy_ = bstack1111lll1ll_opy_.bstack1l1ll1l1l1l_opy_(self.bstack1l1ll11llll_opy_(target))
                    bstack1l1ll1lllll_opy_.data[bstack1ll1l11_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᑩ")] = bstack1l1ll11l11l_opy_
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᑪ") + str(bstack1111lll1ll_opy_.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠧࠨᑫ"))
            else:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡪࡰࡹࡳࡰ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣᑬ") + str(bstack1111lll1ll_opy_.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠢࠣᑭ"))
            instance = bstack1111lll1ll_opy_.bstack1l1ll1l1l1l_opy_(self.bstack1l1ll11llll_opy_(target))
            if bstack1l1ll11ll11_opy_ == bstack1l1111l1l1_opy_.NONE or not instance:
                ctx = bstack1l1ll11l1l1_opy_.create_context(self.bstack1l1ll11llll_opy_(target))
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡸࡲࡹࡸࡡࡤ࡭ࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᑮ") + str(bstack1111lll1ll_opy_.bstack11l111111_opy_.keys()) + bstack1ll1l11_opy_ (u"ࠤࠥᑯ"))
                return bstack1l1lll111ll_opy_(target, *args, **kwargs)
            bstack1l1ll1llll1_opy_ = self.bstack11lll1l1_opy_(
                target,
                (instance, method_name),
                (bstack1l1ll11ll11_opy_, bstack1ll111111l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1ll11l1ll_opy_(bstack1l1ll11ll11_opy_):
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡥࡵࡶ࡬ࡪࡧࡧࠤࡸࡺࡡࡵࡧ࠰ࡸࡷࡧ࡮ࡴ࡫ࡷ࡭ࡴࡴ࠺ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡵࡸࡥࡷ࡫ࡲࡹࡸࡥࡳࡵࡣࡷࡩࢂࠦ࠽࠿ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡹࡴࡢࡶࡨࢁࠥ࠮ࡻࡵࡻࡳࡩ࠭ࡺࡡࡳࡩࡨࡸ࠮ࢃ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡼࡣࡵ࡫ࡸࢃࠩࠡ࡝ࠥᑰ") + str(instance.ref()) + bstack1ll1l11_opy_ (u"ࠦࡢࠨᑱ"))
            result = (
                bstack1l1ll1llll1_opy_(target, bstack1l1lll111ll_opy_, *args, **kwargs)
                if callable(bstack1l1ll1llll1_opy_)
                else bstack1l1lll111ll_opy_(target, *args, **kwargs)
            )
            bstack1l1lll11111_opy_ = self.bstack11lll1l1_opy_(
                target,
                (instance, method_name),
                (bstack1l1ll11ll11_opy_, bstack1ll111111l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1l1ll11l111_opy_(instance, method_name, datetime.now() - bstack1l1l11llll_opy_, *args, **kwargs)
            return bstack1l1lll11111_opy_ if bstack1l1lll11111_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1l1ll11ll11_opy_,)
        return wrapped
    @staticmethod
    def bstack1l1ll1l1l1l_opy_(target: object, strict=True):
        ctx = bstack1l1ll11l1l1_opy_.create_context(target)
        instance = bstack1111lll1ll_opy_.bstack11l111111_opy_.get(ctx.id, None)
        if instance and instance.bstack1l1ll1lll11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1l1ll11l1ll_opy_(
        ctx: bstack1l1ll11lll1_opy_, state: bstack1l1111l1l1_opy_, reverse=True
    ) -> List[bstack1l1ll1111l1_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1111lll1ll_opy_.bstack11l111111_opy_.values(),
            ),
            key=lambda t: t.bstack1l1ll1l1lll_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1l1llll1111_opy_(instance: bstack1l1ll1111l1_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1l1lll1ll11_opy_(instance: bstack1l1ll1111l1_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll11l1ll_opy_(instance: bstack1l1ll1111l1_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1111lll1ll_opy_.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠ࡬ࡧࡼࡁࢀࡱࡥࡺࡿࠣࡺࡦࡲࡵࡦ࠿ࠥᑲ") + str(value) + bstack1ll1l11_opy_ (u"ࠨࠢᑳ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1111lll1ll_opy_.bstack1l1ll1l1l1l_opy_(target, strict)
        return bstack1111lll1ll_opy_.bstack1l1lll1ll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1111lll1ll_opy_.bstack1l1ll1l1l1l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1l1ll1l11ll_opy_(self):
        return self.framework_name == bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᑴ")
    def bstack1l1ll11llll_opy_(self, target):
        return target if not self.bstack1l1ll1l11ll_opy_() else self.bstack1l1ll1l11l1_opy_()
    @staticmethod
    def bstack1l1ll1l11l1_opy_():
        return str(os.getpid()) + str(threading.get_ident())