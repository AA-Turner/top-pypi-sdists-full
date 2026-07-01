# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack111111lllll_opy_ import bstack11111l111ll_opy_
from bstack_utils.constants import bstack1111111l1ll_opy_, bstack111l11l111_opy_
from bstack_utils.bstack11ll1lll1_opy_ import bstack11ll1111l_opy_
from bstack_utils import logger_utils
bstack1llllll11l1l_opy_ = 10
class bstack1ll111l1ll1_opy_:
    def __init__(self, bstack11l11l1ll1_opy_, config, bstack1lllll1ll1ll_opy_=0):
        self.bstack1lllll1l1lll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1lllll1l1ll1_opy_ = bstack1l1llll_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤ⑚").format(bstack1111111l1ll_opy_)
        self.bstack1lllll1lllll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ⑛").format(os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⑜"))))
        self.bstack1lllll1lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ⑝").format(os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⑞"))))
        self.bstack1lllll1lll11_opy_ = 2
        self.bstack11l11l1ll1_opy_ = bstack11l11l1ll1_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack111l11l111_opy_)
        self.bstack1lllll1ll1ll_opy_ = bstack1lllll1ll1ll_opy_
        self.bstack1llllll111l1_opy_ = False
        self.bstack1lllll1llll1_opy_ = not (
                            os.environ.get(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ⑟")) and
                            os.environ.get(bstack1l1llll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ①")) and
                            os.environ.get(bstack1l1llll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ②"))
                        )
        if bstack11ll1111l_opy_.bstack1lllll1l1l1l_opy_(config):
            self.bstack1lllll1lll11_opy_ = bstack11ll1111l_opy_.bstack1lllll1ll11l_opy_(config, self.bstack1lllll1ll1ll_opy_)
            self.bstack1lllll1l11ll_opy_()
    def bstack1lllll1l11l1_opy_(self):
        return bstack1l1llll_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥ③").format(self.config.get(bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ④")), os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ⑤")))
    def bstack1llllll111ll_opy_(self):
        try:
            if self.bstack1lllll1llll1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1lllll1lll1l_opy_, bstack1l1llll_opy_ (u"ࠢࡳࠤ⑥")) as f:
                        bstack1llllll11111_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1llllll11111_opy_ = set()
                bstack1llllll1111l_opy_ = bstack1llllll11111_opy_ - self.bstack1lllll1l1lll_opy_
                if not bstack1llllll1111l_opy_:
                    return
                self.bstack1lllll1l1lll_opy_.update(bstack1llllll1111l_opy_)
                data = {bstack1l1llll_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨ⑦"): list(self.bstack1lllll1l1lll_opy_), bstack1l1llll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ⑧"): self.config.get(bstack1l1llll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⑨")), bstack1l1llll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ⑩"): os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ⑪")), bstack1l1llll_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ⑫"): self.config.get(bstack1l1llll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⑬"))}
            response = bstack11111l111ll_opy_.bstack1llllll11ll1_opy_(self.bstack1lllll1l1ll1_opy_, data)
            if response.get(bstack1l1llll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ⑭")) == 200:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ⑮").format(data))
            else:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ⑯").format(response))
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ⑰").format(e))
    def bstack1lllll1ll1l1_opy_(self):
        if self.bstack1lllll1llll1_opy_:
            with self.lock:
                try:
                    with open(self.bstack1lllll1lll1l_opy_, bstack1l1llll_opy_ (u"ࠧࡸࠢ⑱")) as f:
                        bstack1lllll1l1l11_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1lllll1l1l11_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ⑲").format(failed_count))
                if failed_count >= self.bstack1lllll1lll11_opy_:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ⑳").format(failed_count, self.bstack1lllll1lll11_opy_))
                    self.bstack1llllll11l11_opy_(failed_count)
                    self.bstack1llllll111l1_opy_ = True
            return
        try:
            response = bstack11111l111ll_opy_.bstack1lllll1ll1l1_opy_(bstack1l1llll_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧ⑴").format(self.bstack1lllll1l1ll1_opy_, self.config.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ⑵")), os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ⑶")), self.config.get(bstack1l1llll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⑷"))))
            if response.get(bstack1l1llll_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ⑸")) == 200:
                failed_count = response.get(bstack1l1llll_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤ⑹"), 0)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ⑺").format(failed_count))
                if failed_count >= self.bstack1lllll1lll11_opy_:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ⑻").format(failed_count, self.bstack1lllll1lll11_opy_))
                    self.bstack1llllll11l11_opy_(failed_count)
                    self.bstack1llllll111l1_opy_ = True
            else:
                self.logger.error(bstack1l1llll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ⑼").format(response))
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦ⑽").format(e))
    def bstack1llllll11l11_opy_(self, failed_count):
        with open(self.bstack1lllll1lllll_opy_, bstack1l1llll_opy_ (u"ࠦࡼࠨ⑾")) as f:
            f.write(bstack1l1llll_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥ⑿").format(datetime.now()))
            f.write(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥ⒀").format(failed_count))
        self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣ⒁").format(self.bstack1lllll1lllll_opy_))
    def bstack1lllll1l11ll_opy_(self):
        def bstack1lllll1l111l_opy_():
            while not self.bstack1llllll111l1_opy_:
                time.sleep(bstack1llllll11l1l_opy_)
                self.bstack1llllll111ll_opy_()
                self.bstack1lllll1ll1l1_opy_()
        bstack1lllll1ll111_opy_ = threading.Thread(target=bstack1lllll1l111l_opy_, daemon=True)
        bstack1lllll1ll111_opy_.start()