# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1lll1111ll1_opy_ import bstack1ll1lllllll_opy_, bstack1ll1lll11l1_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1lll111l1l1_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11ll111_opy_ (u"ࠢࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᇔ").format(self.name)
class bstack1ll1ll1l1l1_opy_(Enum):
    NONE = 0
    bstack1lll1111l11_opy_ = 1
    bstack1lll111lll1_opy_ = 3
    bstack1ll1ll1l11l_opy_ = 4
    bstack1lll11l1lll_opy_ = 5
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
        return bstack11ll111_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᇕ").format(self.name)
class bstack1ll1lll1111_opy_(bstack1ll1lllllll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1ll1ll1l1l1_opy_
    previous_state: bstack1ll1ll1l1l1_opy_
    bstack1ll1lll1l1l_opy_: datetime
    bstack1lll11l11ll_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1lll11l1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1ll1ll1l1l1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1ll1ll1l1l1_opy_.NONE
        self.bstack1ll1lll1l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll11l11ll_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll11l1111_opy_(self, bstack1lll11ll11l_opy_: bstack1ll1ll1l1l1_opy_):
        bstack1ll1lll1l11_opy_ = bstack1ll1ll1l1l1_opy_(bstack1lll11ll11l_opy_).name
        if not bstack1ll1lll1l11_opy_:
            return False
        if bstack1lll11ll11l_opy_ == self.state:
            return False
        if self.state == bstack1ll1ll1l1l1_opy_.bstack1lll111lll1_opy_: # bstack1ll1ll1l111_opy_ bstack1ll1llll1l1_opy_ for bstack1ll1llllll1_opy_ in bstack1lll11ll111_opy_, it bstack1ll1lll11ll_opy_ bstack1ll1lllll1l_opy_ bstack1ll1llll11l_opy_ times bstack1ll1ll1l1ll_opy_ a new state
            return True
        if (
            bstack1lll11ll11l_opy_ == bstack1ll1ll1l1l1_opy_.NONE
            or (self.state != bstack1ll1ll1l1l1_opy_.NONE and bstack1lll11ll11l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_)
            or (self.state < bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_ and bstack1lll11ll11l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_)
            or (self.state < bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_ and bstack1lll11ll11l_opy_ == bstack1ll1ll1l1l1_opy_.QUIT)
        ):
            raise ValueError(bstack11ll111_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡹࡧࡴࡦࠢࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࠣᇖ") + str(self.state) + bstack11ll111_opy_ (u"ࠥࠤࡂࡄࠠࠣᇗ") + str(bstack1lll11ll11l_opy_))
        self.previous_state = self.state
        self.state = bstack1lll11ll11l_opy_
        self.bstack1lll11l11ll_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1ll1ll1lll1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1lll1ll1_opy_: Dict[str, bstack1ll1lll1111_opy_] = dict()
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
    def bstack1lll11l1l11_opy_(self, instance: bstack1ll1lll1111_opy_, method_name: str, bstack1lll11l111l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lll1111lll_opy_(
        self, method_name, previous_state: bstack1ll1ll1l1l1_opy_, *args, **kwargs
    ) -> bstack1ll1ll1l1l1_opy_:
        return
    @abc.abstractmethod
    def bstack1ll1lll1lll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lll111ll1l_opy_(self, bstack1ll1ll1ll1l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1ll1ll1ll1l_opy_:
                bstack1lll111ll11_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1lll111ll11_opy_):
                    self.logger.warning(bstack11ll111_opy_ (u"ࠦࡺࡴࡰࡢࡶࡦ࡬ࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࠤᇘ") + str(method_name) + bstack11ll111_opy_ (u"ࠧࠨᇙ"))
                    continue
                bstack1lll111111l_opy_ = self.bstack1lll1111lll_opy_(
                    method_name, previous_state=bstack1ll1ll1l1l1_opy_.NONE
                )
                bstack1lll11l1l1l_opy_ = self.bstack1lll11l1ll1_opy_(
                    method_name,
                    (bstack1lll111111l_opy_ if bstack1lll111111l_opy_ else bstack1ll1ll1l1l1_opy_.NONE),
                    bstack1lll111ll11_opy_,
                )
                if not callable(bstack1lll11l1l1l_opy_):
                    self.logger.warning(bstack11ll111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠦ࡮ࡰࡶࠣࡴࡦࡺࡣࡩࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࠮ࡻࡴࡧ࡯ࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃ࠺ࠡࠤᇚ") + str(self.framework_version) + bstack11ll111_opy_ (u"ࠢࠪࠤᇛ"))
                    continue
                setattr(clazz, method_name, bstack1lll11l1l1l_opy_)
    def bstack1lll11l1ll1_opy_(
        self,
        method_name: str,
        bstack1lll111111l_opy_: bstack1ll1ll1l1l1_opy_,
        bstack1lll111ll11_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11lll11111_opy_ = datetime.now()
            (bstack1lll111111l_opy_,) = wrapped.__vars__
            bstack1lll111111l_opy_ = (
                bstack1lll111111l_opy_
                if bstack1lll111111l_opy_ and bstack1lll111111l_opy_ != bstack1ll1ll1l1l1_opy_.NONE
                else self.bstack1lll1111lll_opy_(method_name, previous_state=bstack1lll111111l_opy_, *args, **kwargs)
            )
            if bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.bstack1lll1111l11_opy_:
                ctx = bstack1ll1lllllll_opy_.create_context(self.bstack1lll111l111_opy_(target))
                if not self.bstack1ll1ll1ll11_opy_() or ctx.id not in bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_:
                    bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_[ctx.id] = bstack1ll1lll1111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lll111111l_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1ll1llll111_opy_ = None
                    if label:
                        if bstack11ll111_opy_ (u"ࠣࠥࠥᇜ") in label:
                            suffix = label.rsplit(bstack11ll111_opy_ (u"ࠤࠦࠦᇝ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1ll1llll111_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1lll11111l1_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡩࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࡷࡺ࡬ࡦࡪࡺࠣࠫࢀࡹࡵࡧࡨ࡬ࡼࢂ࠭ࠠࡪࡰࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡰࡸࡱࡪࡸࡩࡤࠢࡵࡥࡳࡱ࠮ࠣᇞ")
                                )
                        else:
                            self.logger.debug(
                                bstack1lll11111l1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡥࡲࡲࡹࡧࡩ࡯ࠢࠪࠧࠬࡁࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡵࡥࡳࡱࠠࡢࡵࡶ࡭࡬ࡴ࡭ࡦࡰࡷ࠲ࠧᇟ")
                            )
                    self.logger.debug(bstack11ll111_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠦ࡮ࡦࡹࠣࡸࡷࡧࡣ࡬ࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡴࡤࡲࡰࡃࡻࡳࡣࡱ࡯ࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᇠ") + str(bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠨࠢᇡ"))
                    bstack1lll111l11l_opy_ = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(self.bstack1lll111l111_opy_(target))
                    bstack1lll111l11l_opy_.data[bstack11ll111_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᇢ")] = bstack1ll1llll111_opy_
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᇣ") + str(bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠤࠥᇤ"))
            else:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤ࡮ࡴࡶࡰ࡭ࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᇥ") + str(bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠦࠧᇦ"))
            instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(self.bstack1lll111l111_opy_(target))
            if bstack1lll111111l_opy_ == bstack1ll1ll1l1l1_opy_.NONE or not instance:
                ctx = bstack1ll1lllllll_opy_.create_context(self.bstack1lll111l111_opy_(target))
                self.logger.warning(bstack11ll111_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡵ࡯ࡶࡵࡥࡨࡱࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢࡦࡸࡽࡃࡻࡤࡶࡻࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᇧ") + str(bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.keys()) + bstack11ll111_opy_ (u"ࠨࠢᇨ"))
                return bstack1lll111ll11_opy_(target, *args, **kwargs)
            bstack1lll1111l1l_opy_ = self.bstack1ll1lll1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lll111111l_opy_, bstack1lll111l1l1_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll11l1111_opy_(bstack1lll111111l_opy_):
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡢࡲࡳࡰ࡮࡫ࡤࠡࡵࡷࡥࡹ࡫࠭ࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡲࡵࡩࡻ࡯࡯ࡶࡵࡢࡷࡹࡧࡴࡦࡿࠣࡁࡃࠦࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡶࡸࡦࡺࡥࡾࠢࠫࡿࡹࡿࡰࡦࠪࡷࡥࡷ࡭ࡥࡵࠫࢀ࠲ࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤࢀࡧࡲࡨࡵࢀ࠭ࠥࡡࠢᇩ") + str(instance.ref()) + bstack11ll111_opy_ (u"ࠣ࡟ࠥᇪ"))
            result = (
                bstack1lll1111l1l_opy_(target, bstack1lll111ll11_opy_, *args, **kwargs)
                if callable(bstack1lll1111l1l_opy_)
                else bstack1lll111ll11_opy_(target, *args, **kwargs)
            )
            bstack1ll1llll1ll_opy_ = self.bstack1ll1lll1lll_opy_(
                target,
                (instance, method_name),
                (bstack1lll111111l_opy_, bstack1lll111l1l1_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1lll11l1l11_opy_(instance, method_name, datetime.now() - bstack11lll11111_opy_, *args, **kwargs)
            return bstack1ll1llll1ll_opy_ if bstack1ll1llll1ll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lll111111l_opy_,)
        return wrapped
    @staticmethod
    def bstack1lll1111111_opy_(target: object, strict=True):
        ctx = bstack1ll1lllllll_opy_.create_context(target)
        instance = bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll111l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lll11l11l1_opy_(
        ctx: bstack1ll1lll11l1_opy_, state: bstack1ll1ll1l1l1_opy_, reverse=True
    ) -> List[bstack1ll1lll1111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1ll1ll1lll1_opy_.bstack1ll1lll1ll1_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1lll111l_opy_(instance: bstack1ll1lll1111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1lllll11_opy_(instance: bstack1ll1lll1111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll11l1111_opy_(instance: bstack1ll1lll1111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1ll1ll1lll1_opy_.logger.debug(bstack11ll111_opy_ (u"ࠤࡶࡩࡹࡥࡳࡵࡣࡷࡩ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡷ࡫ࡦࠩࠫࢀࠤࡰ࡫ࡹ࠾ࡽ࡮ࡩࡾࢃࠠࡷࡣ࡯ࡹࡪࡃࠢᇫ") + str(value) + bstack11ll111_opy_ (u"ࠥࠦᇬ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(target, strict)
        return bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1ll1ll1ll11_opy_(self):
        return self.framework_name == bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᇭ")
    def bstack1lll111l111_opy_(self, target):
        return target if not self.bstack1ll1ll1ll11_opy_() else self.bstack1lll111llll_opy_()
    @staticmethod
    def bstack1lll111llll_opy_():
        return str(os.getpid()) + str(threading.get_ident())