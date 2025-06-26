# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll11l1ll1_opy_ import bstack11ll11ll111_opy_
from bstack_utils.constants import bstack11l1ll1l111_opy_, bstack1l11l1111_opy_
from bstack_utils.bstack1l111l1ll_opy_ import bstack1ll1lll1_opy_
from bstack_utils import bstack11l1l1l111_opy_
bstack11l1l1l1lll_opy_ = 10
class bstack11lllll11l_opy_:
    def __init__(self, bstack111lll1l_opy_, config, bstack11l1l1l111l_opy_=0):
        self.bstack11l1l1l1ll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l1ll11l_opy_ = bstack11ll1l1_opy_ (u"ࠧࢁࡽ࠰ࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡬ࡡࡪ࡮ࡨࡨ࠲ࡺࡥࡴࡶࡶࠦ᩽").format(bstack11l1ll1l111_opy_)
        self.bstack11l1l11ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢ᩾").format(os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᩿ࠬ"))))
        self.bstack11l1l1ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ᪀").format(os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᪁"))))
        self.bstack11l1l1ll111_opy_ = 2
        self.bstack111lll1l_opy_ = bstack111lll1l_opy_
        self.config = config
        self.logger = bstack11l1l1l111_opy_.get_logger(__name__, bstack1l11l1111_opy_)
        self.bstack11l1l1l111l_opy_ = bstack11l1l1l111l_opy_
        self.bstack11l1l11ll1l_opy_ = False
        self.bstack11l1l1l1l1l_opy_ = not (
                            os.environ.get(bstack11ll1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ᪂")) and
                            os.environ.get(bstack11ll1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ᪃")) and
                            os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢ᪄"))
                        )
        if bstack1ll1lll1_opy_.bstack11l1ll1111l_opy_(config):
            self.bstack11l1l1ll111_opy_ = bstack1ll1lll1_opy_.bstack11l1l1l1l11_opy_(config, self.bstack11l1l1l111l_opy_)
            self.bstack11l1l1lllll_opy_()
    def bstack11l1l1lll11_opy_(self):
        return bstack11ll1l1_opy_ (u"ࠨࡻࡾࡡࡾࢁࠧ᪅").format(self.config.get(bstack11ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᪆")), os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᪇")))
    def bstack11l1l1l1111_opy_(self):
        try:
            if self.bstack11l1l1l1l1l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l1ll1l1_opy_, bstack11ll1l1_opy_ (u"ࠤࡵࠦ᪈")) as f:
                        bstack11l1l1ll1ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l1ll1ll_opy_ = set()
                bstack11l1ll11111_opy_ = bstack11l1l1ll1ll_opy_ - self.bstack11l1l1l1ll1_opy_
                if not bstack11l1ll11111_opy_:
                    return
                self.bstack11l1l1l1ll1_opy_.update(bstack11l1ll11111_opy_)
                data = {bstack11ll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࠣ᪉"): list(self.bstack11l1l1l1ll1_opy_), bstack11ll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ᪊"): self.config.get(bstack11ll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᪋")), bstack11ll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ᪌"): os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭᪍")), bstack11ll1l1_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨ᪎"): self.config.get(bstack11ll1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᪏"))}
            response = bstack11ll11ll111_opy_.bstack11l1l11lll1_opy_(self.bstack11l1l1ll11l_opy_, data)
            if response.get(bstack11ll1l1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᪐")) == 200:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡷࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᪑").format(data))
            else:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ᪒").format(response))
        except Exception as e:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ᪓").format(e))
    def bstack11l1l1lll1l_opy_(self):
        if self.bstack11l1l1l1l1l_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l1ll1l1_opy_, bstack11ll1l1_opy_ (u"ࠢࡳࠤ᪔")) as f:
                        bstack11l1l1l11ll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l1l11ll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠦ᪕").format(failed_count))
                if failed_count >= self.bstack11l1l1ll111_opy_:
                    self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ᪖").format(failed_count, self.bstack11l1l1ll111_opy_))
                    self.bstack11l1l1llll1_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            return
        try:
            response = bstack11ll11ll111_opy_.bstack11l1l1lll1l_opy_(bstack11ll1l1_opy_ (u"ࠥࡿࢂࡅࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࠿ࡾࢁࠫࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࡀࡿࢂࠬࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࡁࢀࢃࠢ᪗").format(self.bstack11l1l1ll11l_opy_, self.config.get(bstack11ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᪘")), os.environ.get(bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ᪙")), self.config.get(bstack11ll1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᪚"))))
            if response.get(bstack11ll1l1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᪛")) == 200:
                failed_count = response.get(bstack11ll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࡉ࡯ࡶࡰࡷࠦ᪜"), 0)
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦ᪝").format(failed_count))
                if failed_count >= self.bstack11l1l1ll111_opy_:
                    self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪ࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ᪞").format(failed_count, self.bstack11l1l1ll111_opy_))
                    self.bstack11l1l1llll1_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            else:
                self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱ࡯ࡰࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ᪟").format(response))
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡲࡰࡱ࡯࡮ࡨ࠼ࠣࡿࢂࠨ᪠").format(e))
    def bstack11l1l1llll1_opy_(self, failed_count):
        with open(self.bstack11l1l11ll11_opy_, bstack11ll1l1_opy_ (u"ࠨࡷࠣ᪡")) as f:
            f.write(bstack11ll1l1_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤࡦࡺࠠࡼࡿ࡟ࡲࠧ᪢").format(datetime.now()))
            f.write(bstack11ll1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿ࡟ࡲࠧ᪣").format(failed_count))
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡄࡦࡴࡸࡴࠡࡄࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡿࠥ᪤").format(self.bstack11l1l11ll11_opy_))
    def bstack11l1l1lllll_opy_(self):
        def bstack11l1l1l11l1_opy_():
            while not self.bstack11l1l11ll1l_opy_:
                time.sleep(bstack11l1l1l1lll_opy_)
                self.bstack11l1l1l1111_opy_()
                self.bstack11l1l1lll1l_opy_()
        bstack11l1l11llll_opy_ = threading.Thread(target=bstack11l1l1l11l1_opy_, daemon=True)
        bstack11l1l11llll_opy_.start()