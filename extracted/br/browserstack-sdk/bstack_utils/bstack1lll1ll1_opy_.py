# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l11111l_opy_ import bstack1111l111111_opy_
from bstack_utils.constants import bstack11111ll1111_opy_, bstack11l1l1111_opy_
from bstack_utils.bstack11lll1lll_opy_ import bstack1lll1111ll_opy_
from bstack_utils import logger_utils
bstack1lllllllll1l_opy_ = 10
class bstack111llll1_opy_:
    def __init__(self, bstack111lllll11_opy_, config, bstack1lllllll11ll_opy_=0):
        self.bstack1lllllll1ll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1lllllll1lll_opy_ = bstack1l1111l_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧ⅛").format(bstack11111ll1111_opy_)
        self.bstack1llllllll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣ⅜").format(os.environ.get(bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⅝"))))
        self.bstack1llllllll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ⅞").format(os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⅟"))))
        self.bstack11111111lll_opy_ = 2
        self.bstack111lllll11_opy_ = bstack111lllll11_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11l1l1111_opy_)
        self.bstack1lllllll11ll_opy_ = bstack1lllllll11ll_opy_
        self.bstack111111111ll_opy_ = False
        self.bstack1lllllll1l11_opy_ = not (
                            os.environ.get(bstack1l1111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥⅠ")) and
                            os.environ.get(bstack1l1111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣⅡ")) and
                            os.environ.get(bstack1l1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣⅢ"))
                        )
        if bstack1lll1111ll_opy_.bstack1lllllllll11_opy_(config):
            self.bstack11111111lll_opy_ = bstack1lll1111ll_opy_.bstack111111111l1_opy_(config, self.bstack1lllllll11ll_opy_)
            self.bstack11111111ll1_opy_()
    def bstack1llllllll111_opy_(self):
        return bstack1l1111l_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨⅣ").format(self.config.get(bstack1l1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫⅤ")), os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨⅥ")))
    def bstack1lllllll1l1l_opy_(self):
        try:
            if self.bstack1lllllll1l11_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1llllllll1ll_opy_, bstack1l1111l_opy_ (u"ࠥࡶࠧⅦ")) as f:
                        bstack1llllllllll1_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1llllllllll1_opy_ = set()
                bstack11111111l1l_opy_ = bstack1llllllllll1_opy_ - self.bstack1lllllll1ll1_opy_
                if not bstack11111111l1l_opy_:
                    return
                self.bstack1lllllll1ll1_opy_.update(bstack11111111l1l_opy_)
                data = {bstack1l1111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤⅧ"): list(self.bstack1lllllll1ll1_opy_), bstack1l1111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣⅨ"): self.config.get(bstack1l1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⅩ")), bstack1l1111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧⅪ"): os.environ.get(bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧⅫ")), bstack1l1111l_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢⅬ"): self.config.get(bstack1l1111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨⅭ"))}
            response = bstack1111l111111_opy_.bstack1llllllll1l1_opy_(self.bstack1lllllll1lll_opy_, data)
            if response.get(bstack1l1111l_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦⅮ")) == 200:
                self.logger.debug(bstack1l1111l_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧⅯ").format(data))
            else:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥⅰ").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢⅱ").format(e))
    def bstack11111111l11_opy_(self):
        if self.bstack1lllllll1l11_opy_:
            with self.lock:
                try:
                    with open(self.bstack1llllllll1ll_opy_, bstack1l1111l_opy_ (u"ࠣࡴࠥⅲ")) as f:
                        bstack1111111111l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111111111l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧⅳ").format(failed_count))
                if failed_count >= self.bstack11111111lll_opy_:
                    self.logger.info(bstack1l1111l_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦⅴ").format(failed_count, self.bstack11111111lll_opy_))
                    self.bstack11111111111_opy_(failed_count)
                    self.bstack111111111ll_opy_ = True
            return
        try:
            response = bstack1111l111111_opy_.bstack11111111l11_opy_(bstack1l1111l_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣⅵ").format(self.bstack1lllllll1lll_opy_, self.config.get(bstack1l1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨⅶ")), os.environ.get(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬⅷ")), self.config.get(bstack1l1111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬⅸ"))))
            if response.get(bstack1l1111l_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣⅹ")) == 200:
                failed_count = response.get(bstack1l1111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧⅺ"), 0)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧⅻ").format(failed_count))
                if failed_count >= self.bstack11111111lll_opy_:
                    self.logger.info(bstack1l1111l_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦⅼ").format(failed_count, self.bstack11111111lll_opy_))
                    self.bstack11111111111_opy_(failed_count)
                    self.bstack111111111ll_opy_ = True
            else:
                self.logger.error(bstack1l1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤⅽ").format(response))
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢⅾ").format(e))
    def bstack11111111111_opy_(self, failed_count):
        with open(self.bstack1llllllll11l_opy_, bstack1l1111l_opy_ (u"ࠢࡸࠤⅿ")) as f:
            f.write(bstack1l1111l_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨↀ").format(datetime.now()))
            f.write(bstack1l1111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨↁ").format(failed_count))
        self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦↂ").format(self.bstack1llllllll11l_opy_))
    def bstack11111111ll1_opy_(self):
        def bstack1lllllll11l1_opy_():
            while not self.bstack111111111ll_opy_:
                time.sleep(bstack1lllllllll1l_opy_)
                self.bstack1lllllll1l1l_opy_()
                self.bstack11111111l11_opy_()
        bstack1lllllllllll_opy_ = threading.Thread(target=bstack1lllllll11l1_opy_, daemon=True)
        bstack1lllllllllll_opy_.start()