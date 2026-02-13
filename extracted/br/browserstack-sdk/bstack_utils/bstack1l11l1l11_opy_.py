# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111llllll1l_opy_ import bstack111lllll1ll_opy_
from bstack_utils.constants import bstack111ll111lll_opy_, bstack11ll111l_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils import logger_utils
bstack111l1l1llll_opy_ = 10
class bstack1ll11l111_opy_:
    def __init__(self, bstack1l1l1l111l_opy_, config, bstack111l1ll11l1_opy_=0):
        self.bstack111l1lll11l_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l1lll1ll_opy_ = bstack11l11_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤ᳸").format(bstack111ll111lll_opy_)
        self.bstack111l1lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ᳹").format(os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᳺ"))))
        self.bstack111l1lll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ᳻").format(os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᳼"))))
        self.bstack111l1ll1l1l_opy_ = 2
        self.bstack1l1l1l111l_opy_ = bstack1l1l1l111l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11ll111l_opy_)
        self.bstack111l1ll11l1_opy_ = bstack111l1ll11l1_opy_
        self.bstack111l1llll1l_opy_ = False
        self.bstack111ll1111l1_opy_ = not (
                            os.environ.get(bstack11l11_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ᳽")) and
                            os.environ.get(bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ᳾")) and
                            os.environ.get(bstack11l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ᳿"))
                        )
        if bstack1l11l1l1ll_opy_.bstack111l1ll11ll_opy_(config):
            self.bstack111l1ll1l1l_opy_ = bstack1l11l1l1ll_opy_.bstack111l1ll111l_opy_(config, self.bstack111l1ll11l1_opy_)
            self.bstack111l1ll1lll_opy_()
    def bstack111l1ll1l11_opy_(self):
        return bstack11l11_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥᴀ").format(self.config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᴁ")), os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬᴂ")))
    def bstack111ll11111l_opy_(self):
        try:
            if self.bstack111ll1111l1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l1lll1l1_opy_, bstack11l11_opy_ (u"ࠢࡳࠤᴃ")) as f:
                        bstack111ll1111ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111ll1111ll_opy_ = set()
                bstack111l1lll111_opy_ = bstack111ll1111ll_opy_ - self.bstack111l1lll11l_opy_
                if not bstack111l1lll111_opy_:
                    return
                self.bstack111l1lll11l_opy_.update(bstack111l1lll111_opy_)
                data = {bstack11l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨᴄ"): list(self.bstack111l1lll11l_opy_), bstack11l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧᴅ"): self.config.get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᴆ")), bstack11l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤᴇ"): os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᴈ")), bstack11l11_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦᴉ"): self.config.get(bstack11l11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᴊ"))}
            response = bstack111lllll1ll_opy_.bstack111ll111l11_opy_(self.bstack111l1lll1ll_opy_, data)
            if response.get(bstack11l11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᴋ")) == 200:
                self.logger.debug(bstack11l11_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤᴌ").format(data))
            else:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢᴍ").format(response))
        except Exception as e:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦᴎ").format(e))
    def bstack111l1ll1ll1_opy_(self):
        if self.bstack111ll1111l1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l1lll1l1_opy_, bstack11l11_opy_ (u"ࠧࡸࠢᴏ")) as f:
                        bstack111l1llllll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111l1llllll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤᴐ").format(failed_count))
                if failed_count >= self.bstack111l1ll1l1l_opy_:
                    self.logger.info(bstack11l11_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣᴑ").format(failed_count, self.bstack111l1ll1l1l_opy_))
                    self.bstack111l1llll11_opy_(failed_count)
                    self.bstack111l1llll1l_opy_ = True
            return
        try:
            response = bstack111lllll1ll_opy_.bstack111l1ll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧᴒ").format(self.bstack111l1lll1ll_opy_, self.config.get(bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᴓ")), os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᴔ")), self.config.get(bstack11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᴕ"))))
            if response.get(bstack11l11_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧᴖ")) == 200:
                failed_count = response.get(bstack11l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤᴗ"), 0)
                self.logger.debug(bstack11l11_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤᴘ").format(failed_count))
                if failed_count >= self.bstack111l1ll1l1l_opy_:
                    self.logger.info(bstack11l11_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣᴙ").format(failed_count, self.bstack111l1ll1l1l_opy_))
                    self.bstack111l1llll11_opy_(failed_count)
                    self.bstack111l1llll1l_opy_ = True
            else:
                self.logger.error(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨᴚ").format(response))
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦᴛ").format(e))
    def bstack111l1llll11_opy_(self, failed_count):
        with open(self.bstack111l1lllll1_opy_, bstack11l11_opy_ (u"ࠦࡼࠨᴜ")) as f:
            f.write(bstack11l11_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥᴝ").format(datetime.now()))
            f.write(bstack11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥᴞ").format(failed_count))
        self.logger.debug(bstack11l11_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣᴟ").format(self.bstack111l1lllll1_opy_))
    def bstack111l1ll1lll_opy_(self):
        def bstack111ll111111_opy_():
            while not self.bstack111l1llll1l_opy_:
                time.sleep(bstack111l1l1llll_opy_)
                self.bstack111ll11111l_opy_()
                self.bstack111l1ll1ll1_opy_()
        bstack111l1ll1111_opy_ = threading.Thread(target=bstack111ll111111_opy_, daemon=True)
        bstack111l1ll1111_opy_.start()