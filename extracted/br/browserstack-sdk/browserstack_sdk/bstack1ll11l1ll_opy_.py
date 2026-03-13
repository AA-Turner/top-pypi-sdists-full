# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as a11y
from browserstack_sdk.bstack1ll1ll111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack111ll11l11_opy_, bstack1lll1lll111_opy_
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from bstack_utils.constants import bstack1lll11lll1l_opy_
from bstack_utils.bstack11ll111ll_opy_ import bstack1l11lll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1l1l1ll_opy_ import bstack1lll1ll11l1_opy_
class bstack11l11llll1_opy_:
    def __init__(self, args, logger, bstack1lll1l1111l_opy_, bstack1lll1l1llll_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll1l1111l_opy_ = bstack1lll1l1111l_opy_
        self.bstack1lll1l1llll_opy_ = bstack1lll1l1llll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1lll1l11_opy_ = []
        self.bstack1lll1l11l11_opy_ = []
        self.bstack1l111111l_opy_ = []
        self.bstack1lll1l1l11l_opy_ = self.bstack1ll111l1ll_opy_()
        self.bstack111ll11111_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll1ll1l1l_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack111lll1l11_opy_(self, bstack1lll1l111l1_opy_):
        self.parse_args()
        self.bstack1lll1l1ll1l_opy_()
        self.bstack1lll1llll1l_opy_(bstack1lll1l111l1_opy_)
        self.bstack1lll11lllll_opy_()
    @measure(event_name=EVENTS.bstack1lll1l111ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack111l1ll1l1_opy_(self):
        bstack11ll111ll_opy_ = bstack1l11lll1l1_opy_.get_instance(self.bstack1lll1l1111l_opy_, self.logger)
        if bstack11ll111ll_opy_ is None:
            self.logger.warn(bstack1111l_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡲࡩࡲࡥࡳࠢ࡬ࡷࠥࡴ࡯ࡵࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࡪ࠮ࠡࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᇪ"))
            return
        bstack1lll1l11ll1_opy_ = False
        bstack11ll111ll_opy_.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠤࡨࡲࡦࡨ࡬ࡦࡦࠥᇫ"), bstack11ll111ll_opy_.bstack11l111l1ll_opy_())
        start_time = time.time()
        if bstack11ll111ll_opy_.bstack11l111l1ll_opy_():
            test_files = self.bstack1lll11ll1ll_opy_()
            bstack1lll1l11ll1_opy_ = True
            bstack1lll1ll1lll_opy_ = bstack11ll111ll_opy_.bstack1lll1lllll1_opy_(test_files)
            if bstack1lll1ll1lll_opy_:
                self.bstack1lll1l11_opy_ = [os.path.normpath(item) for item in bstack1lll1ll1lll_opy_]
                self.__1lll1l1lll1_opy_()
                bstack11ll111ll_opy_.bstack1lll1l1l1l1_opy_(bstack1lll1l11ll1_opy_)
                self.logger.info(bstack1111l_opy_ (u"ࠥࡘࡪࡹࡴࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡻࡳࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᇬ").format(self.bstack1lll1l11_opy_))
            else:
                self.logger.info(bstack1111l_opy_ (u"ࠦࡓࡵࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࡶࠤࡼ࡫ࡲࡦࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥࡨࡹࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠯ࠤᇭ"))
        bstack11ll111ll_opy_.bstack1lll11llll1_opy_(bstack1111l_opy_ (u"ࠧࡺࡩ࡮ࡧࡗࡥࡰ࡫࡮ࡕࡱࡄࡴࡵࡲࡹࠣᇮ"), int((time.time() - start_time) * 1000)) # bstack1lll1ll11ll_opy_ to bstack1lll1lll1l1_opy_
    def __1lll1l1lll1_opy_(self):
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡶ࡬ࡢࡥࡨࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸࠦࡩ࡯ࠢࡆࡐࡎࠦࡦ࡭ࡣࡪࡷࠥࡽࡩࡵࡪࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࠠࡱࡣࡷ࡬ࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡶࡻ࡫ࡲࠡࡴࡨࡸࡺࡸ࡮ࡴࠢࡵࡩࡴࡸࡤࡦࡴࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡲࡦࡳࡥࡴ࠮ࠣࡥࡳࡪࠠࡸࡧࠣࡷ࡮ࡳࡰ࡭ࡻࠣࡹࡵࡪࡡࡵࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡮ࡥࠡࡅࡏࡍࠥࡧࡲࡨࡵࠣࡸࡴࠦࡵࡴࡧࠣࡸ࡭ࡵࡳࡦࠢࡩ࡭ࡱ࡫ࡳ࠯ࠢࡘࡷࡪࡸࠧࡴࠢࡩ࡭ࡱࡺࡥࡳ࡫ࡱ࡫ࠥ࡬࡬ࡢࡩࡶࠤ࠭࠳࡭࠭ࠢ࠰࡯࠮ࠦࡲࡦ࡯ࡤ࡭ࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡰࡷࡥࡨࡺࠠࡢࡰࡧࠤࡼ࡯࡬࡭ࠢࡥࡩࠥࡧࡰࡱ࡮࡬ࡩࡩࠦ࡮ࡢࡶࡸࡶࡦࡲ࡬ࡺࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡽࡹ࡫ࡳࡵࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᇯ")
        try:
            if not self.bstack1lll1l11_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡏࡱࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡲࡤࡸ࡭ࠦࡴࡰࠢࡶࡩࡹࠨᇰ"))
                return
            bstack1lll1l1ll11_opy_ = []
            for flag in self.bstack1lll1l11l11_opy_:
                if flag.startswith(bstack1111l_opy_ (u"ࠨ࠯ࠪᇱ")):
                    bstack1lll1l1ll11_opy_.append(flag)
                    continue
                bstack1lll1llll11_opy_ = False
                if bstack1111l_opy_ (u"ࠩ࠽࠾ࠬᇲ") in flag:
                    bstack1llll111111_opy_ = flag.split(bstack1111l_opy_ (u"ࠪ࠾࠿࠭ᇳ"), 1)[0]
                    if os.path.exists(bstack1llll111111_opy_):
                        bstack1lll1llll11_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1111l_opy_ (u"ࠫ࠳ࡶࡹࠨᇴ"))):
                        bstack1lll1llll11_opy_ = True
                if not bstack1lll1llll11_opy_:
                    bstack1lll1l1ll11_opy_.append(flag)
            bstack1lll1l1ll11_opy_.extend(self.bstack1lll1l11_opy_)
            self.bstack1lll1l11l11_opy_ = bstack1lll1l1ll11_opy_
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸࡪࡪࠠࡴࡧ࡯ࡩࡨࡺ࡯ࡳࡵ࠽ࠤࢀࢃࠢᇵ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll1l11lll_opy_():
        return bstack1lll1ll11l1_opy_(bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᇶ"))
    def bstack1lll1l11l1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111ll11111_opy_ = -1
        if self.bstack1lll1l1llll_opy_ and bstack1111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᇷ") in self.bstack1lll1l1111l_opy_:
            self.bstack111ll11111_opy_ = int(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᇸ")])
        try:
            bstack1lll1ll1ll1_opy_ = [bstack1111l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫᇹ"), bstack1111l_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ᇺ"), bstack1111l_opy_ (u"ࠫ࠲ࡶࠧᇻ")]
            if self.bstack111ll11111_opy_ >= 0:
                bstack1lll1ll1ll1_opy_.extend([bstack1111l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ᇼ"), bstack1111l_opy_ (u"࠭࠭࡯ࠩᇽ")])
            for arg in bstack1lll1ll1ll1_opy_:
                self.bstack1lll1l11l1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll1l1ll1l_opy_(self):
        bstack1lll1l11l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll1l11l11_opy_ = bstack1lll1l11l11_opy_
        return self.bstack1lll1l11l11_opy_
    def bstack1l1l1l11ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll1l11lll_opy_():
                self.logger.warning(bstack1lll1lll111_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1111l_opy_ (u"ࠢࠦࡵ࠽ࠤࠪࡹࠢᇾ"), bstack111ll11l11_opy_, str(e))
    def bstack1lll1llll1l_opy_(self, bstack1lll1l111l1_opy_):
        global_config = Config.get_instance()
        if bstack1lll1l111l1_opy_:
            self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᇿ"))
            self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧሀ"))
        if global_config.should_skip_session_status():
            self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩሁ"))
            self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"࡙ࠫࡸࡵࡦࠩሂ"))
        self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠬ࠳ࡰࠨሃ"))
        self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫሄ"))
        self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩህ"))
        self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨሆ"))
        if self.bstack111ll11111_opy_ > 1:
            self.bstack1lll1l11l11_opy_.append(bstack1111l_opy_ (u"ࠩ࠰ࡲࠬሇ"))
            self.bstack1lll1l11l11_opy_.append(str(self.bstack111ll11111_opy_))
    def bstack1lll11lllll_opy_(self):
        if bstack11ll11l11l_opy_.bstack11lllll111_opy_(self.bstack1lll1l1111l_opy_):
             self.bstack1lll1l11l11_opy_ += [
                bstack1lll11lll1l_opy_.get(bstack1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࠩለ")), str(bstack11ll11l11l_opy_.bstack1l11l11l1l_opy_(self.bstack1lll1l1111l_opy_)),
                bstack1lll11lll1l_opy_.get(bstack1111l_opy_ (u"ࠫࡩ࡫࡬ࡢࡻࠪሉ")), str(bstack1lll11lll1l_opy_.get(bstack1111l_opy_ (u"ࠬࡸࡥࡳࡷࡱ࠱ࡩ࡫࡬ࡢࡻࠪሊ")))
            ]
    def bstack1lll1ll1l11_opy_(self):
        bstack1l111111l_opy_ = []
        for spec in self.bstack1lll1l11_opy_:
            bstack1l1l1l1l1_opy_ = [spec]
            bstack1l1l1l1l1_opy_ += self.bstack1lll1l11l11_opy_
            bstack1l111111l_opy_.append(bstack1l1l1l1l1_opy_)
        self.bstack1l111111l_opy_ = bstack1l111111l_opy_
        return bstack1l111111l_opy_
    def bstack1ll111l1ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll1l1l11l_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll1l1l11l_opy_ = False
        return self.bstack1lll1l1l11l_opy_
    @measure(event_name=EVENTS.bstack1lll1l1l111_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l1ll1l1l1_opy_(self):
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡋࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡴࡦࡵࡷࡷࠥࡽࡩࡵࡪࡲࡹࡹࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡵࡪࡨࡱࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺ࠺ࠡࡖ࡫ࡩࠥࡺ࡯ࡵࡣ࡯ࠤࡳࡻ࡭ࡣࡧࡵࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢላ")
        try:
            from browserstack_sdk.bstack1llll11l111_opy_ import bstack1llll11l1ll_opy_
            bstack1lll1lll1ll_opy_ = bstack1llll11l1ll_opy_(bstack1llll1111l1_opy_=self.bstack1lll1l11l11_opy_)
            if not bstack1lll1lll1ll_opy_.get(bstack1111l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨሌ"), False):
                self.logger.error(bstack1111l_opy_ (u"ࠣࡖࡨࡷࡹࠦࡣࡰࡷࡱࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨል").format(bstack1lll1lll1ll_opy_.get(bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨሎ"), bstack1111l_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪሏ"))))
                return 0
            count = bstack1lll1lll1ll_opy_.get(bstack1111l_opy_ (u"ࠫࡨࡵࡵ࡯ࡶࠪሐ"), 0)
            self.logger.info(bstack1111l_opy_ (u"࡚ࠧ࡯ࡵࡣ࡯ࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࡀࠠࡼࡿࠥሑ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥሒ").format(e))
            return 0
    def bstack11ll1111_opy_(self, bstack1lll1l11111_opy_, bstack111lll1l11_opy_):
        bstack111lll1l11_opy_[bstack1111l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧሓ")] = self.bstack1lll1l1111l_opy_
        multiprocessing.set_start_method(bstack1111l_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧሔ"))
        bstack1ll11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll11lll11_opy_ = manager.list()
        if bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬሕ") in self.bstack1lll1l1111l_opy_:
            for index, platform in enumerate(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ሖ")]):
                bstack1ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll1l11111_opy_,
                                                            args=(self.bstack1lll1l11l11_opy_, bstack111lll1l11_opy_, bstack1lll11lll11_opy_)))
            bstack1lll1lll11l_opy_ = len(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧሗ")])
        else:
            bstack1ll11l11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll1l11111_opy_,
                                                        args=(self.bstack1lll1l11l11_opy_, bstack111lll1l11_opy_, bstack1lll11lll11_opy_)))
            bstack1lll1lll11l_opy_ = 1
        i = 0
        for t in bstack1ll11l11_opy_:
            os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬመ")] = str(i)
            if bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩሙ") in self.bstack1lll1l1111l_opy_:
                os.environ[bstack1111l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨሚ")] = json.dumps(self.bstack1lll1l1111l_opy_[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫማ")][i % bstack1lll1lll11l_opy_])
            i += 1
            t.start()
        for t in bstack1ll11l11_opy_:
            t.join()
        return list(bstack1lll11lll11_opy_)
    @staticmethod
    def bstack11l11l111_opy_(driver, bstack1lll1ll1111_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ሜ"), None)
        if item and getattr(item, bstack1111l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬም"), None) and not getattr(item, bstack1111l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ሞ"), False):
            logger.info(
                bstack1111l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦሟ"))
            bstack1lll1ll111l_opy_ = item.cls.__name__ if not item.cls is None else None
            a11y.bstack1l1l1ll11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll11ll1ll_opy_(self):
        bstack1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡴࡰࠢࡥࡩࠥ࡫ࡸࡦࡥࡸࡸࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧሠ")
        try:
            from browserstack_sdk.bstack1llll11l111_opy_ import bstack1llll11l1ll_opy_
            bstack1lll1llllll_opy_ = bstack1llll11l1ll_opy_(bstack1llll1111l1_opy_=self.bstack1lll1l11l11_opy_)
            if not bstack1lll1llllll_opy_.get(bstack1111l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨሡ"), False):
                self.logger.error(bstack1111l_opy_ (u"ࠣࡖࡨࡷࡹࠦࡦࡪ࡮ࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧሢ").format(bstack1lll1llllll_opy_.get(bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨሣ"), bstack1111l_opy_ (u"࡙ࠪࡳࡱ࡮ࡰࡹࡱࠤࡪࡸࡲࡰࡴࠪሤ"))))
                return []
            test_files = bstack1lll1llllll_opy_.get(bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠨሥ"), [])
            count = bstack1lll1llllll_opy_.get(bstack1111l_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫሦ"), 0)
            self.logger.debug(bstack1111l_opy_ (u"ࠨࡃࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡾࢁࠥࡺࡥࡴࡶࡶࠤ࡮ࡴࠠࡼࡿࠣࡪ࡮ࡲࡥࡴࠤሧ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠾ࠥࢁࡽࠣረ").format(e))
            return []