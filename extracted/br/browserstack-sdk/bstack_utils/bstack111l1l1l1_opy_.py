# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11l111l1111_opy_ import bstack11l1111lll1_opy_
from bstack_utils.constants import bstack111lllll1l1_opy_, bstack111ll1l11_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from bstack_utils import logger_utils
bstack111ll111ll1_opy_ = 10
class bstack1ll11ll1_opy_:
    def __init__(self, bstack1llll1l11_opy_, config, bstack111ll11111l_opy_=0):
        self.bstack111ll1l11l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111ll11ll1l_opy_ = bstack11ll111_opy_ (u"ࠦࢀࢃ࠯ࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡫ࡧࡩ࡭ࡧࡧ࠱ࡹ࡫ࡳࡵࡵࠥᴀ").format(bstack111lllll1l1_opy_)
        self.bstack111l1llllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨᴁ").format(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᴂ"))))
        self.bstack111ll111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨᴃ").format(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᴄ"))))
        self.bstack111ll11lll1_opy_ = 2
        self.bstack1llll1l11_opy_ = bstack1llll1l11_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack111ll1l11_opy_)
        self.bstack111ll11111l_opy_ = bstack111ll11111l_opy_
        self.bstack111ll11l1ll_opy_ = False
        self.bstack111ll1111l1_opy_ = not (
                            os.environ.get(bstack11ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣᴅ")) and
                            os.environ.get(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨᴆ")) and
                            os.environ.get(bstack11ll111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨᴇ"))
                        )
        if bstack1111lll11_opy_.bstack111ll1111ll_opy_(config):
            self.bstack111ll11lll1_opy_ = bstack1111lll11_opy_.bstack111l1lllll1_opy_(config, self.bstack111ll11111l_opy_)
            self.bstack111ll1l111l_opy_()
    def bstack111ll111lll_opy_(self):
        return bstack11ll111_opy_ (u"ࠧࢁࡽࡠࡽࢀࠦᴈ").format(self.config.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᴉ")), os.environ.get(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ᴊ")))
    def bstack111ll1l11ll_opy_(self):
        try:
            if self.bstack111ll1111l1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111ll111111_opy_, bstack11ll111_opy_ (u"ࠣࡴࠥᴋ")) as f:
                        bstack111ll111l11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111ll111l11_opy_ = set()
                bstack111ll1l1111_opy_ = bstack111ll111l11_opy_ - self.bstack111ll1l11l1_opy_
                if not bstack111ll1l1111_opy_:
                    return
                self.bstack111ll1l11l1_opy_.update(bstack111ll1l1111_opy_)
                data = {bstack11ll111_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࠢᴌ"): list(self.bstack111ll1l11l1_opy_), bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨᴍ"): self.config.get(bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᴎ")), bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥᴏ"): os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᴐ")), bstack11ll111_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧᴑ"): self.config.get(bstack11ll111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᴒ"))}
            response = bstack11l1111lll1_opy_.bstack111ll111l1l_opy_(self.bstack111ll11ll1l_opy_, data)
            if response.get(bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤᴓ")) == 200:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡶࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥᴔ").format(data))
            else:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣᴕ").format(response))
        except Exception as e:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧᴖ").format(e))
    def bstack111ll11l111_opy_(self):
        if self.bstack111ll1111l1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111ll111111_opy_, bstack11ll111_opy_ (u"ࠨࡲࠣᴗ")) as f:
                        bstack111ll11l1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111ll11l1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠥᴘ").format(failed_count))
                if failed_count >= self.bstack111ll11lll1_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤᴙ").format(failed_count, self.bstack111ll11lll1_opy_))
                    self.bstack111ll11llll_opy_(failed_count)
                    self.bstack111ll11l1ll_opy_ = True
            return
        try:
            response = bstack11l1111lll1_opy_.bstack111ll11l111_opy_(bstack11ll111_opy_ (u"ࠤࡾࢁࡄࡨࡵࡪ࡮ࡧࡒࡦࡳࡥ࠾ࡽࢀࠪࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࠿ࡾࢁࠫࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࡀࡿࢂࠨᴚ").format(self.bstack111ll11ll1l_opy_, self.config.get(bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᴛ")), os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪᴜ")), self.config.get(bstack11ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᴝ"))))
            if response.get(bstack11ll111_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨᴞ")) == 200:
                failed_count = response.get(bstack11ll111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࡈࡵࡵ࡯ࡶࠥᴟ"), 0)
                self.logger.debug(bstack11ll111_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥᴠ").format(failed_count))
                if failed_count >= self.bstack111ll11lll1_opy_:
                    self.logger.info(bstack11ll111_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤᴡ").format(failed_count, self.bstack111ll11lll1_opy_))
                    self.bstack111ll11llll_opy_(failed_count)
                    self.bstack111ll11l1ll_opy_ = True
            else:
                self.logger.error(bstack11ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡰ࡮࡯ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᴢ").format(response))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠻ࠢࡾࢁࠧᴣ").format(e))
    def bstack111ll11llll_opy_(self, failed_count):
        with open(self.bstack111l1llllll_opy_, bstack11ll111_opy_ (u"ࠧࡽࠢᴤ")) as f:
            f.write(bstack11ll111_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࡥࡹࠦࡻࡾ࡞ࡱࠦᴥ").format(datetime.now()))
            f.write(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾ࡞ࡱࠦᴦ").format(failed_count))
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡃࡥࡳࡷࡺࠠࡃࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡾࠤᴧ").format(self.bstack111l1llllll_opy_))
    def bstack111ll1l111l_opy_(self):
        def bstack111ll11l11l_opy_():
            while not self.bstack111ll11l1ll_opy_:
                time.sleep(bstack111ll111ll1_opy_)
                self.bstack111ll1l11ll_opy_()
                self.bstack111ll11l111_opy_()
        bstack111ll11ll11_opy_ = threading.Thread(target=bstack111ll11l11l_opy_, daemon=True)
        bstack111ll11ll11_opy_.start()