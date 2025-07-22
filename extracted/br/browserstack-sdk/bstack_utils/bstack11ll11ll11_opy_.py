# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll111lll1_opy_
from bstack_utils.constants import bstack11l1lllll1l_opy_, bstack11l1ll11ll_opy_
from bstack_utils.bstack1lll1111ll_opy_ import bstack11llllll_opy_
from bstack_utils import bstack1l1111ll_opy_
bstack11l1l1ll11l_opy_ = 10
class bstack1ll1lll1_opy_:
    def __init__(self, bstack11l1l11111_opy_, config, bstack11l1l1ll1l1_opy_=0):
        self.bstack11l1l1l11ll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l1l1l1l_opy_ = bstack111l111_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤ᪺").format(bstack11l1lllll1l_opy_)
        self.bstack11l1l1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ᪻").format(os.environ.get(bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᪼"))))
        self.bstack11l1l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸ᪽ࠧ").format(os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᪾"))))
        self.bstack11l1l11l11l_opy_ = 2
        self.bstack11l1l11111_opy_ = bstack11l1l11111_opy_
        self.config = config
        self.logger = bstack1l1111ll_opy_.get_logger(__name__, bstack11l1ll11ll_opy_)
        self.bstack11l1l1ll1l1_opy_ = bstack11l1l1ll1l1_opy_
        self.bstack11l1l11ll1l_opy_ = False
        self.bstack11l1l11l1ll_opy_ = not (
                            os.environ.get(bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘᪿࠢ")) and
                            os.environ.get(bstack111l111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ᫀࠧ")) and
                            os.environ.get(bstack111l111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ᫁"))
                        )
        if bstack11llllll_opy_.bstack11l1l11l111_opy_(config):
            self.bstack11l1l11l11l_opy_ = bstack11llllll_opy_.bstack11l1l1l111l_opy_(config, self.bstack11l1l1ll1l1_opy_)
            self.bstack11l1l1l1l11_opy_()
    def bstack11l1l1l11l1_opy_(self):
        return bstack111l111_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥ᫂").format(self.config.get(bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᫃")), os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ᫄ࠬ")))
    def bstack11l1l1l1ll1_opy_(self):
        try:
            if self.bstack11l1l11l1ll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l11l1l1_opy_, bstack111l111_opy_ (u"ࠢࡳࠤ᫅")) as f:
                        bstack11l1l111ll1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l111ll1_opy_ = set()
                bstack11l1l11lll1_opy_ = bstack11l1l111ll1_opy_ - self.bstack11l1l1l11ll_opy_
                if not bstack11l1l11lll1_opy_:
                    return
                self.bstack11l1l1l11ll_opy_.update(bstack11l1l11lll1_opy_)
                data = {bstack111l111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨ᫆"): list(self.bstack11l1l1l11ll_opy_), bstack111l111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ᫇"): self.config.get(bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᫈")), bstack111l111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ᫉"): os.environ.get(bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ᫊ࠫ")), bstack111l111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ᫋"): self.config.get(bstack111l111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᫌ"))}
            response = bstack11ll111lll1_opy_.bstack11l1l1l1111_opy_(self.bstack11l1l1l1l1l_opy_, data)
            if response.get(bstack111l111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᫍ")) == 200:
                self.logger.debug(bstack111l111_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᫎ").format(data))
            else:
                self.logger.debug(bstack111l111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ᫏").format(response))
        except Exception as e:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᫐").format(e))
    def bstack11l1l11llll_opy_(self):
        if self.bstack11l1l11l1ll_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l11l1l1_opy_, bstack111l111_opy_ (u"ࠧࡸࠢ᫑")) as f:
                        bstack11l1l11ll11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l11ll11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack111l111_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ᫒").format(failed_count))
                if failed_count >= self.bstack11l1l11l11l_opy_:
                    self.logger.info(bstack111l111_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ᫓").format(failed_count, self.bstack11l1l11l11l_opy_))
                    self.bstack11l1l1ll111_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            return
        try:
            response = bstack11ll111lll1_opy_.bstack11l1l11llll_opy_(bstack111l111_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧ᫔").format(self.bstack11l1l1l1l1l_opy_, self.config.get(bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᫕")), os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ᫖")), self.config.get(bstack111l111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ᫗"))))
            if response.get(bstack111l111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ᫘")) == 200:
                failed_count = response.get(bstack111l111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤ᫙"), 0)
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ᫚").format(failed_count))
                if failed_count >= self.bstack11l1l11l11l_opy_:
                    self.logger.info(bstack111l111_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ᫛").format(failed_count, self.bstack11l1l11l11l_opy_))
                    self.bstack11l1l1ll111_opy_(failed_count)
                    self.bstack11l1l11ll1l_opy_ = True
            else:
                self.logger.error(bstack111l111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ᫜").format(response))
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦ᫝").format(e))
    def bstack11l1l1ll111_opy_(self, failed_count):
        with open(self.bstack11l1l1l1lll_opy_, bstack111l111_opy_ (u"ࠦࡼࠨ᫞")) as f:
            f.write(bstack111l111_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥ᫟").format(datetime.now()))
            f.write(bstack111l111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥ᫠").format(failed_count))
        self.logger.debug(bstack111l111_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣ᫡").format(self.bstack11l1l1l1lll_opy_))
    def bstack11l1l1l1l11_opy_(self):
        def bstack11l1l1ll1ll_opy_():
            while not self.bstack11l1l11ll1l_opy_:
                time.sleep(bstack11l1l1ll11l_opy_)
                self.bstack11l1l1l1ll1_opy_()
                self.bstack11l1l11llll_opy_()
        bstack11l1l111lll_opy_ = threading.Thread(target=bstack11l1l1ll1ll_opy_, daemon=True)
        bstack11l1l111lll_opy_.start()