# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l11lllll1_opy_ import bstack11l11lll11l_opy_
from bstack_utils.constants import bstack11l11111lll_opy_, bstack1lllll11_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l1llll1l_opy_
from bstack_utils import bstack111llll1ll_opy_
bstack11l11111111_opy_ = 10
class bstack111lll1l1l_opy_:
    def __init__(self, bstack11l11l11l_opy_, config, bstack111llll1ll1_opy_=0):
        self.bstack111llll1l11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111lllll1l1_opy_ = bstack1l1111_opy_ (u"ࠢࡼࡿ࠲ࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡧࡣ࡬ࡰࡪࡪ࠭ࡵࡧࡶࡸࡸࠨᰇ").format(bstack11l11111lll_opy_)
        self.bstack111llll1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤᰈ").format(os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᰉ"))))
        self.bstack111llllll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤᰊ").format(os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᰋ"))))
        self.bstack111llll11ll_opy_ = 2
        self.bstack11l11l11l_opy_ = bstack11l11l11l_opy_
        self.config = config
        self.logger = bstack111llll1ll_opy_.get_logger(__name__, bstack1lllll11_opy_)
        self.bstack111llll1ll1_opy_ = bstack111llll1ll1_opy_
        self.bstack111llllllll_opy_ = False
        self.bstack111llll1l1l_opy_ = not (
                            os.environ.get(bstack1l1111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦᰌ")) and
                            os.environ.get(bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᰍ")) and
                            os.environ.get(bstack1l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᰎ"))
                        )
        if bstack1l1llll1l_opy_.bstack111lll1llll_opy_(config):
            self.bstack111llll11ll_opy_ = bstack1l1llll1l_opy_.bstack111lllll111_opy_(config, self.bstack111llll1ll1_opy_)
            self.bstack111llll1111_opy_()
    def bstack111lllllll1_opy_(self):
        return bstack1l1111_opy_ (u"ࠣࡽࢀࡣࢀࢃࠢᰏ").format(self.config.get(bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᰐ")), os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᰑ")))
    def bstack11l111111l1_opy_(self):
        try:
            if self.bstack111llll1l1l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111llllll11_opy_, bstack1l1111_opy_ (u"ࠦࡷࠨᰒ")) as f:
                        bstack111lll1lll1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111lll1lll1_opy_ = set()
                bstack111lllll1ll_opy_ = bstack111lll1lll1_opy_ - self.bstack111llll1l11_opy_
                if not bstack111lllll1ll_opy_:
                    return
                self.bstack111llll1l11_opy_.update(bstack111lllll1ll_opy_)
                data = {bstack1l1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࠥᰓ"): list(self.bstack111llll1l11_opy_), bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤᰔ"): self.config.get(bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᰕ")), bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨᰖ"): os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᰗ")), bstack1l1111_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣᰘ"): self.config.get(bstack1l1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᰙ"))}
            response = bstack11l11lll11l_opy_.bstack111llllll1l_opy_(self.bstack111lllll1l1_opy_, data)
            if response.get(bstack1l1111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᰚ")) == 200:
                self.logger.debug(bstack1l1111_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡹࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᰛ").format(data))
            else:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᰜ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᰝ").format(e))
    def bstack11l111111ll_opy_(self):
        if self.bstack111llll1l1l_opy_:
            with self.lock:
                try:
                    with open(self.bstack111llllll11_opy_, bstack1l1111_opy_ (u"ࠤࡵࠦᰞ")) as f:
                        bstack111llll111l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111llll111l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1111_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠨᰟ").format(failed_count))
                if failed_count >= self.bstack111llll11ll_opy_:
                    self.logger.info(bstack1l1111_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᰠ").format(failed_count, self.bstack111llll11ll_opy_))
                    self.bstack111lllll11l_opy_(failed_count)
                    self.bstack111llllllll_opy_ = True
            return
        try:
            response = bstack11l11lll11l_opy_.bstack11l111111ll_opy_(bstack1l1111_opy_ (u"ࠧࢁࡽࡀࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࡁࢀࢃࠦࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࡂࢁࡽࠧࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࡃࡻࡾࠤᰡ").format(self.bstack111lllll1l1_opy_, self.config.get(bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᰢ")), os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᰣ")), self.config.get(bstack1l1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᰤ"))))
            if response.get(bstack1l1111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᰥ")) == 200:
                failed_count = response.get(bstack1l1111_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࡄࡱࡸࡲࡹࠨᰦ"), 0)
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨᰧ").format(failed_count))
                if failed_count >= self.bstack111llll11ll_opy_:
                    self.logger.info(bstack1l1111_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᰨ").format(failed_count, self.bstack111llll11ll_opy_))
                    self.bstack111lllll11l_opy_(failed_count)
                    self.bstack111llllllll_opy_ = True
            else:
                self.logger.error(bstack1l1111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡳࡱࡲࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᰩ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡴࡲ࡬ࡪࡰࡪ࠾ࠥࢁࡽࠣᰪ").format(e))
    def bstack111lllll11l_opy_(self, failed_count):
        with open(self.bstack111llll1lll_opy_, bstack1l1111_opy_ (u"ࠣࡹࠥᰫ")) as f:
            f.write(bstack1l1111_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࡡࡵࠢࡾࢁࡡࡴࠢᰬ").format(datetime.now()))
            f.write(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࡡࡴࠢᰭ").format(failed_count))
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡆࡨ࡯ࡳࡶࠣࡆࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࢁࠧᰮ").format(self.bstack111llll1lll_opy_))
    def bstack111llll1111_opy_(self):
        def bstack111llll11l1_opy_():
            while not self.bstack111llllllll_opy_:
                time.sleep(bstack11l11111111_opy_)
                self.bstack11l111111l1_opy_()
                self.bstack11l111111ll_opy_()
        bstack11l1111111l_opy_ = threading.Thread(target=bstack111llll11l1_opy_, daemon=True)
        bstack11l1111111l_opy_.start()