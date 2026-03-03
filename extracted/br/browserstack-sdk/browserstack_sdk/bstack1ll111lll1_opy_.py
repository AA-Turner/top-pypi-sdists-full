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
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack11l11l11ll_opy_
from browserstack_sdk.bstack1l1l11111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1ll1ll1_opy_, bstack1llll111l11_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from bstack_utils.constants import bstack1lll1llll11_opy_
from bstack_utils.bstack1l111llll_opy_ import bstack1llll1lll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1llll1111ll_opy_ import bstack1llll11ll11_opy_
class bstack1l1l111l11_opy_:
    def __init__(self, args, logger, bstack1llll111l1l_opy_, bstack1llll11ll1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1llll111l1l_opy_ = bstack1llll111l1l_opy_
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l111l1lll_opy_ = []
        self.bstack1llll11lll1_opy_ = []
        self.bstack1l111lll_opy_ = []
        self.bstack1llll1l11ll_opy_ = self.bstack1ll1l11l11_opy_()
        self.bstack1lll11l11_opy_ = -1
    @measure(event_name=EVENTS.bstack1llll111ll1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1ll111l1l1_opy_(self, bstack1lll1lll11l_opy_):
        self.parse_args()
        self.bstack1llll1l11l1_opy_()
        self.bstack1llll11111l_opy_(bstack1lll1lll11l_opy_)
        self.bstack1llll1ll1ll_opy_()
    @measure(event_name=EVENTS.bstack1llll1l1lll_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l11lll1l1_opy_(self):
        bstack1l111llll_opy_ = bstack1llll1lll1_opy_.get_instance(self.bstack1llll111l1l_opy_, self.logger)
        if bstack1l111llll_opy_ is None:
            self.logger.warn(bstack11ll111_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࠣ࡭ࡸࠦ࡮ࡰࡶࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤ࠯ࠢࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠲ࠧᅃ"))
            return
        bstack1llll1l1l1l_opy_ = False
        bstack1l111llll_opy_.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠥࡩࡳࡧࡢ࡭ࡧࡧࠦᅄ"), bstack1l111llll_opy_.bstack11l1ll1l_opy_())
        start_time = time.time()
        if bstack1l111llll_opy_.bstack11l1ll1l_opy_():
            test_files = self.bstack1llll1ll1l1_opy_()
            bstack1llll1l1l1l_opy_ = True
            bstack1llll11llll_opy_ = bstack1l111llll_opy_.bstack1llll1lll11_opy_(test_files)
            if bstack1llll11llll_opy_:
                self.bstack1l111l1lll_opy_ = [os.path.normpath(item) for item in bstack1llll11llll_opy_]
                self.__1llll111lll_opy_()
                bstack1l111llll_opy_.bstack1llll1ll11l_opy_(bstack1llll1l1l1l_opy_)
                self.logger.info(bstack11ll111_opy_ (u"࡙ࠦ࡫ࡳࡵࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡵࡴ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᅅ").format(self.bstack1l111l1lll_opy_))
            else:
                self.logger.info(bstack11ll111_opy_ (u"ࠧࡔ࡯ࠡࡶࡨࡷࡹࠦࡦࡪ࡮ࡨࡷࠥࡽࡥࡳࡧࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡢࡺࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠰ࠥᅆ"))
        bstack1l111llll_opy_.bstack1llll111111_opy_(bstack11ll111_opy_ (u"ࠨࡴࡪ࡯ࡨࡘࡦࡱࡥ࡯ࡖࡲࡅࡵࡶ࡬ࡺࠤᅇ"), int((time.time() - start_time) * 1000)) # bstack1llll11l1ll_opy_ to bstack1llll1ll111_opy_
    def __1llll111lll_opy_(self):
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡰ࡭ࡣࡦࡩࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹࠠࡪࡰࠣࡇࡑࡏࠠࡧ࡮ࡤ࡫ࡸࠦࡷࡪࡶ࡫ࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࠡࡲࡤࡸ࡭ࡹ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡶࡩࡷࡼࡥࡳࠢࡵࡩࡹࡻࡲ࡯ࡵࠣࡶࡪࡵࡲࡥࡧࡵࡩࡩࠦࡦࡪ࡮ࡨࠤࡳࡧ࡭ࡦࡵ࠯ࠤࡦࡴࡤࠡࡹࡨࠤࡸ࡯࡭ࡱ࡮ࡼࠤࡺࡶࡤࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡺࡨࡦࠢࡆࡐࡎࠦࡡࡳࡩࡶࠤࡹࡵࠠࡶࡵࡨࠤࡹ࡮࡯ࡴࡧࠣࡪ࡮ࡲࡥࡴ࠰࡙ࠣࡸ࡫ࡲࠨࡵࠣࡪ࡮ࡲࡴࡦࡴ࡬ࡲ࡬ࠦࡦ࡭ࡣࡪࡷࠥ࠮࠭࡮࠮ࠣ࠱ࡰ࠯ࠠࡳࡧࡰࡥ࡮ࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡫ࡱࡸࡦࡩࡴࠡࡣࡱࡨࠥࡽࡩ࡭࡮ࠣࡦࡪࠦࡡࡱࡲ࡯࡭ࡪࡪࠠ࡯ࡣࡷࡹࡷࡧ࡬࡭ࡻࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡾࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᅈ")
        try:
            if not self.bstack1l111l1lll_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡐࡲࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡳࡥࡹ࡮ࠠࡵࡱࠣࡷࡪࡺࠢᅉ"))
                return
            bstack1lll1lll1ll_opy_ = []
            for flag in self.bstack1llll11lll1_opy_:
                if flag.startswith(bstack11ll111_opy_ (u"ࠩ࠰ࠫᅊ")):
                    bstack1lll1lll1ll_opy_.append(flag)
                    continue
                bstack1llll1l111l_opy_ = False
                if bstack11ll111_opy_ (u"ࠪ࠾࠿࠭ᅋ") in flag:
                    bstack1llll11l1l1_opy_ = flag.split(bstack11ll111_opy_ (u"ࠫ࠿ࡀࠧᅌ"), 1)[0]
                    if os.path.exists(bstack1llll11l1l1_opy_):
                        bstack1llll1l111l_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack11ll111_opy_ (u"ࠬ࠴ࡰࡺࠩᅍ"))):
                        bstack1llll1l111l_opy_ = True
                if not bstack1llll1l111l_opy_:
                    bstack1lll1lll1ll_opy_.append(flag)
            bstack1lll1lll1ll_opy_.extend(self.bstack1l111l1lll_opy_)
            self.bstack1llll11lll1_opy_ = bstack1lll1lll1ll_opy_
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡫ࡤࠡࡵࡨࡰࡪࡩࡴࡰࡴࡶ࠾ࠥࢁࡽࠣᅎ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1llll1l1111_opy_():
        return bstack1llll11ll11_opy_(bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᅏ"))
    def bstack1llll11l11l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1lll11l11_opy_ = -1
        if self.bstack1llll11ll1l_opy_ and bstack11ll111_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᅐ") in self.bstack1llll111l1l_opy_:
            self.bstack1lll11l11_opy_ = int(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᅑ")])
        try:
            bstack1lll1llllll_opy_ = [bstack11ll111_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬᅒ"), bstack11ll111_opy_ (u"ࠫ࠲࠳ࡰ࡭ࡷࡪ࡭ࡳࡹࠧᅓ"), bstack11ll111_opy_ (u"ࠬ࠳ࡰࠨᅔ")]
            if self.bstack1lll11l11_opy_ >= 0:
                bstack1lll1llllll_opy_.extend([bstack11ll111_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧᅕ"), bstack11ll111_opy_ (u"ࠧ࠮ࡰࠪᅖ")])
            for arg in bstack1lll1llllll_opy_:
                self.bstack1llll11l11l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll1l11l1_opy_(self):
        bstack1llll11lll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1llll11lll1_opy_ = bstack1llll11lll1_opy_
        return self.bstack1llll11lll1_opy_
    def bstack11111lll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1llll1l1111_opy_():
                self.logger.warning(bstack1llll111l11_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࠧࡶ࠾ࠥࠫࡳࠣᅗ"), bstack11l1ll1ll1_opy_, str(e))
    def bstack1llll11111l_opy_(self, bstack1lll1lll11l_opy_):
        global_config = Config.get_instance()
        if bstack1lll1lll11l_opy_:
            self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᅘ"))
            self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠪࡘࡷࡻࡥࠨᅙ"))
        if global_config.should_skip_session_status():
            self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᅚ"))
            self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"࡚ࠬࡲࡶࡧࠪᅛ"))
        self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"࠭࠭ࡱࠩᅜ"))
        self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠬᅝ"))
        self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪᅞ"))
        self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᅟ"))
        if self.bstack1lll11l11_opy_ > 1:
            self.bstack1llll11lll1_opy_.append(bstack11ll111_opy_ (u"ࠪ࠱ࡳ࠭ᅠ"))
            self.bstack1llll11lll1_opy_.append(str(self.bstack1lll11l11_opy_))
    def bstack1llll1ll1ll_opy_(self):
        if bstack1111lll11_opy_.bstack111ll11111_opy_(self.bstack1llll111l1l_opy_):
             self.bstack1llll11lll1_opy_ += [
                bstack1lll1llll11_opy_.get(bstack11ll111_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࠪᅡ")), str(bstack1111lll11_opy_.bstack11llllll_opy_(self.bstack1llll111l1l_opy_)),
                bstack1lll1llll11_opy_.get(bstack11ll111_opy_ (u"ࠬࡪࡥ࡭ࡣࡼࠫᅢ")), str(bstack1lll1llll11_opy_.get(bstack11ll111_opy_ (u"࠭ࡲࡦࡴࡸࡲ࠲ࡪࡥ࡭ࡣࡼࠫᅣ")))
            ]
    def bstack1llll1l1ll1_opy_(self):
        bstack1l111lll_opy_ = []
        for spec in self.bstack1l111l1lll_opy_:
            bstack11lll1l1ll_opy_ = [spec]
            bstack11lll1l1ll_opy_ += self.bstack1llll11lll1_opy_
            bstack1l111lll_opy_.append(bstack11lll1l1ll_opy_)
        self.bstack1l111lll_opy_ = bstack1l111lll_opy_
        return bstack1l111lll_opy_
    def bstack1ll1l11l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1llll1l11ll_opy_ = True
            return True
        except Exception as e:
            self.bstack1llll1l11ll_opy_ = False
        return self.bstack1llll1l11ll_opy_
    @measure(event_name=EVENTS.bstack1lll1lll1l1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l11lll1l_opy_(self):
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡌ࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡵࡧࡶࡸࡸࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡶ࡫ࡩࡲࠦࡵࡴ࡫ࡱ࡫ࠥࡶࡹࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮ࡴࡴ࠻ࠢࡗ࡬ࡪࠦࡴࡰࡶࡤࡰࠥࡴࡵ࡮ࡤࡨࡶࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᅤ")
        try:
            from browserstack_sdk.bstack1lllll11l11_opy_ import bstack1lllll1l11l_opy_
            bstack1lll1llll1l_opy_ = bstack1lllll1l11l_opy_(bstack1lllll111l1_opy_=self.bstack1llll11lll1_opy_)
            if not bstack1lll1llll1l_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᅥ"), False):
                self.logger.error(bstack11ll111_opy_ (u"ࠤࡗࡩࡸࡺࠠࡤࡱࡸࡲࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢᅦ").format(bstack1lll1llll1l_opy_.get(bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᅧ"), bstack11ll111_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫᅨ"))))
                return 0
            count = bstack1lll1llll1l_opy_.get(bstack11ll111_opy_ (u"ࠬࡩ࡯ࡶࡰࡷࠫᅩ"), 0)
            self.logger.info(bstack11ll111_opy_ (u"ࠨࡔࡰࡶࡤࡰࠥࡺࡥࡴࡶࡶࠤࡨࡵ࡬࡭ࡧࡦࡸࡪࡪ࠺ࠡࡽࢀࠦᅪ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦᅫ").format(e))
            return 0
    def bstack1111llll_opy_(self, bstack1llll1lll1l_opy_, bstack1ll111l1l1_opy_):
        bstack1ll111l1l1_opy_[bstack11ll111_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨᅬ")] = self.bstack1llll111l1l_opy_
        multiprocessing.set_start_method(bstack11ll111_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᅭ"))
        bstack11ll111l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll1llll1_opy_ = manager.list()
        if bstack11ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᅮ") in self.bstack1llll111l1l_opy_:
            for index, platform in enumerate(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅯ")]):
                bstack11ll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1llll1lll1l_opy_,
                                                            args=(self.bstack1llll11lll1_opy_, bstack1ll111l1l1_opy_, bstack1llll1llll1_opy_)))
            bstack1llll1111l1_opy_ = len(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᅰ")])
        else:
            bstack11ll111l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1llll1lll1l_opy_,
                                                        args=(self.bstack1llll11lll1_opy_, bstack1ll111l1l1_opy_, bstack1llll1llll1_opy_)))
            bstack1llll1111l1_opy_ = 1
        i = 0
        for t in bstack11ll111l_opy_:
            os.environ[bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᅱ")] = str(i)
            if bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᅲ") in self.bstack1llll111l1l_opy_:
                os.environ[bstack11ll111_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩᅳ")] = json.dumps(self.bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅴ")][i % bstack1llll1111l1_opy_])
            i += 1
            t.start()
        for t in bstack11ll111l_opy_:
            t.join()
        return list(bstack1llll1llll1_opy_)
    @staticmethod
    def bstack1ll11llll_opy_(driver, bstack1lll1lllll1_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᅵ"), None)
        if item and getattr(item, bstack11ll111_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪ࠭ᅶ"), None) and not getattr(item, bstack11ll111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࡡࡧࡳࡳ࡫ࠧᅷ"), False):
            logger.info(
                bstack11ll111_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠧᅸ"))
            bstack1llll1l1l11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l11l11ll_opy_.bstack111l1l11l1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1llll1ll1l1_opy_(self):
        bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡸࡪࡹࡴࠡࡨ࡬ࡰࡪࡹࠠࡵࡱࠣࡦࡪࠦࡥࡹࡧࡦࡹࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᅹ")
        try:
            from browserstack_sdk.bstack1lllll11l11_opy_ import bstack1lllll1l11l_opy_
            bstack1llll11l111_opy_ = bstack1lllll1l11l_opy_(bstack1lllll111l1_opy_=self.bstack1llll11lll1_opy_)
            if not bstack1llll11l111_opy_.get(bstack11ll111_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᅺ"), False):
                self.logger.error(bstack11ll111_opy_ (u"ࠤࡗࡩࡸࡺࠠࡧ࡫࡯ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨᅻ").format(bstack1llll11l111_opy_.get(bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᅼ"), bstack11ll111_opy_ (u"࡚ࠫࡴ࡫࡯ࡱࡺࡲࠥ࡫ࡲࡳࡱࡵࠫᅽ"))))
                return []
            test_files = bstack1llll11l111_opy_.get(bstack11ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠩᅾ"), [])
            count = bstack1llll11l111_opy_.get(bstack11ll111_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᅿ"), 0)
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡦࡦࠣࡿࢂࠦࡴࡦࡵࡷࡷࠥ࡯࡮ࠡࡽࢀࠤ࡫࡯࡬ࡦࡵࠥᆀ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᆁ").format(e))
            return []