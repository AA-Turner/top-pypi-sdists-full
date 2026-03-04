# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111llll11l1_opy_ import bstack111lll1ll1l_opy_
from bstack_utils.constants import bstack111ll1111l1_opy_, bstack11ll1111l1_opy_
from bstack_utils.bstack1lll1ll111_opy_ import bstack11l1llll1_opy_
from bstack_utils import logger_utils
bstack111l1l1ll1l_opy_ = 10
class bstack111l1l1l1_opy_:
    def __init__(self, bstack11lll1lll1_opy_, config, bstack111l1ll1111_opy_=0):
        self.bstack111l1ll1l11_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l1l1l1l1_opy_ = bstack1lll1l_opy_ (u"ࠣࡽࢀ࠳ࡹ࡫ࡳࡵࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࡨࡤ࡭ࡱ࡫ࡤ࠮ࡶࡨࡷࡹࡹࠢḪ").format(bstack111ll1111l1_opy_)
        self.bstack111l1ll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠤࡤࡦࡴࡸࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡼࡿࠥḫ").format(os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨḬ"))))
        self.bstack111l1l1111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡿࢂ࠴ࡴࡹࡶࠥḭ").format(os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḮ"))))
        self.bstack111l1ll111l_opy_ = 2
        self.bstack11lll1lll1_opy_ = bstack11lll1lll1_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack11ll1111l1_opy_)
        self.bstack111l1ll1111_opy_ = bstack111l1ll1111_opy_
        self.bstack111l1l11ll1_opy_ = False
        self.bstack111l1l1l1ll_opy_ = not (
                            os.environ.get(bstack1lll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠧḯ")) and
                            os.environ.get(bstack1lll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡎࡐࡆࡈࡣࡎࡔࡄࡆ࡚ࠥḰ")) and
                            os.environ.get(bstack1lll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡑࡗࡅࡑࡥࡎࡐࡆࡈࡣࡈࡕࡕࡏࡖࠥḱ"))
                        )
        if bstack11l1llll1_opy_.bstack111l1l1l11l_opy_(config):
            self.bstack111l1ll111l_opy_ = bstack11l1llll1_opy_.bstack111l1l1lll1_opy_(config, self.bstack111l1ll1111_opy_)
            self.bstack111l1l1ll11_opy_()
    def bstack111l1l1llll_opy_(self):
        return bstack1lll1l_opy_ (u"ࠤࡾࢁࡤࢁࡽࠣḲ").format(self.config.get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ḳ")), os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪḴ")))
    def bstack111l1l11l1l_opy_(self):
        try:
            if self.bstack111l1l1l1ll_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l1l1111l_opy_, bstack1lll1l_opy_ (u"ࠧࡸࠢḵ")) as f:
                        bstack111l1l111ll_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111l1l111ll_opy_ = set()
                bstack111l1ll11ll_opy_ = bstack111l1l111ll_opy_ - self.bstack111l1ll1l11_opy_
                if not bstack111l1ll11ll_opy_:
                    return
                self.bstack111l1ll1l11_opy_.update(bstack111l1ll11ll_opy_)
                data = {bstack1lll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࠦḶ"): list(self.bstack111l1ll1l11_opy_), bstack1lll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠥḷ"): self.config.get(bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫḸ")), bstack1lll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠢḹ"): os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩḺ")), bstack1lll1l_opy_ (u"ࠦࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠤḻ"): self.config.get(bstack1lll1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪḼ"))}
            response = bstack111lll1ll1l_opy_.bstack111l1l111l1_opy_(self.bstack111l1l1l1l1_opy_, data)
            if response.get(bstack1lll1l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨḽ")) == 200:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡳࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢḾ").format(data))
            else:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫࡮ࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧḿ").format(response))
        except Exception as e:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤṀ").format(e))
    def bstack111l1l11l11_opy_(self):
        if self.bstack111l1l1l1ll_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l1l1111l_opy_, bstack1lll1l_opy_ (u"ࠥࡶࠧṁ")) as f:
                        bstack111l11lllll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111l11lllll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡕࡵ࡬࡭ࡧࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠢṂ").format(failed_count))
                if failed_count >= self.bstack111l1ll111l_opy_:
                    self.logger.info(bstack1lll1l_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࠫࡰࡴࡩࡡ࡭ࠫ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨṃ").format(failed_count, self.bstack111l1ll111l_opy_))
                    self.bstack111l1l11111_opy_(failed_count)
                    self.bstack111l1l11ll1_opy_ = True
            return
        try:
            response = bstack111lll1ll1l_opy_.bstack111l1l11l11_opy_(bstack1lll1l_opy_ (u"ࠨࡻࡾࡁࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࡂࢁࡽࠧࡤࡸ࡭ࡱࡪࡒࡶࡰࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷࡃࡻࡾࠨࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫࠽ࡼࡿࠥṄ").format(self.bstack111l1l1l1l1_opy_, self.config.get(bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪṅ")), os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧṆ")), self.config.get(bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧṇ"))))
            if response.get(bstack1lll1l_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥṈ")) == 200:
                failed_count = response.get(bstack1lll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࡘࡪࡹࡴࡴࡅࡲࡹࡳࡺࠢṉ"), 0)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃࠢṊ").format(failed_count))
                if failed_count >= self.bstack111l1ll111l_opy_:
                    self.logger.info(bstack1lll1l_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦ࠽ࠤࢀࢃࠠ࠿࠿ࠣࡿࢂࠨṋ").format(failed_count, self.bstack111l1ll111l_opy_))
                    self.bstack111l1l11111_opy_(failed_count)
                    self.bstack111l1l11ll1_opy_ = True
            else:
                self.logger.error(bstack1lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡴࡲ࡬ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦṌ").format(response))
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡩࡻࡲࡪࡰࡪࠤࡵࡵ࡬࡭࡫ࡱ࡫࠿ࠦࡻࡾࠤṍ").format(e))
    def bstack111l1l11111_opy_(self, failed_count):
        with open(self.bstack111l1ll11l1_opy_, bstack1lll1l_opy_ (u"ࠤࡺࠦṎ")) as f:
            f.write(bstack1lll1l_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪࠠࡢࡶࠣࡿࢂࡢ࡮ࠣṏ").format(datetime.now()))
            f.write(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠣࡧࡴࡻ࡮ࡵ࠼ࠣࡿࢂࡢ࡮ࠣṐ").format(failed_count))
        self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡇࡢࡰࡴࡷࠤࡇࡻࡩ࡭ࡦࠣࡪ࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࢂࠨṑ").format(self.bstack111l1ll11l1_opy_))
    def bstack111l1l1ll11_opy_(self):
        def bstack111l1l11lll_opy_():
            while not self.bstack111l1l11ll1_opy_:
                time.sleep(bstack111l1l1ll1l_opy_)
                self.bstack111l1l11l1l_opy_()
                self.bstack111l1l11l11_opy_()
        bstack111l1l1l111_opy_ = threading.Thread(target=bstack111l1l11lll_opy_, daemon=True)
        bstack111l1l1l111_opy_.start()