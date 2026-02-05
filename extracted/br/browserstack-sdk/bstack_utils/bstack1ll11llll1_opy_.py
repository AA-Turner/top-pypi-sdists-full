# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l11ll1l1l_opy_ import bstack11l11lll1l1_opy_
from bstack_utils.constants import bstack11l1111ll1l_opy_, bstack1l1ll1l11_opy_
from bstack_utils.bstack1l1ll1l111_opy_ import bstack11111l1l_opy_
from bstack_utils import bstack1l1111l1l_opy_
bstack111llllll1l_opy_ = 10
class bstack1111111l1_opy_:
    def __init__(self, bstack11ll1lllll_opy_, config, bstack111llllllll_opy_=0):
        self.bstack111llll1111_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111lllll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧᰍ").format(bstack11l1111ll1l_opy_)
        self.bstack111lllll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣᰎ").format(os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᰏ"))))
        self.bstack11l11111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣᰐ").format(os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰑ"))))
        self.bstack111lllllll1_opy_ = 2
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self.config = config
        self.logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack1l1ll1l11_opy_)
        self.bstack111llllllll_opy_ = bstack111llllllll_opy_
        self.bstack111lll1lll1_opy_ = False
        self.bstack111lll1llll_opy_ = not (
                            os.environ.get(bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥᰒ")) and
                            os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣᰓ")) and
                            os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣᰔ"))
                        )
        if bstack11111l1l_opy_.bstack111lll1ll11_opy_(config):
            self.bstack111lllllll1_opy_ = bstack11111l1l_opy_.bstack111lllll11l_opy_(config, self.bstack111llllllll_opy_)
            self.bstack111llll1ll1_opy_()
    def bstack111lllll111_opy_(self):
        return bstack11l1ll1_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨᰕ").format(self.config.get(bstack11l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰖ")), os.environ.get(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᰗ")))
    def bstack111lll1l1ll_opy_(self):
        try:
            if self.bstack111lll1llll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11l11111111_opy_, bstack11l1ll1_opy_ (u"ࠥࡶࠧᰘ")) as f:
                        bstack111llll11ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111llll11ll_opy_ = set()
                bstack111llll11l1_opy_ = bstack111llll11ll_opy_ - self.bstack111llll1111_opy_
                if not bstack111llll11l1_opy_:
                    return
                self.bstack111llll1111_opy_.update(bstack111llll11l1_opy_)
                data = {bstack11l1ll1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤᰙ"): list(self.bstack111llll1111_opy_), bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣᰚ"): self.config.get(bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᰛ")), bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧᰜ"): os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᰝ")), bstack11l1ll1_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢᰞ"): self.config.get(bstack11l1ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᰟ"))}
            response = bstack11l11lll1l1_opy_.bstack111llll1l1l_opy_(self.bstack111lllll1l1_opy_, data)
            if response.get(bstack11l1ll1_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦᰠ")) == 200:
                self.logger.debug(bstack11l1ll1_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᰡ").format(data))
            else:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᰢ").format(response))
        except Exception as e:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᰣ").format(e))
    def bstack111llll1l11_opy_(self):
        if self.bstack111lll1llll_opy_:
            with self.lock:
                try:
                    with open(self.bstack11l11111111_opy_, bstack11l1ll1_opy_ (u"ࠣࡴࠥᰤ")) as f:
                        bstack111lll1ll1l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111lll1ll1l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧᰥ").format(failed_count))
                if failed_count >= self.bstack111lllllll1_opy_:
                    self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᰦ").format(failed_count, self.bstack111lllllll1_opy_))
                    self.bstack111llll1lll_opy_(failed_count)
                    self.bstack111lll1lll1_opy_ = True
            return
        try:
            response = bstack11l11lll1l1_opy_.bstack111llll1l11_opy_(bstack11l1ll1_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣᰧ").format(self.bstack111lllll1l1_opy_, self.config.get(bstack11l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᰨ")), os.environ.get(bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᰩ")), self.config.get(bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᰪ"))))
            if response.get(bstack11l1ll1_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᰫ")) == 200:
                failed_count = response.get(bstack11l1ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧᰬ"), 0)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧᰭ").format(failed_count))
                if failed_count >= self.bstack111lllllll1_opy_:
                    self.logger.info(bstack11l1ll1_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦᰮ").format(failed_count, self.bstack111lllllll1_opy_))
                    self.bstack111llll1lll_opy_(failed_count)
                    self.bstack111lll1lll1_opy_ = True
            else:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᰯ").format(response))
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢᰰ").format(e))
    def bstack111llll1lll_opy_(self, failed_count):
        with open(self.bstack111lllll1ll_opy_, bstack11l1ll1_opy_ (u"ࠢࡸࠤᰱ")) as f:
            f.write(bstack11l1ll1_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨᰲ").format(datetime.now()))
            f.write(bstack11l1ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨᰳ").format(failed_count))
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦᰴ").format(self.bstack111lllll1ll_opy_))
    def bstack111llll1ll1_opy_(self):
        def bstack111llll111l_opy_():
            while not self.bstack111lll1lll1_opy_:
                time.sleep(bstack111llllll1l_opy_)
                self.bstack111lll1l1ll_opy_()
                self.bstack111llll1l11_opy_()
        bstack111llllll11_opy_ = threading.Thread(target=bstack111llll111l_opy_, daemon=True)
        bstack111llllll11_opy_.start()