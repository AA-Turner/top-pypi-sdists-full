# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11ll111lll1_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import bstack11l1ll111l1_opy_, bstack1ll111ll11_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from bstack_utils import bstack11l1111l1_opy_
bstack11l1l11ll1l_opy_ = 10
class bstack1111l111_opy_:
    def __init__(self, bstack1l1lllllll_opy_, config, bstack11l1l1l1ll1_opy_=0):
        self.bstack11l1l1l11l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11l1l11l1l1_opy_ = bstack1111l1l_opy_ (u"ࠤࡾࢁ࠴ࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣᫎ").format(bstack11l1ll111l1_opy_)
        self.bstack11l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦ᫏").format(os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᫐"))))
        self.bstack11l1l1l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦ᫑").format(os.environ.get(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᫒"))))
        self.bstack11l1l1111l1_opy_ = 2
        self.bstack1l1lllllll_opy_ = bstack1l1lllllll_opy_
        self.config = config
        self.logger = bstack11l1111l1_opy_.get_logger(__name__, bstack1ll111ll11_opy_)
        self.bstack11l1l1l1ll1_opy_ = bstack11l1l1l1ll1_opy_
        self.bstack11l1l11lll1_opy_ = False
        self.bstack11l1l11llll_opy_ = not (
                            os.environ.get(bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨ᫓")) and
                            os.environ.get(bstack1111l1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦ᫔")) and
                            os.environ.get(bstack1111l1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦ᫕"))
                        )
        if bstack111l1llll_opy_.bstack11l1l111l11_opy_(config):
            self.bstack11l1l1111l1_opy_ = bstack111l1llll_opy_.bstack11l1l1111ll_opy_(config, self.bstack11l1l1l1ll1_opy_)
            self.bstack11l1l11l11l_opy_()
    def bstack11l1l111l1l_opy_(self):
        return bstack1111l1l_opy_ (u"ࠥࡿࢂࡥࡻࡾࠤ᫖").format(self.config.get(bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᫗")), os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ᫘")))
    def bstack11l1l11l1ll_opy_(self):
        try:
            if self.bstack11l1l11llll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1lll_opy_, bstack1111l1l_opy_ (u"ࠨࡲࠣ᫙")) as f:
                        bstack11l1l11ll11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack11l1l11ll11_opy_ = set()
                bstack11l1l1l1111_opy_ = bstack11l1l11ll11_opy_ - self.bstack11l1l1l11l1_opy_
                if not bstack11l1l1l1111_opy_:
                    return
                self.bstack11l1l1l11l1_opy_.update(bstack11l1l1l1111_opy_)
                data = {bstack1111l1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࠧ᫚"): list(self.bstack11l1l1l11l1_opy_), bstack1111l1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦ᫛"): self.config.get(bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ᫜")), bstack1111l1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ᫝"): os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ᫞")), bstack1111l1l_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥ᫟"): self.config.get(bstack1111l1l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᫠"))}
            response = bstack11ll11l1111_opy_.bstack11l1l1l1l1l_opy_(self.bstack11l1l11l1l1_opy_, data)
            if response.get(bstack1111l1l_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ᫡")) == 200:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡴࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ᫢").format(data))
            else:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ᫣").format(response))
        except Exception as e:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ᫤").format(e))
    def bstack11l1l1l11ll_opy_(self):
        if self.bstack11l1l11llll_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l1l1l1lll_opy_, bstack1111l1l_opy_ (u"ࠦࡷࠨ᫥")) as f:
                        bstack11l1l1l1l11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11l1l1l1l11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠣ᫦").format(failed_count))
                if failed_count >= self.bstack11l1l1111l1_opy_:
                    self.logger.info(bstack1111l1l_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ᫧").format(failed_count, self.bstack11l1l1111l1_opy_))
                    self.bstack11l1l1l111l_opy_(failed_count)
                    self.bstack11l1l11lll1_opy_ = True
            return
        try:
            response = bstack11ll11l1111_opy_.bstack11l1l1l11ll_opy_(bstack1111l1l_opy_ (u"ࠢࡼࡿࡂࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࡃࡻࡾࠨࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠽ࡼࡿࠩࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥ࠾ࡽࢀࠦ᫨").format(self.bstack11l1l11l1l1_opy_, self.config.get(bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ᫩")), os.environ.get(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ᫪")), self.config.get(bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ᫫"))))
            if response.get(bstack1111l1l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ᫬")) == 200:
                failed_count = response.get(bstack1111l1l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࡆࡳࡺࡴࡴࠣ᫭"), 0)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣ᫮").format(failed_count))
                if failed_count >= self.bstack11l1l1111l1_opy_:
                    self.logger.info(bstack1111l1l_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢ᫯").format(failed_count, self.bstack11l1l1111l1_opy_))
                    self.bstack11l1l1l111l_opy_(failed_count)
                    self.bstack11l1l11lll1_opy_ = True
            else:
                self.logger.error(bstack1111l1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵ࡬࡭ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧ᫰").format(response))
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶ࡯࡭࡮࡬ࡲ࡬ࡀࠠࡼࡿࠥ᫱").format(e))
    def bstack11l1l1l111l_opy_(self, failed_count):
        with open(self.bstack11l1l111lll_opy_, bstack1111l1l_opy_ (u"ࠥࡻࠧ᫲")) as f:
            f.write(bstack1111l1l_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࡣࡷࠤࢀࢃ࡜࡯ࠤ᫳").format(datetime.now()))
            f.write(bstack1111l1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃ࡜࡯ࠤ᫴").format(failed_count))
        self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡁࡣࡱࡵࡸࠥࡈࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࢃࠢ᫵").format(self.bstack11l1l111lll_opy_))
    def bstack11l1l11l11l_opy_(self):
        def bstack11l1l11l111_opy_():
            while not self.bstack11l1l11lll1_opy_:
                time.sleep(bstack11l1l11ll1l_opy_)
                self.bstack11l1l11l1ll_opy_()
                self.bstack11l1l1l11ll_opy_()
        bstack11l1l111ll1_opy_ = threading.Thread(target=bstack11l1l11l111_opy_, daemon=True)
        bstack11l1l111ll1_opy_.start()