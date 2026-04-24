# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l111l1l_opy_ import bstack1111l1111ll_opy_
from bstack_utils.constants import bstack1111111ll11_opy_, bstack1111ll1111_opy_
from bstack_utils.bstack111l11lll_opy_ import bstack1l1111ll11_opy_
from bstack_utils import logger_utils
bstack1lllllllllll_opy_ = 10
class bstack11l1llll11_opy_:
    def __init__(self, bstack1l1lll1l1l_opy_, config, bstack11111111l11_opy_=0):
        self.bstack111111111ll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111111111l1_opy_ = bstack111ll11_opy_ (u"ࠦࢀࢃ࠯ࡵࡧࡶࡸࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱ࠳ࡦࡶࡩ࠰ࡸ࠴࠳࡫ࡧࡩ࡭ࡧࡧ࠱ࡹ࡫ࡳࡵࡵࠥ⅙").format(bstack1111111ll11_opy_)
        self.bstack11111111111_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠧࡧࡢࡰࡴࡷࡣࡧࡻࡩ࡭ࡦࡢࡿࢂࠨ⅚").format(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⅛"))))
        self.bstack11111111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡻࡾ࠰ࡷࡼࡹࠨ⅜").format(os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⅝"))))
        self.bstack1lllllll1lll_opy_ = 2
        self.bstack1l1lll1l1l_opy_ = bstack1l1lll1l1l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1111ll1111_opy_)
        self.bstack11111111l11_opy_ = bstack11111111l11_opy_
        self.bstack1llllllllll1_opy_ = False
        self.bstack1llllllll1l1_opy_ = not (
                            os.environ.get(bstack111ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠣ⅞")) and
                            os.environ.get(bstack111ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡑࡓࡉࡋ࡟ࡊࡐࡇࡉ࡝ࠨ⅟")) and
                            os.environ.get(bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡔ࡚ࡁࡍࡡࡑࡓࡉࡋ࡟ࡄࡑࡘࡒ࡙ࠨⅠ"))
                        )
        if bstack1l1111ll11_opy_.bstack11111111ll1_opy_(config):
            self.bstack1lllllll1lll_opy_ = bstack1l1111ll11_opy_.bstack1llllllll1ll_opy_(config, self.bstack11111111l11_opy_)
            self.bstack1llllllll111_opy_()
    def bstack11111111lll_opy_(self):
        return bstack111ll11_opy_ (u"ࠧࢁࡽࡠࡽࢀࠦⅡ").format(self.config.get(bstack111ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⅢ")), os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭Ⅳ")))
    def bstack1lllllllll11_opy_(self):
        try:
            if self.bstack1llllllll1l1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack11111111l1l_opy_, bstack111ll11_opy_ (u"ࠣࡴࠥⅤ")) as f:
                        bstack1111111l111_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111111l111_opy_ = set()
                bstack1lllllll1l1l_opy_ = bstack1111111l111_opy_ - self.bstack111111111ll_opy_
                if not bstack1lllllll1l1l_opy_:
                    return
                self.bstack111111111ll_opy_.update(bstack1lllllll1l1l_opy_)
                data = {bstack111ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࠢⅥ"): list(self.bstack111111111ll_opy_), bstack111ll11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࠨⅦ"): self.config.get(bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧⅧ")), bstack111ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥⅨ"): os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬⅩ")), bstack111ll11_opy_ (u"ࠢࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠧⅪ"): self.config.get(bstack111ll11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭Ⅻ"))}
            response = bstack1111l1111ll_opy_.bstack1111111l11l_opy_(self.bstack111111111l1_opy_, data)
            if response.get(bstack111ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤⅬ")) == 200:
                self.logger.debug(bstack111ll11_opy_ (u"ࠥࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡶࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥⅭ").format(data))
            else:
                self.logger.debug(bstack111ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡱࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣⅮ").format(response))
        except Exception as e:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧⅯ").format(e))
    def bstack1lllllll1ll1_opy_(self):
        if self.bstack1llllllll1l1_opy_:
            with self.lock:
                try:
                    with open(self.bstack11111111l1l_opy_, bstack111ll11_opy_ (u"ࠨࡲࠣⅰ")) as f:
                        bstack1llllllll11l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1llllllll11l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠥⅱ").format(failed_count))
                if failed_count >= self.bstack1lllllll1lll_opy_:
                    self.logger.info(bstack111ll11_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥ࠮࡬ࡰࡥࡤࡰ࠮ࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤⅲ").format(failed_count, self.bstack1lllllll1lll_opy_))
                    self.bstack1lllllllll1l_opy_(failed_count)
                    self.bstack1llllllllll1_opy_ = True
            return
        try:
            response = bstack1111l1111ll_opy_.bstack1lllllll1ll1_opy_(bstack111ll11_opy_ (u"ࠤࡾࢁࡄࡨࡵࡪ࡮ࡧࡒࡦࡳࡥ࠾ࡽࢀࠪࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࠿ࡾࢁࠫࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࡀࡿࢂࠨⅳ").format(self.bstack111111111l1_opy_, self.config.get(bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ⅴ")), os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪⅵ")), self.config.get(bstack111ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪⅶ"))))
            if response.get(bstack111ll11_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨⅷ")) == 200:
                failed_count = response.get(bstack111ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࡈࡵࡵ࡯ࡶࠥⅸ"), 0)
                self.logger.debug(bstack111ll11_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿࠥⅹ").format(failed_count))
                if failed_count >= self.bstack1lllllll1lll_opy_:
                    self.logger.info(bstack111ll11_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࡀࠠࡼࡿࠣࡂࡂࠦࡻࡾࠤⅺ").format(failed_count, self.bstack1lllllll1lll_opy_))
                    self.bstack1lllllllll1l_opy_(failed_count)
                    self.bstack1llllllllll1_opy_ = True
            else:
                self.logger.error(bstack111ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡰ࡮࡯ࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢⅻ").format(response))
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡱࡱ࡯ࡰ࡮ࡴࡧ࠻ࠢࡾࢁࠧⅼ").format(e))
    def bstack1lllllllll1l_opy_(self, failed_count):
        with open(self.bstack11111111111_opy_, bstack111ll11_opy_ (u"ࠧࡽࠢⅽ")) as f:
            f.write(bstack111ll11_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࡥࡹࠦࡻࡾ࡞ࡱࠦⅾ").format(datetime.now()))
            f.write(bstack111ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾ࡞ࡱࠦⅿ").format(failed_count))
        self.logger.debug(bstack111ll11_opy_ (u"ࠣࡃࡥࡳࡷࡺࠠࡃࡷ࡬ࡰࡩࠦࡦࡪ࡮ࡨࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡾࠤↀ").format(self.bstack11111111111_opy_))
    def bstack1llllllll111_opy_(self):
        def bstack1111111111l_opy_():
            while not self.bstack1llllllllll1_opy_:
                time.sleep(bstack1lllllllllll_opy_)
                self.bstack1lllllllll11_opy_()
                self.bstack1lllllll1ll1_opy_()
        bstack1lllllll1l11_opy_ = threading.Thread(target=bstack1111111111l_opy_, daemon=True)
        bstack1lllllll1l11_opy_.start()