# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import bstack11ll111111l_opy_, bstack11ll1lll_opy_
from bstack_utils.bstack111l11l1_opy_ import bstack1l111ll11l_opy_
from bstack_utils import bstack1l1111111_opy_
bstack11l1l1l11l1_opy_ = 10
class bstack1ll11l1l1_opy_:
    def __init__(self, bstack11l11ll111_opy_, config, bstack11l1l1l1l1l_opy_=0):
        self.bstack11l1l1llll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l11lll1_opy_ = bstack11l1_opy_ (u"ࠧࢁࡽ࠰ࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡬ࡡࡪ࡮ࡨࡨ࠲ࡺࡥࡴࡶࡶࠦ᪼").format(bstack11ll111111l_opy_)
        self.bstack11l1l1lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃ᪽ࠢ").format(os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᪾"))))
        self.bstack11l1l1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺᪿࠢ").format(os.environ.get(bstack11l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊᫀࠧ"))))
        self.bstack11l1l1l1111_opy_ = 2
        self.bstack11l11ll111_opy_ = bstack11l11ll111_opy_
        self.config = config
        self.logger = bstack1l1111111_opy_.get_logger(__name__, bstack11ll1lll_opy_)
        self.bstack11l1l1l1l1l_opy_ = bstack11l1l1l1l1l_opy_
        self.bstack11l1l11llll_opy_ = False
        self.bstack11l1l1l1ll1_opy_ = not (
                            os.environ.get(bstack11l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤ᫁")) and
                            os.environ.get(bstack11l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢ᫂")) and
                            os.environ.get(bstack11l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚᫃ࠢ"))
                        )
        if bstack1l111ll11l_opy_.bstack11l1l11ll1l_opy_(config):
            self.bstack11l1l1l1111_opy_ = bstack1l111ll11l_opy_.bstack11l1l1ll111_opy_(config, self.bstack11l1l1l1l1l_opy_)
            self.bstack11l1l1ll1l1_opy_()
    def bstack11l1l1ll1ll_opy_(self):
        return bstack11l1_opy_ (u"ࠨࡻࡾࡡࡾࢁ᫄ࠧ").format(self.config.get(bstack11l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ᫅")), os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ᫆")))
    def bstack11l1l1ll11l_opy_(self):
        try:
            if self.bstack11l1l1l1ll1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l11_opy_, bstack11l1_opy_ (u"ࠤࡵࠦ᫇")) as f:
                        bstack11l1l11ll11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l11ll11_opy_ = set()
                bstack11l1l11l1ll_opy_ = bstack11l1l11ll11_opy_ - self.bstack11l1l1llll1_opy_
                if not bstack11l1l11l1ll_opy_:
                    return
                self.bstack11l1l1llll1_opy_.update(bstack11l1l11l1ll_opy_)
                data = {bstack11l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࠣ᫈"): list(self.bstack11l1l1llll1_opy_), bstack11l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ᫉"): self.config.get(bstack11l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ᫊")), bstack11l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ᫋"): os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᫌ")), bstack11l1_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨᫍ"): self.config.get(bstack11l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᫎ"))}
            response = bstack11ll11l1111_opy_.bstack11l1l1l1lll_opy_(self.bstack11l1l11lll1_opy_, data)
            if response.get(bstack11l1_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ᫏")) == 200:
                self.logger.debug(bstack11l1_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡷࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ᫐").format(data))
            else:
                self.logger.debug(bstack11l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ᫑").format(response))
        except Exception as e:
            self.logger.debug(bstack11l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ᫒").format(e))
    def bstack11l1l1l11ll_opy_(self):
        if self.bstack11l1l1l1ll1_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1l11_opy_, bstack11l1_opy_ (u"ࠢࡳࠤ᫓")) as f:
                        bstack11l1l1l111l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l1l111l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11l1_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠦ᫔").format(failed_count))
                if failed_count >= self.bstack11l1l1l1111_opy_:
                    self.logger.info(bstack11l1_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ᫕").format(failed_count, self.bstack11l1l1l1111_opy_))
                    self.bstack11l1l11l1l1_opy_(failed_count)
                    self.bstack11l1l11llll_opy_ = True
            return
        try:
            response = bstack11ll11l1111_opy_.bstack11l1l1l11ll_opy_(bstack11l1_opy_ (u"ࠥࡿࢂࡅࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࠿ࡾࢁࠫࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࡀࡿࢂࠬࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࡁࢀࢃࠢ᫖").format(self.bstack11l1l11lll1_opy_, self.config.get(bstack11l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᫗")), os.environ.get(bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ᫘")), self.config.get(bstack11l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᫙"))))
            if response.get(bstack11l1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᫚")) == 200:
                failed_count = response.get(bstack11l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࡉ࡯ࡶࡰࡷࠦ᫛"), 0)
                self.logger.debug(bstack11l1_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦ᫜").format(failed_count))
                if failed_count >= self.bstack11l1l1l1111_opy_:
                    self.logger.info(bstack11l1_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪ࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ᫝").format(failed_count, self.bstack11l1l1l1111_opy_))
                    self.bstack11l1l11l1l1_opy_(failed_count)
                    self.bstack11l1l11llll_opy_ = True
            else:
                self.logger.error(bstack11l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱ࡯ࡰࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ᫞").format(response))
        except Exception as e:
            self.logger.error(bstack11l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡲࡰࡱ࡯࡮ࡨ࠼ࠣࡿࢂࠨ᫟").format(e))
    def bstack11l1l11l1l1_opy_(self, failed_count):
        with open(self.bstack11l1l1lll1l_opy_, bstack11l1_opy_ (u"ࠨࡷࠣ᫠")) as f:
            f.write(bstack11l1_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤࡦࡺࠠࡼࡿ࡟ࡲࠧ᫡").format(datetime.now()))
            f.write(bstack11l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿ࡟ࡲࠧ᫢").format(failed_count))
        self.logger.debug(bstack11l1_opy_ (u"ࠤࡄࡦࡴࡸࡴࠡࡄࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡿࠥ᫣").format(self.bstack11l1l1lll1l_opy_))
    def bstack11l1l1ll1l1_opy_(self):
        def bstack11l1l11l11l_opy_():
            while not self.bstack11l1l11llll_opy_:
                time.sleep(bstack11l1l1l11l1_opy_)
                self.bstack11l1l1ll11l_opy_()
                self.bstack11l1l1l11ll_opy_()
        bstack11l1l1lll11_opy_ = threading.Thread(target=bstack11l1l11l11l_opy_, daemon=True)
        bstack11l1l1lll11_opy_.start()