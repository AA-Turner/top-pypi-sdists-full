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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l11l1l1l_opy_
from browserstack_sdk.bstack1ll11l1ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll1l111ll_opy_, bstack1llll1l1l11_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack11111l1l_opy_
from bstack_utils.constants import bstack1llll1ll11l_opy_
from bstack_utils.bstack111ll11ll_opy_ import bstack1l1lllll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll1lllll_opy_ import bstack1lllll1l1l1_opy_
class bstack11l111l11l_opy_:
    def __init__(self, args, logger, bstack1lllll1ll1l_opy_, bstack1lllll111l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lllll1ll1l_opy_ = bstack1lllll1ll1l_opy_
        self.bstack1lllll111l1_opy_ = bstack1lllll111l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1ll1l1_opy_ = []
        self.bstack1llll11ll11_opy_ = []
        self.bstack1l111ll11_opy_ = []
        self.bstack1lllll1ll11_opy_ = self.bstack11l1l111l_opy_()
        self.bstack111lll1l_opy_ = -1
    @measure(event_name=EVENTS.bstack1llll11l1ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack111l1lll1l_opy_(self, bstack1llll1ll1l1_opy_):
        self.parse_args()
        self.bstack1llll1l11ll_opy_()
        self.bstack1lllll11111_opy_(bstack1llll1ll1l1_opy_)
        self.bstack1llll1l1111_opy_()
    @measure(event_name=EVENTS.bstack1lllll11l1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack11l11ll11l_opy_(self):
        bstack111ll11ll_opy_ = bstack1l1lllll1l_opy_.bstack1l11l11l1_opy_(self.bstack1lllll1ll1l_opy_, self.logger)
        if bstack111ll11ll_opy_ is None:
            self.logger.warn(bstack11l1ll1_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨჰ"))
            return
        bstack1llll11l111_opy_ = False
        bstack111ll11ll_opy_.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧჱ"), bstack111ll11ll_opy_.bstack1ll11l1lll_opy_())
        start_time = time.time()
        if bstack111ll11ll_opy_.bstack1ll11l1lll_opy_():
            test_files = self.bstack1llll11llll_opy_()
            bstack1llll11l111_opy_ = True
            bstack1llll1l1l1l_opy_ = bstack111ll11ll_opy_.bstack1llll1ll1ll_opy_(test_files)
            if bstack1llll1l1l1l_opy_:
                self.bstack11l1ll1l1_opy_ = [os.path.normpath(item) for item in bstack1llll1l1l1l_opy_]
                self.__1lllll11l11_opy_()
                bstack111ll11ll_opy_.bstack1lllll11lll_opy_(bstack1llll11l111_opy_)
                self.logger.info(bstack11l1ll1_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥჲ").format(self.bstack11l1ll1l1_opy_))
            else:
                self.logger.info(bstack11l1ll1_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦჳ"))
        bstack111ll11ll_opy_.bstack1lllll1111l_opy_(bstack11l1ll1_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥჴ"), int((time.time() - start_time) * 1000)) # bstack1llll1llll1_opy_ to bstack1llll1l11l1_opy_
    def __1lllll11l11_opy_(self):
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡱ࡮ࡤࡧࡪࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡ࡫ࡱࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡺࡵࡳࡰࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡧ࡫࡯ࡩࠥࡴࡡ࡮ࡧࡶ࠰ࠥࡧ࡮ࡥࠢࡺࡩࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡻࡰࡥࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡇࡑࡏࠠࡢࡴࡪࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡺࡨࡰࡵࡨࠤ࡫࡯࡬ࡦࡵ࠱ࠤ࡚ࡹࡥࡳࠩࡶࠤ࡫࡯࡬ࡵࡧࡵ࡭ࡳ࡭ࠠࡧ࡮ࡤ࡫ࡸࠦࠨ࠮࡯࠯ࠤ࠲ࡱࠩࠡࡴࡨࡱࡦ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡧࡣࡵࠢࡤࡲࡩࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡢࡲࡳࡰ࡮࡫ࡤࠡࡰࡤࡸࡺࡸࡡ࡭࡮ࡼࠤࡩࡻࡲࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨჵ")
        try:
            if not self.bstack11l1ll1l1_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡑࡳࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡴࡦࡺࡨࠡࡶࡲࠤࡸ࡫ࡴࠣჶ"))
                return
            bstack1lllll1l11l_opy_ = []
            for flag in self.bstack1llll11ll11_opy_:
                if flag.startswith(bstack11l1ll1_opy_ (u"ࠪ࠱ࠬჷ")):
                    bstack1lllll1l11l_opy_.append(flag)
                    continue
                bstack1llll11lll1_opy_ = False
                if bstack11l1ll1_opy_ (u"ࠫ࠿ࡀࠧჸ") in flag:
                    bstack1llll1l111l_opy_ = flag.split(bstack11l1ll1_opy_ (u"ࠬࡀ࠺ࠨჹ"), 1)[0]
                    if os.path.exists(bstack1llll1l111l_opy_):
                        bstack1llll11lll1_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11l1ll1_opy_ (u"࠭࠮ࡱࡻࠪჺ"))):
                        bstack1llll11lll1_opy_ = True
                if not bstack1llll11lll1_opy_:
                    bstack1lllll1l11l_opy_.append(flag)
            bstack1lllll1l11l_opy_.extend(self.bstack11l1ll1l1_opy_)
            self.bstack1llll11ll11_opy_ = bstack1lllll1l11l_opy_
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡶࡩࡱ࡫ࡣࡵࡱࡵࡷ࠿ࠦࡻࡾࠤ჻").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llll111lll_opy_():
        return bstack1lllll1l1l1_opy_(bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪჼ"))
    def bstack1llll11l11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111lll1l_opy_ = -1
        if self.bstack1lllll111l1_opy_ and bstack11l1ll1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩჽ") in self.bstack1lllll1ll1l_opy_:
            self.bstack111lll1l_opy_ = int(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪჾ")])
        try:
            bstack1llll1ll111_opy_ = [bstack11l1ll1_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ჿ"), bstack11l1ll1_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨᄀ"), bstack11l1ll1_opy_ (u"࠭࠭ࡱࠩᄁ")]
            if self.bstack111lll1l_opy_ >= 0:
                bstack1llll1ll111_opy_.extend([bstack11l1ll1_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨᄂ"), bstack11l1ll1_opy_ (u"ࠨ࠯ࡱࠫᄃ")])
            for arg in bstack1llll1ll111_opy_:
                self.bstack1llll11l11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll1l11ll_opy_(self):
        bstack1llll11ll11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        return self.bstack1llll11ll11_opy_
    def bstack1l11l11ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llll111lll_opy_():
                self.logger.warning(bstack1llll1l1l11_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤᄄ"), bstack1ll1l111ll_opy_, str(e))
    def bstack1lllll11111_opy_(self, bstack1llll1ll1l1_opy_):
        bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
        if bstack1llll1ll1l1_opy_:
            self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᄅ"))
            self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"࡙ࠫࡸࡵࡦࠩᄆ"))
        if bstack11lll111l_opy_.bstack1lllll1l1ll_opy_():
            self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᄇ"))
            self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"࠭ࡔࡳࡷࡨࠫᄈ"))
        self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠧ࠮ࡲࠪᄉ"))
        self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ᄊ"))
        self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫᄋ"))
        self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᄌ"))
        if self.bstack111lll1l_opy_ > 1:
            self.bstack1llll11ll11_opy_.append(bstack11l1ll1_opy_ (u"ࠫ࠲ࡴࠧᄍ"))
            self.bstack1llll11ll11_opy_.append(str(self.bstack111lll1l_opy_))
    def bstack1llll1l1111_opy_(self):
        if bstack11111l1l_opy_.bstack1lll1l1l_opy_(self.bstack1lllll1ll1l_opy_):
             self.bstack1llll11ll11_opy_ += [
                bstack1llll1ll11l_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫᄎ")), str(bstack11111l1l_opy_.bstack11ll1ll1l1_opy_(self.bstack1lllll1ll1l_opy_)),
                bstack1llll1ll11l_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬᄏ")), str(bstack1llll1ll11l_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬᄐ")))
            ]
    def bstack1llll1lll11_opy_(self):
        bstack1l111ll11_opy_ = []
        for spec in self.bstack11l1ll1l1_opy_:
            bstack111lllll_opy_ = [spec]
            bstack111lllll_opy_ += self.bstack1llll11ll11_opy_
            bstack1l111ll11_opy_.append(bstack111lllll_opy_)
        self.bstack1l111ll11_opy_ = bstack1l111ll11_opy_
        return bstack1l111ll11_opy_
    def bstack11l1l111l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lllll1ll11_opy_ = True
            return True
        except Exception as e:
            self.bstack1lllll1ll11_opy_ = False
        return self.bstack1lllll1ll11_opy_
    @measure(event_name=EVENTS.bstack1llll11l1l1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack11lllll1_opy_(self):
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࡳࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᄑ")
        try:
            from browserstack_sdk.bstack1lllllll111_opy_ import bstack1llllll11l1_opy_
            bstack1lllll1l111_opy_ = bstack1llllll11l1_opy_(bstack1llllll1l1l_opy_=self.bstack1llll11ll11_opy_)
            if not bstack1lllll1l111_opy_.get(bstack11l1ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᄒ"), False):
                self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡥࡲࡹࡳࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᄓ").format(bstack1lllll1l111_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᄔ"), bstack11l1ll1_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᄕ"))))
                return 0
            count = bstack1lllll1l111_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᄖ"), 0)
            self.logger.info(bstack11l1ll1_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧᄗ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᄘ").format(e))
            return 0
    def bstack11ll11l1l_opy_(self, bstack1llll11ll1l_opy_, bstack111l1lll1l_opy_):
        bstack111l1lll1l_opy_[bstack11l1ll1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩᄙ")] = self.bstack1lllll1ll1l_opy_
        multiprocessing.set_start_method(bstack11l1ll1_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩᄚ"))
        bstack111llll111_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllll11ll1_opy_ = manager.list()
        if bstack11l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᄛ") in self.bstack1lllll1ll1l_opy_:
            for index, platform in enumerate(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄜ")]):
                bstack111llll111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll11ll1l_opy_,
                                                            args=(self.bstack1llll11ll11_opy_, bstack111l1lll1l_opy_, bstack1lllll11ll1_opy_)))
            bstack1lllll111ll_opy_ = len(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᄝ")])
        else:
            bstack111llll111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll11ll1l_opy_,
                                                        args=(self.bstack1llll11ll11_opy_, bstack111l1lll1l_opy_, bstack1lllll11ll1_opy_)))
            bstack1lllll111ll_opy_ = 1
        i = 0
        for t in bstack111llll111_opy_:
            os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᄞ")] = str(i)
            if bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄟ") in self.bstack1lllll1ll1l_opy_:
                os.environ[bstack11l1ll1_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪᄠ")] = json.dumps(self.bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄡ")][i % bstack1lllll111ll_opy_])
            i += 1
            t.start()
        for t in bstack111llll111_opy_:
            t.join()
        return list(bstack1lllll11ll1_opy_)
    @staticmethod
    def bstack11l1l1l11l_opy_(driver, bstack1llll1lll1l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᄢ"), None)
        if item and getattr(item, bstack11l1ll1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧᄣ"), None) and not getattr(item, bstack11l1ll1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨᄤ"), False):
            logger.info(
                bstack11l1ll1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨᄥ"))
            bstack1llll1l1lll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11l1l1l_opy_.bstack11ll1l111_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llll11llll_opy_(self):
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᄦ")
        try:
            from browserstack_sdk.bstack1lllllll111_opy_ import bstack1llllll11l1_opy_
            bstack1llll1l1ll1_opy_ = bstack1llllll11l1_opy_(bstack1llllll1l1l_opy_=self.bstack1llll11ll11_opy_)
            if not bstack1llll1l1ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᄧ"), False):
                self.logger.error(bstack11l1ll1_opy_ (u"ࠥࡘࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢᄨ").format(bstack1llll1l1ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᄩ"), bstack11l1ll1_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᄪ"))))
                return []
            test_files = bstack1llll1l1ll1_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠪᄫ"), [])
            count = bstack1llll1l1ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᄬ"), 0)
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡾࢁࠥ࡬ࡩ࡭ࡧࡶࠦᄭ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᄮ").format(e))
            return []