# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll1l111l1_opy_ import bstack11ll11lllll_opy_
from bstack_utils.constants import bstack11l1ll1ll11_opy_, bstack1ll1ll1l_opy_
from bstack_utils.bstack1llll1llll_opy_ import bstack1ll11111l_opy_
from bstack_utils import bstack1llll1l111_opy_
bstack11l1l1ll1l1_opy_ = 10
class bstack1llll1l1ll_opy_:
    def __init__(self, bstack1l11ll1l_opy_, config, bstack11l1l1l1l11_opy_=0):
        self.bstack11l1l1lllll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l1l1ll1_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡽࢀ࠳ࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡨࡤ࡭ࡱ࡫ࡤ࠮ࡶࡨࡷࡹࡹࠢᩝ").format(bstack11l1ll1ll11_opy_)
        self.bstack11l1ll111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠤࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡼࡿࠥᩞ").format(os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᩟"))))
        self.bstack11l1l1l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶ᩠ࠥ").format(os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᩡ"))))
        self.bstack11l1l1l1lll_opy_ = 2
        self.bstack1l11ll1l_opy_ = bstack1l11ll1l_opy_
        self.config = config
        self.logger = bstack1llll1l111_opy_.get_logger(__name__, bstack1ll1ll1l_opy_)
        self.bstack11l1l1l1l11_opy_ = bstack11l1l1l1l11_opy_
        self.bstack11l1l1lll11_opy_ = False
        self.bstack11l1ll1111l_opy_ = not (
                            os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧᩢ")) and
                            os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥᩣ")) and
                            os.environ.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥᩤ"))
                        )
        if bstack1ll11111l_opy_.bstack11l1l1lll1l_opy_(config):
            self.bstack11l1l1l1lll_opy_ = bstack1ll11111l_opy_.bstack11l1l1ll111_opy_(config, self.bstack11l1l1l1l11_opy_)
            self.bstack11l1l1ll11l_opy_()
    def bstack11l1ll11l11_opy_(self):
        return bstack1l1l1l1_opy_ (u"ࠤࡾࢁࡤࢁࡽࠣᩥ").format(self.config.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᩦ")), os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᩧ")))
    def bstack11l1ll11ll1_opy_(self):
        try:
            if self.bstack11l1ll1111l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࠢᩨ")) as f:
                        bstack11l1l1ll1ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l1ll1ll_opy_ = set()
                bstack11l1l1llll1_opy_ = bstack11l1l1ll1ll_opy_ - self.bstack11l1l1lllll_opy_
                if not bstack11l1l1llll1_opy_:
                    return
                self.bstack11l1l1lllll_opy_.update(bstack11l1l1llll1_opy_)
                data = {bstack1l1l1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࠦᩩ"): list(self.bstack11l1l1lllll_opy_), bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥᩪ"): self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᩫ")), bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢᩬ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᩭ")), bstack1l1l1l1_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤᩮ"): self.config.get(bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᩯ"))}
            response = bstack11ll11lllll_opy_.bstack11l1l1l11ll_opy_(self.bstack11l1l1l1ll1_opy_, data)
            if response.get(bstack1l1l1l1_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᩰ")) == 200:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡳࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᩱ").format(data))
            else:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᩲ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᩳ").format(e))
    def bstack11l1ll11lll_opy_(self):
        if self.bstack11l1ll1111l_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠥࡶࠧᩴ")) as f:
                        bstack11l1ll111ll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1ll111ll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠢ᩵").format(failed_count))
                if failed_count >= self.bstack11l1l1l1lll_opy_:
                    self.logger.info(bstack1l1l1l1_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨ᩶").format(failed_count, self.bstack11l1l1l1lll_opy_))
                    self.bstack11l1ll1l111_opy_(failed_count)
                    self.bstack11l1l1lll11_opy_ = True
            return
        try:
            response = bstack11ll11lllll_opy_.bstack11l1ll11lll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡻࡾࡁࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࡂࢁࡽࠧࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡃࡻࡾࠨࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫࠽ࡼࡿࠥ᩷").format(self.bstack11l1l1l1ll1_opy_, self.config.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᩸")), os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᩹")), self.config.get(bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᩺"))))
            if response.get(bstack1l1l1l1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᩻")) == 200:
                failed_count = response.get(bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࡅࡲࡹࡳࡺࠢ᩼"), 0)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢ᩽").format(failed_count))
                if failed_count >= self.bstack11l1l1l1lll_opy_:
                    self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨ᩾").format(failed_count, self.bstack11l1l1l1lll_opy_))
                    self.bstack11l1ll1l111_opy_(failed_count)
                    self.bstack11l1l1lll11_opy_ = True
            else:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡴࡲ࡬ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀ᩿ࠦ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡵࡵ࡬࡭࡫ࡱ࡫࠿ࠦࡻࡾࠤ᪀").format(e))
    def bstack11l1ll1l111_opy_(self, failed_count):
        with open(self.bstack11l1ll111l1_opy_, bstack1l1l1l1_opy_ (u"ࠤࡺࠦ᪁")) as f:
            f.write(bstack1l1l1l1_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࡢࡶࠣࡿࢂࡢ࡮ࠣ᪂").format(datetime.now()))
            f.write(bstack1l1l1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࡢ࡮ࠣ᪃").format(failed_count))
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡇࡢࡰࡴࡷࠤࡇࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࢂࠨ᪄").format(self.bstack11l1ll111l1_opy_))
    def bstack11l1l1ll11l_opy_(self):
        def bstack11l1ll11l1l_opy_():
            while not self.bstack11l1l1lll11_opy_:
                time.sleep(bstack11l1l1ll1l1_opy_)
                self.bstack11l1ll11ll1_opy_()
                self.bstack11l1ll11lll_opy_()
        bstack11l1ll11111_opy_ = threading.Thread(target=bstack11l1ll11l1l_opy_, daemon=True)
        bstack11l1ll11111_opy_.start()