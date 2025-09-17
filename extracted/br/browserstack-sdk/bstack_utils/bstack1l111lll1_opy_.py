# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll111ll1l_opy_ import bstack11ll111l1ll_opy_
from bstack_utils.constants import bstack11l1l1ll1ll_opy_, bstack11lllll1l1_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11llll1111_opy_
from bstack_utils import bstack1lll1l1l1l_opy_
bstack11l1l11llll_opy_ = 10
class bstack1llllll1l_opy_:
    def __init__(self, bstack11ll111ll_opy_, config, bstack11l1l1l1l11_opy_=0):
        self.bstack11l1l111l11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l11lll1_opy_ = bstack1l11ll1_opy_ (u"ࠢࡼࡿ࠲ࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡧࡣ࡬ࡰࡪࡪ࠭ࡵࡧࡶࡸࡸࠨᫌ").format(bstack11l1l1ll1ll_opy_)
        self.bstack11l1l111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤᫍ").format(os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᫎ"))))
        self.bstack11l1l1l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤ᫏").format(os.environ.get(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᫐"))))
        self.bstack11l1l1l111l_opy_ = 2
        self.bstack11ll111ll_opy_ = bstack11ll111ll_opy_
        self.config = config
        self.logger = bstack1lll1l1l1l_opy_.get_logger(__name__, bstack11lllll1l1_opy_)
        self.bstack11l1l1l1l11_opy_ = bstack11l1l1l1l11_opy_
        self.bstack11l1l11ll1l_opy_ = False
        self.bstack11l1l11111l_opy_ = not (
                            os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦ᫑")) and
                            os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤ᫒")) and
                            os.environ.get(bstack1l11ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤ᫓"))
                        )
        if bstack11llll1111_opy_.bstack11l1l1111ll_opy_(config):
            self.bstack11l1l1l111l_opy_ = bstack11llll1111_opy_.bstack11l1l111lll_opy_(config, self.bstack11l1l1l1l11_opy_)
            self.bstack11l1l1l1ll1_opy_()
    def bstack11l1l1l11ll_opy_(self):
        return bstack1l11ll1_opy_ (u"ࠣࡽࢀࡣࢀࢃࠢ᫔").format(self.config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᫕")), os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ᫖")))
    def bstack11l1l11l111_opy_(self):
        try:
            if self.bstack11l1l11111l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l1l_opy_, bstack1l11ll1_opy_ (u"ࠦࡷࠨ᫗")) as f:
                        bstack11l1l11ll11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l11ll11_opy_ = set()
                bstack11l1l1l11l1_opy_ = bstack11l1l11ll11_opy_ - self.bstack11l1l111l11_opy_
                if not bstack11l1l1l11l1_opy_:
                    return
                self.bstack11l1l111l11_opy_.update(bstack11l1l1l11l1_opy_)
                data = {bstack1l11ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࠥ᫘"): list(self.bstack11l1l111l11_opy_), bstack1l11ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤ᫙"): self.config.get(bstack1l11ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᫚")), bstack1l11ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨ᫛"): os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᫜")), bstack1l11ll1_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣ᫝"): self.config.get(bstack1l11ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ᫞"))}
            response = bstack11ll111l1ll_opy_.bstack11l1l111ll1_opy_(self.bstack11l1l11lll1_opy_, data)
            if response.get(bstack1l11ll1_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᫟")) == 200:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡹࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ᫠").format(data))
            else:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᫡").format(response))
        except Exception as e:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ᫢").format(e))
    def bstack11l1l1l1111_opy_(self):
        if self.bstack11l1l11111l_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l1l_opy_, bstack1l11ll1_opy_ (u"ࠤࡵࠦ᫣")) as f:
                        bstack11l1l11l1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l11l1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠨ᫤").format(failed_count))
                if failed_count >= self.bstack11l1l1l111l_opy_:
                    self.logger.info(bstack1l11ll1_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧ᫥").format(failed_count, self.bstack11l1l1l111l_opy_))
                    self.bstack11l1l11l1ll_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            return
        try:
            response = bstack11ll111l1ll_opy_.bstack11l1l1l1111_opy_(bstack1l11ll1_opy_ (u"ࠧࢁࡽࡀࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࡁࢀࢃࠦࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࡂࢁࡽࠧࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࡃࡻࡾࠤ᫦").format(self.bstack11l1l11lll1_opy_, self.config.get(bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᫧")), os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭᫨")), self.config.get(bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᫩"))))
            if response.get(bstack1l11ll1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ᫪")) == 200:
                failed_count = response.get(bstack1l11ll1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࡄࡱࡸࡲࡹࠨ᫫"), 0)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨ᫬").format(failed_count))
                if failed_count >= self.bstack11l1l1l111l_opy_:
                    self.logger.info(bstack1l11ll1_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧ᫭").format(failed_count, self.bstack11l1l1l111l_opy_))
                    self.bstack11l1l11l1ll_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            else:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡳࡱࡲࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ᫮").format(response))
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡴࡲ࡬ࡪࡰࡪ࠾ࠥࢁࡽࠣ᫯").format(e))
    def bstack11l1l11l1ll_opy_(self, failed_count):
        with open(self.bstack11l1l111l1l_opy_, bstack1l11ll1_opy_ (u"ࠣࡹࠥ᫰")) as f:
            f.write(bstack1l11ll1_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࡡࡵࠢࡾࢁࡡࡴࠢ᫱").format(datetime.now()))
            f.write(bstack1l11ll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࡡࡴࠢ᫲").format(failed_count))
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡆࡨ࡯ࡳࡶࠣࡆࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࢁࠧ᫳").format(self.bstack11l1l111l1l_opy_))
    def bstack11l1l1l1ll1_opy_(self):
        def bstack11l1l1111l1_opy_():
            while not self.bstack11l1l11ll1l_opy_:
                time.sleep(bstack11l1l11llll_opy_)
                self.bstack11l1l11l111_opy_()
                self.bstack11l1l1l1111_opy_()
        bstack11l1l11l11l_opy_ = threading.Thread(target=bstack11l1l1111l1_opy_, daemon=True)
        bstack11l1l11l11l_opy_.start()