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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1l11l1l111_opy_
from browserstack_sdk.bstack1ll11l111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1l1111l_opy_, bstack1lllll11ll1_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l1llll1l_opy_
from bstack_utils.constants import bstack1lllll111ll_opy_
from bstack_utils.bstack1ll1ll1l_opy_ import bstack11111l1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll11l11l_opy_ import bstack1lllll1ll11_opy_
class bstack111ll1l1ll_opy_:
    def __init__(self, args, logger, bstack1llll1l1lll_opy_, bstack1lllll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll1l1lll_opy_ = bstack1llll1l1lll_opy_
        self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1lllll1l_opy_ = []
        self.bstack1llll11ll11_opy_ = []
        self.bstack1l1l1111l1_opy_ = []
        self.bstack1llll11lll1_opy_ = self.bstack1lll11lll1_opy_()
        self.bstack11lll111l1_opy_ = -1
    @measure(event_name=EVENTS.bstack1llll1l1l1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1111111l1_opy_(self, bstack1llll1l1ll1_opy_):
        self.parse_args()
        self.bstack1llll11ll1l_opy_()
        self.bstack1lllll1l11l_opy_(bstack1llll1l1ll1_opy_)
        self.bstack1lllll1lll1_opy_()
    @measure(event_name=EVENTS.bstack1llll1ll111_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack111111ll_opy_(self):
        bstack1ll1ll1l_opy_ = bstack11111l1l1_opy_.bstack111ll1lll1_opy_(self.bstack1llll1l1lll_opy_, self.logger)
        if bstack1ll1ll1l_opy_ is None:
            self.logger.warn(bstack1l1111_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࠦࡩࡴࠢࡱࡳࡹࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧ࠲࡙ࠥ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠮ࠣძ"))
            return
        bstack1lllll11111_opy_ = False
        bstack1ll1ll1l_opy_.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡥ࡯ࡣࡥࡰࡪࡪࠢწ"), bstack1ll1ll1l_opy_.bstack1l11111l_opy_())
        start_time = time.time()
        if bstack1ll1ll1l_opy_.bstack1l11111l_opy_():
            test_files = self.bstack1llll1lll1l_opy_()
            bstack1lllll11111_opy_ = True
            bstack1llll1lll11_opy_ = bstack1ll1ll1l_opy_.bstack1lllll111l1_opy_(test_files)
            if bstack1llll1lll11_opy_:
                self.bstack1l1lllll1l_opy_ = [os.path.normpath(item) for item in bstack1llll1lll11_opy_]
                self.__1lllll1l1ll_opy_()
                bstack1ll1ll1l_opy_.bstack1lllll11lll_opy_(bstack1lllll11111_opy_)
                self.logger.info(bstack1l1111_opy_ (u"ࠢࡕࡧࡶࡸࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡸࡷ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧჭ").format(self.bstack1l1lllll1l_opy_))
            else:
                self.logger.info(bstack1l1111_opy_ (u"ࠣࡐࡲࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡹࡨࡶࡪࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡥࡽࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨხ"))
        bstack1ll1ll1l_opy_.bstack1llll1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡷ࡭ࡲ࡫ࡔࡢ࡭ࡨࡲ࡙ࡵࡁࡱࡲ࡯ࡽࠧჯ"), int((time.time() - start_time) * 1000)) # bstack1lllll1111l_opy_ to bstack1llll1ll1l1_opy_
    def __1lllll1l1ll_opy_(self):
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡳࡰࡦࡩࡥࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵࠣ࡭ࡳࠦࡃࡍࡋࠣࡪࡱࡧࡧࡴࠢࡺ࡭ࡹ࡮ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡥࡳࡸࡨࡶࠥࡸࡥࡵࡷࡵࡲࡸࠦࡲࡦࡱࡵࡨࡪࡸࡥࡥࠢࡩ࡭ࡱ࡫ࠠ࡯ࡣࡰࡩࡸ࠲ࠠࡢࡰࡧࠤࡼ࡫ࠠࡴ࡫ࡰࡴࡱࡿࠠࡶࡲࡧࡥࡹ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡶ࡫ࡩࠥࡉࡌࡊࠢࡤࡶ࡬ࡹࠠࡵࡱࠣࡹࡸ࡫ࠠࡵࡪࡲࡷࡪࠦࡦࡪ࡮ࡨࡷ࠳ࠦࡕࡴࡧࡵࠫࡸࠦࡦࡪ࡮ࡷࡩࡷ࡯࡮ࡨࠢࡩࡰࡦ࡭ࡳࠡࠪ࠰ࡱ࠱ࠦ࠭࡬ࠫࠣࡶࡪࡳࡡࡪࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴࡢࡥࡷࠤࡦࡴࡤࠡࡹ࡬ࡰࡱࠦࡢࡦࠢࡤࡴࡵࡲࡩࡦࡦࠣࡲࡦࡺࡵࡳࡣ࡯ࡰࡾࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣჰ")
        try:
            if not self.bstack1l1lllll1l_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡓࡵࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡶࡡࡵࡪࠣࡸࡴࠦࡳࡦࡶࠥჱ"))
                return
            bstack1llll1llll1_opy_ = []
            for flag in self.bstack1llll11ll11_opy_:
                if flag.startswith(bstack1l1111_opy_ (u"ࠬ࠳ࠧჲ")):
                    bstack1llll1llll1_opy_.append(flag)
                    continue
                bstack1llll1l1111_opy_ = False
                if bstack1l1111_opy_ (u"࠭࠺࠻ࠩჳ") in flag:
                    bstack1llll1ll11l_opy_ = flag.split(bstack1l1111_opy_ (u"ࠧ࠻࠼ࠪჴ"), 1)[0]
                    if os.path.exists(bstack1llll1ll11l_opy_):
                        bstack1llll1l1111_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1l1111_opy_ (u"ࠨ࠰ࡳࡽࠬჵ"))):
                        bstack1llll1l1111_opy_ = True
                if not bstack1llll1l1111_opy_:
                    bstack1llll1llll1_opy_.append(flag)
            bstack1llll1llll1_opy_.extend(self.bstack1l1lllll1l_opy_)
            self.bstack1llll11ll11_opy_ = bstack1llll1llll1_opy_
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤࡸ࡫࡬ࡦࡥࡷࡳࡷࡹ࠺ࠡࡽࢀࠦჶ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llll1ll1ll_opy_():
        return bstack1lllll1ll11_opy_(bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬჷ"))
    def bstack1llll1l1l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11lll111l1_opy_ = -1
        if self.bstack1lllll11l1l_opy_ and bstack1l1111_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫჸ") in self.bstack1llll1l1lll_opy_:
            self.bstack11lll111l1_opy_ = int(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬჹ")])
        try:
            bstack1lllll1ll1l_opy_ = [bstack1l1111_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨჺ"), bstack1l1111_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ჻"), bstack1l1111_opy_ (u"ࠨ࠯ࡳࠫჼ")]
            if self.bstack11lll111l1_opy_ >= 0:
                bstack1lllll1ll1l_opy_.extend([bstack1l1111_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪჽ"), bstack1l1111_opy_ (u"ࠪ࠱ࡳ࠭ჾ")])
            for arg in bstack1lllll1ll1l_opy_:
                self.bstack1llll1l1l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll11ll1l_opy_(self):
        bstack1llll11ll11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        return self.bstack1llll11ll11_opy_
    def bstack1ll1111ll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llll1ll1ll_opy_():
                self.logger.warning(bstack1lllll11ll1_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1l1111_opy_ (u"ࠦࠪࡹ࠺ࠡࠧࡶࠦჿ"), bstack11l1l1111l_opy_, str(e))
    def bstack1lllll1l11l_opy_(self, bstack1llll1l1ll1_opy_):
        bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
        if bstack1llll1l1ll1_opy_:
            self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᄀ"))
            self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"࠭ࡔࡳࡷࡨࠫᄁ"))
        if bstack1llllll11l_opy_.bstack1llll11l111_opy_():
            self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᄂ"))
            self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠨࡖࡵࡹࡪ࠭ᄃ"))
        self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠩ࠰ࡴࠬᄄ"))
        self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠨᄅ"))
        self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ᄆ"))
        self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᄇ"))
        if self.bstack11lll111l1_opy_ > 1:
            self.bstack1llll11ll11_opy_.append(bstack1l1111_opy_ (u"࠭࠭࡯ࠩᄈ"))
            self.bstack1llll11ll11_opy_.append(str(self.bstack11lll111l1_opy_))
    def bstack1lllll1lll1_opy_(self):
        if bstack1l1llll1l_opy_.bstack1lllll1l1l_opy_(self.bstack1llll1l1lll_opy_):
             self.bstack1llll11ll11_opy_ += [
                bstack1lllll111ll_opy_.get(bstack1l1111_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠭ᄉ")), str(bstack1l1llll1l_opy_.bstack1llll111l_opy_(self.bstack1llll1l1lll_opy_)),
                bstack1lllll111ll_opy_.get(bstack1l1111_opy_ (u"ࠨࡦࡨࡰࡦࡿࠧᄊ")), str(bstack1lllll111ll_opy_.get(bstack1l1111_opy_ (u"ࠩࡵࡩࡷࡻ࡮࠮ࡦࡨࡰࡦࡿࠧᄋ")))
            ]
    def bstack1llll1l11l1_opy_(self):
        bstack1l1l1111l1_opy_ = []
        for spec in self.bstack1l1lllll1l_opy_:
            bstack1ll1111l1l_opy_ = [spec]
            bstack1ll1111l1l_opy_ += self.bstack1llll11ll11_opy_
            bstack1l1l1111l1_opy_.append(bstack1ll1111l1l_opy_)
        self.bstack1l1l1111l1_opy_ = bstack1l1l1111l1_opy_
        return bstack1l1l1111l1_opy_
    def bstack1lll11lll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llll11lll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1llll11lll1_opy_ = False
        return self.bstack1llll11lll1_opy_
    @measure(event_name=EVENTS.bstack1lllll1l1l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack111l1ll1_opy_(self):
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡹ࡮ࡥ࡮ࠢࡸࡷ࡮ࡴࡧࠡࡲࡼࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷ࠾࡚ࠥࡨࡦࠢࡷࡳࡹࡧ࡬ࠡࡰࡸࡱࡧ࡫ࡲࠡࡱࡩࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᄌ")
        try:
            from browserstack_sdk.bstack1llllll1l11_opy_ import bstack1llllll1l1l_opy_
            bstack1llll1l111l_opy_ = bstack1llllll1l1l_opy_(bstack1llllll11l1_opy_=self.bstack1llll11ll11_opy_)
            if not bstack1llll1l111l_opy_.get(bstack1l1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᄍ"), False):
                self.logger.error(bstack1l1111_opy_ (u"࡚ࠧࡥࡴࡶࠣࡧࡴࡻ࡮ࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠥᄎ").format(bstack1llll1l111l_opy_.get(bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᄏ"), bstack1l1111_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧᄐ"))))
                return 0
            count = bstack1llll1l111l_opy_.get(bstack1l1111_opy_ (u"ࠨࡥࡲࡹࡳࡺࠧᄑ"), 0)
            self.logger.info(bstack1l1111_opy_ (u"ࠤࡗࡳࡹࡧ࡬ࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠽ࠤࢀࢃࠢᄒ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢᄓ").format(e))
            return 0
    def bstack111ll1l11_opy_(self, bstack1lllll1l111_opy_, bstack1111111l1_opy_):
        bstack1111111l1_opy_[bstack1l1111_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫᄔ")] = self.bstack1llll1l1lll_opy_
        multiprocessing.set_start_method(bstack1l1111_opy_ (u"ࠬࡹࡰࡢࡹࡱࠫᄕ"))
        bstack111l11ll11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll11llll_opy_ = manager.list()
        if bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᄖ") in self.bstack1llll1l1lll_opy_:
            for index, platform in enumerate(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᄗ")]):
                bstack111l11ll11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lllll1l111_opy_,
                                                            args=(self.bstack1llll11ll11_opy_, bstack1111111l1_opy_, bstack1llll11llll_opy_)))
            bstack1lllll11l11_opy_ = len(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄘ")])
        else:
            bstack111l11ll11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lllll1l111_opy_,
                                                        args=(self.bstack1llll11ll11_opy_, bstack1111111l1_opy_, bstack1llll11llll_opy_)))
            bstack1lllll11l11_opy_ = 1
        i = 0
        for t in bstack111l11ll11_opy_:
            os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᄙ")] = str(i)
            if bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄚ") in self.bstack1llll1l1lll_opy_:
                os.environ[bstack1l1111_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬᄛ")] = json.dumps(self.bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄜ")][i % bstack1lllll11l11_opy_])
            i += 1
            t.start()
        for t in bstack111l11ll11_opy_:
            t.join()
        return list(bstack1llll11llll_opy_)
    @staticmethod
    def bstack1l1l1l1ll_opy_(driver, bstack1llll1lllll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1l1111_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᄝ"), None)
        if item and getattr(item, bstack1l1111_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩᄞ"), None) and not getattr(item, bstack1l1111_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪᄟ"), False):
            logger.info(
                bstack1l1111_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣᄠ"))
            bstack1llll11l1ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1l11l1l111_opy_.bstack111ll1ll1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llll1lll1l_opy_(self):
        bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡸࡴࠦࡢࡦࠢࡨࡼࡪࡩࡵࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᄡ")
        try:
            from browserstack_sdk.bstack1llllll1l11_opy_ import bstack1llllll1l1l_opy_
            bstack1llll11l1l1_opy_ = bstack1llllll1l1l_opy_(bstack1llllll11l1_opy_=self.bstack1llll11ll11_opy_)
            if not bstack1llll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᄢ"), False):
                self.logger.error(bstack1l1111_opy_ (u"࡚ࠧࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᄣ").format(bstack1llll11l1l1_opy_.get(bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᄤ"), bstack1l1111_opy_ (u"ࠧࡖࡰ࡮ࡲࡴࡽ࡮ࠡࡧࡵࡶࡴࡸࠧᄥ"))))
                return []
            test_files = bstack1llll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠬᄦ"), [])
            count = bstack1llll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡦࡳࡺࡴࡴࠨᄧ"), 0)
            self.logger.debug(bstack1l1111_opy_ (u"ࠥࡇࡴࡲ࡬ࡦࡥࡷࡩࡩࠦࡻࡾࠢࡷࡩࡸࡺࡳࠡ࡫ࡱࠤࢀࢃࠠࡧ࡫࡯ࡩࡸࠨᄨ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᄩ").format(e))
            return []