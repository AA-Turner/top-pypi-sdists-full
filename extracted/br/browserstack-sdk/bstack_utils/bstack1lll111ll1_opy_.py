# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l1111ll1l_opy_ import bstack11l1111l1ll_opy_
from bstack_utils.constants import bstack111ll1lllll_opy_, bstack1llllll1l_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from bstack_utils import logger_utils
bstack111ll11ll1l_opy_ = 10
class bstack111ll1111_opy_:
    def __init__(self, bstack1l111ll11l_opy_, config, bstack111ll11llll_opy_=0):
        self.bstack111ll1111l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111ll11l111_opy_ = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠲ࡸࡪࡹࡴࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴ࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࡧࡣ࡬ࡰࡪࡪ࠭ࡵࡧࡶࡸࡸࠨᴃ").format(bstack111ll1lllll_opy_)
        self.bstack111ll1l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠣࡣࡥࡳࡷࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡻࡾࠤᴄ").format(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᴅ"))))
        self.bstack111ll1l1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡾࢁ࠳ࡺࡸࡵࠤᴆ").format(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᴇ"))))
        self.bstack111ll1l11l1_opy_ = 2
        self.bstack1l111ll11l_opy_ = bstack1l111ll11l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1llllll1l_opy_)
        self.bstack111ll11llll_opy_ = bstack111ll11llll_opy_
        self.bstack111ll11l11l_opy_ = False
        self.bstack111l1llllll_opy_ = not (
                            os.environ.get(bstack11l1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠦᴈ")) and
                            os.environ.get(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡔࡏࡅࡇࡢࡍࡓࡊࡅ࡙ࠤᴉ")) and
                            os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡐࡖࡄࡐࡤࡔࡏࡅࡇࡢࡇࡔ࡛ࡎࡕࠤᴊ"))
                        )
        if bstack1l1l11l11l_opy_.bstack111ll111l1l_opy_(config):
            self.bstack111ll1l11l1_opy_ = bstack1l1l11l11l_opy_.bstack111ll11l1l1_opy_(config, self.bstack111ll11llll_opy_)
            self.bstack111ll111ll1_opy_()
    def bstack111ll11l1ll_opy_(self):
        return bstack11l1l11_opy_ (u"ࠣࡽࢀࡣࢀࢃࠢᴋ").format(self.config.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᴌ")), os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᴍ")))
    def bstack111ll11lll1_opy_(self):
        try:
            if self.bstack111l1llllll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111ll1l1l11_opy_, bstack11l1l11_opy_ (u"ࠦࡷࠨᴎ")) as f:
                        bstack111ll11111l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111ll11111l_opy_ = set()
                bstack111ll111lll_opy_ = bstack111ll11111l_opy_ - self.bstack111ll1111l1_opy_
                if not bstack111ll111lll_opy_:
                    return
                self.bstack111ll1111l1_opy_.update(bstack111ll111lll_opy_)
                data = {bstack11l1l11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࠥᴏ"): list(self.bstack111ll1111l1_opy_), bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠤᴐ"): self.config.get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᴑ")), bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࠨᴒ"): os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨᴓ")), bstack11l1l11_opy_ (u"ࠥࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠣᴔ"): self.config.get(bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᴕ"))}
            response = bstack11l1111l1ll_opy_.bstack111ll111111_opy_(self.bstack111ll11l111_opy_, data)
            if response.get(bstack11l1l11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᴖ")) == 200:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥࡹࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᴗ").format(data))
            else:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡴࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᴘ").format(response))
        except Exception as e:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᴙ").format(e))
    def bstack111ll1l111l_opy_(self):
        if self.bstack111l1llllll_opy_:
            with self.lock:
                try:
                    with open(self.bstack111ll1l1l11_opy_, bstack11l1l11_opy_ (u"ࠤࡵࠦᴚ")) as f:
                        bstack111ll11ll11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111ll11ll11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠨᴛ").format(failed_count))
                if failed_count >= self.bstack111ll1l11l1_opy_:
                    self.logger.info(bstack11l1l11_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࠪ࡯ࡳࡨࡧ࡬ࠪ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᴜ").format(failed_count, self.bstack111ll1l11l1_opy_))
                    self.bstack111ll1111ll_opy_(failed_count)
                    self.bstack111ll11l11l_opy_ = True
            return
        try:
            response = bstack11l1111l1ll_opy_.bstack111ll1l111l_opy_(bstack11l1l11_opy_ (u"ࠧࢁࡽࡀࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࡁࢀࢃࠦࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࡂࢁࡽࠧࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࡃࡻࡾࠤᴝ").format(self.bstack111ll11l111_opy_, self.config.get(bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᴞ")), os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᴟ")), self.config.get(bstack11l1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᴠ"))))
            if response.get(bstack11l1l11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᴡ")) == 200:
                failed_count = response.get(bstack11l1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࡄࡱࡸࡲࡹࠨᴢ"), 0)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࠨᴣ").format(failed_count))
                if failed_count >= self.bstack111ll1l11l1_opy_:
                    self.logger.info(bstack11l1l11_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥ࠼ࠣࡿࢂࠦ࠾࠾ࠢࡾࢁࠧᴤ").format(failed_count, self.bstack111ll1l11l1_opy_))
                    self.bstack111ll1111ll_opy_(failed_count)
                    self.bstack111ll11l11l_opy_ = True
            else:
                self.logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡳࡱࡲࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᴥ").format(response))
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡴࡴࡲ࡬ࡪࡰࡪ࠾ࠥࢁࡽࠣᴦ").format(e))
    def bstack111ll1111ll_opy_(self, failed_count):
        with open(self.bstack111ll1l11ll_opy_, bstack11l1l11_opy_ (u"ࠣࡹࠥᴧ")) as f:
            f.write(bstack11l1l11_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࡡࡵࠢࡾࢁࡡࡴࠢᴨ").format(datetime.now()))
            f.write(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࡡࡴࠢᴩ").format(failed_count))
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡆࡨ࡯ࡳࡶࠣࡆࡺ࡯࡬ࡥࠢࡩ࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࢁࠧᴪ").format(self.bstack111ll1l11ll_opy_))
    def bstack111ll111ll1_opy_(self):
        def bstack111ll1l1111_opy_():
            while not self.bstack111ll11l11l_opy_:
                time.sleep(bstack111ll11ll1l_opy_)
                self.bstack111ll11lll1_opy_()
                self.bstack111ll1l111l_opy_()
        bstack111ll111l11_opy_ = threading.Thread(target=bstack111ll1l1111_opy_, daemon=True)
        bstack111ll111l11_opy_.start()