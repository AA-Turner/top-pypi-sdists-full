# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l11l1l1_opy_ import bstack1111l11l1ll_opy_
from bstack_utils.constants import bstack11111l1llll_opy_, bstack11111l1l11_opy_
from bstack_utils.bstack1l1lll1l11_opy_ import bstack1ll11l11l1_opy_
from bstack_utils import logger_utils
bstack111111l1111_opy_ = 10
class bstack1l1l11l111_opy_:
    def __init__(self, bstack111l11lll1_opy_, config, bstack1111111llll_opy_=0):
        self.bstack111111111l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1lllllllll11_opy_ = bstack11ll11_opy_ (u"ࠨࡻࡾ࠱ࡷࡩࡸࡺ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࡦࡢ࡫࡯ࡩࡩ࠳ࡴࡦࡵࡷࡷࠧℸ").format(bstack11111l1llll_opy_)
        self.bstack1111111l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠢࡢࡤࡲࡶࡹࡥࡢࡶ࡫࡯ࡨࡤࢁࡽࠣℹ").format(os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭℺"))))
        self.bstack1111111l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡽࢀ࠲ࡹࡾࡴࠣ℻").format(os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨℼ"))))
        self.bstack1111111ll11_opy_ = 2
        self.bstack111l11lll1_opy_ = bstack111l11lll1_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11111l1l11_opy_)
        self.bstack1111111llll_opy_ = bstack1111111llll_opy_
        self.bstack11111111l11_opy_ = False
        self.bstack1111111ll1l_opy_ = not (
                            os.environ.get(bstack11ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠥℽ")) and
                            os.environ.get(bstack11ll11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡓࡕࡄࡆࡡࡌࡒࡉࡋࡘࠣℾ")) and
                            os.environ.get(bstack11ll11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡏࡕࡃࡏࡣࡓࡕࡄࡆࡡࡆࡓ࡚ࡔࡔࠣℿ"))
                        )
        if bstack1ll11l11l1_opy_.bstack1llllllllll1_opy_(config):
            self.bstack1111111ll11_opy_ = bstack1ll11l11l1_opy_.bstack11111111l1l_opy_(config, self.bstack1111111llll_opy_)
            self.bstack1lllllllllll_opy_()
    def bstack11111111111_opy_(self):
        return bstack11ll11_opy_ (u"ࠢࡼࡿࡢࡿࢂࠨ⅀").format(self.config.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⅁")), os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⅂")))
    def bstack1111111lll1_opy_(self):
        try:
            if self.bstack1111111ll1l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1111111l1ll_opy_, bstack11ll11_opy_ (u"ࠥࡶࠧ⅃")) as f:
                        bstack1111111l11l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111111l11l_opy_ = set()
                bstack1llllllll1ll_opy_ = bstack1111111l11l_opy_ - self.bstack111111111l1_opy_
                if not bstack1llllllll1ll_opy_:
                    return
                self.bstack111111111l1_opy_.update(bstack1llllllll1ll_opy_)
                data = {bstack11ll11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࠤ⅄"): list(self.bstack111111111l1_opy_), bstack11ll11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠣⅅ"): self.config.get(bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩⅆ")), bstack11ll11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡘࡵ࡯ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧⅇ"): os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧⅈ")), bstack11ll11_opy_ (u"ࠤࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠢⅉ"): self.config.get(bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⅊"))}
            response = bstack1111l11l1ll_opy_.bstack11111111ll1_opy_(self.bstack1lllllllll11_opy_, data)
            if response.get(bstack11ll11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦ⅋")) == 200:
                self.logger.debug(bstack11ll11_opy_ (u"࡙ࠧࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭࡮ࡼࠤࡸ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧ⅌").format(data))
            else:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥ⅍").format(response))
        except Exception as e:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡨࡺࡸࡩ࡯ࡩࠣࡷࡪࡴࡤࡪࡰࡪࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢⅎ").format(e))
    def bstack1111111l1l1_opy_(self):
        if self.bstack1111111ll1l_opy_:
            with self.lock:
                try:
                    with open(self.bstack1111111l1ll_opy_, bstack11ll11_opy_ (u"ࠣࡴࠥ⅏")) as f:
                        bstack1lllllllll1l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1lllllllll1l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠧ⅐").format(failed_count))
                if failed_count >= self.bstack1111111ll11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࠩ࡮ࡲࡧࡦࡲࠩ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦ⅑").format(failed_count, self.bstack1111111ll11_opy_))
                    self.bstack1111111111l_opy_(failed_count)
                    self.bstack11111111l11_opy_ = True
            return
        try:
            response = bstack1111l11l1ll_opy_.bstack1111111l1l1_opy_(bstack11ll11_opy_ (u"ࠦࢀࢃ࠿ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࡀࡿࢂࠬࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࡁࢀࢃࠦࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࡂࢁࡽࠣ⅒").format(self.bstack1lllllllll11_opy_, self.config.get(bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⅓")), os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ⅔")), self.config.get(bstack11ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⅕"))))
            if response.get(bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ⅖")) == 200:
                failed_count = response.get(bstack11ll11_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࡖࡨࡷࡹࡹࡃࡰࡷࡱࡸࠧ⅗"), 0)
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡔࡴࡲ࡬ࡦࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠢࡦࡳࡺࡴࡴ࠻ࠢࡾࢁࠧ⅘").format(failed_count))
                if failed_count >= self.bstack1111111ll11_opy_:
                    self.logger.info(bstack11ll11_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤ࠻ࠢࡾࢁࠥࡄ࠽ࠡࡽࢀࠦ⅙").format(failed_count, self.bstack1111111ll11_opy_))
                    self.bstack1111111111l_opy_(failed_count)
                    self.bstack11111111l11_opy_ = True
            else:
                self.logger.error(bstack11ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡲࡰࡱࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ⅚").format(response))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡳࡳࡱࡲࡩ࡯ࡩ࠽ࠤࢀࢃࠢ⅛").format(e))
    def bstack1111111111l_opy_(self, failed_count):
        with open(self.bstack1111111l111_opy_, bstack11ll11_opy_ (u"ࠢࡸࠤ⅜")) as f:
            f.write(bstack11ll11_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨࠥࡧࡴࠡࡽࢀࡠࡳࠨ⅝").format(datetime.now()))
            f.write(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࡠࡳࠨ⅞").format(failed_count))
        self.logger.debug(bstack11ll11_opy_ (u"ࠥࡅࡧࡵࡲࡵࠢࡅࡹ࡮ࡲࡤࠡࡨ࡬ࡰࡪࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࢀࠦ⅟").format(self.bstack1111111l111_opy_))
    def bstack1lllllllllll_opy_(self):
        def bstack11111111lll_opy_():
            while not self.bstack11111111l11_opy_:
                time.sleep(bstack111111l1111_opy_)
                self.bstack1111111lll1_opy_()
                self.bstack1111111l1l1_opy_()
        bstack111111111ll_opy_ = threading.Thread(target=bstack11111111lll_opy_, daemon=True)
        bstack111111111ll_opy_.start()