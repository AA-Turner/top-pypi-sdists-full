# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l111l11_opy_ import bstack1111l111l1l_opy_
from bstack_utils.constants import bstack111111llll1_opy_, bstack1l1lllll1l_opy_
from bstack_utils.bstack1111l11l_opy_ import bstack1l1l111111_opy_
from bstack_utils import logger_utils
bstack1lllllllll1l_opy_ = 10
class bstack1llll11l1_opy_:
    def __init__(self, bstack1l11l1111l_opy_, config, bstack1lllllllllll_opy_=0):
        self.bstack1llllllll1ll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1lllllll1l1l_opy_ = bstack1l111l_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧ⅔").format(bstack111111llll1_opy_)
        self.bstack11111111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣ⅕").format(os.environ.get(bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⅖"))))
        self.bstack1111111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ⅗").format(os.environ.get(bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⅘"))))
        self.bstack1lllllll1lll_opy_ = 2
        self.bstack1l11l1111l_opy_ = bstack1l11l1111l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l1lllll1l_opy_)
        self.bstack1lllllllllll_opy_ = bstack1lllllllllll_opy_
        self.bstack1111111111l_opy_ = False
        self.bstack11111111lll_opy_ = not (
                            os.environ.get(bstack1l111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥ⅙")) and
                            os.environ.get(bstack1l111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣ⅚")) and
                            os.environ.get(bstack1l111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣ⅛"))
                        )
        if bstack1l1l111111_opy_.bstack1llllllll11l_opy_(config):
            self.bstack1lllllll1lll_opy_ = bstack1l1l111111_opy_.bstack11111111ll1_opy_(config, self.bstack1lllllllllll_opy_)
            self.bstack111111111ll_opy_()
    def bstack1lllllll1ll1_opy_(self):
        return bstack1l111l_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨ⅜").format(self.config.get(bstack1l111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⅝")), os.environ.get(bstack1l111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⅞")))
    def bstack11111111111_opy_(self):
        try:
            if self.bstack11111111lll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111111l111_opy_, bstack1l111l_opy_ (u"ࠥࡶࠧ⅟")) as f:
                        bstack1llllllll1l1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1llllllll1l1_opy_ = set()
                bstack1111111l11l_opy_ = bstack1llllllll1l1_opy_ - self.bstack1llllllll1ll_opy_
                if not bstack1111111l11l_opy_:
                    return
                self.bstack1llllllll1ll_opy_.update(bstack1111111l11l_opy_)
                data = {bstack1l111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤⅠ"): list(self.bstack1llllllll1ll_opy_), bstack1l111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣⅡ"): self.config.get(bstack1l111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⅢ")), bstack1l111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧⅣ"): os.environ.get(bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧⅤ")), bstack1l111l_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢⅥ"): self.config.get(bstack1l111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⅦ"))}
            response = bstack1111l111l1l_opy_.bstack1lllllllll11_opy_(self.bstack1lllllll1l1l_opy_, data)
            if response.get(bstack1l111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦⅧ")) == 200:
                self.logger.debug(bstack1l111l_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧⅨ").format(data))
            else:
                self.logger.debug(bstack1l111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥⅩ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢⅪ").format(e))
    def bstack1llllllllll1_opy_(self):
        if self.bstack11111111lll_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111111l111_opy_, bstack1l111l_opy_ (u"ࠣࡴࠥⅫ")) as f:
                        bstack11111111l11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack11111111l11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l111l_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧⅬ").format(failed_count))
                if failed_count >= self.bstack1lllllll1lll_opy_:
                    self.logger.info(bstack1l111l_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦⅭ").format(failed_count, self.bstack1lllllll1lll_opy_))
                    self.bstack1llllllll111_opy_(failed_count)
                    self.bstack1111111111l_opy_ = True
            return
        try:
            response = bstack1111l111l1l_opy_.bstack1llllllllll1_opy_(bstack1l111l_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣⅮ").format(self.bstack1lllllll1l1l_opy_, self.config.get(bstack1l111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨⅯ")), os.environ.get(bstack1l111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬⅰ")), self.config.get(bstack1l111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬⅱ"))))
            if response.get(bstack1l111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣⅲ")) == 200:
                failed_count = response.get(bstack1l111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧⅳ"), 0)
                self.logger.debug(bstack1l111l_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧⅴ").format(failed_count))
                if failed_count >= self.bstack1lllllll1lll_opy_:
                    self.logger.info(bstack1l111l_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦⅵ").format(failed_count, self.bstack1lllllll1lll_opy_))
                    self.bstack1llllllll111_opy_(failed_count)
                    self.bstack1111111111l_opy_ = True
            else:
                self.logger.error(bstack1l111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤⅶ").format(response))
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢⅷ").format(e))
    def bstack1llllllll111_opy_(self, failed_count):
        with open(self.bstack11111111l1l_opy_, bstack1l111l_opy_ (u"ࠢࡸࠤⅸ")) as f:
            f.write(bstack1l111l_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨⅹ").format(datetime.now()))
            f.write(bstack1l111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨⅺ").format(failed_count))
        self.logger.debug(bstack1l111l_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦⅻ").format(self.bstack11111111l1l_opy_))
    def bstack111111111ll_opy_(self):
        def bstack1lllllll1l11_opy_():
            while not self.bstack1111111111l_opy_:
                time.sleep(bstack1lllllllll1l_opy_)
                self.bstack11111111111_opy_()
                self.bstack1llllllllll1_opy_()
        bstack111111111l1_opy_ = threading.Thread(target=bstack1lllllll1l11_opy_, daemon=True)
        bstack111111111l1_opy_.start()