# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import multiprocessing
import os
import json
from time import sleep
import time
import bstack_utils.accessibility as bstack1ll11lll11_opy_
from browserstack_sdk.bstack11ll1ll1_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1l1ll11l_opy_, bstack1lll1l1l111_opy_
from bstack_utils.bstack111ll11l_opy_ import bstack1l1ll111l_opy_
from bstack_utils.constants import bstack1lll1ll111l_opy_
from bstack_utils.bstack1111ll1ll1_opy_ import bstack11l11llll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1ll1111_opy_ import bstack1lll1lll11l_opy_
class bstack1l1ll11l1l_opy_:
    def __init__(self, args, logger, bstack1lll1lllll1_opy_, bstack1lll1l11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack1lll1lllll1_opy_ = bstack1lll1lllll1_opy_
        self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l111l111_opy_ = []
        self.bstack1lll1l1111l_opy_ = []
        self.bstack11l1111l_opy_ = []
        self.bstack1lll1ll1l11_opy_ = self.bstack1ll1ll1l11_opy_()
        self.bstack11l11lll1_opy_ = -1
    @measure(event_name=EVENTS.bstack1lll1l111l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l11l1l1ll_opy_(self, bstack1lll1ll11ll_opy_):
        self.parse_args()
        self.bstack1llll111111_opy_()
        self.bstack1lll1l11lll_opy_(bstack1lll1ll11ll_opy_)
        self.bstack1lll1l1ll1l_opy_()
    @measure(event_name=EVENTS.bstack1lll1lll1l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11ll1llll1_opy_(self):
        bstack1111ll1ll1_opy_ = bstack11l11llll1_opy_.get_instance(self.bstack1lll1lllll1_opy_, self.logger)
        if bstack1111ll1ll1_opy_ is None:
            self.logger.warn(bstack1ll111_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵࠤ࡮ࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࡥ࠰ࠣࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠳ࠨᆴ"))
            return
        bstack1lll1llll1l_opy_ = False
        bstack1111ll1ll1_opy_.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠦࡪࡴࡡࡣ࡮ࡨࡨࠧᆵ"), bstack1111ll1ll1_opy_.bstack11l1ll11ll_opy_())
        start_time = time.time()
        if bstack1111ll1ll1_opy_.bstack11l1ll11ll_opy_():
            test_files = self.bstack1lll1l1llll_opy_()
            bstack1lll1llll1l_opy_ = True
            bstack1lll1lll111_opy_ = bstack1111ll1ll1_opy_.bstack1lll11lllll_opy_(test_files)
            if bstack1lll1lll111_opy_:
                self.bstack11l111l111_opy_ = [os.path.normpath(item) for item in bstack1lll1lll111_opy_]
                self.__1lll1l11ll1_opy_()
                bstack1111ll1ll1_opy_.bstack1lll1llll11_opy_(bstack1lll1llll1l_opy_)
                self.logger.info(bstack1ll111_opy_ (u"࡚ࠧࡥࡴࡶࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡶࡵ࡬ࡲ࡬ࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᆶ").format(self.bstack11l111l111_opy_))
            else:
                self.logger.info(bstack1ll111_opy_ (u"ࠨࡎࡰࠢࡷࡩࡸࡺࠠࡧ࡫࡯ࡩࡸࠦࡷࡦࡴࡨࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡣࡻࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠱ࠦᆷ"))
        bstack1111ll1ll1_opy_.bstack1lll1ll1lll_opy_(bstack1ll111_opy_ (u"ࠢࡵ࡫ࡰࡩ࡙ࡧ࡫ࡦࡰࡗࡳࡆࡶࡰ࡭ࡻࠥᆸ"), int((time.time() - start_time) * 1000)) # bstack1lll1l11111_opy_ to bstack1lll1llllll_opy_
    def __1lll1l11ll1_opy_(self):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡱ࡮ࡤࡧࡪࠦࡴࡦࡵࡷࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳࠡ࡫ࡱࠤࡈࡒࡉࠡࡨ࡯ࡥ࡬ࡹࠠࡸ࡫ࡷ࡬ࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࠢࡳࡥࡹ࡮ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡷࡪࡸࡶࡦࡴࠣࡶࡪࡺࡵࡳࡰࡶࠤࡷ࡫࡯ࡳࡦࡨࡶࡪࡪࠠࡧ࡫࡯ࡩࠥࡴࡡ࡮ࡧࡶ࠰ࠥࡧ࡮ࡥࠢࡺࡩࠥࡹࡩ࡮ࡲ࡯ࡽࠥࡻࡰࡥࡣࡷࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡩࡧࠣࡇࡑࡏࠠࡢࡴࡪࡷࠥࡺ࡯ࠡࡷࡶࡩࠥࡺࡨࡰࡵࡨࠤ࡫࡯࡬ࡦࡵ࠱ࠤ࡚ࡹࡥࡳࠩࡶࠤ࡫࡯࡬ࡵࡧࡵ࡭ࡳ࡭ࠠࡧ࡮ࡤ࡫ࡸࠦࠨ࠮࡯࠯ࠤ࠲ࡱࠩࠡࡴࡨࡱࡦ࡯࡮ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡬ࡲࡹࡧࡣࡵࠢࡤࡲࡩࠦࡷࡪ࡮࡯ࠤࡧ࡫ࠠࡢࡲࡳࡰ࡮࡫ࡤࠡࡰࡤࡸࡺࡸࡡ࡭࡮ࡼࠤࡩࡻࡲࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᆹ")
        try:
            if not self.bstack11l111l111_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡑࡳࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡴࡦࡺࡨࠡࡶࡲࠤࡸ࡫ࡴࠣᆺ"))
                return
            bstack1llll11111l_opy_ = []
            for flag in self.bstack1lll1l1111l_opy_:
                if flag.startswith(bstack1ll111_opy_ (u"ࠪ࠱ࠬᆻ")):
                    bstack1llll11111l_opy_.append(flag)
                    continue
                bstack1llll1111ll_opy_ = False
                if bstack1ll111_opy_ (u"ࠫ࠿ࡀࠧᆼ") in flag:
                    bstack1lll1l1l1ll_opy_ = flag.split(bstack1ll111_opy_ (u"ࠬࡀ࠺ࠨᆽ"), 1)[0]
                    if os.path.exists(bstack1lll1l1l1ll_opy_):
                        bstack1llll1111ll_opy_ = True
                elif os.path.exists(flag):
                    if os.path.isdir(flag) or (os.path.isfile(flag) and flag.endswith(bstack1ll111_opy_ (u"࠭࠮ࡱࡻࠪᆾ"))):
                        bstack1llll1111ll_opy_ = True
                if not bstack1llll1111ll_opy_:
                    bstack1llll11111l_opy_.append(flag)
            bstack1llll11111l_opy_.extend(self.bstack11l111l111_opy_)
            self.bstack1lll1l1111l_opy_ = bstack1llll11111l_opy_
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡥࡥࠢࡶࡩࡱ࡫ࡣࡵࡱࡵࡷ࠿ࠦࡻࡾࠤᆿ").format(str(e)))
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1lll1ll1l1l_opy_():
        return bstack1lll1lll11l_opy_(bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᇀ"))
    def bstack1llll111l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11lll1_opy_ = -1
        if self.bstack1lll1l11l1l_opy_ and bstack1ll111_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᇁ") in self.bstack1lll1lllll1_opy_:
            self.bstack11l11lll1_opy_ = int(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᇂ")])
        try:
            bstack1lll1l1lll1_opy_ = [bstack1ll111_opy_ (u"ࠫ࠲࠳ࡤࡳ࡫ࡹࡩࡷ࠭ᇃ"), bstack1ll111_opy_ (u"ࠬ࠳࠭ࡱ࡮ࡸ࡫࡮ࡴࡳࠨᇄ"), bstack1ll111_opy_ (u"࠭࠭ࡱࠩᇅ")]
            if self.bstack11l11lll1_opy_ >= 0:
                bstack1lll1l1lll1_opy_.extend([bstack1ll111_opy_ (u"ࠧ࠮࠯ࡱࡹࡲࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨᇆ"), bstack1ll111_opy_ (u"ࠨ࠯ࡱࠫᇇ")])
            for arg in bstack1lll1l1lll1_opy_:
                self.bstack1llll111l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1llll111111_opy_(self):
        bstack1lll1l1111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1lll1l1111l_opy_ = bstack1lll1l1111l_opy_
        return self.bstack1lll1l1111l_opy_
    def bstack111l1llll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            if not self.bstack1lll1ll1l1l_opy_():
                self.logger.warning(bstack1lll1l1l111_opy_)
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warning(bstack1ll111_opy_ (u"ࠤࠨࡷ࠿ࠦࠥࡴࠤᇈ"), bstack1l1ll11l_opy_, str(e))
    def bstack1lll1l11lll_opy_(self, bstack1lll1ll11ll_opy_):
        global_config = Config.get_instance()
        if bstack1lll1ll11ll_opy_:
            self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᇉ"))
            self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"࡙ࠫࡸࡵࡦࠩᇊ"))
        if global_config.should_skip_session_status():
            self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᇋ"))
            self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"࠭ࡔࡳࡷࡨࠫᇌ"))
        self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠧ࠮ࡲࠪᇍ"))
        self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ᇎ"))
        self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫᇏ"))
        self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᇐ"))
        if self.bstack11l11lll1_opy_ > 1:
            self.bstack1lll1l1111l_opy_.append(bstack1ll111_opy_ (u"ࠫ࠲ࡴࠧᇑ"))
            self.bstack1lll1l1111l_opy_.append(str(self.bstack11l11lll1_opy_))
    def bstack1lll1l1ll1l_opy_(self):
        if bstack1l1ll111l_opy_.bstack1lll11l11_opy_(self.bstack1lll1lllll1_opy_):
             self.bstack1lll1l1111l_opy_ += [
                bstack1lll1ll111l_opy_.get(bstack1ll111_opy_ (u"ࠬࡸࡥࡳࡷࡱࠫᇒ")), str(bstack1l1ll111l_opy_.bstack1l1l11ll1l_opy_(self.bstack1lll1lllll1_opy_)),
                bstack1lll1ll111l_opy_.get(bstack1ll111_opy_ (u"࠭ࡤࡦ࡮ࡤࡽࠬᇓ")), str(bstack1lll1ll111l_opy_.get(bstack1ll111_opy_ (u"ࠧࡳࡧࡵࡹࡳ࠳ࡤࡦ࡮ࡤࡽࠬᇔ")))
            ]
    def bstack1lll1l1ll11_opy_(self):
        bstack11l1111l_opy_ = []
        for spec in self.bstack11l111l111_opy_:
            bstack11111ll1_opy_ = [spec]
            bstack11111ll1_opy_ += self.bstack1lll1l1111l_opy_
            bstack11l1111l_opy_.append(bstack11111ll1_opy_)
        self.bstack11l1111l_opy_ = bstack11l1111l_opy_
        return bstack11l1111l_opy_
    def bstack1ll1ll1l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1lll1ll1l11_opy_ = True
            return True
        except Exception as e:
            self.bstack1lll1ll1l11_opy_ = False
        return self.bstack1lll1ll1l11_opy_
    @measure(event_name=EVENTS.bstack1lll1ll1ll1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l1111l1ll_opy_(self):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡶࡨࡷࡹࡹࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡷ࡬ࡪࡳࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯࡮ࡵ࠼ࠣࡘ࡭࡫ࠠࡵࡱࡷࡥࡱࠦ࡮ࡶ࡯ࡥࡩࡷࠦ࡯ࡧࠢࡷࡩࡸࡺࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᇕ")
        try:
            from browserstack_sdk.bstack1llll111lll_opy_ import bstack1llll111l1l_opy_
            bstack1llll1111l1_opy_ = bstack1llll111l1l_opy_(bstack1llll11lll1_opy_=self.bstack1lll1l1111l_opy_)
            if not bstack1llll1111l1_opy_.get(bstack1ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᇖ"), False):
                self.logger.error(bstack1ll111_opy_ (u"ࠥࡘࡪࡹࡴࠡࡥࡲࡹࡳࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᇗ").format(bstack1llll1111l1_opy_.get(bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᇘ"), bstack1ll111_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᇙ"))))
                return 0
            count = bstack1llll1111l1_opy_.get(bstack1ll111_opy_ (u"࠭ࡣࡰࡷࡱࡸࠬᇚ"), 0)
            self.logger.info(bstack1ll111_opy_ (u"ࠢࡕࡱࡷࡥࡱࠦࡴࡦࡵࡷࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤ࠻ࠢࡾࢁࠧᇛ").format(count))
            return count
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᇜ").format(e))
            return 0
    def bstack11l1ll1ll1_opy_(self, bstack1lll1l111ll_opy_, bstack1l11l1l1ll_opy_):
        bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩᇝ")] = self.bstack1lll1lllll1_opy_
        multiprocessing.set_start_method(bstack1ll111_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩᇞ"))
        bstack1l1lllll11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lll1lll1ll_opy_ = manager.list()
        if bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᇟ") in self.bstack1lll1lllll1_opy_:
            for index, platform in enumerate(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᇠ")]):
                bstack1l1lllll11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack1lll1l111ll_opy_,
                                                            args=(self.bstack1lll1l1111l_opy_, bstack1l11l1l1ll_opy_, bstack1lll1lll1ll_opy_)))
            bstack1lll1ll11l1_opy_ = len(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᇡ")])
        else:
            bstack1l1lllll11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack1lll1l111ll_opy_,
                                                        args=(self.bstack1lll1l1111l_opy_, bstack1l11l1l1ll_opy_, bstack1lll1lll1ll_opy_)))
            bstack1lll1ll11l1_opy_ = 1
        i = 0
        for t in bstack1l1lllll11_opy_:
            os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᇢ")] = str(i)
            if bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᇣ") in self.bstack1lll1lllll1_opy_:
                os.environ[bstack1ll111_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪᇤ")] = json.dumps(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᇥ")][i % bstack1lll1ll11l1_opy_])
            i += 1
            t.start()
        for t in bstack1l1lllll11_opy_:
            t.join()
        return list(bstack1lll1lll1ll_opy_)
    @staticmethod
    def bstack1l1l11l111_opy_(driver, bstack1lll1l1l11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᇦ"), None)
        if item and getattr(item, bstack1ll111_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧᇧ"), None) and not getattr(item, bstack1ll111_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨᇨ"), False):
            logger.info(
                bstack1ll111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨᇩ"))
            bstack1lll1l11l11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll11lll11_opy_.bstack11lll1lll1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)
    def bstack1lll1l1llll_opy_(self):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡹ࡫ࡳࡵࠢࡩ࡭ࡱ࡫ࡳࠡࡶࡲࠤࡧ࡫ࠠࡦࡺࡨࡧࡺࡺࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᇪ")
        try:
            from browserstack_sdk.bstack1llll111lll_opy_ import bstack1llll111l1l_opy_
            bstack1lll1l1l1l1_opy_ = bstack1llll111l1l_opy_(bstack1llll11lll1_opy_=self.bstack1lll1l1111l_opy_)
            if not bstack1lll1l1l1l1_opy_.get(bstack1ll111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᇫ"), False):
                self.logger.error(bstack1ll111_opy_ (u"ࠥࡘࡪࡹࡴࠡࡨ࡬ࡰࡪࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢᇬ").format(bstack1lll1l1l1l1_opy_.get(bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᇭ"), bstack1ll111_opy_ (u"࡛ࠬ࡮࡬ࡰࡲࡻࡳࠦࡥࡳࡴࡲࡶࠬᇮ"))))
                return []
            test_files = bstack1lll1l1l1l1_opy_.get(bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠪᇯ"), [])
            count = bstack1lll1l1l1l1_opy_.get(bstack1ll111_opy_ (u"ࠧࡤࡱࡸࡲࡹ࠭ᇰ"), 0)
            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡅࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࢀࢃࠠࡵࡧࡶࡸࡸࠦࡩ࡯ࠢࡾࢁࠥ࡬ࡩ࡭ࡧࡶࠦᇱ").format(count, len(test_files)))
            return test_files
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡪ࡮ࡲࡥࡴࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᇲ").format(e))
            return []