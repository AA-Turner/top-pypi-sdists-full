# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11111lll1ll_opy_ import bstack11111llllll_opy_
from bstack_utils.constants import bstack11111l1l1l1_opy_, bstack1l11l1lll1_opy_
from bstack_utils.bstack111llll111_opy_ import bstack1ll11l1l_opy_
from bstack_utils import logger_utils
bstack11111111111_opy_ = 10
class bstack111l1ll11l_opy_:
    def __init__(self, bstack1l1ll11ll_opy_, config, bstack1llllllll1ll_opy_=0):
        self.bstack1lllllll11ll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1llllll1llll_opy_ = bstack111ll_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤ↥").format(bstack11111l1l1l1_opy_)
        self.bstack1llllll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ↦").format(os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ↧"))))
        self.bstack1llllllll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ↨").format(os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ↩"))))
        self.bstack1lllllllll11_opy_ = 2
        self.bstack1l1ll11ll_opy_ = bstack1l1ll11ll_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l11l1lll1_opy_)
        self.bstack1llllllll1ll_opy_ = bstack1llllllll1ll_opy_
        self.bstack1lllllll1lll_opy_ = False
        self.bstack1111111111l_opy_ = not (
                            os.environ.get(bstack111ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ↪")) and
                            os.environ.get(bstack111ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ↫")) and
                            os.environ.get(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ↬"))
                        )
        if bstack1ll11l1l_opy_.bstack1llllllll111_opy_(config):
            self.bstack1lllllllll11_opy_ = bstack1ll11l1l_opy_.bstack1lllllll1l11_opy_(config, self.bstack1llllllll1ll_opy_)
            self.bstack1lllllll11l1_opy_()
    def bstack1lllllllll1l_opy_(self):
        return bstack111ll_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥ↭").format(self.config.get(bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ↮")), os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ↯")))
    def bstack1llllllllll1_opy_(self):
        try:
            if self.bstack1111111111l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1llllllll1l1_opy_, bstack111ll_opy_ (u"ࠢࡳࠤ↰")) as f:
                        bstack1lllllll1l1l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1lllllll1l1l_opy_ = set()
                bstack1lllllllllll_opy_ = bstack1lllllll1l1l_opy_ - self.bstack1lllllll11ll_opy_
                if not bstack1lllllllllll_opy_:
                    return
                self.bstack1lllllll11ll_opy_.update(bstack1lllllllllll_opy_)
                data = {bstack111ll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨ↱"): list(self.bstack1lllllll11ll_opy_), bstack111ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ↲"): self.config.get(bstack111ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭↳")), bstack111ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ↴"): os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ↵")), bstack111ll_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ↶"): self.config.get(bstack111ll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ↷"))}
            response = bstack11111llllll_opy_.bstack1lllllll1ll1_opy_(self.bstack1llllll1llll_opy_, data)
            if response.get(bstack111ll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ↸")) == 200:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ↹").format(data))
            else:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ↺").format(response))
        except Exception as e:
            self.logger.debug(bstack111ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ↻").format(e))
    def bstack1llllllll11l_opy_(self):
        if self.bstack1111111111l_opy_:
            with self.lock:
                try:
                    with open(self.bstack1llllllll1l1_opy_, bstack111ll_opy_ (u"ࠧࡸࠢ↼")) as f:
                        bstack1lllllll111l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1lllllll111l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack111ll_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ↽").format(failed_count))
                if failed_count >= self.bstack1lllllllll11_opy_:
                    self.logger.info(bstack111ll_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ↾").format(failed_count, self.bstack1lllllllll11_opy_))
                    self.bstack111111111l1_opy_(failed_count)
                    self.bstack1lllllll1lll_opy_ = True
            return
        try:
            response = bstack11111llllll_opy_.bstack1llllllll11l_opy_(bstack111ll_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧ↿").format(self.bstack1llllll1llll_opy_, self.config.get(bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⇀")), os.environ.get(bstack111ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ⇁")), self.config.get(bstack111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⇂"))))
            if response.get(bstack111ll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ⇃")) == 200:
                failed_count = response.get(bstack111ll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤ⇄"), 0)
                self.logger.debug(bstack111ll_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ⇅").format(failed_count))
                if failed_count >= self.bstack1lllllllll11_opy_:
                    self.logger.info(bstack111ll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ⇆").format(failed_count, self.bstack1lllllllll11_opy_))
                    self.bstack111111111l1_opy_(failed_count)
                    self.bstack1lllllll1lll_opy_ = True
            else:
                self.logger.error(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ⇇").format(response))
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦ⇈").format(e))
    def bstack111111111l1_opy_(self, failed_count):
        with open(self.bstack1llllll1lll1_opy_, bstack111ll_opy_ (u"ࠦࡼࠨ⇉")) as f:
            f.write(bstack111ll_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥ⇊").format(datetime.now()))
            f.write(bstack111ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥ⇋").format(failed_count))
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣ⇌").format(self.bstack1llllll1lll1_opy_))
    def bstack1lllllll11l1_opy_(self):
        def bstack1lllllll1111_opy_():
            while not self.bstack1lllllll1lll_opy_:
                time.sleep(bstack11111111111_opy_)
                self.bstack1llllllllll1_opy_()
                self.bstack1llllllll11l_opy_()
        bstack111111111ll_opy_ = threading.Thread(target=bstack1lllllll1111_opy_, daemon=True)
        bstack111111111ll_opy_.start()