# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll11lll1l_opy_ import bstack11ll1l11111_opy_
from bstack_utils.constants import bstack11l1ll1ll11_opy_, bstack11ll11ll_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack111l11l1l_opy_
from bstack_utils import bstack1111l1ll1_opy_
bstack11l1ll111l1_opy_ = 10
class bstack11l111lll_opy_:
    def __init__(self, bstack11ll1l11l_opy_, config, bstack11l1l1ll111_opy_=0):
        self.bstack11l1l1l1lll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1ll1l111_opy_ = bstack11ll11_opy_ (u"ࠢࡼࡿ࠲ࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡧࡣ࡬ࡰࡪࡪ࠭ࡵࡧࡶࡸࡸࠨᩜ").format(bstack11l1ll1ll11_opy_)
        self.bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤᩝ").format(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᩞ"))))
        self.bstack11l1ll11l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤ᩟").format(os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅ᩠ࠩ"))))
        self.bstack11l1ll11l11_opy_ = 2
        self.bstack11ll1l11l_opy_ = bstack11ll1l11l_opy_
        self.config = config
        self.logger = bstack1111l1ll1_opy_.get_logger(__name__, bstack11ll11ll_opy_)
        self.bstack11l1l1ll111_opy_ = bstack11l1l1ll111_opy_
        self.bstack11l1ll11ll1_opy_ = False
        self.bstack11l1l1l11ll_opy_ = not (
                            os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦᩡ")) and
                            os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᩢ")) and
                            os.environ.get(bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᩣ"))
                        )
        if bstack111l11l1l_opy_.bstack11l1l1lll11_opy_(config):
            self.bstack11l1ll11l11_opy_ = bstack111l11l1l_opy_.bstack11l1ll11lll_opy_(config, self.bstack11l1l1ll111_opy_)
            self.bstack11l1l1ll1ll_opy_()
    def bstack11l1ll1111l_opy_(self):
        return bstack11ll11_opy_ (u"ࠣࡽࢀࡣࢀࢃࠢᩤ").format(self.config.get(bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᩥ")), os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᩦ")))
    def bstack11l1l1lll1l_opy_(self):
        try:
            if self.bstack11l1l1l11ll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1ll11l1l_opy_, bstack11ll11_opy_ (u"ࠦࡷࠨᩧ")) as f:
                        bstack11l1l1lllll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l1lllll_opy_ = set()
                bstack11l1l1l1ll1_opy_ = bstack11l1l1lllll_opy_ - self.bstack11l1l1l1lll_opy_
                if not bstack11l1l1l1ll1_opy_:
                    return
                self.bstack11l1l1l1lll_opy_.update(bstack11l1l1l1ll1_opy_)
                data = {bstack11ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࠥᩨ"): list(self.bstack11l1l1l1lll_opy_), bstack11ll11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤᩩ"): self.config.get(bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᩪ")), bstack11ll11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨᩫ"): os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᩬ")), bstack11ll11_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣᩭ"): self.config.get(bstack11ll11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᩮ"))}
            response = bstack11ll1l11111_opy_.bstack11l1l1l1l1l_opy_(self.bstack11l1ll1l111_opy_, data)
            if response.get(bstack11ll11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᩯ")) == 200:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡹࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᩰ").format(data))
            else:
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᩱ").format(response))
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᩲ").format(e))
    def bstack11l1ll111ll_opy_(self):
        if self.bstack11l1l1l11ll_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1ll11l1l_opy_, bstack11ll11_opy_ (u"ࠤࡵࠦᩳ")) as f:
                        bstack11l1l1llll1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l1llll1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠨᩴ").format(failed_count))
                if failed_count >= self.bstack11l1ll11l11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧ᩵").format(failed_count, self.bstack11l1ll11l11_opy_))
                    self.bstack11l1l1ll1l1_opy_(failed_count)
                    self.bstack11l1ll11ll1_opy_ = True
            return
        try:
            response = bstack11ll1l11111_opy_.bstack11l1ll111ll_opy_(bstack11ll11_opy_ (u"ࠧࢁࡽࡀࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࡁࢀࢃࠦࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࡂࢁࡽࠧࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࡃࡻࡾࠤ᩶").format(self.bstack11l1ll1l111_opy_, self.config.get(bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᩷")), os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭᩸")), self.config.get(bstack11ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᩹"))))
            if response.get(bstack11ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᩺")) == 200:
                failed_count = response.get(bstack11ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࡄࡱࡸࡲࡹࠨ᩻"), 0)
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨ᩼").format(failed_count))
                if failed_count >= self.bstack11l1ll11l11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧ᩽").format(failed_count, self.bstack11l1ll11l11_opy_))
                    self.bstack11l1l1ll1l1_opy_(failed_count)
                    self.bstack11l1ll11ll1_opy_ = True
            else:
                self.logger.error(bstack11ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡳࡱࡲࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ᩾").format(response))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡴࡲ࡬ࡪࡰࡪ࠾ࠥࢁࡽ᩿ࠣ").format(e))
    def bstack11l1l1ll1l1_opy_(self, failed_count):
        with open(self.bstack11l1l1l1l11_opy_, bstack11ll11_opy_ (u"ࠣࡹࠥ᪀")) as f:
            f.write(bstack11ll11_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࡡࡵࠢࡾࢁࡡࡴࠢ᪁").format(datetime.now()))
            f.write(bstack11ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࡡࡴࠢ᪂").format(failed_count))
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡆࡨ࡯ࡳࡶࠣࡆࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࢁࠧ᪃").format(self.bstack11l1l1l1l11_opy_))
    def bstack11l1l1ll1ll_opy_(self):
        def bstack11l1l1ll11l_opy_():
            while not self.bstack11l1ll11ll1_opy_:
                time.sleep(bstack11l1ll111l1_opy_)
                self.bstack11l1l1lll1l_opy_()
                self.bstack11l1ll111ll_opy_()
        bstack11l1ll11111_opy_ = threading.Thread(target=bstack11l1l1ll11l_opy_, daemon=True)
        bstack11l1ll11111_opy_.start()