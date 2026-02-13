# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1lllll111l_opy_
from browserstack_sdk.bstack1l11l11l1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11lllll11_opy_, bstack1llll111l1l_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.constants import bstack1lll1ll1l1l_opy_
from bstack_utils.bstack1l1llll1l_opy_ import bstack1l1lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll1111l1_opy_ import bstack1llll11l1ll_opy_
class bstack1ll11l1l11_opy_:
    def __init__(self, args, logger, bstack1llll111111_opy_, bstack1llll11ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll111111_opy_ = bstack1llll111111_opy_
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1111l1ll1_opy_ = []
        self.bstack1lll1ll111l_opy_ = []
        self.bstack1llll111_opy_ = []
        self.bstack1lll1l1lll1_opy_ = self.bstack11l11l111_opy_()
        self.bstack1lll111l1l_opy_ = -1
    @measure(event_name=EVENTS.bstack1llll11l111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11ll1lll1_opy_(self, bstack1lll1ll11ll_opy_):
        self.parse_args()
        self.bstack1lll1lll1l1_opy_()
        self.bstack1llll1111ll_opy_(bstack1lll1ll11ll_opy_)
        self.bstack1llll11111l_opy_()
    @measure(event_name=EVENTS.bstack1lll1l1ll1l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack11111l1ll_opy_(self):
        bstack1l1llll1l_opy_ = bstack1l1lll11l_opy_.bstack111l1lll_opy_(self.bstack1llll111111_opy_, self.logger)
        if bstack1l1llll1l_opy_ is None:
            self.logger.warn(bstack11l11_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࠥ࡯ࡳࠡࡰࡲࡸࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦ࠱ࠤࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠴ࠢᄾ"))
            return
        bstack1lll1lll1ll_opy_ = False
        bstack1l1llll1l_opy_.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠧ࡫࡮ࡢࡤ࡯ࡩࡩࠨᄿ"), bstack1l1llll1l_opy_.bstack1l11lllll_opy_())
        start_time = time.time()
        if bstack1l1llll1l_opy_.bstack1l11lllll_opy_():
            test_files = self.bstack1lll1ll1111_opy_()
            bstack1lll1lll1ll_opy_ = True
            bstack1llll111l11_opy_ = bstack1l1llll1l_opy_.bstack1lll1l1ll11_opy_(test_files)
            if bstack1llll111l11_opy_:
                self.bstack1111l1ll1_opy_ = [os.path.normpath(item) for item in bstack1llll111l11_opy_]
                self.__1llll11llll_opy_()
                bstack1l1llll1l_opy_.bstack1lll1lll11l_opy_(bstack1lll1lll1ll_opy_)
                self.logger.info(bstack11l11_opy_ (u"ࠨࡔࡦࡵࡷࡷࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᅀ").format(self.bstack1111l1ll1_opy_))
            else:
                self.logger.info(bstack11l11_opy_ (u"ࠢࡏࡱࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡸࡧࡵࡩࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡤࡼࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᅁ"))
        bstack1l1llll1l_opy_.bstack1llll111lll_opy_(bstack11l11_opy_ (u"ࠣࡶ࡬ࡱࡪ࡚ࡡ࡬ࡧࡱࡘࡴࡇࡰࡱ࡮ࡼࠦᅂ"), int((time.time() - start_time) * 1000)) # bstack1lll1ll1ll1_opy_ to bstack1lll1ll1lll_opy_
    def __1llll11llll_opy_(self):
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡲ࡯ࡥࡨ࡫ࠠࡵࡧࡶࡸࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴࠢ࡬ࡲࠥࡉࡌࡊࠢࡩࡰࡦ࡭ࡳࠡࡹ࡬ࡸ࡭ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡸ࡫ࡲࡷࡧࡵࠤࡷ࡫ࡴࡶࡴࡱࡷࠥࡸࡥࡰࡴࡧࡩࡷ࡫ࡤࠡࡨ࡬ࡰࡪࠦ࡮ࡢ࡯ࡨࡷ࠱ࠦࡡ࡯ࡦࠣࡻࡪࠦࡳࡪ࡯ࡳࡰࡾࠦࡵࡱࡦࡤࡸࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡪࡨࠤࡈࡒࡉࠡࡣࡵ࡫ࡸࠦࡴࡰࠢࡸࡷࡪࠦࡴࡩࡱࡶࡩࠥ࡬ࡩ࡭ࡧࡶ࠲࡛ࠥࡳࡦࡴࠪࡷࠥ࡬ࡩ࡭ࡶࡨࡶ࡮ࡴࡧࠡࡨ࡯ࡥ࡬ࡹࠠࠩ࠯ࡰ࠰ࠥ࠳࡫ࠪࠢࡵࡩࡲࡧࡩ࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡭ࡳࡺࡡࡤࡶࠣࡥࡳࡪࠠࡸ࡫࡯ࡰࠥࡨࡥࠡࡣࡳࡴࡱ࡯ࡥࡥࠢࡱࡥࡹࡻࡲࡢ࡮࡯ࡽࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᅃ")
        try:
            if not self.bstack1111l1ll1_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡒࡴࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶࡨࡨࠥ࡬ࡩ࡭ࡧࡶࠤࡵࡧࡴࡩࠢࡷࡳࠥࡹࡥࡵࠤᅄ"))
                return
            bstack1lll1ll1l11_opy_ = []
            for flag in self.bstack1lll1ll111l_opy_:
                if flag.startswith(bstack11l11_opy_ (u"ࠫ࠲࠭ᅅ")):
                    bstack1lll1ll1l11_opy_.append(flag)
                    continue
                bstack1lll1llllll_opy_ = False
                if bstack11l11_opy_ (u"ࠬࡀ࠺ࠨᅆ") in flag:
                    bstack1llll1l1111_opy_ = flag.split(bstack11l11_opy_ (u"࠭࠺࠻ࠩᅇ"), 1)[0]
                    if os.path.exists(bstack1llll1l1111_opy_):
                        bstack1lll1llllll_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11l11_opy_ (u"ࠧ࠯ࡲࡼࠫᅈ"))):
                        bstack1lll1llllll_opy_ = True
                if not bstack1lll1llllll_opy_:
                    bstack1lll1ll1l11_opy_.append(flag)
            bstack1lll1ll1l11_opy_.extend(self.bstack1111l1ll1_opy_)
            self.bstack1lll1ll111l_opy_ = bstack1lll1ll1l11_opy_
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡷࡪࡲࡥࡤࡶࡲࡶࡸࡀࠠࡼࡿࠥᅉ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll1llll1l_opy_():
        return bstack1llll11l1ll_opy_(bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᅊ"))
    def bstack1lll1ll11l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll111l1l_opy_ = -1
        if self.bstack1llll11ll1l_opy_ and bstack11l11_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᅋ") in self.bstack1llll111111_opy_:
            self.bstack1lll111l1l_opy_ = int(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫᅌ")])
        try:
            bstack1lll1l1llll_opy_ = [bstack11l11_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧᅍ"), bstack11l11_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩᅎ"), bstack11l11_opy_ (u"ࠧ࠮ࡲࠪᅏ")]
            if self.bstack1lll111l1l_opy_ >= 0:
                bstack1lll1l1llll_opy_.extend([bstack11l11_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩᅐ"), bstack11l11_opy_ (u"ࠩ࠰ࡲࠬᅑ")])
            for arg in bstack1lll1l1llll_opy_:
                self.bstack1lll1ll11l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1lll1lll1l1_opy_(self):
        bstack1lll1ll111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll1ll111l_opy_ = bstack1lll1ll111l_opy_
        return self.bstack1lll1ll111l_opy_
    def bstack11ll11l1ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll1llll1l_opy_():
                self.logger.warning(bstack1llll111l1l_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11l11_opy_ (u"ࠥࠩࡸࡀࠠࠦࡵࠥᅒ"), bstack11lllll11_opy_, str(e))
    def bstack1llll1111ll_opy_(self, bstack1lll1ll11ll_opy_):
        bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
        if bstack1lll1ll11ll_opy_:
            self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᅓ"))
            self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"࡚ࠬࡲࡶࡧࠪᅔ"))
        if bstack11l1l1111_opy_.bstack1llll11l11l_opy_():
            self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᅕ"))
            self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠧࡕࡴࡸࡩࠬᅖ"))
        self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠨ࠯ࡳࠫᅗ"))
        self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧᅘ"))
        self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬᅙ"))
        self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᅚ"))
        if self.bstack1lll111l1l_opy_ > 1:
            self.bstack1lll1ll111l_opy_.append(bstack11l11_opy_ (u"ࠬ࠳࡮ࠨᅛ"))
            self.bstack1lll1ll111l_opy_.append(str(self.bstack1lll111l1l_opy_))
    def bstack1llll11111l_opy_(self):
        if bstack1l11l1l1ll_opy_.bstack11l11lll11_opy_(self.bstack1llll111111_opy_):
             self.bstack1lll1ll111l_opy_ += [
                bstack1lll1ll1l1l_opy_.get(bstack11l11_opy_ (u"࠭ࡲࡦࡴࡸࡲࠬᅜ")), str(bstack1l11l1l1ll_opy_.bstack11l1l1lll1_opy_(self.bstack1llll111111_opy_)),
                bstack1lll1ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠧࡥࡧ࡯ࡥࡾ࠭ᅝ")), str(bstack1lll1ll1l1l_opy_.get(bstack11l11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࠭ࡥࡧ࡯ࡥࡾ࠭ᅞ")))
            ]
    def bstack1lll1lll111_opy_(self):
        bstack1llll111_opy_ = []
        for spec in self.bstack1111l1ll1_opy_:
            bstack1l11l1l1_opy_ = [spec]
            bstack1l11l1l1_opy_ += self.bstack1lll1ll111l_opy_
            bstack1llll111_opy_.append(bstack1l11l1l1_opy_)
        self.bstack1llll111_opy_ = bstack1llll111_opy_
        return bstack1llll111_opy_
    def bstack11l11l111_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll1l1lll1_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll1l1lll1_opy_ = False
        return self.bstack1lll1l1lll1_opy_
    @measure(event_name=EVENTS.bstack1llll1l111l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack111l1lll1l_opy_(self):
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡇࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡹ࡬ࡸ࡭ࡵࡵࡵࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡸ࡭࡫࡭ࠡࡷࡶ࡭ࡳ࡭ࠠࡱࡻࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡩ࡯ࡶ࠽ࠤ࡙࡮ࡥࠡࡶࡲࡸࡦࡲࠠ࡯ࡷࡰࡦࡪࡸࠠࡰࡨࠣࡸࡪࡹࡴࡴࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᅟ")
        try:
            from browserstack_sdk.bstack1llll1ll111_opy_ import bstack1llll1ll1l1_opy_
            bstack1llll11l1l1_opy_ = bstack1llll1ll1l1_opy_(bstack1llll1llll1_opy_=self.bstack1lll1ll111l_opy_)
            if not bstack1llll11l1l1_opy_.get(bstack11l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᅠ"), False):
                self.logger.error(bstack11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡦࡳࡺࡴࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᅡ").format(bstack1llll11l1l1_opy_.get(bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᅢ"), bstack11l11_opy_ (u"࠭ࡕ࡯࡭ࡱࡳࡼࡴࠠࡦࡴࡵࡳࡷ࠭ᅣ"))))
                return 0
            count = bstack1llll11l1l1_opy_.get(bstack11l11_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᅤ"), 0)
            self.logger.info(bstack11l11_opy_ (u"ࠣࡖࡲࡸࡦࡲࠠࡵࡧࡶࡸࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥ࠼ࠣࡿࢂࠨᅥ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨᅦ").format(e))
            return 0
    def bstack1l1111111_opy_(self, bstack1llll1l11l1_opy_, bstack11ll1lll1_opy_):
        bstack11ll1lll1_opy_[bstack11l11_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪᅧ")] = self.bstack1llll111111_opy_
        multiprocessing.set_start_method(bstack11l11_opy_ (u"ࠫࡸࡶࡡࡸࡰࠪᅨ"))
        bstack11l1ll1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1lllll1_opy_ = manager.list()
        if bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᅩ") in self.bstack1llll111111_opy_:
            for index, platform in enumerate(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅪ")]):
                bstack11l1ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll1l11l1_opy_,
                                                            args=(self.bstack1lll1ll111l_opy_, bstack11ll1lll1_opy_, bstack1lll1lllll1_opy_)))
            bstack1lll1llll11_opy_ = len(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅫ")])
        else:
            bstack11l1ll1111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll1l11l1_opy_,
                                                        args=(self.bstack1lll1ll111l_opy_, bstack11ll1lll1_opy_, bstack1lll1lllll1_opy_)))
            bstack1lll1llll11_opy_ = 1
        i = 0
        for t in bstack11l1ll1111_opy_:
            os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᅬ")] = str(i)
            if bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅭ") in self.bstack1llll111111_opy_:
                os.environ[bstack11l11_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫᅮ")] = json.dumps(self.bstack1llll111111_opy_[bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅯ")][i % bstack1lll1llll11_opy_])
            i += 1
            t.start()
        for t in bstack11l1ll1111_opy_:
            t.join()
        return list(bstack1lll1lllll1_opy_)
    @staticmethod
    def bstack1l1l111l_opy_(driver, bstack1llll11ll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩᅰ"), None)
        if item and getattr(item, bstack11l11_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡧࡦࡹࡥࠨᅱ"), None) and not getattr(item, bstack11l11_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡳࡵࡱࡳࡣࡩࡵ࡮ࡦࠩᅲ"), False):
            logger.info(
                bstack11l11_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠢᅳ"))
            bstack1llll111ll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lllll111l_opy_.bstack1ll1l111l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll1ll1111_opy_(self):
        bstack11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡷࡳࠥࡨࡥࠡࡧࡻࡩࡨࡻࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᅴ")
        try:
            from browserstack_sdk.bstack1llll1ll111_opy_ import bstack1llll1ll1l1_opy_
            bstack1llll11lll1_opy_ = bstack1llll1ll1l1_opy_(bstack1llll1llll1_opy_=self.bstack1lll1ll111l_opy_)
            if not bstack1llll11lll1_opy_.get(bstack11l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᅵ"), False):
                self.logger.error(bstack11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᅶ").format(bstack1llll11lll1_opy_.get(bstack11l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᅷ"), bstack11l11_opy_ (u"࠭ࡕ࡯࡭ࡱࡳࡼࡴࠠࡦࡴࡵࡳࡷ࠭ᅸ"))))
                return []
            test_files = bstack1llll11lll1_opy_.get(bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠫᅹ"), [])
            count = bstack1llll11lll1_opy_.get(bstack11l11_opy_ (u"ࠨࡥࡲࡹࡳࡺࠧᅺ"), 0)
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶࡨࡨࠥࢁࡽࠡࡶࡨࡷࡹࡹࠠࡪࡰࠣࡿࢂࠦࡦࡪ࡮ࡨࡷࠧᅻ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࡵࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᅼ").format(e))
            return []