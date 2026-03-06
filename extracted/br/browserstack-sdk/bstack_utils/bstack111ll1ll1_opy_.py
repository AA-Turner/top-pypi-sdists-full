# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111lll1l11l_opy_ import bstack111lll1lll1_opy_
from bstack_utils.constants import bstack111ll11l1ll_opy_, bstack1l11ll11l1_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack11l111lll1_opy_
from bstack_utils import logger_utils
bstack111l11lll1l_opy_ = 10
class bstack1l1111l111_opy_:
    def __init__(self, bstack1ll1llllll_opy_, config, bstack111l1l11ll1_opy_=0):
        self.bstack111l1l1lll1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack111l1ll111l_opy_ = bstack1111_opy_ (u"ࠤࡾࢁ࠴ࡺࡥࡴࡶࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࡩࡥ࡮ࡲࡥࡥ࠯ࡷࡩࡸࡺࡳࠣḫ").format(bstack111ll11l1ll_opy_)
        self.bstack111l1l1llll_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠥࡥࡧࡵࡲࡵࡡࡥࡹ࡮ࡲࡤࡠࡽࢀࠦḬ").format(os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḭ"))))
        self.bstack111l1ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࢀࢃ࠮ࡵࡺࡷࠦḮ").format(os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫḯ"))))
        self.bstack111l1l1l111_opy_ = 2
        self.bstack1ll1llllll_opy_ = bstack1ll1llllll_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l11ll11l1_opy_)
        self.bstack111l1l11ll1_opy_ = bstack111l1l11ll1_opy_
        self.bstack111l1l1ll11_opy_ = False
        self.bstack111l1l1l1l1_opy_ = not (
                            os.environ.get(bstack1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗࠨḰ")) and
                            os.environ.get(bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡏࡑࡇࡉࡤࡏࡎࡅࡇ࡛ࠦḱ")) and
                            os.environ.get(bstack1111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡒࡘࡆࡒ࡟ࡏࡑࡇࡉࡤࡉࡏࡖࡐࡗࠦḲ"))
                        )
        if bstack11l111lll1_opy_.bstack111l1l11111_opy_(config):
            self.bstack111l1l1l111_opy_ = bstack11l111lll1_opy_.bstack111l1l11lll_opy_(config, self.bstack111l1l11ll1_opy_)
            self.bstack111l1l1l1ll_opy_()
    def bstack111l1l11l1l_opy_(self):
        return bstack1111_opy_ (u"ࠥࡿࢂࡥࡻࡾࠤḳ").format(self.config.get(bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧḴ")), os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫḵ")))
    def bstack111l11llll1_opy_(self):
        try:
            if self.bstack111l1l1l1l1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111l1ll1111_opy_, bstack1111_opy_ (u"ࠨࡲࠣḶ")) as f:
                        bstack111l1l1ll1l_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack111l1l1ll1l_opy_ = set()
                bstack111l11lllll_opy_ = bstack111l1l1ll1l_opy_ - self.bstack111l1l1lll1_opy_
                if not bstack111l11lllll_opy_:
                    return
                self.bstack111l1l1lll1_opy_.update(bstack111l11lllll_opy_)
                data = {bstack1111_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࡔࡦࡵࡷࡷࠧḷ"): list(self.bstack111l1l1lll1_opy_), bstack1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠦḸ"): self.config.get(bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬḹ")), bstack1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣḺ"): os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪḻ")), bstack1111_opy_ (u"ࠧࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠥḼ"): self.config.get(bstack1111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫḽ"))}
            response = bstack111lll1lll1_opy_.bstack111l1ll11l1_opy_(self.bstack111l1ll111l_opy_, data)
            if response.get(bstack1111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢḾ")) == 200:
                self.logger.debug(bstack1111_opy_ (u"ࠣࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡴࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣḿ").format(data))
            else:
                self.logger.debug(bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥ࡯ࡦࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨṀ").format(response))
        except Exception as e:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࡀࠠࡼࡿࠥṁ").format(e))
    def bstack111l1l111ll_opy_(self):
        if self.bstack111l1l1l1l1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111l1ll1111_opy_, bstack1111_opy_ (u"ࠦࡷࠨṂ")) as f:
                        bstack111l1l1111l_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack111l1l1111l_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1111_opy_ (u"ࠧࡖ࡯࡭࡮ࡨࡨࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠣṃ").format(failed_count))
                if failed_count >= self.bstack111l1l1l111_opy_:
                    self.logger.info(bstack1111_opy_ (u"ࠨࡔࡩࡴࡨࡷ࡭ࡵ࡬ࡥࠢࡦࡶࡴࡹࡳࡦࡦࠣࠬࡱࡵࡣࡢ࡮ࠬ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢṄ").format(failed_count, self.bstack111l1l1l111_opy_))
                    self.bstack111l1l1l11l_opy_(failed_count)
                    self.bstack111l1l1ll11_opy_ = True
            return
        try:
            response = bstack111lll1lll1_opy_.bstack111l1l111ll_opy_(bstack1111_opy_ (u"ࠢࡼࡿࡂࡦࡺ࡯࡬ࡥࡐࡤࡱࡪࡃࡻࡾࠨࡥࡹ࡮ࡲࡤࡓࡷࡱࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࠽ࡼࡿࠩࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥ࠾ࡽࢀࠦṅ").format(self.bstack111l1ll111l_opy_, self.config.get(bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫṆ")), os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨṇ")), self.config.get(bstack1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨṈ"))))
            if response.get(bstack1111_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦṉ")) == 200:
                failed_count = response.get(bstack1111_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨ࡙࡫ࡳࡵࡵࡆࡳࡺࡴࡴࠣṊ"), 0)
                self.logger.debug(bstack1111_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽࠣṋ").format(failed_count))
                if failed_count >= self.bstack111l1l1l111_opy_:
                    self.logger.info(bstack1111_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧ࠾ࠥࢁࡽࠡࡀࡀࠤࢀࢃࠢṌ").format(failed_count, self.bstack111l1l1l111_opy_))
                    self.bstack111l1l1l11l_opy_(failed_count)
                    self.bstack111l1l1ll11_opy_ = True
            else:
                self.logger.error(bstack1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡵ࡬࡭ࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳ࠻ࠢࡾࢁࠧṍ").format(response))
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡪࡵࡳ࡫ࡱ࡫ࠥࡶ࡯࡭࡮࡬ࡲ࡬ࡀࠠࡼࡿࠥṎ").format(e))
    def bstack111l1l1l11l_opy_(self, failed_count):
        with open(self.bstack111l1l1llll_opy_, bstack1111_opy_ (u"ࠥࡻࠧṏ")) as f:
            f.write(bstack1111_opy_ (u"࡙ࠦ࡮ࡲࡦࡵ࡫ࡳࡱࡪࠠࡤࡴࡲࡷࡸ࡫ࡤࠡࡣࡷࠤࢀࢃ࡜࡯ࠤṐ").format(datetime.now()))
            f.write(bstack1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠤࡨࡵࡵ࡯ࡶ࠽ࠤࢀࢃ࡜࡯ࠤṑ").format(failed_count))
        self.logger.debug(bstack1111_opy_ (u"ࠨࡁࡣࡱࡵࡸࠥࡈࡵࡪ࡮ࡧࠤ࡫࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡦࡦ࠽ࠤࢀࢃࠢṒ").format(self.bstack111l1l1llll_opy_))
    def bstack111l1l1l1ll_opy_(self):
        def bstack111l1l11l11_opy_():
            while not self.bstack111l1l1ll11_opy_:
                time.sleep(bstack111l11lll1l_opy_)
                self.bstack111l11llll1_opy_()
                self.bstack111l1l111ll_opy_()
        bstack111l1l111l1_opy_ = threading.Thread(target=bstack111l1l11l11_opy_, daemon=True)
        bstack111l1l111l1_opy_.start()